mylist = []
for i in range(5):
    mylist.append(int(input()))
mylist.sort(reverse=True)
print(mylist)
print(mylist[2])

necrotics = 3
parasitics = "headcrab"

hazard = (necrotics,parasitics)

otherlist = [(1,"omega"), (2,"lambda"), (5,"hazard"), (4,"contanment")]
otherlist.append(hazard)
otherlist.sort()
print(otherlist)
