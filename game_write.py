import json
import os


def load_attempts(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}


def save_attempts(attempts_dict, filename):
    with open(filename, 'w') as file:
        json.dump(attempts_dict, file)


def play_game(guess_number):
    start_number = 1
    end_number = 100
    count = 0

    while True:
        count += 1
        guess = (start_number + end_number) // 2

        if guess == guess_number:
            return count
        elif guess < guess_number:
            start_number = guess + 1
        else:
            end_number = guess - 1


def main():
    filename = 'attempts_record.json'
    attempts_dict = load_attempts(filename)

    for guess_number in range(1, 101):
        if str(guess_number) not in attempts_dict:
            attempts = play_game(guess_number)
            attempts_dict[str(guess_number)] = attempts

    save_attempts(attempts_dict, filename)


main()