#!/usr/bin/env python3
import sys

sentence_ids = set()

with open('sentences_filtered.csv') as f:
  for line in f:
    sentence_ids.add(line.split('\t')[0])

print('Done loading sentence IDs', file=sys.stderr)

with open('links.csv') as fin, open('links_filtered.csv', 'w') as fout:
  for line in fin:
    ida, idb = line.strip().split('\t')
    if ida in sentence_ids and idb in sentence_ids:
      fout.write(line)


