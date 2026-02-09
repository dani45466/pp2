numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)



numbers = [10, 15, 20, 25, 30]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)



numbers = [1, 3, 5, 7, 9, 2, 4]
greater_than_five = list(filter(lambda x: x > 5, numbers))
print(greater_than_five)




numbers = [-5, -2, 0, 3, 7, -1, 4]
positive_numbers = list(filter(lambda x: x > 0, numbers))
print(positive_numbers)




words = ["apple", "hi", "banana", "cat", "elephant"]
long_words = list(filter(lambda word: len(word) > 4, words))
print(long_words)
