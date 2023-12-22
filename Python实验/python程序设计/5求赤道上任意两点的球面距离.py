r = 6378.137
p = 3.141592653589793

str = input()
str1 = str.split(" ")
a1 = float(str1[0])
a2 = float(str1[1])

tal = abs(a1 - a2)
tal = min(tal,360-tal)

print("{:.3f}".format(2*p*r*tal/360))