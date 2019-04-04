import subprocess
import sys
import urllib.request
import whois


try:
	urllib.request.urlopen('http://ipinfo.io/8.8.8.8/json')
except Exception as e:
	print('check the Internet connection')
	sys.exit()

domen = sys.argv[1]

a = whois.whois(domen)
if a["domain_name"] is None:
	print('this domen does not exist')
	sys.exit()

with open('trace.sh', 'w') as file:
	file.write('#!/bin/bash\n')
	file.write("traceroute " + '"' + domen + '"' + " | awk '{print $3}' | sed 's/(//; s/)//' > traceroute.txt")

subprocess.call("./trace.sh", shell=True)

with open('traceroute.txt', 'r') as trace:
	trace = trace.readlines()
	trace = trace[1:]

with open('result', 'w') as result:
	count = 0
	for line in trace:
		count += 1
		if not '*' in line:
			result.write(str(count) + ' ')
			result.write(line[:-1] +' ')
			ask = str(urllib.request.urlopen('http://ipinfo.io/' + line[:-1] + '/json').read())
			b = ask.split()
			n = 0
			aut_s = ''
			country = ''
			host = ''
			for line in b:
				n+=1
				if 'AS' in line:
					aut_s = line[3:] + ' '
				if 'country' in line:
					country = b[n][1:-4] + ' '
				if 'host' in line:
					host = b[n][1:-4]
			result.write(aut_s + country + host + '\n')

print('result in "result.txt"')
