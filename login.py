import getpass
import os
import json
import requests
from bs4 import BeautifulSoup

UA_CHROME='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'

class Login:
	"""docstring for Login"""
	def __init__(self,netid='',password='',ua=UA_CHROME):
		self.netid = netid
		self.password = password
		self.session=requests.Session()
		self.session.headers.update({'User-Agent': ua})
	def prompt(self,filename=None):
		if not filename:
			self.netid=input("NetID:")
			self.password=getpass.getpass()
			return
		if not os.path.isfile(filename):
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
		#Get sessionid
		r=self.session.get('https://cas.xjtu.edu.cn/login')
		br=BeautifulSoup(r.content, "html.parser")
		lt=br.select_one('input[name="lt"]')['value']
		exe=br.select_one('input[name="execution"]')['value']
		#Auth
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		data = 'username='+self.netid+'&password='+self.password+'&code=&lt='+lt+'&execution='+exe+'&_eventId=submit&submit=%E7%99%BB%E5%BD%95'
		self.session.post('https://cas.xjtu.edu.cn/login', headers=headers, data=data)
	def get(self,url,doubleAuth=0):
		if doubleAuth:
			self.session.get(url)
		return self.session.get(url)