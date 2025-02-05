from operator import attrgetter


mylist = []
#for i in range(5):
#    mylist.append(int(input())
#mylist.sort(reverse=True)
#print(mylist)
#print(mylist[2])

class item :
    def __init__(self, xp, lv):
        self.xp = xp
        self.lv = lv

apple = item(20, 1)
orange = item(50, 2)

#print("Apples give you", apple.xp, "xp.")
#print("But oranges get you to level", orange.lv)


class status :
    def __init__(self, name, score):
        self.name = name
        self.score = score

boardplayer1 = status("Kaarlo", 23)
boardplayer2 = status("Nallis21", 17)
boardplayer3 = status("A_Swedish_Gamer", 32)
boardplayer4 = status("sweatlord", 100)
boardplayer5 = status("dounce", 8)

playerlist = [boardplayer1, boardplayer2, boardplayer3, boardplayer4, boardplayer5]

#print(playerlist)

playerlist.sort(key=attrgetter('score'), reverse=True) 