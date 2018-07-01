#!/usr/bin/env python3
import jieba
import unicodedata
import sys

dict_file = sys.argv[1]
sentences_file = sys.argv[2]

traditional_words = set()
simplified_words = set()

with open(dict_file) as f:
  for line in f:
    if line.startswith('#') or not line.strip():
      continue
    trad, simp, rest = line.split(maxsplit=2)
    traditional_words.add(trad)
    simplified_words.add(simp)

def is_traditional(sentence):
  words = jieba.cut(sentence)
  for word in words:
    if not all(unicodedata.category(c) == 'Lo' for c in word):
      continue

    if word in traditional_words:
      continue

    if word in simplified_words:
      return False

    for c in word:
      if c in traditional_words:
        continue

      if c in simplified_words:
        return False

      # raise Exception(f'Unknown character {c}!')
      return False

  return True

with open(sentences_file) as f:
  for line in f:
    sentence = line.split('\t')[-1]
    if is_traditional(sentence):
      sys.stdout.write(line)
