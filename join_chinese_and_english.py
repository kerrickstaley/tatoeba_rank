#!/usr/bin/env python3
import copy
import sys
import yaml

from collections import OrderedDict

chin_file = sys.argv[1]
eng_file = sys.argv[2]
links_file = sys.argv[3]

class UnionFind:
  def __init__(self):
    self.parent = {}

  def find(self, item):
    if item not in self.parent:
      return None

    if self.parent[item] == item:
      return item

    rv = self.find(self.parent[item])
    self.parent[item] = rv

    return rv

  def union(self, a, b):
    if a not in self.parent:
      self.parent[a] = a
    if b not in self.parent:
      self.parent[b] = b

    if self.find(a) == self.find(b):
      return

    self.parent[a] = self.find(b)


uf = UnionFind()
with open(links_file) as f:
  for line in f:
    s1, s2 = map(int, line.strip().split())
    uf.union(s1, s2)


chin_sentences = OrderedDict()
eng_sentences = OrderedDict()
for filename, dict_ in [(chin_file, chin_sentences), (eng_file, eng_sentences)]:
  with open(filename) as f:
    for line in f:
      pieces = line.strip().split('\t')
      dict_[int(pieces[0])] = pieces[2]

all_sentences = dict(chin_sentences)
all_sentences.update(eng_sentences)


groups = {}
for id_, sentence in all_sentences.items():
  group = uf.find(id_)
  groups.setdefault(group, {'chin': [], 'eng': []})
  if id_ in chin_sentences:
    groups[group]['chin'].append(sentence)
  else:
    groups[group]['eng'].append(sentence)


groups_list = []
used_groups = set()
for id_, sentence in chin_sentences.items():
  if id_ in used_groups:
    continue
  groups_list.append(groups[uf.find(id_)])
  used_groups.add(uf.find(id_))


groups_list = [g for g in groups_list if len(g['chin']) == 1 and len(g['eng']) == 1]

output = [{'trad': g['chin'][0], 'eng': g['eng'][0]} for g in groups_list]

yaml.dump(output, sys.stdout, allow_unicode=True, default_flow_style=False)
