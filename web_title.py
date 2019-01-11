#coding:utf-8
import argparse
import sys
import multiprocessing
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False

reload(sys)
sys.setdefaultencoding('utf-8')

def check(host):
	try:
		url = 'http://'+str(host.strip())
		driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR"])
		driver.set_page_load_timeout(10)
		driver.get(url)
		result = driver.title
		if not len(result)==0:
			result = host+':'+driver.title+'\n'
			print result
			driver.quit()
		else:
			try:
				driver.quit()
				url = 'https://'+str(host.strip())
				driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR"])
				driver.set_page_load_timeout(10)
				driver.get(url)
				result = driver.title
				if not len(result)==0:
					result = host+':'+driver.title+'\n'
					print result
					driver.quit()
				else:
					driver.quit()
					print host+':'+'unkonwn\n'
			except Exception,e:
				print host+':'+'unkonwn\n'
				pass
	except Exception,e:
		print host+':'+'unkonwn\n'
		pass

def main(host,file,threads):
	try:
		if host:
			check(host)
		elif file:
			pool = multiprocessing.Pool(processes = int(threads))
			f = open(file)
			for i in f:
				pool.apply_async(check, (i.strip(), ))
			f.close()
			pool.close()
			pool.join()
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
	parse.add_argument('--threads', help="Input the number of threads")
	args = parse.parse_args()
	if len(sys.argv) == 1:
		print 'usage: web_title.py [-h] [--host HOST] [--file FILE]'
		print 'optional arguments:'
		print '-h, --help   show this help message and exit'
		print '--host HOST  Enter the host that you want to check'
		print '--file FILE  Input from list of hosts'
		print '--threads THREADS  Input the number of threads'
	else:
		host = args.host
		file = args.file
		if args.threads:
			threads = int(args.threads)
		else:
			threads = 5
		main(host,file,threads)