#!/usr/bin/env python3

import sys
import syslog
import json

def correct_url(correct_url):
	if correct_url[0:7] == 'http://':
			if correct_url[7:10] != 'www':
				correct_url = 'http://' + correct_url[10:]
	else:
		if correct_url[0:3] == 'www':
			correct_url = 'http://' + correct_url
		else:
			correct_url = 'http://www.' + correct_url
	return correct_url

def rewrite(url):
	with open('/etc/squid3/url.json') as jd:
		data = jd.read()
		jsondata = json.loads(data)
	final_url = '\n'
	check_edit_url = False
	for line in jsondata['url']:
		first_url = line['from']
		first_url = correct_url(first_url)
		second_url = line['to']
		second_url = correct_url(second_url)

		if url.startswith(first_url):
			final_url = second_url + final_url
			check_edit_url = True
			break	

	if check_edit_url == True:
		syslog.syslog(6, 'Requested URL : ' + url + ' redirect to : ' + second_url)
	else:
		syslog.syslog(6, 'Requested URL : ' + url)
	return final_url

while True:
	stream = sys.stdin.readline().strip()
	streamToList = stream.split(' ')
	url = streamToList[0]
	stream_out = rewrite(url)
	sys.stdout.write(stream_out)
	sys.stdout.flush()
