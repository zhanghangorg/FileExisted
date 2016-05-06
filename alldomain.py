#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup

ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36"

# 查域名注册邮箱
def whois(domain):
	interface = "http://whois.chinaz.com/%s" % domain
	r = requests.get(interface, headers={'User-Agent': ua}).text
	# 域名注册信息受保护时返回一个不存在的邮箱
	tmp = re.findall(r'[\w\-]+\@[\w\-]+\.\w+', r)
	return tmp[0] if len(tmp)>0 else "abc@1a2b3c.com"

# 查邮箱注册的域名
def alldomain(email):
	domains = []
	interface = "http://whois.chinaz.com/reverse?host=%s&ddlSearchMode=1" % email
	r = requests.get(interface, headers={'User-Agent': ua}).text
	for domain in BeautifulSoup(r, 'lxml').find(id="ajaxInfo").find_all('a'):
		if re.match(r'\w+\.\w+', domain.text):
			domains.append(domain.text)
	return domains



def main():
	# domain = "guokr.com"
	# reg_email = whois(domain)
	# domains = alldomain(reg_email)
	# print domains
	reader = open("wooyun.txt", "r")
	writer = open("result.txt", "a")
	for line in reader.readlines():
		line = line.rstrip()
		print "read ---->"+line

		for domain in alldomain(whois(line)):
			print "get ----" + domain
			writer.write(domain+"\n")
		writer.flush()
	writer.close()
	reader.close()


if __name__ == "__main__":
	main()

