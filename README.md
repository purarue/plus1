# plus1

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

A symmetric substitution cipher that adds/subtracts one to each Unicode character in a file/directory.

The motivation for this was to obfuscate code so I could [post solutions online](https://github.com/purarue/CS-Assignments) without them being indexed.

`plus1` creates an extension blacklist at `~/.config/plus1_blacklist.txt` (a plain text file), which defines extension types to ignore, one per line. These will be ignored by plus1 unless the `--ignore-blacklist` option is passed. Some extensions you may want to ignore are listed in [`plus1_blacklist.txt.dist`](./plus1/plus1_blacklist.txt.dist).

Requires: python3.4+

Install: `pip3 install git+https://github.com/purarue/plus1`

```
usage: plus1 [-h] [-r] [-d] [-i] [--encrypt-hidden-files]
             [--encrypt-hidden-directories] [--force-delete] -f FILE (-a | -s)

A symmetric substitution cipher that adds/subtracts one to each unicode
character in a file/directory.

optional arguments:
  -h, --help                    show this help message and exit
  -r, --recursive               encrypt/decrypt directories recursively
  -d, --delete                  after encrypting/decrypting, delete the
                                original file
  -i, --ignore-blacklist        ignore the extension blacklist and consider
                                files that would have been ignored otherwise
  --hidden-files        don't ignore hidden files
  --hidden-directories  don't ignore hidden directories
  --force-delete                don't ask for confirmation when removing files

required arguments:
  -f FILE, --file FILE          file or directory to encrypt/decrypt
  -a, --add                     encrypt; add 1 to each unicode character
  -s, --subtract                decrypt; subtract 1 from each unicode
                                character
```

Example:

```
❯ find . -type f | xargs -I {} sh -c "echo {}; cat {}"
./bin/hi
echo hi!
./123.txt
123
./.secret
key=cOkcz3RzZkFENFWAaWxx

/tmp/example
❯ plus1 -adrf .
Skipping hidden file: /private/tmp/example/.secret
Encrypting /private/tmp/example/bin/hi...
Remove '/private/tmp/example/bin/hi'? y
Encrypting /private/tmp/example/123.txt...
Remove '/private/tmp/example/123.txt'? y

/tmp/example
❯ find . -type f | xargs -I {} sh -c "echo {}; cat {}"
./bin/hi[plus1]
fdip!ij"
        ./123[plus1].txt
234
   ./.secret
key=cOkcz3RzZkFENFWAaWxx

/tmp/example
❯ plus1 -adf .secret --hidden-files
Encrypting /private/tmp/example/.secret...
Remove '/private/tmp/example/.secret'? y

/tmp/example
❯ find . -type f | xargs -I {} sh -c "echo {}; cat {}"
./bin/hi[plus1]
fdip!ij"
        ./123[plus1].txt
234
   ./.secret[plus1]
lfz>dPld{4S{[lGFOGXBbXyy

/tmp/example
❯ plus1 -sdrf . --force-delete --hidden-files
Decrypting /private/tmp/example/.secret[plus1]...
Decrypting /private/tmp/example/123[plus1].txt...
Decrypting /private/tmp/example/bin/hi[plus1]...

/tmp/example
❯ find . -type f | xargs -I {} sh -c "echo {}; cat {}"
./bin/hi
echo hi!
./123.txt
123
./.secret
key=cOkcz3RzZkFENFWAaWxx
```
