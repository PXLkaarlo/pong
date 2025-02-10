import pygame, random, zmq, threading
from queue import Queue
from operator import attrgetter

# server setup
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.setsockopt(zmq.CONNECT_TIMEOUT, 5000)
socket.setsockopt(zmq.LINGER, 0)
socket.setsockopt(zmq.RCVTIMEO, 1000)

def server_connect():
    socket.connect("tcp://127.0.0.1:696969")
    socket.send_string("get")
    try:
        leaderboard_queue.put(socket.recv())
    except:
        leaderboard_queue.put("None 0 None 0 None 0 None 0 None 0")
    
leaderboard_queue = Queue()
networking_thread = threading.Thread(target=server_connect)

networking_thread.start()


# saving setup
def ask(window, question) :
    "ask(window, question) -> answer"
    pygame.font.init()
    current_name = []
    screen(window, question + ": " + str.join(current_name, ""))
    
    while 1 :
        name_letter = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE] :
            current_name = current_name[0:-1]
        
        elif keys[pygame.K_RETURN] :
            break

        elif keys[pygame.K_MINUS] :
            current_name.append("_")
        
        elif name_letter < 127 :
            current_name.append(chr(name_letter))

        screen(window, question + ": " + str.join(current_name, ""))
    return str.join(current_name,"")


# leaderboard setup
class player :
    def __init__(self, name, score):
        self.name = name
        self.score = score

splitter = leaderboard_queue.get().split()

playerlist = []

for index in range(10) :
    if index % 2 == 0:
        playerlist.append(player(splitter[index], splitter[index+1]))


for player in playerlist :
    print(player.name)
    print(player.score)


#playerlist.sort(key=attrgetter('score'), reverse=True)


# major game setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("PYPONG")
clock = pygame.time.Clock()
running = True
game_active = False
leaderboard_menu = False
saving = False
game_font = pygame.font.Font("minecraftRegularBmg3.otf", 150)
tutorial_font = pygame.font.Font("minecraftRegularBmg3.otf", 30)
score_p1 = 0
score_p2 = 0
score_p1_pos = screen.get_width() * 11/15
hyphen = pygame.Surface((100,10))
hyphen.fill ("white")
title_surf = game_font.render("PYPONG", False, "white")
tutorial_1 = tutorial_font.render("Player 1 : arrows UP & DOWN", False, "cyan")
tutorial_2 = tutorial_font.render("Player 2 : W & S", False, "orange")
tutorial_3 = tutorial_font.render("SPACE = start", False, "white")
leaderboard_title = game_font.render("LEADERBOARD", False, "white")


# player positioning
player1_pos = pygame.Vector2(screen.get_width() * 14/15, (screen.get_height() / 2) -80)
player2_pos = pygame.Vector2(screen.get_width() * 1/15, (screen.get_height() / 2) -80)


# ball setup
ball_origin = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_pos = pygame.Vector2(ball_origin.x, ball_origin.y)
ball_org_speed = 2
ball_vert_speed = 1
ball_horz_speed = 1
max_vert_speed = 16
max_horz_speed = 12


# randomiser for starting direction
starting_direction = random.choice([1, 2, 3, 4])
if starting_direction == 1 : 
    ball_up = True
    ball_left = True
elif starting_direction == 2 :
    ball_up = True
    ball_left = False
elif starting_direction == 3 :
    ball_up = False
    ball_left = True
else :
    ball_up = False
    ball_left = False


