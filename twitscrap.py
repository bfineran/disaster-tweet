
import os
import usaddress
import datetime
import json

import twitterscraper
print(os.path.dirname(twitterscraper.__file__))


F = open("tweetsfile.txt", "w")

for tweet in twitterscraper.query.query_tweets("@houstonoem help", 1000)[:1000]:
	text = tweet.text.encode('utf-8')
	try:
		addr, confidence = usaddress.tag(text)
	except:
		continue

	if confidence is not "Ambiguous":
		print(tweet.user.encode('utf-8'))
		F.write(tweet.user.encode('utf-8'))
		print(tweet.timestamp)
		timestr = tweet.timestamp.strftime("%Y-%m-%d %H:%M:%S")
		F.write(timestr)
		print(text)
		F.write(text)
		print(addr)
		F.write(json.dumps(dict(addr)))
		F.write("\n\n\n")
