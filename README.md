# To do list for Pong

2 player

What I need to do{
    create a game window

    5 objects{
        player1
        player2
        ball
        player1 score
        player2 score
    }
    make player1 move using w & s
    make player2 move using arrowUp & arrowDown
    ball starts moving in a random direction
    ball speeds up after each bounce

    collision for ball to top wall
    collision for ball to bottom wall

    collision for ball and player1
    collision for ball and player2

    make a goal system for player1
    make a goal system for player2
}

cut content {
    funny = pygame.image.load("kekw-emote.jpg")
    screen.blit(funny, ((screen.get_width() /2) - 100, (screen.get_height() /2) - 100))
    
    man = pygame.image.load("the-mystery.man.jpg")
    screen.blit(funny, (1,1))
}

Credits {
    Help in setting up program : David
    
    Feedback : David
}