DESKeygen - Is a commandline tool for generating keys with a modified DES key generation.

Dependencies: python3 
	      BitVector Module	: https://engineering.purdue.edu/kak/dist/BitVector-3.4.9.html#42 

This tool takes any given key in hexadecimal notation and any given permutation and calculates a number of keys
using a modified version of the DES key generation. 
Be sure to use a key that is long enough for the given permutation.

USAGE:
	python DESKeygen.py [Key] [-n Number_of_Keys] [-o output_file] [-p permutation] 


For help use: 
	python DESKeygen.ph -h


Default values for optional parameters are: 
number_of_keys = 16, 
output_file = output.txt, 
permutation = permutation.txt
