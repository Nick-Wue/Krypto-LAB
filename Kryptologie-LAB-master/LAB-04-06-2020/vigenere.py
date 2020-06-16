import sys
import math

def calc_language_e_dictionary(language):
    lang_dict = get_count_dict(language)
    for entry in lang_dict:
        lang_dict[entry] /= len(language)
    return lang_dict


def calc_rauheit(text):
    alpha_dict = {}
    sum_ = 0
    for letter in text:
        if letter not in alpha_dict:
            alpha_dict[letter] = 1
        else:
            alpha_dict[letter] += 1
    for numbers in alpha_dict:
        sum_ += (alpha_dict[numbers] / len(text)) ** 2
    return sum_ - (1 / 128)


def get_count_dict(iterable):  #count unique elements in dictionary (element : count)
    lang_dict = {}
    for letter in iterable:
        if letter not in lang_dict:
            lang_dict[letter] = 1
        else:
            lang_dict[letter] += 1
    return lang_dict


def brute_rauheit(text): #calc rauheit to every possible blocklength,return list of average rauheitsgrade
    average_list = []
    for blocklength in range(1, 100):
        mr_sum = 0
        for blocksteps in range(1, blocklength + 1):
            iter_text = text[blocksteps::blocklength]
            mr_sum += calc_rauheit(iter_text)
        avg_mr = mr_sum / blocklength
        average_list.append(avg_mr)
    return average_list


def get_key(text, blocklength):
    key_list = list()
    for iterator in range(blocklength):
        blocked_text = text[iterator::blocklength]
        chi_list = list()
        for i in range(0, 128):
            decrypted_text_list = [chr((ord(letter) - i) % 128) for letter in blocked_text]
            chi_list.append(calc_chi(get_count_dict(decrypted_text_list)))
        key_list.append(get_index_of_min(chi_list)) #for smallest chi the textcolumn is nearest to the original
    return key_list                                  # distribution of letters


def find_smallest_mr(average_list):# because smallest mr is likely to be the keylenght this most likely works
    for i, entry in enumerate(average_list):
        if entry > 0.06:    #because rauheit of Laurem about 0.06 this works
            return i + 1


def calc_chi(count_dict): #calculate a metric that is small if the number of letters is close to the expected number in
    chi = 0                # of letters in the original language
    chi_sum = 0
    for i in count_dict:
        if i not in LANG_DICT:
            expected_count = 0
        else:
            expected_count = LANG_DICT[i]
        count = count_dict[i]
        chi = (count - expected_count) ** 2
        chi_sum += chi
    return math.sqrt(chi_sum)

def get_index_of_min(list):
    for i, value in enumerate(list):
        if value == min(list):
            return i


def decrypt(crypto_text, key_list):
    decrypt_text_list = list()
    for place_nr, letter in enumerate(crypto_text):
        decrypt_text_list.append(chr((ord(letter) - key_list[place_nr % len(key_list)]) % 128))
    return str("".join(decrypt_text_list))


LANGUAGE = open("lorem.txt", "r").read()    #Language is Lorem in this case but can be changed if needed
LANG_DICT = calc_language_e_dictionary(LANGUAGE)
crypt_in = open(sys.argv[1], "r")
crypt_text = crypt_in.read()
block_length = find_smallest_mr(brute_rauheit(crypt_text))
key = get_key(crypt_text, block_length)
clear_text = decrypt(crypt_text, key)
clear_out = open(sys.argv[2], "w")
clear_out.write(clear_text)
crypt_in.close()
clear_out.close()
