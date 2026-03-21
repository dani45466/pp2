

from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

# map()
doubled = list(map(lambda x: x * 2, numbers))


# filter()
evens = list(filter(lambda x: x % 2 == 0, numbers))


# reduce()
total = reduce(lambda a, b: a + b, numbers)


product = reduce(lambda a, b: a * b, numbers)
