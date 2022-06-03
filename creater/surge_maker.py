#regex find server

import datetime
import os
import urllib.request
import requests

#time and date stamp for file name
stamp = datetime.datetime.now()

#!!!important!!! airport url
image_url = ""

#online(github surge template)
onlinefile = "https://raw.githubusercontent.com/mp8atuk/Profiles/ma%D1%95ter/template_surge.conf"


#get airport file
filename = "surge4_template.conf"

# URL of the airport(surge servers) to be downloaded is defined as image_url
r = requests.get(image_url) # create HTTP response object

# send a HTTP request to the server and save
# the HTTP response in a response object called r
with open(filename,'wb') as f:

    # Saving received content as a png file in
    # binary format

    # write the contents of the response (r.content)
    # to a new file in binary mode.
    f.write(r.content)



output_file = "Surge_lt_"+stamp.strftime("%Y-%m-%d-%H%M%S")+".conf"

#get  template file 
template = "surge4_conf.conf"

with urllib.request.urlopen(onlinefile) as f:
    html = f.read().decode('utf-8')

if os.path.exists(template):
  os.remove(template)


conf= open(template,'w', encoding='UTF-8')
conf.write(html)
conf.close()


#organize template
conf = open(filename,'r', encoding='UTF-8')

server = []
flag = False

for i,c in enumerate(conf.readlines()):
	if "[Proxy]" in c:
		flag = True
		continue
	
	if "[Proxy Group]" in c:
		flag = False
		break
	if flag is True:
		if c == "\n":
			continue
		else:
			server.append(c)



#countries
keywords = ["香港","台湾","韩国","日本","美国","英国","印度","法国"]
#hongkong
hk="香港"
#server dictionery
sd={}

for key in keywords:
	sd[key]=[]

for se in server:
	for i in keywords:
		if i in se:
			sd[i].append(se)

upstring = "国峯"
sd[upstring]=[]
remove_list=[]

for key in keywords:
	for server in sd[key]:
		if upstring in server:
			sd[upstring].append(server)
			remove_list.append(server)
	for n,l in enumerate(remove_list):
		sd[key].remove(l)
	remove_list=[]

def get_server(server):
	server_name = server[:server.find('=')]
	return server_name.strip()


	



template_file= open(template,'r',	encoding='UTF-8')




f = open(output_file, "w",encoding='UTF-8')
f.write("#Version ")
f.write(str(stamp))
f.write("\n")

for c in template_file:
	if "{=-=-=here=-=-=}" in c:
		# output server group by country
		for country in sd.keys():
			line=[]
			line.append(country)
			line.append("= url-test,")
			for server in sd[country]:
				line.append(get_server(server)+",")
			line.append("update-interval=0")
			f.write(' '.join(line))
			f.write("\n")
	elif "{=-=-=here1=-=-=}" in c:
		for country in sd.keys():
			for ser in sd[country]:
				f.write(ser)

	else:
		
		f.write(c)







f.close()
template_file.close()
conf.close()
if os.path.exists(filename):
  os.remove(filename)
