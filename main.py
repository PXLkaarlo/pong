# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Pong_prototype")
clock = pygame.time.Clock()
running = True
dt = 0

#player positioning
player1_pos = pygame.Vector2(screen.get_width() * 14/15, screen.get_height() / 2)
player2_pos = pygame.Vector2(screen.get_width() * 1/15, screen.get_height() / 2)

#ball setup
ball_origin = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
ball_pos = pygame.Vector2(ball_origin.x, ball_origin.y)
ball_up = True
ball_side = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")



    #Pong ball
    ball = pygame.Surface((16,16))
    ball.fill("white")
    screen.blit(ball, (ball_pos.x -8, ball_pos.y -8))
    
    if ball_up :
        ball_pos.y -= 2
    else :
        ball_pos.y += 2
    
    if ball_pos.y < 8 :
        ball_up = False
    if ball_pos.y > screen.get_height() -8 :
        ball_up = True
    
    if ball_side :
        ball_pos.x -= 2
    else :
        ball_pos.x += 2



    #player1
    player1 = pygame.Surface((10,160))
    player1.fill("cyan")
    screen.blit(player1, (player1_pos.x, player1_pos.y - 80))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player1_pos.y -= 500 * dt
    if keys[pygame.K_DOWN]:
        player1_pos.y += 500 * dt


    
    #player2
    player2 = pygame.Surface((10,160))
    player2.fill("orange")
    screen.blit(player2, (player2_pos.x, player2_pos.y - 80))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player2_pos.y -= 500 * dt
    if keys[pygame.K_s]:
        player2_pos.y += 500 * dt

    


    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()