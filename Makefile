sentences.tar.bz2:
	curl -L http://downloads.tatoeba.org/exports/sentences.tar.bz2 > $@

sentences.csv: sentences.tar.bz2
	tar -xjf $< --touch

links.tar.bz2:
	curl -L http://downloads.tatoeba.org/exports/links.tar.bz2 > $@

links.csv: links.tar.bz2
	tar -xjf $< --touch

sentences_chinese.csv: sentences.csv
	grep -P '^[^\t]+\tcmn\t' $< > $@

sentences_english.csv: sentences.csv
	grep -P '^[^\t]+\teng\t' $< > $@

links_filtered.csv: links.csv sentences_chinese.csv sentences_english.csv
	./filter_links.py $^ > $@
