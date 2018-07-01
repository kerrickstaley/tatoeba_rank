#!/usr/bin/env python3
import jieba
import opencc
import sys
import unicodedata

subtlex_file = sys.argv[1]
hanzidb_file = sys.argv[2]
sentences_file = sys.argv[3]

IGNORE_WORDS = frozenset([
  '汤姆',  # "Tom" (simplified)
  '湯姆',  # "Tom" (traditional)
  '玛丽',  # "Mary" (simplified)
  '瑪麗',  # "Mary" (traditional)
])


class WordRankerSubtlex:
  def __init__(self):
    self.rank_map = {}
    with open(subtlex_file) as f:
      next(f)  # skip first line
      for rank, line in enumerate(f):
        word = line.split()[0]
        # rank + 1 because rank is zero-indexed
        # setdefault because some words appear twice
        self.rank_map.setdefault(word, rank + 1)

  def rank(self, word):
    # returns None if word rank is unknown
    if word in self.rank_map:
      return self.rank_map[word]

    simp_word = opencc.convert(word)
    if simp_word in self.rank_map:
      return self.rank_map[simp_word]

    return None


class WordRankerTatoeba:
  # this is really inefficient, we're reading the file and cut()ing the sentences twice ¯\_(ツ)_/¯
  # also code duplication
  def __init__(self):
    counts = {}
    with open(sentences_file) as f:
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

    last_count = 0
    last_rank = 0
    for i, word in enumerate(reversed(words_sorted_by_count)):
      # for words that have the same count, give them the same (tied) rank
      if counts[word] == last_count:
        rank = last_rank
      else:
        rank = i + 1

      self.rank_map[word] = rank

      last_count = counts[word]
      last_rank = rank

  def rank(self, word):
    return self.rank_map.get(word)


class CharacterRanker:
  def __init__(self):
    self.rank_map = {}
    with open(hanzidb_file) as f:
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
    self.wrt = WordRankerTatoeba()
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

      word_rank = self.wrt.rank(word)
      ranks.append(word_rank)

    if not ranks:
      print(f'WARNING: Could not rank sentence {sentence}', file=sys.stderr)
      return None

    return sum(ranks) / len(ranks)


def extract_sentence_from_line(line):
  return line.split('\t')[2]


def main():
  sr = SentenceRanker()

  with open(sentences_file) as f:
    ranked_cmn_lines = []
    for line in f:
      id_, lang, sentence = line.strip().split('\t')

      if lang != 'cmn':
        continue

      rank = sr.rank(sentence)

      if rank is not None:
        ranked_cmn_lines.append((rank, line))

  ranked_cmn_lines.sort()

  for rank, line in ranked_cmn_lines:
    print(line, end='')


if __name__ == '__main__' and not hasattr(sys, 'ps1'):
  main()
