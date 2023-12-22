class date:
    def __init__(self, year: int, month: int, day: int):
        self.year = year
        self.month = month
        self.day = day

    def __str__(self):
        if self.month < 10 and self.day < 10:
            return '{}年0{}月0{}日'.format(self.year, self.month, self.day)
        if self.month < 10:
            return '{}年0{}月{}日' .format(self.year, self.month, self.day)
        if self.day < 10:
            return '{}年{}月0{}日' .format(self.year, self.month, self.day)
        return '{}年{}月{}日'.format(self.year, self.month, self.day)

class person:
    def __init__(self, name:str, date:date):
        self.name = name
        self.date = date

class student(person):
    def __init__(self, name:str, date:date, stuID:int, Major:str):
        person.__init__(self, name, date)
        self.stuID = stuID
        self.Major = Major

    def whatsyourbithday(self):
        return self.date

    def __str__(self):
        return "I'm {}，my birthday is {} , my stuID is {} and my major is {}".format(self.name, self.whatsyourbithday(), self.stuID, self.Major)

w = date(2000, 11, 11)
x = date(2003, 11, 1)
y = date(2004, 2, 12)
z = date(2005, 1, 3)

a = student('Li hua', x, 114514, 'Computer Science')
b = student('Xiao ming', y , 1008611, 'Mathematics')
c = student('Zhang san', z, 110119120, 'Physics')

print("不同生日之间的输出： ")
print(w)
print(x)
print(y)
print(z)

print("*********************************")
print("学生信息打印： ")
print(a)
print(b)
print(c)

