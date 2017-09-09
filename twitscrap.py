
import os
import usaddress
import datetime
import json

import twitterscraper

def searchquery(keyword, numsearches, filename):
	for tweet in twitterscraper.query.query_tweets(keyword, numsearches)[:numsearches]:
		text = tweet.text.encode('utf-8')
		try:
			addr, confidence = usaddress.tag(text)
		except:
			continue

		if confidence is not "Ambiguous":
			print(tweet.user.encode('utf-8'))
			filename.write(tweet.user.encode('utf-8'))
			print(tweet.timestamp)
			timestr = tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
			filename.write(timestr)
			print(text)
			filename.write(text)
			print(addr)
			filename.write(json.dumps(dict(addr)))
			filename.write("\n\n\n")

	return

print("HELOOWOWSOISOHSFIU")

F = open("tweetsfile.txt", "w")
Q = open("searchterms.txt", "r")




for line in Q:
	print("New Query:")
	print("\n\n\n")
	searchquery(line, 1000, F)
	print("\n\n\n")
	print("finished search for " + line)
