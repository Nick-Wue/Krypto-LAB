This is a command line tool to encrypt/decrypt ASCII encoded text using a modified DES encryption.
To get a working list of keys use the DESKeygen tool provided. 

Dependencies: BitVector module: https://engineering.purdue.edu/kak/dist/BitVector-3.1.1.html
	      Python3
Usage: 

python DES.py -h 
- for help

python DES.py key_file input_file [-o output_file] [-d]

-d option for decryption
