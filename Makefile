sentences.tar.bz2:
	curl -L http://downloads.tatoeba.org/exports/sentences.tar.bz2 > $@

sentences.csv: sentences.tar.bz2
	tar -xjf $< --touch

links.tar.bz2:
	curl -L http://downloads.tatoeba.org/exports/links.tar.bz2 > $@

links.csv: links.tar.bz2
	tar -xjf $< --touch

cedict_1_0_ts_utf-8_mdbg.txt.gz:
	curl -L https://www.mdbg.net/chinese/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz > $@

cedict_1_0_ts_utf-8_mdbg.txt: cedict_1_0_ts_utf-8_mdbg.txt.gz
	zcat $< > $@

sentences_chinese.csv: sentences.csv
	grep -P '^[^\t]+\tcmn\t' $< > $@

sentences_english.csv: sentences.csv
	grep -P '^[^\t]+\teng\t' $< > $@

links_filtered.csv: filter_links.py links.csv sentences_chinese.csv sentences_english.csv
	./filter_links.py links.csv sentences_chinese.csv sentences_english.csv > $@

sentences_traditional.csv: filter_traditional.py sentences_chinese.csv cedict_1_0_ts_utf-8_mdbg.txt
	./filter_traditional.py cedict_1_0_ts_utf-8_mdbg.txt sentences_chinese.csv > $@

sentences_traditional_ranked.csv: rank.py subtlex_ch.tsv sentences_traditional.csv
	./rank.py subtlex_ch.tsv hanziDB.csv sentences_traditional.csv > $@

trad_eng.yaml: join_chinese_and_english.py sentences_traditional_ranked.csv sentences_english.csv links_filtered.csv
	./join_chinese_and_english.py sentences_traditional_ranked.csv sentences_english.csv links_filtered.csv > $@

trad_simp_eng.yaml: add_simp.py trad_eng.yaml
	./add_simp.py trad_eng.yaml > $@

trad_simp_eng_pinyin.yaml: add_pinyin.py trad_simp_eng.yaml
	./add_pinyin.py trad_simp_eng.yaml > $@
