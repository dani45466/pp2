n = int(input())

def g(n):
    for i in range(n+1):
        yield i*i



def even(n):
    for i in range(n+1):
        if i%2==0:
            yield i
print(",".join(str(num) for num in even(n)))



def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i



def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
a = int(input())
b = int(input())

for value in squares(a, b):
    print(value)



def countdown(n):
    for i in range(n, -1, -1):
        yield i