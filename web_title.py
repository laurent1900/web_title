#coding:utf-8
import argparse
import sys
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')

def check(host):
	try:
		url = 'http://'+str(host.strip())
		driver = webdriver.PhantomJS()
		driver.get(url)
		result = driver.title
		if not len(result)==0:
			result = host+':'+driver.title
			print result
			driver.quit()
		else:
			try:
				url = 'https://'+str(host.strip())
				driver = webdriver.PhantomJS()
				driver.get(url)
				result = driver.title
				if not len(result)==0:
					result = host+':'+driver.title
					print result
					driver.quit()
				else:
					print host+':'+'unkonwn'
			except Exception,e:
				pass
	except Exception,e:
		pass

def main(host,file):
	try:
		if host:
			check(host)
		elif file:
			f = open(file)
			for i in f:
				check(i.strip())
			f.close()
		else:
			print 'usage: web_title.py [-h] [--host HOST] [--file FILE]'
			print 'optional arguments:'
			print '-h, --help   show this help message and exit'
			print '--host HOST  Enter the host that you want to check'
			print '--file FILE  Input from list of hosts'
	except Exception,e:
		print e

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('--host', help="Enter the host that you want to check")
	parse.add_argument('--file', help="Input from list of hosts")
	args = parse.parse_args()
	if len(sys.argv) == 1:
		print 'usage: web_title.py [-h] [--host HOST] [--file FILE]'
		print 'optional arguments:'
		print '-h, --help   show this help message and exit'
		print '--host HOST  Enter the host that you want to check'
		print '--file FILE  Input from list of hosts'
	else:
		host = args.host
		file = args.file
		main(host,file)