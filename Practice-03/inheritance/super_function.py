class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name)
s = Student("Danial")
print(s.name)




class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        super().speak()
        print("Dog barks")

d = Dog()
d.speak()





class Vehicle:
    def start(self):
        print("Vehicle starts")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car is ready")

c = Car()
c.start()




#multi-level inheritance
class A:
    def show(self):
        print("A")

class B(A):
    def show(self):
        super().show()
        print("B")

class C(B):
    def show(self):
        super().show()
        print("C")

c = C()
c.show()





class Account:
    def __init__(self, balance):
        self.balance = balance

class SavingsAccount(Account):
    def __init__(self, balance, interest):
        super().__init__(balance)
        self.interest = interest

a = SavingsAccount(1000, 5)
print(a.balance, a.interest)
