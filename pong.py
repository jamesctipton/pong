import pygame, sys, random, time

import warnings
warnings.filterwarnings("ignore")
#python3 -m PyInstaller pong.spec

pygame.init()

WINDOW_SIZE = (1000,750) #width, height
DEFAULT = (150,150,250)
BLACK = (0,0,0)
colors = {'red': (230, 110, 110), 'orange': (230, 170, 110), 'yellow': (230, 220, 110),
          'chartreuse': (180, 210, 130) ,'green': (140, 230, 110),'aqua': (90, 210, 200),
          'blue': (110, 160, 230), 'purple': (180, 110, 230), 'pink': (210, 130, 180),
          'white': (255, 255, 255), 'gray': (150, 150, 150), 'default': DEFAULT
          }

window = pygame.display.set_mode((WINDOW_SIZE[0], WINDOW_SIZE[1]), 0, 2)
pygame.display.set_caption("Pong")
pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

### GLOBALS
gear = pygame.image.load("gear.png")
gear_color = pygame.image.load("gear_color.png")
blip = pygame.mixer.Sound('blip.ogg')
button = pygame.mixer.Sound('button.ogg')


clock = pygame.time.Clock()

#defaults
defaults= [100,100,8,'normal',6,6,20,False,4,DEFAULT,False,5]
settings = {'paddle size': 100,
            'cpu size': 100,
            'ball speed': 8,
            'cpu difficulty': 'normal',
            'paddle speed': 6,
            'cpu speed': 6,
            'ball size': 20,
            'random respawn': False,
            'respawn speed': 4,
            'color': DEFAULT,
            'sound': False,
            'max score':5,
            }

bar1 = pygame.Rect(100,100,200,6)
bar2 = pygame.Rect(100,200,200,6)
bar3 = pygame.Rect(100,300,200,6)
bar4 = pygame.Rect(100,450,200,6)
bar5 = pygame.Rect(100,550,200,6)
bar6 = pygame.Rect(100,650,200,6)

impossible = pygame.Rect(100,350,40,40)

pos1 = (bar1.centerx, bar1.centery)
pos2 = (bar2.centerx, bar2.centery)
pos3 = (bar3.centerx, bar3.centery)
pos4 = (bar4.centerx, bar4.centery)
pos5 = (bar5.centerx, bar5.centery)
pos6 = (bar6.centerx, bar6.centery)
pos7 = (665, 165)
pos8 = (530, 265)
pos_color = (680, 445)
pos9 = (665, 515)
pos10 = (530, 615)
### END GLOBALS


def reset_ball(ball,direction=1):
    ball.centerx = WINDOW_SIZE[0]/2
    ball.centery = WINDOW_SIZE[1]/2
    ball_x_speed = settings['respawn speed']*direction
    ball_y_speed = 0
    return ball_x_speed, ball_y_speed

def end_game(winner, single_player, player_time):
    window.fill(BLACK)

    text_font = pygame.font.SysFont('ptmono',70,False)
    subtext_font = pygame.font.SysFont('arial',32,False)
    if settings['cpu difficulty'] == 'impossible' and single_player:
        text = f"LASTED {player_time}s!"
        end_text = text_font.render(text, False, settings['color'])
    else:
        if winner:
            text = "YOU WIN!"
            end_text = text_font.render(text, False, settings['color'])
            if not single_player:
                text = "PLAYER 1 WINS"
                end_text = text_font.render(text, False, settings['color'])
        else:
            text = "YOU LOSE!"
            end_text = text_font.render(text, False, settings['color'])
            if not single_player:
                text = "PLAYER 2 WINS"
                end_text = text_font.render(text, False, settings['color'])

    subtext = subtext_font.render("Press [ESC] to return to the menu", False, settings['color'])

    if single_player:
        window.blit(end_text, (WINDOW_SIZE[0]/2 - text_font.size(text)[0]/2,250))
    else:
        window.blit(end_text, (WINDOW_SIZE[0]/2 - text_font.size(text)[0]/2, 250))
        
    window.blit(subtext, (260, 325))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                menu()

