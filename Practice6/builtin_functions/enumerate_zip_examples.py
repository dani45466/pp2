

names = ["Ali", "Dana", "Mira"]
scores = [85, 90, 78]

for index, name in enumerate(names, start=1):
    print(index, name)


for name, score in zip(names, scores):
    print(name, score)

for index, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{index}. {name} -> {score}")



# type_conversion.py

x = "123"
y = 45.67
z = 1

print("Типы до преобразования:")
print(type(x))
print(type(y))
print(type(z))
print()

a = int(x)
b = float(x)
c = str(y)
d = bool(z)

print("После преобразования:")
print(a, type(a))
print(b, type(b))
print(c, type(c))
print(d, type(d))