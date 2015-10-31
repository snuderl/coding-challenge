#!/usr/bin/env bash

# This script should be run from the root directory.
python src/tweets_cleaned.py < data-gen/tweets.txt > tweet_output/ft1.txt
python src/average_degree.py < tweet_output/ft1.txt > tweet_output/ft2.txt


