Insight Data Engineering - Coding Challenge
===========================================================

Code should work out of the book on a recent version of both python2 and python3.

Optionaly if ujson library is available the tweets_cleaned.py will use that for a nice speed boost.
'pip install ujson'

Both scripts read input from stdin and write to stdout. It seems the simplest solution.
Script 2 (calculating average degree) works on the output of script 1. This enables us
to skip parsing the json again which is quite expensive..


Running run.sh (both scritps) takes about .65 seconds on my computer with ujson installed. That seems fast enough (get-tweets.py generates new tweets at a much slower rate).

Cleaning tweets: not much to say about this solutions. It is constrained by json decoding speed. 
It could easily be parallelized though.

Running average degree: 

We use a simple data structure that has 3 fields.
vertices : vertices of graph with corresponding number of lines they were seen in.
edges: edges of graph with corresponding number of lines they were seen in.
(Note that edges are always sorted so we need to store them only once per pair)
queue: this is a list of hashtags and the corresponding timestamps of when they were seen.

Every time we read a tweet we update the counts for vertices and edges. After that we
pop all the elements from the queue that are more than 60 seconds old and decrement 
counts. If an edge or vertex count drops to 0 we remove.

To calculate average degree we then just look at the length of vertices and edges field.