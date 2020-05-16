#coding:utf-8
import requests

headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
               'Accept - Encoding':'gzip, deflate',
               'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
               'Connection':'Keep-Alive',
               'Host':'zhannei.baidu.com',
               'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

def check200(i):
	try:
		r = requests.get('http://'+i,timeout=3,headers=headers)
		code = r.status_code
		return code
	except Exception,e:
		try:
			r = requests.get('https://'+i,timeout=3,headers=headers)
			code = r.status_code
			return code
		except Exception,e:
			code = 404
			return code
			pass

if __name__ == '__main__':
	f = open('2.txt','r')
	for i in f:
		print i.strip(),check200(i.strip())