while running:
    # poll for events
    keys = pygame.key.get_pressed()
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("dimgrey")
    screen.blit(title_surf, (375,260))
    screen.blit(tutorial_1, (700,450))
    screen.blit(tutorial_2, (250,450))
    screen.blit(tutorial_3, (550,550))
    screen.blit(tutorial_font.render("L = leaderboard", False, "crimson"), (525,600))
    screen.blit(tutorial_font.render("J = Save score to leaderboard", False, "green"), (425,650))

    score_p1_surf = game_font.render(f"{score_p1}", False, "cyan")
    score_p2_surf = game_font.render(f"{score_p2}", False, "orange")

    score_p1_rect = score_p1_surf.get_rect(topright = (score_p1_pos, 100))

    screen.blit(score_p1_surf, score_p1_rect)
    screen.blit(score_p2_surf, (screen.get_width() * 4/15 ,100))


    if game_active == False :
        ball_pos.x = ball_origin.x
        ball_pos.y = ball_origin.y
    
    if game_active == False and ball_vert_speed >= 2 : 
        ball_vert_speed = ball_org_speed
    if game_active == False and ball_horz_speed >= 2 :
        ball_horz_speed = ball_org_speed


    if keys[pygame.K_SPACE] :
        game_active = True
    
    if keys[pygame.K_l] and game_active == False :
        leaderboard_menu = True
    
    if keys[pygame.K_j] and game_active == False :
        saving = True

    if game_active :
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(score_p1_surf, score_p1_rect)
        # screen.blit(hyphen, ((screen.get_width() /2) -50, 175))
        screen.blit(score_p2_surf, (screen.get_width() * 4/15, 100))


        # ball object
        ball = pygame.Surface((16,16))
        ball.fill("white")
        screen.blit(ball, (ball_pos.x -8, ball_pos.y -8))
        

        if ball_up :
            ball_pos.y -= 200 * ball_vert_speed * dt
        else :
            ball_pos.y += 200 * ball_vert_speed * dt
        
        if ball_pos.y < 8 :
            ball_up = False
            if ball_vert_speed <= max_vert_speed :
                ball_vert_speed += 0.1

        if ball_pos.y > screen.get_height() -8 :
            ball_up = True
            if ball_vert_speed <= max_vert_speed :
                ball_vert_speed += 0.1
        
        if ball_left :
            ball_pos.x -= 200 * ball_horz_speed * dt
        else :
            ball_pos.x += 200 * ball_horz_speed * dt
        
        if ball_pos.x < -8 :
            ball_left = False
            game_active = False
            score_p1 += 1

        if ball_pos.x > screen.get_width() +8 :
            ball_left = True
            game_active = False
            score_p2 += 1



        # player1
        player1 = pygame.Surface((10,160))
        player1.fill("cyan")
        screen.blit(player1, (player1_pos.x, player1_pos.y))

        if keys[pygame.K_UP] and player1_pos.y >0 :
            player1_pos.y -= 500 * (ball_vert_speed * 2/4) * dt
        if keys[pygame.K_DOWN] and player1_pos.y < 560 :
            player1_pos.y += 500 * (ball_vert_speed * 2/4) * dt


        # setting up top and bottom collision boxes for player1
        ball_p1_top_collision = ball_pos.x > player1_pos.x -10 and ball_pos.x < player1_pos.x +18 and ball_pos.y > player1_pos.y and ball_pos.y < player1_pos.y +80
        ball_p1_bottom_collision = ball_pos.x > player1_pos.x -10 and ball_pos.x < player1_pos.x +18 and ball_pos.y > player1_pos.y +80 and ball_pos.y < player1_pos.y +160

        if ball_p1_top_collision and ball_left == False :
            ball_left = True
            ball_up = True
            if ball_horz_speed <= max_horz_speed :
                ball_horz_speed += 0.2
        elif ball_p1_bottom_collision and ball_left == False :
            ball_left = True
            ball_up = False
            if ball_horz_speed <= max_horz_speed :
                ball_horz_speed += 0.2

        
        # player2
        player2 = pygame.Surface((10,160))
        player2.fill("orange")
        screen.blit(player2, (player2_pos.x -10, player2_pos.y))
        
        if keys[pygame.K_w] and player2_pos.y > 0 :
            player2_pos.y -= 500 * (ball_vert_speed * 2/4) * dt
        if keys[pygame.K_s] and player2_pos.y < 560 :
            player2_pos.y += 500 * (ball_vert_speed * 2/4) * dt
        

        # ball collision with player2
        ball_p2_top_collision = ball_pos.x > player2_pos.x -18 and ball_pos.x < player2_pos.x +10 and ball_pos.y > player2_pos.y and ball_pos.y < player2_pos.y +80
        ball_p2_bottom_collision = ball_pos.x > player2_pos.x -18 and ball_pos.x < player2_pos.x +10 and ball_pos.y > player2_pos.y +80 and ball_pos.y < player2_pos.y +160

        if ball_p2_top_collision and ball_left :
            ball_left = False
            ball_up = True
            if ball_horz_speed <= max_horz_speed :
                ball_horz_speed += 0.2
        elif ball_p2_bottom_collision and ball_left :
            ball_left = False
            ball_up = False
            if ball_horz_speed <= max_horz_speed :
                ball_horz_speed += 0.2
        
        # end of gameloop


    if leaderboard_menu :
        screen.fill("brown")
        screen.blit(leaderboard_title, (150 ,100))
        screen.blit(tutorial_font.render("K = Main Menu", False, "white"), (screen.get_width() * 9/20, 600))

        screen.blit(tutorial_font.render("#1", False, "white"), (screen.get_width() * 4/15, 300))
        screen.blit(tutorial_font.render("#2", False, "white"), (screen.get_width() * 4/15, 350))
        screen.blit(tutorial_font.render("#3", False, "white"), (screen.get_width() * 4/15, 400))
        screen.blit(tutorial_font.render("#4", False, "white"), (screen.get_width() * 4/15, 450))
        screen.blit(tutorial_font.render("#5", False, "white"), (screen.get_width() * 4/15, 500))

        
        screen.blit(tutorial_font.render(f"{playerlist[0].name}", False, "white"), (screen.get_width() * 5/15, 300))
        screen.blit(tutorial_font.render(f"{playerlist[1].name}", False, "white"), (screen.get_width() * 5/15, 350))
        screen.blit(tutorial_font.render(f"{playerlist[2].name}", False, "white"), (screen.get_width() * 5/15, 400))
        screen.blit(tutorial_font.render(f"{playerlist[3].name}", False, "white"), (screen.get_width() * 5/15, 450))
        screen.blit(tutorial_font.render(f"{playerlist[4].name}", False, "white"), (screen.get_width() * 5/15, 500))


        screen.blit(tutorial_font.render(f"{playerlist[0].score}", False, "white"), (screen.get_width() * 11/15, 300))
        screen.blit(tutorial_font.render(f"{playerlist[1].score}", False, "white"), (screen.get_width() * 11/15, 350))
        screen.blit(tutorial_font.render(f"{playerlist[2].score}", False, "white"), (screen.get_width() * 11/15, 400))
        screen.blit(tutorial_font.render(f"{playerlist[3].score}", False, "white"), (screen.get_width() * 11/15, 450))
        screen.blit(tutorial_font.render(f"{playerlist[4].score}", False, "white"), (screen.get_width() * 11/15, 500))
        


        if keys[pygame.K_k] : 
            leaderboard_menu = False
    

    if saving :
        screen.fill("darkgreen")
        screen.blit(tutorial_font.render("K = Main Menu", False, "white"), (screen.get_width() * 9/20, 600))

        ask()

        if keys[pygame.K_k] : 
            saving = False


    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
networking_thread.join()
context.destroy()