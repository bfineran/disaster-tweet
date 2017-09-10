import boto3
import json

import os
import usaddress
import datetime
import json
from dbfuns import DBWriter
import phonenumbers

import twitterscraper


def updatedata():
	def searchnumber(wholetext):
		try:
			x = phonenumbers.parse(wholetext)
			numberstr = str(x)
			idx = numberstr.find("National Number: ")
			realnumber = numberstr[(idx+17):(idx+17+10)]
			return realnumber
		except:
			return 0000000



	def searchquery(keyword, numsearches):
		prev_keys = []
		writer = DBWriter()
		for tweet in twitterscraper.query.query_tweets(keyword, numsearches)[:numsearches]:
			text = tweet.text.encode('utf-8')
			try:
				addr, confidence = usaddress.tag(text)
			except:
				continue

			if confidence is not "Ambiguous":
				timestr = tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
				realphone = searchnumber(text)
				contents = tweet.fullname.encode('utf-8') + '\t' + tweet.user.encode('utf-8') + '\t' + timestr + '\t' +  str(realphone) + '\t' + text + '\t' + json.dumps(dict(addr)) + "\t" + "\n"

				addrs = dict(addr)
				b = True
				if 'StreetNamePosType' not in addrs:
					addrs['StreetNamePosType'] = ''
				if 'AddressNumber' not in addrs:
					b = False
				if 'StreetName' not in addrs:
					b = False
				if b:
					print(tweet.user.encode('utf-8'))
					print(tweet.timestamp)
					address = addrs['AddressNumber'] + ' ' + addrs['StreetName'] + ' ' + addrs['StreetNamePosType']
					try:
						if address in prev_keys:
							print(address)
							continue
						prev_keys.append(str(address))
						writer.add_item(str(address), tweet.user.encode('utf-8'), tweet.fullname.encode('utf-8'), text, timestr, 'Houston, TX')
					except:
						continue

		writer.write_to_db()
		return

	print("HELOOWOWSOISOHSFIU")


	Q = {"@houstonoem help", "@houstonpolice help since:2017-08-25 until:2017-08-28"}

	for line in Q:
		print("New Query:")
		searchquery(line, 1000)
		print("finished search for " + line)