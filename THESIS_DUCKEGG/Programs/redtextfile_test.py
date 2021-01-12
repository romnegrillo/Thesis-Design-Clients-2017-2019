data=[]
balut=[]
penoy=[]

with open("training_records_10days.txt","r") as f:
    data=f.readlines()

    for i in data:

        if i.split(",")[0]=="balut":
            balut.append(int(i.split(",")[1]))
        else:
            penoy.append(int(i.split(",")[1]))

balut.sort()
penoy.sort()

print(balut)
print(penoy)

print("10 DAYS")

print("Balut Range")
print(min(balut))
print(max(balut))

print("Penoy Range")
print(min(penoy))
print(max(penoy))

data=[]
balut=[]
penoy=[]
abnoy=[]

with open("training_records_14days.txt","r") as f:
    data=f.readlines()

    for i in data:

        if i.split(",")[0]=="balut":
            balut.append(int(i.split(",")[1]))
        elif i.split(",")[0]=="penoy":
            penoy.append(int(i.split(",")[1]))
        elif i.split(",")[0]=="abnoy":
            abnoy.append(int(i.split(",")[1]))

balut.sort()
penoy.sort()

print(balut)
print(penoy)

print("14 DAYS")

print("Balut Range")
print(min(balut))
print(max(balut))

print("Penoy Range")
try:    
    print(min(penoy))
    print(max(penoy))
except:
    pass

print("Abnoy Range")
print(min(abnoy))
print(max(abnoy))
    