def menu():
    #buttons
    single_player = pygame.Rect(0,0,250,80)
    single_player.centerx = WINDOW_SIZE[0]/2
    single_player.centery = WINDOW_SIZE[1]/3

    two_player = pygame.Rect(0,0,250,80)
    two_player.centerx = WINDOW_SIZE[0]/2
    two_player.centery = WINDOW_SIZE[1]/2

    _quit = pygame.Rect(0,0,150,60)
    _quit.centerx = WINDOW_SIZE[0]/2
    _quit.centery = WINDOW_SIZE[1]*2/3

    #highlight outlines
    sin_outline = pygame.Rect(0,0,250,80)
    sin_outline.centerx = WINDOW_SIZE[0]/2
    sin_outline.centery = WINDOW_SIZE[1]/3

    two_outline = pygame.Rect(0,0,250,80)
    two_outline.centerx = WINDOW_SIZE[0]/2
    two_outline.centery = WINDOW_SIZE[1]/2

    quit_outline = pygame.Rect(0,0,150,60)
    quit_outline.centerx = WINDOW_SIZE[0]/2
    quit_outline.centery = WINDOW_SIZE[1]*2/3

    text_font = pygame.font.SysFont('ptmono',30,True)
    title_font = pygame.font.SysFont('ptmono',140,True)
    tiny_font = pygame.font.SysFont('ptmono',16)
    
    while True:
        window.fill(BLACK)
        if not settings['sound']: button.set_volume(0)
        else: button.set_volume(0.5)

        title = title_font.render("PONG",False,settings['color'])
        window.blit(title, (WINDOW_SIZE[0]/2 - title_font.size("PONG")[0]/2,35))

        credit = tiny_font.render("By James Tipton",False,settings['color'])
        window.blit(credit, (427, 550))

        pygame.draw.rect(window,settings['color'],single_player,0,3)
        pygame.draw.rect(window,settings['color'],two_player,0,3)
        pygame.draw.rect(window,settings['color'],_quit,0,3)

        sin_text = text_font.render("SINGLE PLAYER", False, BLACK)
        two_text = text_font.render("TWO PLAYER", False, BLACK)
        quit_text = text_font.render("QUIT", False, BLACK)

        window.blit(sin_text, (385, 237))
        window.blit(two_text, (410, 360))
        window.blit(quit_text, (465, 485))

        sin_info1 = tiny_font.render("Use ▲ and ▼ arrow keys",False,settings['color'])
        sin_info2 = tiny_font.render(f"First to {settings['max score']} wins!",False,settings['color'])
        imp_info = tiny_font.render("Last as long as you can!",False,settings['color'])
        
        two_info1 = tiny_font.render("Player 1 uses ▲ and ▼ keys",False,settings['color'])
        two_info2 = tiny_font.render("Player 2 uses W and S keys",False,settings['color'])

        circ = pygame.draw.circle(window, settings['color'], (100,650), 32)
        window.blit(gear, (68,618))

        if single_player.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,BLACK,single_player,0,3)
            sin_text = text_font.render("SINGLE PLAYER", False, settings['color'])
            pygame.draw.rect(window,settings['color'],sin_outline,3,3)
            window.blit(sin_text, (385, 237))
            window.blit(sin_info1, (640, 235))
            if settings['cpu difficulty'] == 'impossible':
                window.blit(imp_info, (640, 255))
            else:
                window.blit(sin_info2, (640, 255))
            
        if two_player.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,BLACK,two_player,0,3)
            two_text = text_font.render("TWO PLAYER", False, settings['color'])
            pygame.draw.rect(window,settings['color'],two_outline,3,3)
            window.blit(two_text, (410, 360))
            window.blit(two_info1, (640, 350))
            window.blit(two_info2, (640, 370))
            window.blit(sin_info2, (640, 390))
            
        if _quit.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,BLACK,_quit,0,3)
            quit_text = text_font.render("QUIT", False, settings['color'])
            pygame.draw.rect(window,settings['color'],quit_outline,3,3)
            window.blit(quit_text, (465, 485))

        if circ.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(window,BLACK,(100,650), 32)
            pygame.draw.circle(window,settings['color'],(100,650), 32, 3)
            window.blit(gear_color, (68,618))
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if single_player.collidepoint(pygame.mouse.get_pos()):
                    button.play()
                    gameplay(True)
                if two_player.collidepoint(pygame.mouse.get_pos()):
                    button.play()
                    gameplay(False)
                if _quit.collidepoint(pygame.mouse.get_pos()):
                    button.play()
                    time.sleep(0.2)
                    pygame.quit()
                    sys.exit()
                if circ.collidepoint(pygame.mouse.get_pos()):
                    button.play()
                    settings_menu()
        
        pygame.display.update()

