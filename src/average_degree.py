# example of program that calculates the average degree of hashtags
import itertools
import sys
import re
import datetime
from collections import defaultdict

EPOCH = datetime.datetime.utcfromtimestamp(0)

# Used for extracting all hastags from cleaned tweets.
HASHTAG_RE = re.compile(r"#(\w+)")
# Used to extract timestamp from cleaned tweets.
TS_RE = re.compile(r"\(timestamp: (.+)\)")

class RunningAvgDegre(object):
  def __init__(self):
    # Map of vertices to number of occurrences in last 60 seconds.
    self.vertices = {}
    # Map of edges to number of occurrences in last 60 seconds.
    self.edges = {}
    # This is a sorted list of hashtag, timestamp pairs.
    self.queue = list()

  def new_tweet(self, hashtags, ts):
    if len(hashtags) > 1:
      # If hash tags are present we remember when we added them
      # and increase vertex and edge counts
      self.queue.append((hashtags, ts))
      self._add_hashtags(hashtags)

    # Evict old tweetss
    while len(self.queue) > 0:
      hashtags, current_ts = self.queue[0]
      if (current_ts + 60) >= ts:
        break

      self._remove(hashtags)
      self.queue.pop(0)

  def _add_hashtags(self, hashtags):
    for hashtag in hashtags:
      if hashtag in self.vertices:
        self.vertices[hashtag] += 1
      else:
        self.vertices[hashtag] = 1

    for edge in itertools.combinations(hashtags, 2):
      # Because hashtags are sorted, edge will also always
      # be sorted. 
      if edge in self.edges:
        self.edges[edge] += 1
      else:
        self.edges[edge] = 1

  def _remove(self, hashtags):
    for hashtag in hashtags:
      self.vertices[hashtag] -= 1
      if self.vertices[hashtag] == 0:
        del self.vertices[hashtag]

    for edge in itertools.combinations(hashtags, 2):
      self.edges[edge] -= 1
      if self.edges[edge] == 0:
        del self.edges[edge]

  def degree(self):
    num_vertices = len(self.vertices)
    if num_vertices == 0:
      return 0.0
    # We have to multiply edges by 2 as we store each edge only once.
    return len(self.edges) * 2 / float(num_vertices)


def parse_line(line):
  hashtags = HASHTAG_RE.findall(line)
  dt = time.strptime(TS_RE.findall(line)[0], '%a %b %d %H:%M:%S +0000 %Y')
  return hashtags, time.mktime(dt)

import time
if __name__ == "__main__":
  g = RunningAvgDegre()
  for line in sys.stdin:
    # Finish on empty line (this makes us able to reuse the result of tweets_cleaner)
    if line.strip() == "":
      break
    tags, ts = parse_line(line)

    # 1. Lowercase all tags
    # 2. Make them unique
    # 3. Sort them
    tags = sorted(set([x.lower() for x in tags]))
    g.new_tweet(tags, ts)
    print ("%.2f" % g.degree())
