import login
import requests
from bs4 import BeautifulSoup

def innerHTML(element):
	return element.decode_contents(formatter="html").strip()

l = login.Login()
l.prompt('login.json')
l.login()
r=l.get('http://202.117.1.179/mark/showMarkOne.do',doubleAuth=1)

br=BeautifulSoup(r.content, "html.parser")
for i in br.select('tbody tr')[1:]:
	print(innerHTML(i.select('font')[0]))
	for j in i.select('td')[1:]:
		print(innerHTML(j))
	print()