def settings_menu():

    title_font = pygame.font.SysFont('ptmono',70,True)
    text_font = pygame.font.SysFont('ptmono',26,True)
    name_font = pygame.font.SysFont('ptmono',18,False)
    info_font = pygame.font.SysFont('ptmono',14,False)

    radius = 15

    back_font = pygame.font.SysFont('ptmono',20,True)
    back = pygame.Rect(800,650,80,40)
    back_outline = pygame.Rect(800,650,80,40)

    global pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos_color, pos9, pos10
    #   easiest way i could think of to get settings visual indicators to be persistent
    #   from game to game
    
    while True:
        window.fill(BLACK)
        if not settings['sound']: button.set_volume(0)
        else: button.set_volume(0.5)

        title = title_font.render("SETTINGS",False,settings['color'])
        window.blit(title, (500,20))


        back = pygame.draw.rect(window, settings['color'], back, 0, 3)
        back_text = back_font.render("«BACK", False, BLACK)
        window.blit(back_text, (808, 660))

        #----format----#
        # title of text
        # put text on screen
        # settings bar
        # circle left
        # circle middle
        # circle right
        # selection circle
        # informational text below settings bar
        # put info on screen

        pad_size_text = text_font.render("Paddle Size",False,settings['color'])
        window.blit(pad_size_text, (50,55))
        pad_size = pygame.draw.rect(window, settings['color'], bar1)
        p_sz1 = pygame.draw.circle(window, settings['color'], (bar1.x, bar1.centery), radius)
        p_sz2 = pygame.draw.circle(window, settings['color'], (bar1.centerx, bar1.centery), radius)
        p_sz3 = pygame.draw.circle(window, settings['color'], (bar1.right, bar1.centery), radius)
        sel1 = pygame.draw.circle(window, BLACK, pos1, 7)
        info1 = info_font.render("small       normal       large",False,settings['color'])
        window.blit(info1, (80,120))


        cpu_size_text = text_font.render("CPU Paddle Size",False,settings['color'])
        window.blit(cpu_size_text, (50,155))
        cpu_size = pygame.draw.rect(window, settings['color'], bar2)
        c_sz1 = pygame.draw.circle(window, settings['color'], (bar2.x, bar2.centery), radius)
        c_sz2 = pygame.draw.circle(window, settings['color'], (bar2.centerx, bar2.centery), radius)
        c_sz3 = pygame.draw.circle(window, settings['color'], (bar2.right, bar2.centery), radius)
        sel2 = pygame.draw.circle(window, BLACK, pos2, 7)
        info2 = info_font.render("small       normal       large",False,settings['color'])
        window.blit(info2, (80,220))


        cpu_diff_text = text_font.render("CPU Difficulty",False,settings['color'])
        window.blit(cpu_diff_text, (50,255))
        cpu_diff = pygame.draw.rect(window, settings['color'], bar3)
        c_df1 = pygame.draw.circle(window, settings['color'], (bar3.x, bar3.centery), radius)
        c_df2 = pygame.draw.circle(window, settings['color'], (bar3.centerx, bar3.centery), radius)
        c_df3 = pygame.draw.circle(window, settings['color'], (bar3.right, bar3.centery), radius)
        info3 = info_font.render("easy        medium        hard",False,settings['color'])
        window.blit(info3, (80,320))
        
        impossible = pygame.draw.circle(window, settings['color'], (bar3.x,370), radius)
        imp_text = name_font.render("impossible (time trials mode)",False,settings['color'])
        window.blit(imp_text, (120, 360))
        sel3 = pygame.draw.circle(window, BLACK, pos3, 7)


        pad_speed_text = text_font.render("Paddle Speed",False,settings['color'])
        window.blit(pad_speed_text, (50,405))
        pad_speed = pygame.draw.rect(window, settings['color'], bar4)
        p_sd1 = pygame.draw.circle(window, settings['color'], (bar4.x, bar4.centery), radius)
        p_sd2 = pygame.draw.circle(window, settings['color'], (bar4.centerx, bar4.centery), radius)
        p_sd3 = pygame.draw.circle(window, settings['color'], (bar4.right, bar4.centery), radius)
        sel4 = pygame.draw.circle(window, BLACK, pos4, 7)
        info6 = info_font.render("slow        normal        fast",False,settings['color'])
        window.blit(info6, (80,470))


        ball_speed_text = text_font.render("Ball Speed",False,settings['color'])
        window.blit(ball_speed_text, (50,505))
        ball_speed = pygame.draw.rect(window, settings['color'], bar5)
        b_sd1 = pygame.draw.circle(window, settings['color'], (bar5.x, bar5.centery), radius)
        b_sd2 = pygame.draw.circle(window, settings['color'], (bar5.centerx, bar5.centery), radius)
        b_sd3 = pygame.draw.circle(window, settings['color'], (bar5.right, bar5.centery), radius)
        sel5 = pygame.draw.circle(window, BLACK, pos5, 7)
        info5 = info_font.render("slow        normal        fast",False,settings['color'])
        window.blit(info5, (80,570))


        ball_size_text = text_font.render("Ball Size",False,settings['color'])
        window.blit(ball_size_text, (50,605))
        ball_size = pygame.draw.rect(window, settings['color'], bar6)
        b_sz1 = pygame.draw.circle(window, settings['color'], (bar6.x, bar6.centery), radius)
        b_sz2 = pygame.draw.circle(window, settings['color'], (bar6.centerx, bar6.centery), radius)
        b_sz3 = pygame.draw.circle(window, settings['color'], (bar6.right, bar6.centery), radius)
        sel6 = pygame.draw.circle(window, BLACK, pos6, 7)
        info1 = info_font.render("small       normal       large",False,settings['color'])
        window.blit(info1, (80,670))


        direction_text = text_font.render("Who Gets Serve",False,settings['color'])
        window.blit(direction_text, (475,115))
        dir1 = pygame.draw.circle(window, settings['color'], (530, 165), radius)
        random = name_font.render("random",False,settings['color'])
        window.blit(random, (555, 155))
        dir2 = pygame.draw.circle(window, settings['color'], (665, 165), radius)
        sel7 = pygame.draw.circle(window, BLACK, pos7, 7)
        lost_last = name_font.render("whoever lost last",False,settings['color'])
        window.blit(lost_last, (690, 155))


        serve_text = text_font.render("Serve Speed",False,settings['color'])
        window.blit(serve_text, (475,215))
        ser1 = pygame.draw.circle(window, settings['color'], (530, 265), radius)
        slow = name_font.render("slow",False,settings['color'])
        window.blit(slow, (555, 255))
        ser2 = pygame.draw.circle(window, settings['color'], (665, 265), radius)
        sel8 = pygame.draw.circle(window, BLACK, pos8, 7)
        normal = name_font.render("normal",False,settings['color'])
        window.blit(normal, (690, 255))


        theme_text = text_font.render("Theme",False,settings['color'])
        window.blit(theme_text, (475,315))
        red = pygame.draw.circle(window, colors['red'], (530, 365), radius)
        orn = pygame.draw.circle(window, colors['orange'], (580, 365), radius)
        yel = pygame.draw.circle(window, colors['yellow'], (630, 365), radius)
        cha = pygame.draw.circle(window, colors['chartreuse'], (680, 365), radius)
        gre = pygame.draw.circle(window, colors['green'], (530, 405), radius)
        aqu = pygame.draw.circle(window, colors['aqua'], (580, 405), radius)
        blu = pygame.draw.circle(window, colors['blue'], (630, 405), radius)
        pur = pygame.draw.circle(window, colors['purple'], (680, 405), radius)
        pin = pygame.draw.circle(window, colors['pink'], (530, 445), radius)
        whi = pygame.draw.circle(window, colors['white'], (580, 445), radius)
        gra = pygame.draw.circle(window, colors['gray'], (630, 445), radius)
        default = pygame.draw.circle(window, colors['default'], (680, 445), radius)
        color_sel = pygame.draw.circle(window, BLACK, pos_color, 7)


        sound_text = text_font.render("Sound",False,settings['color'])
        window.blit(sound_text, (475,465))
        sou1 = pygame.draw.circle(window, settings['color'], (530, 515), radius)
        on = name_font.render("on",False,settings['color'])
        window.blit(on, (555, 505))
        sou2 = pygame.draw.circle(window, settings['color'], (665, 515), radius)
        off = name_font.render("off",False,settings['color'])
        window.blit(off, (690, 505))
        sel9 = pygame.draw.circle(window, BLACK, pos9, 7)
        


        score_text = text_font.render("Max Score",False,settings['color'])
        window.blit(score_text, (475,565))
        max_score1 = pygame.draw.circle(window, settings['color'], (530, 615), radius)
        five = name_font.render("5",False,settings['color'])
        window.blit(five, (550, 605))
        max_score2 = pygame.draw.circle(window, settings['color'], (595, 615), radius)
        ten = name_font.render("10",False,settings['color'])
        window.blit(ten, (615, 605))
        max_score3 = pygame.draw.circle(window, settings['color'], (665, 615), radius)
        fifteen = name_font.render("15",False,settings['color'])
        window.blit(fifteen, (683, 605))
        sel10 = pygame.draw.circle(window, BLACK, pos10, 7)
        

        default_button = pygame.draw.circle(window, settings['color'], (530, 665), radius)
        default_text = name_font.render("Default Settings",False,settings['color'])
        window.blit(default_text, (555, 655))

        if back.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(window,BLACK,back,0,3)
            back_text = back_font.render("«BACK", False, settings['color'])
            pygame.draw.rect(window,settings['color'],back_outline,3,3)
            window.blit(back_text, (808, 660))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(pygame.mouse.get_pos()):
                    button.play()
                    menu()
                    
                if p_sz1.collidepoint(pygame.mouse.get_pos()):
                    pos1 = (bar1.x, bar1.centery)
                    settings['paddle size'] = 60
                if p_sz2.collidepoint(pygame.mouse.get_pos()):
                    pos1 = (bar1.centerx, bar1.centery)
                    settings['paddle size'] = 100
                if p_sz3.collidepoint(pygame.mouse.get_pos()):
                    pos1 = (bar1.right, bar1.centery)
                    settings['paddle size'] = 140
                    
                if c_sz1.collidepoint(pygame.mouse.get_pos()):
                    pos2 = (bar2.x, bar2.centery)
                    settings['cpu size'] = 60
                if c_sz2.collidepoint(pygame.mouse.get_pos()):
                    pos2 = (bar2.centerx, bar2.centery)
                    settings['cpu size'] = 100
                if c_sz3.collidepoint(pygame.mouse.get_pos()):
                    pos2 = (bar2.right, bar2.centery)
                    settings['cpu size'] = 140
                    
                if c_df1.collidepoint(pygame.mouse.get_pos()):
                    pos3 = (bar3.x, bar3.centery)
                    settings['cpu speed'] = 4
                    settings['cpu difficulty'] = 'easy'
                if c_df2.collidepoint(pygame.mouse.get_pos()):
                    pos3 = (bar3.centerx, bar3.centery)
                    settings['cpu speed'] = 6
                    settings['cpu difficulty'] = 'normal'
                if c_df3.collidepoint(pygame.mouse.get_pos()):
                    pos3 = (bar3.right, bar3.centery)
                    settings['cpu speed'] = 8
                    settings['cpu difficulty'] = 'hard'
                if impossible.collidepoint(pygame.mouse.get_pos()):
                    pos3 = (bar3.x,370)
                    settings['cpu difficulty'] = 'impossible'
                    
                if p_sd1.collidepoint(pygame.mouse.get_pos()):
                    pos4 = (bar4.x, bar4.centery)
                    settings['paddle speed'] = 4
                if p_sd2.collidepoint(pygame.mouse.get_pos()):
                    pos4 = (bar4.centerx, bar4.centery)
                    settings['paddle speed'] = 6
                if p_sd3.collidepoint(pygame.mouse.get_pos()):
                    pos4 = (bar4.right, bar4.centery)
                    settings['paddle speed'] = 10
                    
                if b_sd1.collidepoint(pygame.mouse.get_pos()):
                    pos5 = (bar5.x, bar5.centery)
                    settings['ball speed'] = 6
                if b_sd2.collidepoint(pygame.mouse.get_pos()):
                    pos5 = (bar5.centerx, bar5.centery)
                    settings['ball speed'] = 10
                if b_sd3.collidepoint(pygame.mouse.get_pos()):
                    pos5 = (bar5.right, bar5.centery)
                    settings['ball speed'] = 14
                    
                if b_sz1.collidepoint(pygame.mouse.get_pos()):
                    pos6 = (bar6.x, bar6.centery)
                    settings['ball size'] = 10
                if b_sz2.collidepoint(pygame.mouse.get_pos()):
                    pos6 = (bar6.centerx, bar6.centery)
                    settings['ball size'] = 20
                if b_sz3.collidepoint(pygame.mouse.get_pos()):
                    pos6 = (bar6.right, bar6.centery)
                    settings['ball size'] = 40
                    
                if dir1.collidepoint(pygame.mouse.get_pos()):
                    pos7 = (530, 165)
                    settings['random respawn'] = True
                if dir2.collidepoint(pygame.mouse.get_pos()):
                    pos7 = (665, 165)
                    settings['random respawn'] = False
                    
                if ser1.collidepoint(pygame.mouse.get_pos()):
                    pos8 = (530, 265)
                    settings['respawn speed'] = 4
                if ser2.collidepoint(pygame.mouse.get_pos()):
                    pos8 = (665, 265)
                    settings['respawn speed'] = settings['ball speed']
                    
                if red.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (530, 365)
                    settings['color'] = colors['red']
                if orn.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (580, 365)
                    settings['color'] = colors['orange']
                if yel.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (630, 365)
                    settings['color'] = colors['yellow']
                if cha.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (680, 365)
                    settings['color'] = colors['chartreuse']
                if gre.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (530, 405)
                    settings['color'] = colors['green']
                if aqu.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (580, 405)
                    settings['color'] = colors['aqua']
                if blu.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (630, 405)
                    settings['color'] = colors['blue']
                if pur.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (680, 405)
                    settings['color'] = colors['purple']
                if pin.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (530, 445)
                    settings['color'] = colors['pink']
                if whi.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (580, 445)
                    settings['color'] = colors['white']
                if gra.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (630, 445)
                    settings['color'] = colors['gray']
                if default.collidepoint(pygame.mouse.get_pos()):
                    pos_color = (680, 445)
                    settings['color'] = colors['default']
                    
                if sou1.collidepoint(pygame.mouse.get_pos()):
                    pos9 = (530, 515)
                    settings['sound'] = True
                if sou2.collidepoint(pygame.mouse.get_pos()):
                    pos9 = (665, 515)
                    settings['sound'] = False

                if max_score1.collidepoint(pygame.mouse.get_pos()):
                    pos10 = (530, 615)
                    settings['max score'] = 5
                if max_score2.collidepoint(pygame.mouse.get_pos()):
                    pos10 = (595, 615)
                    settings['max score'] = 10
                if max_score3.collidepoint(pygame.mouse.get_pos()):
                    pos10 = (665, 615)
                    settings['max score'] = 15

                if default_button.collidepoint(pygame.mouse.get_pos()):
                    pos1 = (bar1.centerx, bar1.centery)
                    pos2 = (bar2.centerx, bar2.centery)
                    pos3 = (bar3.centerx, bar3.centery)
                    pos4 = (bar4.centerx, bar4.centery)
                    pos5 = (bar5.centerx, bar5.centery)
                    pos6 = (bar6.centerx, bar6.centery)
                    pos7 = (665, 165)
                    pos8 = (530, 265)
                    pos_color = (680, 445)
                    pos9 = (665, 515)
                    pos10 = (530, 615)

                    i=0
                    for key in settings.keys():
                        settings[key] = defaults[i]
                        i+=1
                

        pygame.display.update()

