# example of program that calculates the number of tweets cleaned
import sys

try: 
	import ujson as json
except ImportError:
	import json


def clean_unicode(text):
	"""
		Returns a string with unicode characters removed.
	"""
	return text.encode('utf-8').decode('unicode_escape').encode('ascii','ignore')

class Cleaner(object):
	def __init__(self):
		self.total_count = 0
		self.unicode_count = 0

	def clean_tweet(self, record):
		data = json.loads(record)
		text = data["text"].replace("\n", " ")
		cleaned = clean_unicode(text)
		timestamp = data["created_at"]

		self.total_count += 1
		if text != cleaned:
			self.unicode_count += 1

		return "%s (timestamp: %s)" % (cleaned, timestamp)

cleaner = Cleaner()
for line in sys.stdin:
	try:
		print(cleaner.clean_tweet(line))
	except KeyError:
		# Not all lines are tweets. We get a key error if either
		# created_at or text is missing. In that case just skip the line.
		pass

print("")
print("%s tweets contained unicode." % cleaner.unicode_count)