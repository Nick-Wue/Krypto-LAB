import sys


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


def brute_rauheit(text):
    for iterator in range(1, 100):
        mr_sum = 0
        for j in range(1, iterator + 1):
            iter_text = text[j::iterator]
            mr_sum += calc_rauheit(iter_text)
        avg = mr_sum / iterator
        print("Blocklength: {}, MR : {}".format(iterator, avg)) #TODO: Alle MR in Liste, max berechnen, kgt finden
                                                                # -> Wahrscheinlich Blocklänge.


text = open("encrypted-lorem-3.txt", "r")
brute_rauheit(text.read())

