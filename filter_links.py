#!/usr/bin/env python3
import sys

link_file = sys.argv[1]
sentence_files = sys.argv[2:]

sentence_ids = set()
for sentence_file in sentence_files:
  with open(sentence_file) as f:
    for line in f:
      sentence_ids.add(line.split('\t')[0])

with open(link_file) as f:
  for line in f:
    ida, idb = line.strip().split('\t')
    if ida in sentence_ids and idb in sentence_ids:
      sys.stdout.write(line)


