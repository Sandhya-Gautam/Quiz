def play_game():
    result = fizz_buzz(30)
    return result


def fizz_buzz(n):
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


def fibonacci():
    n = 10
    for i in range(n, 1):
        if i == 1:
            a = 1 + 0
            return a
        else:
            return fibonacci(n) + fibonacci(n - 1)


def test_fibonacci(benchmark):
    benchmark(fibonacci)


def test_game(benchmark):
    def run_game():
        for i in range(1, 101):
            play_game()

    benchmark(run_game)


def test_game2(benchmark):
    benchmark(play_game)
