import requests
import getpass
import os
import json
from bs4 import BeautifulSoup

print("查成绩")

if not os.path.isfile('login.json'):
	netid=input("NetID:")
	password=getpass.getpass()
	sp=input("保存密码?[y/n]")
	if sp=='y':
		with open('login.json','w') as f:
			json.dump({'netid':netid,'password':password}, f)
else:
	with open('login.json','r') as f:
		d=json.load(f)
	netid=input("NetID("+d['netid']+"):")
	if not netid:
		netid=d['netid']
		password=d['password']
	else:
		password=getpass.getpass()

print("查询中...\n")

def innerHTML(element):
    return element.decode_contents(formatter="html").strip()

#Get sessionid
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
}

r=requests.get('https://cas.xjtu.edu.cn/login', headers=headers)

br=BeautifulSoup(r.content, "html.parser")
sessionid=r.cookies.get('JSESSIONID')
lt=br.select('input[name="lt"]')[0]['value']
exe=br.select('input[name="execution"]')[0]['value']

#Auth
cookies = {
    'JSESSIONID': sessionid,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = 'username='+netid+'&password='+password+'&code=&lt='+lt+'&execution='+exe+'&_eventId=submit&submit=%E7%99%BB%E5%BD%95'

r2=requests.post('https://cas.xjtu.edu.cn/login', headers=headers, cookies=cookies, data=data)

#Auth OK
castgc=r2.cookies.get('CASTGC')

cookies = {
    'JSESSIONID': sessionid,
    'CASTGC': castgc,
}

r3=requests.get('http://202.117.1.179/mark/showMarkOne.do', cookies=cookies)
sessionid=r3.history[0].cookies.get('JSESSIONID')

cookies = {
	'JSESSIONID': sessionid
}

r4=requests.get('http://202.117.1.179/mark/showMarkOne.do', cookies=cookies)

#Finally we get the data
br=BeautifulSoup(r4.content, "html.parser")
for i in br.select('tbody tr')[1:]:
	print(innerHTML(i.select('font')[0]))
	for j in i.select('td')[1:]:
		print(innerHTML(j))
	print()

input()