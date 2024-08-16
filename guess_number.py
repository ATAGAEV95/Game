import random

def input_number(number):
    while True:
        try:
            user_input  = int(input(number))
            return user_input
        except ValueError:
            print("Пожалуйста, введите целое число.")

def guess_number():
    print("Давайте начнем игру - угадай число.")

    start_number = input_number("Введите начальное число: ")
    end_number = input_number("Введите конечное число: ")

    while end_number <= start_number:
        print("Конечное число должно быть больше начального.")
        end_number = input_number("Введите корректное конечное число: ")

    random_number = random.randint(start_number, end_number)
    count = 0

    while True:
        my_number = input_number(f'Введите число от {start_number} до {end_number}: ')
        count += 1
        if my_number == random_number:
            print('Поздравляю, вы угадали:', random_number)
            break
        else:
            print('Неверно, загаданное число больше' if random_number > my_number else 'Неверно, загаданное число меньше')
    print(f"Попыток было сделано: {count}")
    print('Начнем заново!')
    guess_number()

guess_number()