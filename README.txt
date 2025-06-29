# Password Cracker Project

## How to Use

1. Open this folder in Visual Studio Code.
2. Make sure Python is installed on your system.
3. Open terminal inside VS Code.

### Run with wordlist:
```
python password_cracker.py 098f6bcd4621d373cade4e832627b4f6 --wordlist wordlist.txt
```

### Run with brute-force:
```
python password_cracker.py 098f6bcd4621d373cade4e832627b4f6 --min_length 1 --max_length 4
```

Sample hash = MD5("test") = 098f6bcd4621d373cade4e832627b4f6
