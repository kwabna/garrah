import sys
import optparse
import whois
import dns.resolver

def get_dns_records(dname, rec_type):
    try:
        data = dns.resolver.query(dname, rec_type)
        rec_list = []
        for rdata in data:
            rec_list.append(str(rdata))
        return rec_list
    except:
        return "No Records Found"

def main():
	print """
	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

	########################    Domain OSINT    ##########################
	#####################   Author: OSINTKwadjo   ########################
	##################  Email: ###########@gmail.com   ###################
	##################   Appreciation to @Datasploit   ###################

	++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	"""
	parser = optparse.OptionParser("usage %prog " + "-d <domain> ")
	parser.add_option('-d', dest='dname', type='string', help='Specify the domain name')

	(options, args) = parser.parse_args()

	if (options.dname == None):
		print parser.usage
		exit(0)

	else:
		dname = options.dname

	domaininfo = whois.whois(dname)
        print " ------- Domain Whois Information -------"
	print domaininfo
	
	print "--------------- DNS Information ---------------"
	dnsinfo = dns.resolver.query(dname)
	for data in dnsinfo:
	    dict_dns_record = {}
	    dict_dns_record['SOA Records'] = get_dns_records(dname, "SOA")
	    dict_dns_record['MX Records'] = get_dns_records(dname, "MX")
	    dict_dns_record['TXT Records'] = get_dns_records(dname, "TXT")
	    dict_dns_record['A Records'] = get_dns_records(dname, "A")
	    dict_dns_record['Name Server'] = get_dns_records(dname, "NS")
	    dict_dns_record['CNAME Records'] = get_dns_records(dname, "CNAME")
	    dict_dns_record['AAAA Records'] = get_dns_records(dname, "AAAA")
	    for key,val in dict_dns_record.items():
                print key, ":" ,val

if __name__ == '__main__':
	main()
