import pygame
from sys import exit
import random
import sqlite3

con = sqlite3.connect("C:\\Users\\Roberto\\Documents\\Project\\University\\Databases\\Runner_game_db//runner_database.db")

leaderboard_list = []
res = con.execute("SELECT NAME,SCORE FROM PLAYER ORDER BY SCORE DESC Limit 5")
fetch = res.fetchall()
for i in fetch:
    leaderboard_list.append(i)
name = ""
l = 0
res = con.execute("SELECT NAME FROM PLAYER")
fetch = res.fetchall()
for i in fetch:
    l += 1

pygame.init()

clock = pygame.time.Clock()

width, height = 800, 400
FPS = 60
obstacle_speed = 5

screen = pygame.display.set_mode((width, height))

background_surface = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Sky.png")
ground_surface = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//ground.png")

player_walk1 = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Player//player_walk_1.png")
player_walk2 = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Player//player_walk_2.png")
player_walk = [player_walk1,player_walk2]
player_index = 0

player_jump = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Player//jump.png")

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80,300))

snail_surface = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//snail//snail1.png")
snail_rect = snail_surface.get_rect(midbottom = (800,300))

fly_surface = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Fly//Fly1.png")
fly_height = [190,250]

obstacle_rect_list = []

end_surface = pygame.Surface((width,height))
end_surface.fill("lightblue")

end_character_surface = pygame.image.load("UltimatePygameIntro-main//UltimatePygameIntro-main//graphics//Player//player_stand.png")
end_character_rect = end_character_surface.get_rect(center = (width / 5, 170))

font = pygame.font.Font("UltimatePygameIntro-main//UltimatePygameIntro-main//font//Pixeltype.ttf", 50)
next_surface = font.render(f"Enter your name", False, "black")
next_rect = next_surface.get_rect(center = (width / 5, 270))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

score = 0
def text(score,wherex, wherey,pos):

    if isinstance(score, int):
        score += 1

    font = pygame.font.Font("UltimatePygameIntro-main//UltimatePygameIntro-main//font//Pixeltype.ttf", 50)
    text_surface = font.render(f"{score}", False, "black")
    if pos == 1:
        text_rect = text_surface.get_rect(midleft = (wherex, wherey))
    else:
        text_rect = text_surface.get_rect(center = (wherex, wherey))
    screen.blit(text_surface, text_rect)

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= obstacle_speed

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else: screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list

    else: return []

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surface = player_walk[int(player_index)]

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

gravity = 0
game_state = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_state == False:
                l += 1
                con.execute(f"INSERT INTO PLAYER (ID, NAME, SCORE) VALUES ({l}, '{name}', {score})")
                con.commit()
                game_state = True
                snail_rect.left = 800
                score = 0
            elif event.key != pygame.K_SPACE and game_state == False and len(name) < 8 and event.key != pygame.K_BACKSPACE:
                name += event.unicode
            elif event.key == pygame.K_BACKSPACE and game_state == False and len(name) > 0:
                name = name[:-1]

        if event.type == obstacle_timer and game_state:
            if random.randint(0,2):
                obstacle_rect_list.append(fly_surface.get_rect(midbottom = (random.randint(900,1100), random.choice(fly_height))))
            else:
                obstacle_rect_list.append(snail_surface.get_rect(midbottom = (random.randint(900,1100),300)))

    if game_state:
        screen.blit(background_surface,(0,0))
        screen.blit(ground_surface, (0,300))
        player_animation()
        screen.blit(player_surface, player_rect)
        #screen.blit(snail_surface, snail_rect)
        text(score, width / 2, 80,2)

        #if snail_rect.right == 0: snail_rect.left = 800

        #snail_rect.x -= 4

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE] and player_rect.bottom == 300:
            gravity = -20
        score += 1

        gravity += 1
        player_rect.bottom += gravity

        if player_rect.bottom >= 300:
            player_rect.bottom = 300

        game_state = collisions(player_rect, obstacle_rect_list)
        obstacle_speed += 0.003
        name = ""

    else:
        obstacle_rect_list.clear()
        player_rect.bottom = 300
        obstacle_speed = 5
        screen.blit(end_surface,(0,0))
        screen.blit(end_character_surface, end_character_rect)
        screen.blit(next_surface, next_rect)
        text(score, width / 5, 80,2)
        text("Leaderboard", 520,40,2)
        text(leaderboard_list[0][1] - 1, 580, 120,1)
        text(leaderboard_list[0][0], 410, 120,1)
        text(leaderboard_list[1][1] - 1, 580, 180,1)
        text(leaderboard_list[1][0], 410, 180,1)
        text(leaderboard_list[2][1] - 1, 580, 240,1)
        text(leaderboard_list[2][0], 410, 240,1)
        text(leaderboard_list[3][1] - 1, 580, 300,1)
        text(leaderboard_list[3][0], 410, 300,1)
        text(leaderboard_list[4][1] - 1, 580, 360,1)
        text(leaderboard_list[4][0], 410, 360,1)
        text(name,width / 5, 340, 2)

    pygame.display.update()
    clock.tick(FPS)