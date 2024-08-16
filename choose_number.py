def input_number(number):
    while True:
        try:
            user_input  = int(input(number))
            return user_input
        except ValueError:
            print("Пожалуйста, введите целое число.")

def choose_number():
    print("Давайте начнем игру! Загадайте число.")

    start_number = input_number("Введите начальное число: ")
    end_number = input_number("Введите конечное число: ")

    while end_number <= start_number:
        print("Конечное число должно быть больше начального.")
        end_number = input_number("Введите корректное конечное число: ")

    guess_number = input_number(f"Введите загаданное число ({start_number} - {end_number}): ")

    while guess_number < start_number or guess_number > end_number:
        print(f"Загаданное число должно быть в диапазоне от {start_number} до {end_number}.")
        guess_number = input_number(f"Введите корректное загаданное число: ")

    count = 0

    while True:
        count += 1
        guess = (start_number + end_number) // 2

        if guess == guess_number:
            print(f"Ура! Число {guess} угадано за {count} попыток.")
            break
        elif guess < guess_number:
            print(f"Ваше число больше, чем мое предположение {guess}.")
            start_number = guess + 1
        else:
            print(f"Ваше число меньше, чем мое предположение {guess}.")
            end_number = guess - 1
    choose_number()

choose_number()
# Написать код для чтобы узнать какие числа угадает за меньше попыток