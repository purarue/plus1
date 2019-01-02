A symmetric substitution cipher that adds/subtracts one to each unicode character in a file/directory.

The motivation for this was to obfuscate code so I could post solutions online without them being indexed.

```
usage: python3 run.py [-h] [-r] [-d] -f FILE (-a | -s)

optional arguments:
  -h, --help            show this help message and exit
  -r, --recursive       encypt/decrpyt files recursively. required for folders
  -d, --delete          after encrypting/decrypting, delete the original file

required arguments:
  -f FILE, --file FILE  file or directory to encode/decode
  -a, --add             encypt; add 1 to each unicode character
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