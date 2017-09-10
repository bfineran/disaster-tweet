
import os
import usaddress
import datetime
import json
from dbfuns import DBWriter
import phonenumbers

import twitterscraper

def searchnumber(wholetext):
	try:
		x = phonenumbers.parse(wholetext)
		numberstr = str(x)
		idx = numberstr.find("National Number: ")
		realnumber = numberstr[(idx+17):(idx+17+10)]
		return realnumber
	except:
		return 0000000



def searchquery(keyword, numsearches, filename, sinceid):
	maxid = sinceid
	writer = DBWriter()
	for tweet in twitterscraper.query.query_tweets(keyword + " since_id:" + str(sinceid), numsearches)[:numsearches]:
		text = tweet.text.encode('utf-8')
		try:
			addr, confidence = usaddress.tag(text)
		except:
			continue

		if confidence is not "Ambiguous":
			print(tweet.user.encode('utf-8'))
			print(tweet.timestamp)
			timestr = tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
			print(text)
			print(addr)
			realphone = searchnumber(text)
			contents = tweet.fullname.encode('utf-8') + '\t' + tweet.user.encode('utf-8') + '\t' + timestr + '\t' +  str(realphone) + '\t' + text + '\t' + json.dumps(dict(addr)) + "\t" + "\n"
			filename.write(contents)

			addrs = dict(addr)
			b = True
			if 'StreetNamePosType' not in addrs:
				addrs['StreetNamePosType'] = ''
			if 'AddressNumber' not in addrs:
				b = False
			if 'StreetName' not in addrs:
				b = False
			if b:
				address = addrs['AddressNumber'] + ' ' + addrs['StreetName'] + ' ' + addrs['StreetNamePosType']
				writer.add_item(str(address), tweet.user.encode('utf-8'), tweet.fullname.encode('utf-8'), text, timestr, 'Houston, TX')



			if int(tweet.id) > maxid:
				maxid = int(tweet.id)
	writer.write_to_db()
	return maxid

print("HELOOWOWSOISOHSFIU")

F = open("tweetsfile.txt", "w")
Q = open("searchterms.txt", "r")
C = open("config.txt", "r+")

startid = int(C.readline())
newmaxid = 0

for line in Q:
	print("New Query:")
	newid = searchquery(line, 1000, F, startid)
	if newid > newmaxid:
		newmaxid = newid
	print("finished search for " + line)
C.close()

D = open("config.txt", "w")
D.write(str(newmaxid))