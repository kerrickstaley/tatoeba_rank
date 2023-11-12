# tatoeba_rank
Contains source code used to generate the [tatoeba_sentences.yaml](https://github.com/kerrickstaley/Chinese-Vocab-List/blob/master/reference_files/tatoeba_sentences.yaml) file for the [Chinese Vocab List](https://github.com/kerrickstaley/Chinese-Vocab-List) project.

## Setup
### macOS
1. Run `brew install opencc`
1. Run `python3 -m pip install pypinyin`
1. Switch to GNU binaries:
   ```
   brew install coreutils grep gnu-sed gnu-tar
   # The below commands last for the duration of your terminal session.
   # Put them in ~/.zshrc to make them permanent.
   export PATH="/opt/homebrew/opt/coreutils/libexec/gnubin:$PATH"  # coreutils
   export PATH="/opt/homebrew/opt/grep/libexec/gnubin:$PATH"       # grep
   export PATH="/opt/homebrew/opt/gnu-sed/libexec/gnubin:$PATH"    # sed
   export PATH="/opt/homebrew/opt/gnu-tar/libexec/gnubin:$PATH"    # tar
   ```

## Usage
Run `make` to build `trad_simp_eng_pinyin.yaml`, which is the final output file.

## Similar projects
* [tatoeba-easy-translations](https://github.com/tomcumming/tatoeba-easy-translations)
