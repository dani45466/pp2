students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)


# sorting by module
numbers = [-10, 5, -3, 2]
result = sorted(numbers, key=lambda x: abs(x))
print(result)



#sorting by string length
words = ["apple", "kiwi", "banana", "fig"]
result = sorted(words, key=lambda word: len(word))
print(result)



#sorting a list of tuples (by age)
students = [("Danial", 20), ("Anna", 18), ("Bob", 22)]
result = sorted(students, key=lambda student: student[1])
print(result)



numbers = [1, 4, 2, 5, 3]
result = sorted(numbers, key=lambda x: x, reverse=True)
print(result)

