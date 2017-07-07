import pythonwhois
import json
import datetime
import csv
import argparse

parser = argparse.ArgumentParser(description="domain list file")
parser.add_argument("-f","--file",action="store",help="domain list file",default=None)
#parser.add_argument("domain",nargs=1)
args = parser.parse_args()

with open(args.file,"r") as f:
	domainlist = f.readlines()
#f = open("domainlist.txt","r")

#domainlist = f.readlines()						

def convert_csv(data, domain):
    f = open("./result/csv/" + domain + ".csv","w")
    w = csv.writer(f)
    writelist = []
    maxlen = 0
    header = []
    data.pop("contacts")
    data.pop("raw")
    for key in data.keys():
        header.append(key)
        if maxlen < len(data[key]):
            maxlen = len(data[key])
    w.writerow(header)
    for i in range(maxlen):
        output = []
        for key in data.keys():
            if(i < len(data[key])):
                output.append(data[key][i])
            else:
                output.append(" ")
        w.writerow(output)


def json_fallback(obj):
   if isinstance(obj, datetime.datetime):
      return obj.isoformat()
   else:
      return obj


for domain in domainlist:
    if(domain[-1:] == "\n"):
        domain = domain[:-1]
    data , server_list = pythonwhois.net.get_whois_raw(domain, with_server_list=True)
    if len(server_list) > 0:
		parsed = pythonwhois.parse.parse_raw_whois(data, normalized=True, never_query_handles=False, handle_server=server_list[-1])
    else:
		parsed = pythonwhois.parse.parse_raw_whois(data, normalized=True)
    
    #domain = domain.split(".")[0]
    result = open("./result/json/" + domain + ".json","w")
    jsonstring = json.dumps(parsed,default = json_fallback)
    result.write(jsonstring)
    tmpdict = json.loads(jsonstring)
    convert_csv(tmpdict,domain)


print "done!"
