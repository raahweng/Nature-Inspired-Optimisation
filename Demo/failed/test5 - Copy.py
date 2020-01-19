upper = 0
lower = 0
counter = 3
chance = 99
for k in range(counter):
    lower = upper
    upper += (99/(counter*(counter+1)/2))*(k+1)
    print(lower, upper)
    if lower <= chance <= upper:
        print("chance:", str(k+1))
