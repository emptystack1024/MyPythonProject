r = 6378.137
p = 3.141592653589793

a1,a2 = map(float,input().split())

tal = abs(a1 - a2)
tal = min(tal,360-tal)

print("{:.3f}".format(2*p*r*tal/360))