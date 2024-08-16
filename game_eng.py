import random

def get_number(prompt, a=None, b=None):
    while True:
        try:
            number = int(input(prompt))
            if a is not None and b is not None and (number < a or number > b):
                print(f'You did not enter a number between {a} and {b}.')
            else:
                return number
        except ValueError:
            print('Please enter a valid number.')

def game():
    a = get_number('Enter the starting number: ')
    b = get_number('Enter the ending number: ')
    while a >= b:
        print('The ending number must be greater than the starting number.')
        b = get_number('Enter the ending number: ')
    x = random.randint(a, b)
    count = 0
    while True:
        y = get_number(f'Enter a number between {a} and {b}: ', a, b)
        count += 1
        if y == x:
            print('Congratulations, you guessed it:', x)
            break
        else:
            print('Incorrect, the number is greater' if x > y else 'Incorrect, the number is smaller')
    print(f"Total attempts made: {count}")
    print('Let\'s start again!')
    game()

game()
