#심화프로그래밍 기말과제, 권민서, 20244360
import pygame
import random

pygame.init()

screen_width = 1000
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))


BLACK = (0, 0, 0)
pygame.display.set_caption("Avoid OGJI")

clock = pygame.time.Clock()

background_image = pygame.image.load("bg.png").convert() 
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

white = (255, 255, 255)
black = (0, 0, 0)

character = pygame.image.load("bbang.png")
character = pygame.transform.scale(character, (80, 100))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = 400
character_y_pos = 327

character_speed = 10

ball_image = pygame.image.load("og.png") 
ball_image = pygame.transform.scale(ball_image, (50, 50)) 
ball_size = ball_image.get_rect().size
ball_width = ball_size[0]
ball_height = ball_size[1]
ball_speed = 10

balls = []

score = 0
font = pygame.font.Font(None, 36)

pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.play(-1) 

hit_sound = pygame.mixer.Sound("GameOver.mp3")

def game_over():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(hit_sound)
    show_game_over_screen()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return False
                if event.key == pygame.K_RIGHT:
                    reset_game()
                    return True

def reset_game():
    global character_x_pos, character_y_pos, balls, score
    character_x_pos = 400
    character_y_pos = 327
    balls = []
    score = 0
    pygame.mixer.music.play(-1)  

def show_game_over_screen():
    screen.fill(white)
    game_over_font = pygame.font.Font(None, 74)
    game_over_text = game_over_font.render("Game Over", True, black)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, screen_height / 2 - game_over_text.get_height() / 2))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, screen_height / 2 + game_over_text.get_height() / 2))
    quit_text = font.render("PRESS LEFT KEY - GAME QUIT!", True, black)
    screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, screen_height / 2 - (quit_text.get_height()+200) / 2))
    start_text = font.render("PRESS RIGHT KEY - RESTART!", True, black)
    screen.blit(start_text, (screen_width / 2 - start_text.get_width() / 2, screen_height / 2 - (start_text.get_height()+250) / 2))
    
    pygame.display.update()
   

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character_x_pos -= character_speed
    if keys[pygame.K_RIGHT]:
        character_x_pos += character_speed

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if random.randint(1, 20) == 1:
        ball_x_pos = random.randint(0, screen_width - ball_width)
        ball_y_pos = 0
        balls.append([ball_x_pos, ball_y_pos])

    balls = [[x, y + ball_speed] for x, y in balls]

    for ball_x_pos, ball_y_pos in balls:
        if character_y_pos < ball_y_pos + ball_height and character_y_pos + character_height > ball_y_pos and character_x_pos < ball_x_pos + ball_width and character_x_pos + character_width > ball_x_pos:
            running = game_over()

    balls = [[x, y] for x, y in balls if y < screen_height]

    score += 1

    screen.blit(background_image, (0, 0))

    screen.blit(character, (character_x_pos, character_y_pos))

    for ball_x_pos, ball_y_pos in balls:
        screen.blit(ball_image, (ball_x_pos, ball_y_pos))

    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(30)


pygame.quit()


