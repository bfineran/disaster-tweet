
import os
import usaddress
import datetime
import json

import twitterscraper

def searchquery(keyword, numsearches, filename, sinceid):
	maxid = sinceid
	for tweet in twitterscraper.query.query_tweets(keyword + " since_id:" + str(sinceid), numsearches)[:numsearches]:
		text = tweet.text.encode('utf-8')
		try:
			addr, confidence = usaddress.tag(text)
		except:
			continue

		print(tweet.user.encode('utf-8'))
		print(tweet.timestamp)
		timestr = tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
		print(text)
		print(addr)
		contents = tweet.user.encode('utf-8') + timestr + text + json.dumps(dict(addr)) + "\n\n\n"
		filename.write(contents)
		if int(tweet.id) > maxid:
			maxid = int(tweet.id)
	return maxid

print("HELOOWOWSOISOHSFIU")

F = open("tweetsfile.txt", "w")
Q = open("searchterms.txt", "r")
C = open("config.txt", "r+")

startid = int(C.readline())
newmaxid = 0

for line in Q:
	print("New Query:")
	print("\n\n\n")
	newid = searchquery(line, 100, F, startid)
	if newid > newmaxid:
		newmaxid = newid
	print("\n\n\n")
	print("finished search for " + line)
C.close()

D = open("config.txt", "w")
D.write(str(newmaxid))