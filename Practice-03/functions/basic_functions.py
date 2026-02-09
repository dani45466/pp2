def my_function():
  print("Hello from a function")

my_function()


#2 ex
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))



#3 ex
def greet(name):
    print("Hello,", name)

greet("Danial")



#4 ex
def add_numbers(a, b):
    return a + b

result = add_numbers(3, 5)
print(result)



#5 ex
def power(number, exponent=2):
    return number ** exponent

print(power(4))      # uses default exponent (2)
print(power(2, 3))   # uses custom exponent



