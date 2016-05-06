#!/usr/bin/python
#-*- coding=utf-8 -*-

"""
* web系统周期性巡检
* 1.svn git泄露
* 2.备份文件扫描
* 3.列出目录
* ???4.任意域名指向
"""

import io
import sys
import urllib
import urllib2
import httplib
import socket
import time
import threading

socket.setdefaulttimeout(5) 

secretRs = []

# 重定义http方法 防止302跟随
class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):  
		result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)              
		result.status = code
		return result

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)              
		result.status = code                                
		return result 

def scanner(target):
	print target
	# 敏感文件扫描
	secretList = ["/.svn/entries", "/.git/config",
					"/www.tar.gz", "/www.zip", "/www.rar",
					"/wwwroot.tar.gz", "/wwwroot.zip", "/wwwroot.rar",
					"/backup.tar.gz", "/backup.zip", "/backup.rar",
					"/web.tar.gz", "/web.zip", "/web.rar",
					"/log.tar.gz", "/log.zip", "/log.rar",
					"/"+target+".sql", "/db.sql",
					"/"+target+".tar.gz", "/"+target+".zip", "/"+target+".rar",
					"/.config.php.swp", "/config.php.bak", "/test.php"]

	# 取404页面大小用于比较 防止统一错误页面误记录
	notfound_length = 0
	try:
		req = urllib2.Request(target + "/notfound_123ada12314ad889.tmp")
		httplib.HTTPConnection.debuglevel = 1
		opener_nf = urllib2.build_opener(SmartRedirectHandler)
		resp_nf = opener_nf.open(req)
		notfound_length = len(resp_nf.read())
	except Exception, e:
		pass
		#print e

	for info in secretList:
		res = target + info
		try:
			req = urllib2.Request(res)
			opener = urllib2.build_opener(SmartRedirectHandler)
			resp = opener.open(req)
			status = resp.code
			content_length = len(resp.read())
			print str(content_length) + "-" + str(notfound_length) + "|" + res
			if (200 == status) and (content_length <> notfound_length):
				print "\t#found# " + res
				secretRs.append(res)
				writer = open("wooyun-res.txt", "a")
				writer.write(res+"\n")
				writer.close()
		except Exception, e:
			#pass
			print e


def dirList(target):
	pass
	

def main():
	reader = open("wooyun_company.txt", "r")
	for line in reader.readlines():
		line = line.rstrip()
		scanner(line)
	reader.close()

if __name__ == '__main__':
	main()