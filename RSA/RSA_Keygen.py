import random
E = 3
times = 20


def test_miller_rabin(number):
    n = number - 1
    k = 0
    while n % 2 == 0:
        n //= 2
        k += 1
    m = n
    a = random.randrange(1, number - 1, 1)
    b = pow(a, m, number)
    if b % number == 1:
        return True
    for i in range(k):
        if b % number == number - 1:
            return True
        else:
            b = pow(b, 2, number)
    return False


def ext_euclidean_algorithm(a, b):
    rest = -1
    x0, x1, y0, y1 = 0, 1, 1, 0
    while rest != 0:
        div = a // b
        rest = a - (b * div)
        a = b
        b = rest
        y0, y1 = y1, y0 - div * y1  # keep track of the divisors
        x0, x1 = x1, x0 - div * x1
    return a, x0, y0


def prime_test(number):     # run miller rabin n times to minimize chance of not being prime
    for _ in range(times):
        if not test_miller_rabin(number):
            return False
    return True


def find_prime():   # run through likely prime candidates and test them with miller rabin
    x = random.randrange(1, 2 ** 32)
    add_list = [1, 11, 17, 23, 29]
    while not prime_test(x):
        x = random.randrange(1, 2 ** 32)
        for i in add_list:
            if prime_test(x + i):
                break
    return x


def write_keys_to_file(key, mod, file_name):
    key_out = open(file_name, "w")
    key_out.write(str((key, mod)))
    key_out.close()


def main():
    p = find_prime()
    while p % E == 1:  # prime - 1 should not be divisible by 3 (because of EEA)
        p = find_prime()
    q = find_prime()
    while q % E == 1:
        q = find_prime()
    phi = (p - 1) * (q - 1)
    n = p * q
    ggT, lam, my = ext_euclidean_algorithm(phi, E)
    write_keys_to_file(lam, n, "private_key.txt")
    write_keys_to_file(3, n, "public_key.txt")


if __name__ == "__main__":
    main()
