import BitVector
import argparse
import sys
import warnings

# Array.to_string() is deprecated in Python3.8 but is used in BitVector, it still works perfectly fine in this
# version but can't be guaranteed for future versions. Ideally there will be a release of BitVector in the future that
# fixes this but until then muting those Warnings seems reasonable.
warnings.filterwarnings("ignore", category=DeprecationWarning)


ROUNDS = 16
s_box_in = open("s-box.txt", "r")
s_box = s_box_in.read()[1:-2].split(",")  # read s-box as constant


arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("key_file", type=str, help="text file containing 16 round keys")
arg_parser.add_argument("input_file", type=str, help="text file to be encrypted")
arg_parser.add_argument("-d", "--decrypt_flag", action="store_true", default=False, help="enable decryption mode")
arg_parser.add_argument("-o", "--output_file", type=str, default="output.txt", help="set an output file")
arguments = arg_parser.parse_args()


def encrypt_block(clear_block, key_list):   # encrypt one 128 Bit Block
    left_key, right_key = clear_block.divide_into_two()
    for round in range(ROUNDS):
        round_key = key_list[round]  # get key for current round
        new_right_key = function(right_key, round_key) ^ left_key
        left_key = right_key
        right_key = new_right_key
    return right_key + left_key  # return swapped left and right


# as long as the encrypted text is some sort of natural text spaces at the end of given text have no meaning and
# can usually be removed. For other types of text this may cause problems because information is removed.
def remove_padding(clear_text):  # removes spaces at the end of cleartext (spaces are used for padding)
    for number, letter in enumerate(clear_text[::-1]):
        if letter != " ":
            return clear_text[:-number]


def s_box_func(byte):
    global s_box
    x = ord(byte.get_bitvector_in_ascii())
    return BitVector.BitVector(intVal=int(s_box[x]))


def function(bit_vector, round_key):  # calculates f on given block
    f_bit_vector = BitVector.BitVector(size=0)
    bit_vector = bit_vector ^ round_key
    for i in range(64 // 8):
        f_bit_vector += s_box_func(bit_vector[8 * i: 8 + i * 8])  # slice to 8 bit blocks and calculate s-box
    return f_bit_vector


def pad_and_slice(cleartext):
    padding = ""
    block_list = list()
    if len(cleartext) % 16 != 0:
        times_to_pad = (len(cleartext) // 16 + 1) * 16 - len(cleartext)
        padding = times_to_pad * " "
    cleartext = "".join((cleartext, padding))
    number_of_blocks = len(cleartext) // 16
    for i in range(number_of_blocks):
        block_list.append(BitVector.BitVector(textstring=cleartext[16 * i: 16 * i + 16]))  # cut text in 128 Bit long blocks
    return block_list


def encrypt_blocked_clear(blocked_list, key_list):
    encrypted_text = ""
    for i in blocked_list:
        encrypted_text += encrypt_block(i, key_list).get_bitvector_in_ascii()
    return encrypted_text


def fetch_key_list():
    key_in = open(arguments.key_file, "r")
    key_list = list()
    hex_key_list = key_in.read()[1:-2].split(",")
    for key in hex_key_list:
        key_list.append(BitVector.BitVector(hexstring=key.replace("'", "").replace(" ", "")))
    key_in.close()
    return key_list


def fetch_from_bytefile():
    bit_vector_list = list()
    bit_vector_reader = BitVector.BitVector(filename=arguments.input_file)
    while bit_vector_reader.more_to_read:
        bv_read = bit_vector_reader.read_bits_from_file(128)
        bit_vector_list.append(bv_read)
    bit_vector_reader.close_file_object()
    return bit_vector_list


def output_to_files(text):
    text_out = open(arguments.output_file, "w")
    text_out.write(text)
    text_out.close()


def decrypt(blocked_text, key_list):
    decrypted_list = list()
    for i in blocked_text:
        decrypted_list.append(encrypt_block(i, key_list))
    return decrypted_list


def output_as_bitfile(decrypted_list):
    bit_out = open(arguments.output_file + ".bit", "wb")
    for i in decrypted_list:
        i.write_to_file(bit_out)
    bit_out.close()


def main():
    key_list = fetch_key_list()
    if arguments.decrypt_flag:
        key_list = key_list[::-1]
        blocked_text = fetch_from_bytefile()
        cypher_text = encrypt_blocked_clear(blocked_text, key_list)
        cypher_text = remove_padding(cypher_text)
        output_to_files(cypher_text)
    else:
        text_in = open(arguments.input_file, "r")
        text = text_in.read()
        blocked_text = pad_and_slice(text)
        decrypted_list = decrypt(blocked_text, key_list)
        output_as_bitfile(decrypted_list)


if __name__ == "__main__":
    main()
