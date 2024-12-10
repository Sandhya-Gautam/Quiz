# from datetime import datetime

# pytest_plugins = ("pytest_benchmark",)

# def create_list(size):
#     return [i**2 for i in range(size)]

# def test_create_list():
#     n=10000
#     data=create_list(n)
#     assert len(data)==n

# def just_count_some_number():
#     for i in range(1_000_000_00):
#         pass


# def test_just_count(benchmark):
#     benchmark(just_count_some_number)


# def test_just_count(benchmark):
#     result = benchmark(just_count_some_number)
#     assert result is not None


# if __name__ == "__main__":
#     start_time = datetime.now()
#     just_count_some_number()
#     print(datetime.now() - start_time)

