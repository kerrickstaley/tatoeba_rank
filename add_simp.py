#!/usr/bin/env python3
import opencc
import sys
import yaml

trad_eng_file = sys.argv[1]

with open(trad_eng_file) as f:
  data = yaml.full_load(f)


for group in data:
  group['simp'] = opencc.convert(group['trad'])


yaml.dump(data, sys.stdout, allow_unicode=True, default_flow_style=False)
