upper = 0
lower = 0
pointnum = 10
counter = 2
chance = 3
for k in range(counter):
    lower = upper
    upper += ((pointnum-1)/(counter*(counter+1)/2))*(k+1)
    if lower <= chance <= upper:
        print(k)
