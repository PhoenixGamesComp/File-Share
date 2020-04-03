# File share
## This project was made in one and a half day. Feel free to suggest any improvement.
## Both scripts are written in python 3 only by using the modules that came with the language.

### Usage:
#### For the server you can just run the script like:
`python3 file-server.py`
### The script will detect your local ip address and host the server automatically.
### However in many UNIX-based systems the server detected ip is 127.0.0.1 which makes the server undetected to the local or the global network.
### You can use:
`python3 file-server.py --address [your_local_ip]`
### to host the server. Port forwarding the 9999 port you can make your server reachable to the global network.

### For the client there are three different modes to use:
`python3 file-client.py --mode [mode]`
### The available modes are:
###	-> single to transfer a single file
### -> multi to transfer every file in the given directory
### -> zip to compress the given folder before sending it

### Examples of running the client:
```
python3 file-client.py --mode single --dir C:\Users\Username\Documents\Test --file test.txt --address [server_address]
python3 file-client.py --mode multi --dir ~/Documents/Test --address [server_address]
python3 file-client.py --mode zip --dir [directory_path] --address [server_address]
```

### For both of the scripts you can use:
```
python3 file-server.py --help
python3 file-client.py --help
```
### if you need assistance
