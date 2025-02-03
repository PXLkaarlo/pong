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

class item :
    def __init__(self, xp, lv):
        self.xp = xp
        self.lv = lv

apple = item(20, 1)
orange = item(50, 2)

print("Apples give you", apple.xp, "xp.")
print("But oranges get you to level", orange.lv)