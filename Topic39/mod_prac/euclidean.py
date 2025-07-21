def main():
    b = 26513
    a = 32321
    print(gcd(a, b))


def gcd(a, b):
    while b != 0:
        t = b
        b = a % b
        a = t
    return a

if __name__ == '__main__':
    main()