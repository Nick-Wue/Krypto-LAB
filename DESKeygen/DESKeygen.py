#!/usr/bin/env python -W ignore::DeprecationWarning
import argparse
import string
import BitVector# https://engineering.purdue.edu/kak/dist/BitVector-3.1.1.html documentation
                 # very efficient for bitwise operations

def left_cyclic_shift(key_bitvector, n):
    original_length = len(key_bitvector)
    key_bitvector += key_bitvector[0:n] #append first n bits to end of new vector
    key_bitvector.shift_left(n)        # logic shift (lose first n bits, appended bits shift into original vectorlenght)
    return key_bitvector[0:original_length]  #cut vector to original length


def check_hex(key): #checks if key is hexadecimal
    for letters in key:
        if letters not in string.hexdigits:
            return False
    return True

#setting up argument parser
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-n", "--number_of_keys", type=int, default=16, help="set how many keys are generated")
arg_parser.add_argument("key", type=str, help="set the key in hexadecimal and length according to the permutation")
arg_parser.add_argument("-o", "--output_file", type=str, help="define an output file", default="output.txt")
arg_parser.add_argument("-p", "--permutation", type=str, help="set a custom permutation", default="permutation.txt")
arguments = arg_parser.parse_args()


permutation_in = open(arguments.permutation, "r")
permutation_list = permutation_in.read()[1:-2:1].split(",") #prep permutation list
permutation_list_int = [int(i) for i in permutation_list] #convert to contain integers for BitVectors permute()
permutation_in.close()

#check if key is valid
if 4 * len(arguments.key) == len(permutation_list) and check_hex(arguments.key):
    original_key = BitVector.BitVector(hexstring=arguments.key)
else:
    print("Given key was wrong. Use -h for usage.")
    exit()

#generating the required number of keys
generated_key_list = list()
for i in range(arguments.number_of_keys):
    left_key, right_key = original_key.divide_into_two()  #splits key into left and right part
    left_key = left_cyclic_shift(left_key, 2)
    right_key = left_cyclic_shift(right_key, 2)
    original_key = left_key + right_key
    generated_key_list.append(str(original_key.permute(permutation_list_int)))

#set an output file if given argument
if arguments.output_file:
    output_file = open(arguments.output_file, "w")
    output_file.write(str(generated_key_list))
    output_file.close()
else:
    print(str(generated_key_list))
