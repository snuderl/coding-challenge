import unittest
import average_degree

class RunningAvgDegreTest(unittest.TestCase):
	def setUp(self):
		self.avg = average_degree.RunningAvgDegre()

	def test_single_edge_should_have_degree_one(self):
		self.avg.new_tweet(["spark", "hbase"], 1)
		self.assertEquals(self.avg.degree(), 1)

	def test_eviction(self):
		self.avg.new_tweet(["spark", "hbase"], 1)
		self.avg.new_tweet(["bla", "ble"], 1)

		self.assertEquals(len(self.avg.vertices), 4)
		self.assertEquals(len(self.avg.edges), 2)

		# At time 61, tweets with time 1 are exactly 60 seconds old 
		# and should not be evicted.
		self.avg.new_tweet([], 61)
		self.assertEquals(len(self.avg.vertices), 4)
		self.assertEquals(len(self.avg.edges), 2)

		# At 62 tweets with time < 2 should be evicted.
		self.avg.new_tweet([], 62)
		self.assertEquals(len(self.avg.vertices), 0)
		self.assertEquals(len(self.avg.edges), 0)

	def test_inserting_same_stuff_shouldnt_change_anything(self):
		self.avg.new_tweet(["spark", "hbase"], 1)
		self.avg.new_tweet(["spark", "hbase"], 1)
		self.assertEquals(len(self.avg.vertices), 2)
		self.assertEquals(len(self.avg.edges), 1)

		self.avg.new_tweet([], 62)
		self.assertEquals(len(self.avg.vertices), 0)
		self.assertEquals(len(self.avg.edges), 0)

	def test_sample(self):
		self.avg.new_tweet(("apache", "spark"), 1)
		self.assertEquals(self.avg.degree(), 1)
		self.assertEquals(len(self.avg.vertices), 2)
		self.assertEquals(len(self.avg.edges), 1)

		self.avg.new_tweet(("apache", "hadoop", "storm"), 2)
		self.assertEquals(self.avg.degree(), 2)
		self.assertEquals(len(self.avg.vertices), 4)
		self.assertEquals(len(self.avg.edges), 4)

		self.avg.new_tweet(["apache"], 3)
		self.assertEquals(self.avg.degree(), 2)
		self.assertEquals(len(self.avg.vertices), 4)
		self.assertEquals(len(self.avg.edges), 4)

		self.avg.new_tweet(["flink", "spark"], 4)
		self.assertEquals(self.avg.degree(), 2)
		self.assertEquals(len(self.avg.vertices), 5)
		self.assertEquals(len(self.avg.edges), 5)

		self.avg.new_tweet(["apache", "hbase"], 5)
		self.assertEquals(self.avg.degree(), 10 / 5.0)
		self.assertEquals(len(self.avg.vertices), 6)
		self.assertEquals(len(self.avg.edges), 6)


		# spark - apache, and spark vertex should get evicted after this
		self.avg.new_tweet(["apache", "hadoop"], 62)
		self.assertEquals(self.avg.degree(), 10 / 6.0)
		self.assertEquals(len(self.avg.vertices), 6)
		self.assertEquals(len(self.avg.edges), 5)


class ParseTest(unittest.TestCase):
	def test_parse_line(self):
		line = "We're #hiring! Click to apply: SMB Analyst #BusinessMgmt #NettempsJobs #MenloPark (timestamp: Fri Oct 30 15:29:45 +0000 2015)"
		tags, ts = average_degree.parse_line(line)

		self.assertEquals(tags, ["hiring", "BusinessMgmt", "NettempsJobs", "MenloPark"])

	def test_timestamp_parse(self):
		line = "(timestamp: Fri Oct 30 15:29:45 +0000 2015)"
		_, ts = average_degree.parse_line(line)

		line2 = "(timestamp: Fri Oct 30 15:29:50 +0000 2015)"
		_, ts2 = average_degree.parse_line(line2)

		self.assertEquals(ts + 5, ts2)


if __name__ == "__main__":
	unittest.main()