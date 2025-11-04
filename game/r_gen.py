from random import randrange

def rgen():
    a = 0
    b = 0

    while True:
        for i in range(1, 101):
            number_01 = randrange(1, 100)

            if number_01 % 2 == 0:
                a = a + 1
            else:
                b = b + 1

        print(f"Четные: {a}, Нечетные: {b}")

        if a < b:
            return 1
        elif a > b:
            return 2
        else:
            return 3