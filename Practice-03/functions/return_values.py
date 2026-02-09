#Functions can return values using the return statement:
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)




#A function that returns a tuple:

def my_function():
  return (10, 20)

x, y = my_function()
print("x:", x)
print("y:", y)





def is_even(number):
    return number % 2 == 0

print(is_even(4))  # True
print(is_even(7))  # False





def max_of_two(a, b):
    if a > b:
        return a
    else:
        return b

print(max_of_two(5, 9))





def calculate(a, b):
    sum_result = a + b
    diff_result = a - b
    return sum_result, diff_result

result = calculate(10, 3)
print(result) # returns a tuple

# unpacking
s, d = calculate(10, 3)
print(s, d)
