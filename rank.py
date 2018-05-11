#!/usr/bin/env python3
import jieba
import sys
import unicodedata

IGNORE_WORDS = frozenset([
  '汤姆',  # "Tom" (simplified)
  '湯姆',  # "Tom" (traditional)
  '玛丽',  # "Mary" (simplified)
  '瑪麗',  # "Mary" (traditional)
])


class WordRankerSubtlex:
  def __init__(self):
    self.rank_map = {}
    with open('subtlex_ch.tsv') as f:
      next(f)  # skip first line
      for rank, line in enumerate(f):
        word = line.split()[0]
        # rank + 1 because rank is zero-indexed
        # setdefault because some words appear twice
        self.rank_map.setdefault(word, rank + 1)

  def rank(self, word):
    # returns None if word rank is unknown
    return self.rank_map.get(word)


class WordRankerTatoeba:
  # this is really inefficient, we're reading the file and cut()ing the sentences twice ¯\_(ツ)_/¯
  # also code duplication
  def __init__(self):
    counts = {}
    with open('sentences_filtered.csv') as f:
      for line in f:
        id_, lang, sentence = line.strip().split('\t')

        if lang != 'cmn':
          continue

        for word in jieba.cut(sentence):
          # we want to consider things like 的 which are "Letter, other" ("Lo")
          # but not things like 。 which are "Punctuation, other" ("Po")
          if unicodedata.category(word[0]) != 'Lo':
            continue
          if word in IGNORE_WORDS:
            continue

          counts.setdefault(word, 0)
          counts[word] += 1

    self.rank_map = {}

    words_sorted_by_count = sorted(counts, key=counts.get)
    for i, word in enumerate(reversed(words_sorted_by_count)):
      self.rank_map[word] = i + 1

  def rank(self, word):
    return self.rank_map.get(word)


class CharacterRanker:
  def __init__(self):
    self.rank_map = {}
    with open('hanziDB.csv') as f:
      next(f)  # skip first line
      for rank, line in enumerate(f):
        word = line.split(',')[1]
        # rank + 1 because rank is zero-indexed
        self.rank_map[word] = rank + 1

  def rank(self, word):
    return self.rank_map.get(word)


class SentenceRanker:
  def __init__(self):
    self.wrs = WordRankerSubtlex()
    self.cr = CharacterRanker()

  def rank(self, sentence):
    ranks = []  # rank of each word in sentence

    for word in jieba.cut(sentence):
      # we want to consider things like 的 which are "Letter, other" ("Lo")
      # but not things like 。 which are "Punctuation, other" ("Po")
      if unicodedata.category(word[0]) != 'Lo':
        continue
      if word in IGNORE_WORDS:
        continue

      word_rank = self.wrs.rank(word)
      if word_rank:
        ranks.append(word_rank)
        continue

      char_ranks = [self.cr.rank(c) for c in word]
      char_ranks = [r for r in char_ranks if r]
      if char_ranks:
        ranks.append(max(char_ranks))

    if not ranks:
      print(f'WARNING: Could not rank sentence {sentence}', file=sys.stderr)
      return float('inf')

    return sum(ranks) / len(ranks)


def extract_sentence_from_line(line):
  return line.split('\t')[2]


def main():
  sr = SentenceRanker()

  with open('sentences_filtered.csv') as f:
    ranked_cmn_lines = []
    for line in f:
      id_, lang, sentence = line.strip().split('\t')

      if lang != 'cmn':
        continue

      ranked_cmn_lines.append((sr.rank(sentence), line))

  ranked_cmn_lines.sort()

  for _, line in ranked_cmn_lines[:10]:
    print(line, end='')


if __name__ == '__main__':
  main()
