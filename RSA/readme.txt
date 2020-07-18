This is a command line tool to encrypt/decrypt ASCII encoded text RES.
To get a public and a private key run the included RSA_Keygen script.
Use the public key for encryption and the private key for decryption.

Dependencies: BitVector module: https://engineering.purdue.edu/kak/dist/BitVector-3.1.1.html
	      Python3
Usage: 

python RSA.py -h 
- for help

python RSA.py key_file input_file [-o output_file] [-d]

-d option for decryption
