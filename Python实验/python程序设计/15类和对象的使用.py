class Student:
    def __init__(self):
        self.__name = ''
        self.__sex = ''
        self.__studentID = ''
        self.__age = 0
        self.__major = ''

    def set_name(self, name):
        self.__name = name

    def set_sex(self, sex):
        self.__sex = sex

    def set_studentID(self, studentID):
        self.__studentID = studentID

    def set_age(self, age):
        self.__age = age

    def set_major(self, major):
        self.__major = major

    def get_name(self):
        return self.__name

    def get_sex(self):
        return self.__sex

    def get_studentID(self):
        return self.__studentID

    def get_age(self):
        return self.__age

    def get_major(self):
        return self.__major

    def __init__(self, name, sex, studentID, age, major):
        self.__name = name
        self.__sex = sex
        self.__studentID = studentID
        self.__age = age
        self.__major = major

    def printInfo(self):
        print("姓名：%s，性别：%s，学号：%s,年龄：%d,专业：%s" % (
        self.__name, self.__sex, self.__studentID, self.__age, self.__major))

    def __str__(self):
        return "姓名：%s，性别：%s，学号：%s,年龄：%d,专业：%s" % (
        self.__name, self.__sex, self.__studentID, self.__age, self.__major)


name = input().strip()
sex = input().strip()
age = input().strip()
major = input().strip()
studentID = input().strip()

s = Student(name, sex, studentID, int(age), major)
s.printInfo()