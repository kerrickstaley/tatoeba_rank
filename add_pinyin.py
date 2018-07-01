#!/usr/bin/env python3
import jieba
import pypinyin
import sys
import yaml

trad_simp_eng_file = sys.argv[1]

with open(trad_simp_eng_file) as f:
  data = yaml.load(f)


def get_pinyin(hanzi):
  words = jieba.cut(hanzi)
  word_pinyins = []
  for word in words:
    pinyin = ''.join(g[0] for g in pypinyin.pinyin(word))
    word_pinyins.append(pinyin)

  return ' '.join(word_pinyins)


for group in data:
  group['pinyin'] = get_pinyin(group['trad'])


yaml.dump(data, sys.stdout, allow_unicode=True, default_flow_style=False)
