import pygame, sys, os, random

# Setting window size
WIN_WIDTH = 500
WIN_HEIGHT = 800

# Placing the floor
def draw_floor():
    screen.blit(BASE_IMGS, (floor_x_pos,700))
    screen.blit(BASE_IMGS, (floor_x_pos + 672,700))

# Creating pipes
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = PIPE_IMGS.get_rect(midtop= (600,random_pipe_pos))
    top_pipe = PIPE_IMGS.get_rect(midbottom= (600,random_pipe_pos - 200))
    return bottom_pipe,top_pipe

# Moving pipes
def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= pipe_speed
    return pipes

# Making pipes
def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 800:
            screen.blit(PIPE_IMGS,pipe)
        else:
            flip_pipe = pygame.transform.flip(PIPE_IMGS,False,True)
            screen.blit(flip_pipe,pipe)

# Giving the pipes and ground collition
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    
    if bird_rect.top <= -100 or bird_rect.bottom >= 730:
        return False
    
    return True

# Rotates bird
def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_movement * -3.5, 1)
    return new_bird

# Fixing the hitbox of the bird for the animation
def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

# Adding the score and high score
def score_display(game_state):
    if game_state == 'game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #0's for black / 255's for white
        score_rect = score_surface.get_rect(center = (250, 70))
        screen.blit(score_surface,score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(str(int(score)),True,(255,255,255)) #0's for black / 255's for white
        score_rect = score_surface.get_rect(center = (250, 70))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(str(int(high_score)),True,(255,255,255)) #0's for black / 255's for white
        high_score_rect = high_score_surface.get_rect(center = (250, 140))
        screen.blit(high_score_surface,high_score_rect)

# Tells player how to start playing
def start_text():
    if game_active == False:
        game_start_text = start_font.render('Press space to play',True,(255,255,255)) #0's for black / 255's for white
        game_start_text_rect = game_start_text.get_rect(center = (250, 400))
        screen.blit(game_start_text,game_start_text_rect)

# Setting up the window
pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Flappybird by Olav')
game_font = pygame.font.Font('PKMN RBYGSC.ttf', 40)
start_font = pygame.font.Font('PKMN RBYGSC.ttf', 30)

# Variables
gravity = 0.25
bird_movement = 0
floor_speed = 1.5
pipe_speed = 2
game_active = False
score = 0
high_score = 0

# Importing images / Adding hitboxes / Making the list of pipes
BG_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

BASE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
floor_x_pos = 0

PIPE_IMGS = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,2400)
pipe_height = [400,600,650]

bird_upflap = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png")))
bird_midflap = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
bird_downflap = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP,200)

bird_index = 1
bird_frames = [bird_upflap, bird_midflap, bird_downflap]
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100,400))

# Running the game
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Making flapping possible
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_active:
                bird_movement = 0
                bird_movement -= 6
            
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = 100,400
                bird_movement = 0
                score = 0

        # Making the pipe list
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        
        # Animates the bird
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
        
        bird_surface,bird_rect = bird_animation()
    
    # Adding everyting to the game
    screen.blit(BG_IMGS, (0,0))

    # Stoping the bird from falling and creating more pipes if you have lost the game
    if game_active:

         # Bird settings
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_frames[bird_index])
        bird_rect.centery += bird_movement
        if bird_movement >= 14:
            bird_movement = 14
        screen.blit(rotated_bird,bird_rect)
        game_active = check_collision(pipe_list)

        # Adding the pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.004
        score_display('game')

        if score > high_score:
            high_score = score
    else:
        score_display('game_over')

    if game_active == False:
        start_text()
    
    # Making the floor move
    floor_x_pos -= floor_speed
    draw_floor()
    if floor_x_pos <= -672:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)


# Sources
#  Python Flappy Bird AI Tutorial (with NEAT)
# https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2

#  Learning pygame by making Flappy Bird
# https://www.youtube.com/watch?v=UZg49z76cLw&t=1184s

#  The font
# https://www.dafont.com/fr/pkmn-rbygsc.font?text=Pokemon+GB

#  The images
# https://bit.ly/3nLJUwD



# Made by Olav