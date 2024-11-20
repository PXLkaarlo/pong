# Example file showing a basic pygame "game loop"
import pygame

# random number genorator setup
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong_prototype")
clock = pygame.time.Clock()
running = True
dt = 0

# player positioning
player1_pos = pygame.Vector2(screen.get_width() * 14/15, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() * 1/15, screen.get_height() / 2)

# ball setup
ball_origin = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_pos = pygame.Vector2(ball_origin.x, ball_origin.y)
ball_speed = 1

# Randomiser for starting direction
starting_direction = random.choice([1, 2, 3, 4])
if starting_direction == 1 : 
    ball_up = True
    ball_side = True
elif starting_direction == 2 :
    ball_up = True
    ball_side = False
elif starting_direction == 3 :
    ball_up = False
    ball_side = True
elif starting_direction == 4 :
    ball_up = False
    ball_side = False


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")



    # ball object
    ball = pygame.Surface((16,16))
    ball.fill("white")
    screen.blit(ball, (ball_pos.x -8, ball_pos.y -8))
    

    if ball_up :
        ball_pos.y -= 2 * ball_speed
    else :
        ball_pos.y += 2 * ball_speed
    
    if ball_pos.y < 8 :
        ball_up = False
        ball_speed += 0.2

    if ball_pos.y > screen.get_height() -8 :
        ball_up = True
        ball_speed += 0.2
    
    if ball_side :
        ball_pos.x -= 2 * ball_speed
    else :
        ball_pos.x += 2 * ball_speed
    
    if ball_pos.x < -8 :
        ball_side = False

    if ball_pos.x > screen.get_width() +8 :
        ball_side = True



    # player1
    player1 = pygame.Surface((10,160))
    player1.fill("cyan")
    screen.blit(player1, (player1_pos.x, player1_pos.y))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player1_pos.y >0:
        player1_pos.y -= 500 * dt
    if keys[pygame.K_DOWN] and player1_pos.y < 560 :
        player1_pos.y += 500 * dt
    

    # ball collision with player1
    ball_p1_collide = ball_pos.x > player1_pos.x -10 and ball_pos.x < player1_pos.x +18 and ball_pos.y > player1_pos.y and ball_pos.y < player1_pos.y +160
    
    if ball_p1_collide and keys[pygame.K_LEFT] :
        ball_side = True
        ball_up = True
    elif ball_p1_collide :
        ball_side = True
        ball_up = False

    
    # player2
    player2 = pygame.Surface((10,160))
    player2.fill("orange")
    screen.blit(player2, (player2_pos.x -10, player2_pos.y))
    
    if keys[pygame.K_w] and player2_pos.y > 0 :
        player2_pos.y -= 500 * dt
    if keys[pygame.K_s] and player2_pos.y < 560 :
        player2_pos.y += 500 * dt
    

    # ball collision with player2
    ball_p2_collide = ball_pos.x > player2_pos.x -18 and ball_pos.x < player2_pos.x +10 and ball_pos.y > player2_pos.y and ball_pos.y < player2_pos.y +160

    if ball_p2_collide and keys[pygame.K_d] :
        ball_side = False
        ball_up = True
    elif ball_p2_collide :
        ball_side = False
        ball_up = False

    


    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()