def gameplay(single_player):

    #initialize game variables
    top_wall = pygame.Rect(0,0,WINDOW_SIZE[0],20)    
    bottom_wall = pygame.Rect(0,WINDOW_SIZE[1] - 20,WINDOW_SIZE[0],20)
    midline = pygame.Rect(WINDOW_SIZE[0]/2-1,0,2,WINDOW_SIZE[1])

    paddle_height = settings['paddle size']
    if single_player:
        cpu_height = settings['cpu size']
    else: cpu_height = settings['paddle size']
    paddle_width = 10
    ball_size = settings['ball size']

    ball = pygame.Rect(0,0,ball_size,ball_size)
    ball.centerx = WINDOW_SIZE[0]/2
    ball.centery = WINDOW_SIZE[1]/2

    paddle = pygame.Rect(WINDOW_SIZE[0] - 10, 0,paddle_width,paddle_height) #right side
    cpu = pygame.Rect(0, 0,paddle_width,cpu_height)                      #left side
    paddle.centery = WINDOW_SIZE[1]/2
    cpu.centery = WINDOW_SIZE[1]/2
    
    ball_x_speed, ball_y_speed = reset_ball(ball)

    paddle_speed = settings['paddle speed']
    if single_player:
        cpu_speed = settings['cpu speed']
    else: cpu_speed = settings['paddle speed']
    ball_speed = settings['ball speed']

    score_right = 0
    score_left = 0

    max_score = settings['max score']

    text_font = pygame.font.SysFont('ptmono',70,True)
    tiny_font = pygame.font.SysFont('ptmono',16)

    #game loop
    start_time = time.time()
    end = False
    count = 0
    while not end:
        window.fill(BLACK)
        if not settings['sound']: blip.set_volume(0)
        else: blip.set_volume(0.5)

        #draw_rects
        pygame.draw.rect(window, settings['color'], top_wall)
        pygame.draw.rect(window, settings['color'], bottom_wall)
        pygame.draw.rect(window, (100,100,100), midline)
        pygame.draw.rect(window, settings['color'], ball)
        pygame.draw.rect(window, settings['color'], paddle)
        pygame.draw.rect(window, settings['color'], cpu)

        #draw_text
        text_right = text_font.render(str(score_right), False, (200,200,200))
        text_left = text_font.render(str(score_left), False, (200,200,200))

        esc_text = tiny_font.render("Press ESC at any time to return to the menu.",False, settings['color'])
        
        player_time = int(time.time() - start_time)
        time_text = text_font.render(str(player_time), False, (200,200,200))
        if settings['cpu difficulty'] != 'impossible' or not single_player:
            window.blit(text_left, (WINDOW_SIZE[0]/4, WINDOW_SIZE[1]/6))
            window.blit(text_right, (WINDOW_SIZE[0]*3/4, WINDOW_SIZE[1]/6))
        else:
            window.blit(time_text, (WINDOW_SIZE[0]*3/4, WINDOW_SIZE[1]/6))

        if count < 200:
            window.blit(esc_text, (WINDOW_SIZE[0]/2 - tiny_font.size("Press ESC at any time to return to the menu.")[0]/2, 50))
        
        ball.x += ball_x_speed
        ball.y += ball_y_speed
        
        #move cpu
        if single_player:
            if settings["cpu difficulty"] == 'impossible':
                cpu.centery = ball.centery
            else:
                if cpu.centery < ball.centery:
                    cpu.y += cpu_speed
                if cpu.centery > ball.centery:
                    cpu.y -= cpu_speed

        if pygame.Rect.colliderect(ball, paddle):
            if ball_x_speed > 0: ball_x_speed = ball_speed
            else: ball_x_speed = -ball_speed
            ball_x_speed *= -1

            if ball.centery < paddle.y+paddle_height/5:
                ball_y_speed -= 6
            if paddle.y+paddle_height/5 <= ball.centery < paddle.y+paddle_height*2/5:
                ball_y_speed -= 3 #ball between paddle.y+2/5 and y+3/5 doesnt change speed (mid)
            if paddle.y+paddle_height*3/5 < ball.centery <= paddle.y+paddle_height*4/5:
                ball_y_speed += 3
            if paddle.y+paddle_height*4/5 < ball.centery:
                ball_y_speed += 6
            ball_y_speed += random.uniform(-1,1)
            blip.play()

        if pygame.Rect.colliderect(ball, cpu):
            if ball_x_speed > 0: ball_x_speed = ball_speed
            else: ball_x_speed = -ball_speed
            ball_x_speed *= -1

            if ball.centery < cpu.y+paddle_height/5:
                ball_y_speed -= 6
            if cpu.y+paddle_height/5 <= ball.centery < cpu.y+paddle_height*2/5:
                ball_y_speed -= 3 #ball between paddle.y+2/5 and y+3/5 doesnt change speed (middle)
            if cpu.y+paddle_height*3/5 < ball.centery <= cpu.y+paddle_height*4/5:
                ball_y_speed += 3
            if cpu.y+paddle_height*4/5 < ball.centery:
                ball_y_speed += 6
            ball_y_speed += random.uniform(-1,1)
            blip.play()
            
        #hitting walls
        if paddle.top <= top_wall.bottom:
            paddle.y = top_wall.bottom
        if paddle.bottom >= bottom_wall.top:
            paddle.y = bottom_wall.top - paddle_height

        if cpu.top <= top_wall.bottom:
            cpu.y = top_wall.bottom
        if cpu.bottom >= bottom_wall.top:
            cpu.y = bottom_wall.top - cpu_height

        if ball.top <= top_wall.bottom:
            ball_y_speed *= -1
            ball.y = ball_size + 1
            blip.play()
        if ball.bottom >= bottom_wall.top:
            ball_y_speed *= -1
            ball.y = WINDOW_SIZE[1] - 2*ball_size + 1
            blip.play()

        if ball.left > WINDOW_SIZE[0]: #cpu score
            score_left += 1
            if settings['random respawn']:
                direction = random.choice((-1,1))
            else:
                direction = 1
            ball_x_speed, ball_y_speed = reset_ball(ball,direction)
        if ball.right < 0: #player score
            score_right += 1
            if settings['random respawn']:
                direction = random.choice((-1,1))
            else:
                direction = -1
            ball_x_speed, ball_y_speed = reset_ball(ball,direction)
            
        #key controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                menu()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            paddle.move_ip(0,-paddle_speed)
        if keys[pygame.K_DOWN]:
            paddle.move_ip(0,paddle_speed)

        if not single_player:
            if keys[pygame.K_w]:
                cpu.move_ip(0,-cpu_speed)
            if keys[pygame.K_s]:
                cpu.move_ip(0,cpu_speed)

        if score_left == max_score:
            end = True
            winner = False
        if score_right == max_score:
            end = True
            winner = True

        if settings['cpu difficulty'] == 'impossible' and score_left != 0 and single_player:
            end = True
            winner = None
            
        count += 1
        pygame.display.update()
        clock.tick(80)
        if end:
            end_game(winner, single_player, player_time)


menu()
