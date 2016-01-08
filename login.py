import getpass
import os
import json
import requests
from bs4 import BeautifulSoup

def innerHTML(element):
	return element.decode_contents(formatter="html").strip()

class Login:
	"""docstring for Login"""
	def __init__(self,netid='',password=''):
		self.netid = netid
		self.password = password
		self.authCookies = {}
	def prompt(self,filename=None):
		if not filename:
			self.netid=input("NetID:")
			self.password=getpass.getpass()
			return
		if not os.path.isfile(self,filename):
			self.netid=input("NetID:")
			self.password=getpass.getpass()
			sp=input("Save password?[y/n]")
			if sp=='y':
				with open(filename,'w') as f:
					json.dump({'netid':self.netid,'password':self.password}, f)
		else:
			with open(filename,'r') as f:
				d=json.load(f)
			self.netid=input("NetID("+d['netid']+"):")
			if not self.netid or self.netid==d['netid']:
				self.netid=d['netid']
				self.password=d['password']
			else:
				self.password=getpass.getpass()
	def login(self):
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
		}
		#Get sessionid
		r=requests.get('https://cas.xjtu.edu.cn/login',headers=headers)
		br=BeautifulSoup(r.content, "html.parser")
		sessionid=r.cookies.get('JSESSIONID')
		lt=br.select_one('input[name="lt"]')['value']
		exe=br.select_one('input[name="execution"]')['value']
		#Auth
		cookies = {
			'JSESSIONID': sessionid
		}
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		data = 'username='+self.netid+'&password='+self.password+'&code=&lt='+lt+'&execution='+exe+'&_eventId=submit&submit=%E7%99%BB%E5%BD%95'
		r=requests.post('https://cas.xjtu.edu.cn/login', headers=headers, cookies=cookies, data=data)
		self.castgc=r.cookies.get('CASTGC')
	def auth(self,url,cookieName):
		cookies = {
			'CASTGC': self.castgc
		}
		self.authCookies[cookieName]=requests.get(url).history[0].cookies