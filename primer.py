from random import randint

def randnum_find(r_num):
    count = 0
    start = 1
    end = 1000000

    while start <= end:
        count += 1
        guess = (start + end) // 2

        if guess == r_num:
            return count
        elif guess < r_num:
            start = guess + 1
        else:
            end = guess - 1

num_counts = [randnum_find(randint(1, 1000000)) for _ in range(10 ** 6)]
print('Среднее число угадываний:', sum(num_counts) / len(num_counts))
for i in range(1, 25):
    print(f'Угадал с {i}-го раза: {num_counts.count(i)} раз ')
