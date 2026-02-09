class Student:
    university = "ABC University"

s1 = Student()
s2 = Student()

print(s1.university)
print(s2.university)


class Student:
    university = "ABC University"

Student.university = "XYZ University"

s = Student()
print(s.university)



class Counter:
    count = 0

    def __init__(self):
        Counter.count += 1

a = Counter()
b = Counter()
c = Counter()

print(Counter.count)



class Dog:
    species = "Canine"

    def __init__(self, name):
        self.name = name

d1 = Dog("Buddy")
d2 = Dog("Max")

print(d1.species, d1.name)
print(d2.species, d2.name)




class Car:
    wheels = 4

car1 = Car()
car2 = Car()

car1.wheels = 6

print(car1.wheels)
print(car2.wheels)





