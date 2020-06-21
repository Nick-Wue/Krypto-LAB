import struct
import sys
import string
import BitVector# https://engineering.purdue.edu/kak/dist/BitVector-3.1.1.html documentation
                 # very efficient for bitwise operations

def left_cyclic_shift(key_bitvector, n):
    original_length = len(key_bitvector)
    key_bitvector += key_bitvector[0:n] #append first n bits to end of new vector
    key_bitvector.shift_left(n)        # logic shift (lose first n bits, appended bits shift into original vectorlenght)
    return key_bitvector[0:original_length]  #cut vector to original length


permutation_in = open("permutation.txt", "r")
permutation_list = permutation_in.read()[1:-2:1].split(",") #prep permutation list
permutation_list_int = [int(i) for i in permutation_list] #convert to contain integers for BitVectors permute()
permutation_in.close()
key_number = int(sys.argv[1])
kbv = BitVector.BitVector(hexstring="A153B2142231917A")
generated_key_list = list()


for i in range(key_number):
    left_key, right_key = kbv.divide_into_two() # splits key into left and right part
    left_key = left_cyclic_shift(left_key, 2)
    right_key = left_cyclic_shift(right_key, 2)
    kbv = left_key + right_key
    generated_key_list.append(str(kbv.permute(permutation_list_int)))

print(generated_key_list)

