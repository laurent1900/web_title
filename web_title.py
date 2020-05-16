#coding:utf-8
import argparse
import sys
import multiprocessing
import json
import os
from check_200 import check200
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# driver=webdriver.PhantomJS(executable_path='存放路径/phantomjs.exe')

# headers = {
# 	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
# 	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
# 	'Connection': 'keep-alive'
# }
# dcap = DesiredCapabilities.PHANTOMJS.copy()#使用copy()防止修改原代码定义dict
# for key, value in headers.items():
# 	dcap['phantomjs.page.customHeaders.{}'.format(key)] = value

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.loadImages"] = False
dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"

reload(sys)
sys.setdefaultencoding('utf-8')

# service_args = ['--proxy=http://127.0.0.1:8080','--proxy-type=http',]

def check(host,data):
	try:
		url = 'http://'+str(host.strip())
		driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR","--ssl-protocol=any"])
		driver.set_page_load_timeout(10)
		driver.get(url)
		result = driver.title
		if not len(result)==0:
			result = data[host]+','+driver.title.replace(",","#")+','+host
			driver.quit()
		else:
			try:
				driver.quit()
				url = 'https://'+str(host.strip())
				driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR","--ssl-protocol=any"])
				driver.set_page_load_timeout(10)
				driver.get(url)
				result = driver.title
				if not len(result)==0:
					result = data[host]+','+driver.title.replace(",","#")+','+host
					driver.quit()
				else:
					code = check200(host)
					if code == 200:
						result = data[host]+','+'需要手动探测'+','+host
						driver.quit()
					else:
						result = data[host]+','+'不可达'+','+host
						driver.quit()
					return result
				return result
			except Exception,e:
				result = data[host]+','+'不可达'+','+host
				driver.quit()
				return result
				pass
		return result
	except Exception,e:
		result = data[host]+','+'不可达'+','+host
		driver.quit()
		return result
		pass

def check_print(host):
	try:
		url = 'http://'+str(host.strip())
		driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR","--ssl-protocol=any"])
		driver.set_page_load_timeout(10)
		driver.get(url)
		result = driver.title
		if not len(result)==0:
			result = host+','+driver.title+''
			print result
			driver.quit()
		else:
			try:
				driver.quit()
				url = 'https://'+str(host.strip())
				driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=["--webdriver-loglevel=ERROR","--ssl-protocol=any"])
				driver.set_page_load_timeout(10)
				driver.get(url)
				result = driver.title
				if not len(result)==0:
					result = host+','+driver.title+''
					print result
					driver.quit()
				else:
					result = host+','+'不可达'
					driver.quit()
					print result
				# return result
			except Exception,e:
				result = host+','+'不可达'
				print result
				driver.quit()
				# return result
				pass
		return result
	except Exception,e:
		result = host+','+'不可达'
		print result
		driver.quit()
		# return result
		pass


def mycallback(x):
	with open('result.csv', 'a+') as f:
		f.write(str(x)+'\n')
	f.close()

def main(host,file,threads):
	try:
		if host:
			check_print(host)
		elif file:
			pool = multiprocessing.Pool(processes = int(threads))
			f = open(file)
			data = json.load(f)
			for i in data.keys():
				pool.apply_async(check, (i.strip(), data,), callback=mycallback)
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
	m = open('result.csv','w+')
	m.write('网站名称'+','+'实测名称'+','+'域名\n')
	m.close()
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
	# main(host='',file='./1.txt',threads=1)