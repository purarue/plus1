A symmetric substitution cipher that adds/subtracts one to each unicode character in a file/directory.

The motivation for this was to obfuscate code so I could [post solutions online](https://github.com/seanbreckenridge/CS-Assignments) without them being indexed.

```
usage: python3 run.py [-h] [-r] [-d] [-i] [--hidden-files]
                      [--hidden-directories] -f FILE (-a | -s)

A symmetric substitution cipher that adds/subtracts one to each unicode
character in a file/directory.

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       encrypt/decrypt directories recursively
  -d, --delete          after encrypting/decrypting, delete the original file
  -i, --ignore-blacklist
                        ignore the extension blacklist and consider files that
                        would have been blocked otherwise
  --hidden-files        don't ignore hidden files
  --hidden-directories  don't ignore hidden directories

required arguments:
  -f FILE, --file FILE  file or directory to encode/decode
  -a, --add             encrypt; add 1 to each unicode character
  -s, --subtract        decrypt; subtract 1 from each unicode character
```

Example:

```
~/bin/plus1 $ ls
README.md run.py
~/bin/plus1 $ echo 123abc > temp.txt
~/bin/plus1 $ python3 run.py -adf temp.txt
~/bin/plus1 $ ls
README.md       run.py          temp[plus1].txt
~/bin/plus1 $ cat temp\[plus1\].txt
234bcd
~/bin/plus1 $ python3 run.py -sdf temp\[plus1\].txt
~/bin/plus1 $ ls
README.md run.py    temp.txt
~/bin/plus1 $ cat temp.txt
123abc
```
