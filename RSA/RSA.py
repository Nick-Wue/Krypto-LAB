import BitVector
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("key_file",
                        type=str,
                        help="text file containing the public or private key")
arg_parser.add_argument("input_file",
                        type=str,
                        help="text file to be encrypted / decrypted")
arg_parser.add_argument("-d", "--decrypt_flag",
                        action="store_true",
                        default=False,
                        help="enable decryption mode")
arg_parser.add_argument("-o", "--output_file",
                        type=str,
                        default="output.txt",
                        help="set an output file")
arguments = arg_parser.parse_args()


def encrypt_block(text_block, key, mod):
    return pow(text_block.int_val(), key, mod)


def decrypt_block(blocked_crypt, key, mod):
    decrypted_block = pow(blocked_crypt, key, mod)
    bv = BitVector.BitVector(intVal=decrypted_block)
    if len(bv) % 8 != 0:    # pad to multiple of 8 from left for get_bitvector_in_ascii()
        times_to_pad = (len(bv) // 8 + 1) * 8 - len(bv)
        bv.pad_from_left(times_to_pad)
    return bv.get_bitvector_in_ascii()


def input_block_and_convert(text):  # conversion to BitVector to get bit representation of Blocks
    padding = ""
    vector_list = list()
    if len(text) % 4 != 0:  # pad to 32 bit length
        times_to_pad = (len(text) // 4 + 1) * 4 - len(text)
        padding = times_to_pad * " "
    text += padding
    number_of_blocks = len(text) // 4
    for i in range(number_of_blocks):  # slice to 4 Byte chunks
        text_block = text[4 * i: 4 * i + 4]
        vector_list.append(BitVector.BitVector(textstring=text_block))
    return vector_list


def out_to_file(text):
    bit_out = open(arguments.output_file, "w")
    bit_out.write(text)
    bit_out.close()


def fetch_from_textfile():
    inp = open(arguments.input_file, "r")
    text = inp.read()
    inp.close()
    return text


def encrypt_list(clear_text_list, key, mod):
    encrypted_int_list = list()
    for number in clear_text_list:
        encrypted_int = encrypt_block(number, key, mod)
        encrypted_int_list.append(encrypted_int)
    return encrypted_int_list


def decrypt_list(number_list, key, mod):
    decrypted_text = ""
    for number in number_list:
        decrypted_text += decrypt_block(int(number), key, mod)
    return decrypted_text


def fetch_key():
    pkey_in = open(arguments.key_file, "r")
    key_text = pkey_in.read()[1:-1]
    key, mod = key_text.split(",")
    pkey_in.close()
    return int(key), int(mod)


def fetch_from_encrypted():  # to get and prepare the encrypted integers
    in_encrypted = open(arguments.input_file, "r")
    numbers_as_text = in_encrypted.read()[1:-1]
    numbers_list = numbers_as_text.split(",")
    return numbers_list

def main():
    if arguments.decrypt_flag:
        private_key, mod = fetch_key()
        encrypted_numbers_list = fetch_from_encrypted()
        decrypted_text = decrypt_list(encrypted_numbers_list, private_key, mod)
        out_to_file(decrypted_text)
        print("Done!")
    else:
        public_key, mod = fetch_key()
        text = fetch_from_textfile()
        vector_list = input_block_and_convert(text)
        encrypted_list = encrypt_list(vector_list, public_key, mod)
        out_to_file(str(encrypted_list))
        print("Done!")


if __name__ == "__main__":
    main()

