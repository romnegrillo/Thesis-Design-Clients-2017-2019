data=[]
balut=[]
penoy=[]

with open("training_records.txt","r") as f:
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

print(min(balut))
print(max(balut))

print(min(penoy))
print(max(penoy))
    
