import pygame, sys
from pygame import mixer
from fighter import Fighter
from button import Button

mixer.init()
pygame.init()

SCREEN_WIDTH = 1500  #dimensions of window
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  #displays window
pygame.display.set_caption('SCRAP IT OUT')  #names window 

#menu backround
BG = pygame.image.load("assets/photo.jpg").convert_alpha()
SCALED_BACK1 = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))

#font for menu
def get_font(size):
    return pygame.font.Font("assets/GAME_glm.ttf", size)

def play(): #when play button is clicked
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        #set framerate
        clock = pygame.time.Clock()
        FPS = 60

        #define colours
        RED = (255, 0, 0)
        YELLOW = (255, 255, 0)
        WHITE = (255, 255, 255)

        #define game variables
        intro_count = 3
        last_count_update = pygame.time.get_ticks()
        score = [0, 0] #player scores, [P1, P2] 
        round_over = False 
        ROUND_OVER_COOLDOWN = 2000

        #define fighter variables
        HERO_SIZE = 162
        HERO_SCALE = 4
        HERO_OFFSET = [72, 56]
        HERO_DATA = [HERO_SIZE, HERO_SCALE, HERO_OFFSET]
        WIZARD_SIZE = 250
        WIZARD_SCALE = 3
        WIZARD_OFFSET = [112, 107]
        WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

        #load music and sounds 
        pygame.mixer.music.load('assets/music2.mp3')
        pygame.mixer.music.set_volume(0.10)
        pygame.mixer.music.play(-1, 0.0, 5000)

        sword_fx = pygame.mixer.Sound('assets/sword.wav')
        sword_fx.set_volume(0.1)

        magic_fx = pygame.mixer.Sound('assets/magic.wav') 
        magic_fx.set_volume(0.2)

        #load backround image 
        BACK_IMAGE = pygame.image.load('assets/background.gif').convert_alpha()

        #load spritesheets
        hero_sheet = pygame.image.load('assets/hero/Sprites/Sprite.png').convert_alpha()
        wizard_sheet = pygame.image.load('assets/wizard/Sprite.png').convert_alpha()

        #define # of steps in each animations
        HERO_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

        #define font
        count_font = pygame.font.Font('assets/FunGames.ttf', 120)
        score_font = pygame.font.Font('assets/FunGames.ttf', 30)
        end_font = pygame.font.Font('assets/FunGames.ttf', 150)

        #fuction for drawing text
        def draw_text(text, font, text_col, x, y):
            img = font.render(text, True, text_col)
            SCREEN.blit(img, (x, y))

        #drawing background
        def draw_back():
            SCALED_BACK = pygame.transform.scale(BACK_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT))
            SCREEN.blit(SCALED_BACK, (0, 0))

        #drawing health bars
        def draw_health_bar(health, x, y):
            ratio = health / 100
            pygame.draw.rect(SCREEN, WHITE, (x - 2, y - 2, 404, 34))
            pygame.draw.rect(SCREEN, RED, (x, y, 400, 30))
            pygame.draw.rect(SCREEN, YELLOW, (x, y, 400 * ratio, 30))


        #create two instances of fighters
        fighter1 = Fighter(1, 300, 410, False, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx)
        fighter2 = Fighter(2, 1100, 410, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  

        #game loop     
        run = True
        while run: 
            clock.tick(FPS)   

            #draw background
            draw_back()

            #show player stats
            draw_health_bar(fighter1.health, 40, 30)
            draw_health_bar(fighter2.health, 1060, 30)
            draw_text("P1: " + str(score[0]), score_font, WHITE, 40, 80)
            draw_text("P2: " + str(score[1]), score_font, WHITE, 1060, 80)

            #update countdown
            if intro_count <= 0:
                #move fighters
                fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter2, round_over)
                fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter1, round_over)
            else: 
                #display timer
                draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                #update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()
            
            #update fighters
            fighter1.update()
            fighter2.update()

            #draw fighters
            fighter1.draw(SCREEN)
            fighter2.draw(SCREEN)

            #check for player defeat
            if round_over == False:
                if fighter1.alive == False:
                    score[1] += 1 
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif fighter2.alive == False:
                    score[0] += 1 
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                draw_text('VICTORY', end_font, RED, SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 3)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    fighter1 = Fighter(1, 300, 410, False, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx)
                    fighter2 = Fighter(2, 1100, 410, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False

            #update display
            pygame.display.update()

        #exit pygame
        pygame.quit()#game loop     
        run = True
        while run: 
            clock.tick(FPS)   

            #draw background
            draw_back()

            #show player stats
            draw_health_bar(fighter1.health, 40, 30)
            draw_health_bar(fighter2.health, 1060, 30)
            draw_text("P1: " + str(score[0]), score_font, WHITE, 40, 80)
            draw_text("P2: " + str(score[1]), score_font, WHITE, 1060, 80)

            #update countdown
            if intro_count <= 0:
                #move fighters
                fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter2, round_over)
                fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN, fighter1, round_over)
            else: 
                #display timer
                draw_text(str(intro_count), count_font, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
                #update count timer
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()
            
            #update fighters
            fighter1.update()
            fighter2.update()

            #draw fighters
            fighter1.draw(SCREEN)
            fighter2.draw(SCREEN)

            #check for player defeat
            if round_over == False:
                if fighter1.alive == False:
                    score[1] += 1 
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif fighter2.alive == False:
                    score[0] += 1 
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else:
                draw_text('VICTORY', end_font, RED, SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT / 3)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    fighter1 = Fighter(1, 300, 410, False, HERO_DATA, hero_sheet, HERO_ANIMATION_STEPS, sword_fx)
                    fighter2 = Fighter(2, 1100, 410, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)  

            #event handler
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    run = False

            #update display
            pygame.display.update()

        #exit pygame
        pygame.quit()

    
def options(): #when options button is clicked
    RED = (255, 0, 0)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = get_font(30).render("P1: W = JUMP, A = LEFT, D = RIGHT, R = ATTACK 1, T = ATTACK 2", True, RED)
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(750, 50))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_TEXT2 = get_font(30).render("P2: UP = JUMP, LEFT = LEFT, RIGHT = RIGHT, NUM1 = ATTACK 1, NUM2 = ATTACK 2", True, RED)
        OPTIONS_RECT2 = OPTIONS_TEXT.get_rect(center=(600, 250))
        SCREEN.blit(OPTIONS_TEXT2, OPTIONS_RECT2)

        OPTIONS_BACK = Button(image=None, pos=(SCREEN_WIDTH / 2, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color= RED)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu(): #menu design
    while True:
        RED = (255, 0, 0)
        WHITE = (255, 255, 255)

        #draws backround
        SCREEN.blit(SCALED_BACK1, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, RED)
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH / 2, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(SCREEN_WIDTH / 2, 250), 
                            text_input="PLAY", font=get_font(75), base_color= WHITE, hovering_color= RED)
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(SCREEN_WIDTH / 2, 400), 
                            text_input="CONTROLS", font=get_font(75), base_color= WHITE, hovering_color= RED)
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(SCREEN_WIDTH / 2, 550), 
                            text_input="QUIT", font=get_font(75), base_color= WHITE, hovering_color= RED)

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()































































































