# acess instace var in static method
# acess class var in static method
# acess static var in static method

class Student:
    college = "ABC College"   # Class variable

    def __init__(self, name):
        self.name = name      # Instance variable

    @staticmethod
    def greet():
        print("Hello")

    @staticmethod
    def show():
        # Access class variable
        print(Student.college)

        # Access static method
        Student.greet()

Student.show()
