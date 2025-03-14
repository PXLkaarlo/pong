import pygame, random, zmq, threading, pygame_textinput
from queue import Queue

# server connection
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
        leaderboard_queue.put(b'Could 0 Not 0 Connect 0 To 0 Server 0')
    
leaderboard_queue = Queue()
networking_thread = threading.Thread(target=server_connect)

networking_thread.start()


# saving setup
textinput_font = pygame.font.Font("minecraftRegularBmg3.otf", 50)
manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 10)
textinput_custom = pygame_textinput.TextInputVisualizer(manager=manager, font_object=textinput_font)

textinput = pygame_textinput.TextInputVisualizer()

def score_calc(p1, p2) :
    if p1 > p2 :
        return p1
    else :
        return p2


# leaderboard setup
class player :
    def __init__(self, name, score):
        self.name = name
        self.score = score

splitter = leaderboard_queue.get().split()

playerlist = []

for index in range(10) :
    if index % 2 == 0:
        playerlist.append(player(splitter[index].decode(), splitter[index+1].decode()))


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
    events = pygame.event.get()
    # pygame.QUIT event means the user clicked X to close your window
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("dimgrey")
    screen.blit(title_surf, (375,260))
    screen.blit(tutorial_1, (700,450))
    screen.blit(tutorial_2, (250,450))
    screen.blit(tutorial_3, (550,550))
    screen.blit(tutorial_font.render("L = leaderboard", False, "crimson"), (525,600))
    screen.blit(tutorial_font.render("K = Save score to leaderboard", False, "green"), (425,650))

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

    if keys[pygame.K_SPACE] and saving == False and leaderboard_menu == False :
        game_active = True
    
    if keys[pygame.K_l] and game_active == False :
        leaderboard_menu = True
    
    if keys[pygame.K_k] and game_active == False :
        saving = True

    if game_active :
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        screen.blit(score_p1_surf, score_p1_rect)
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


    if leaderboard_menu :
        screen.fill("brown")
        screen.blit(leaderboard_title, (150 ,100))
        screen.blit(tutorial_font.render("ENTER = Main Menu", False, "white"), (screen.get_width() * 8/20, 600))

        for i in range(5):
            latitude = 300 + 50 * i
            screen.blit(tutorial_font.render(f"#{i + 1}", False, "white"), (screen.get_width() * 4/15, latitude))
            screen.blit(tutorial_font.render(f"{playerlist[i].name}", False, "white"), (screen.get_width() * 5/15, latitude))
            screen.blit(tutorial_font.render(f"{playerlist[i].score}", False, "white"), (screen.get_width() * 11/15, latitude))


        if keys[pygame.K_RETURN] : 
            leaderboard_menu = False
    


    if saving :
        screen.fill("darkgreen")
        screen.blit(tutorial_font.render("ENTER = Main Menu", False, "white"), (screen.get_width() * 8/20, 600))

        textinput.update(events)
        textinput_custom.update(events)

        screen.blit(textinput_custom.surface, (400,200))

        cantDoThat = not " " in textinput_custom.value

        if cantDoThat == False :
            screen.blit(tutorial_font.render("Can't use a space in your name.", False, "yellow"), (screen.get_width() * 8/20, 500))

        if keys[pygame.K_RETURN] and cantDoThat : 
            try:
                socket.send_string(textinput_custom.value + " " + str(score_calc(score_p1, score_p2)))
                socket.recv()
            except:
                print("Not connected to server")
            finally:
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