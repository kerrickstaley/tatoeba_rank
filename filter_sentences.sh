#!/bin/bash
grep -P '^[^\t]+\t(cmn|eng)\t' sentences.csv > sentences_filtered.csv
