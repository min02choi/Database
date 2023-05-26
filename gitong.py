import math

def printArray(arr):
    for i in arr:
        print(i, end = " ")
    print()

def getS(arr, n):
    front = sum([m * m for m in arr])
    back = n * (sum(arr) / n)**2
    print(front, back)
    return front - back

def getSxy(x, y, n):
    front = sum([x[i] * y[i] for i in range(n)])
    back = (sum(x) / n) * (sum(y) / n) * n
    return front - back


age = [ 74, 63, 56, 54, 39, 17, 52, 20, 38,
        31, 57, 31, 32, 57, 67, 55, 41, 34, 
        60, 37, 83, 49, 45, 23, 33, 68, 53 ]

king = [  7,  2, 18, 32,  2,  3, 14,  1, 25,
         12, 39,  1, 22, 41, 15, 27, 10, 15,
         46,  4, 52, 24, 34, 15, 14, 44,  3  ]

avg = sum(age) / 27
print(avg)

one = [ m - avg for m in age ]
two = [ (m - avg)**2 for m in age ]
three = [ (m - avg)**3 for m in age ]
four = [ (m - avg)**4 for m in age ]

printArray(two)
printArray(three)
printArray(four)

print(sum(two))
print(sum(two) / 26)
print(sum(three) / 26)
print(sum(four) / 26)


print()
####################################
print("표본 표준편차 구히기")
total = 0
n = 27
for i in age:
    temp = (i - avg)**2
    total += temp
var = total / (n - 1)
s = math.sqrt(var)
print("var: ", var, "s: ", s)


####################################



# s = 16.8
z = [ (m - avg) / s for m in age ]
print("표준화 자료 z")
printArray(z)
print(sum(z))

n = 27
# 왜도, 첨도 계산
k3 = sum([m**3 for m in z]) / (n - 1)
k4 = sum([m**4 for m in z]) / (n - 1)

print("왜도: ", k3, "첨도: ", k4)

print()

Sxx = getS(age, 27)
Syy = getS(king, 27)
Sxy = getSxy(age, king, 27)

print("Sxx", Sxx, "Syy", Syy, "Sxy", Sxy)
print(Sxy / (math.sqrt(Sxx) * math.sqrt(Syy)))


#############################

EX2 = [m * m for m in age]
print(EX2, sum(EX2))

Ex2 = sum([m for m in age]) / 27
print(Ex2**2)