import pygame
import random
import sys
from pygame.locals import *

window_width = 800
window_height = 600
cell_size = 20 # 贪吃蛇方块的大小

map_width = int(window_width / cell_size)
map_height = int(window_height / cell_size)

# 定义方向
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4
HEAD = 0 # 贪吃蛇的头部下标

snake_speed = 15 #贪吃蛇的速度

# 颜色定义
white = (255, 255, 255)
black = (0, 0, 0)
gray = (230, 230, 230)
dark_gray = (40, 40, 40)
DARKGreen = (0, 155, 0)
Green = (0, 255, 0)
Red = (255, 0, 0)
blue = (0, 0, 255)
dark_blue =(0,0, 139)

BG_COLOR = black # 游戏背景颜色

# 欢迎界面
def show_start_info(screen):
    # 先创建一个Font对象，用自己的字体。有了Font对象以后， 就可以用render方法来写字了，然后通过blit方法blit到屏幕上。
    font = pygame.font.Font('simsun.ttc',40)
    tip = font.render('按任意键开始游戏',True,(65,105,225))
    # 用pygame.image.load()加载图像获得对象，在用blit方法刷到屏幕上。做完以上事件以后，记得要update一下刷新一下屏幕
    gamestart = pygame.image.load('123.jpg')
    screen.blit(gamestart,(140,30))
    screen.blit(tip,(240,400))
    pygame.display.update()

    # 键盘监听事件
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate() # 终止程序
            elif event.type == KEYDOWN:
                if (event.key == K_ESCAPE):
                    terminate()
                else:
                    return # 结束此函数，开始游戏

#游戏结束信息显示
def show_gameover_info(screen):
    font = pygame.font.Font('simsun.ttc', 30)
    tip = font.render('按Q或者ESC退出游戏, 按任意键重新开始游戏~', True, (65, 105, 225))
    gamestart = pygame.image.load('123.jpg')
    screen.blit(gamestart, (140, 30))
    screen.blit(tip, (100, 400))
    pygame.display.update()

    while True:  #键盘监听事件
        for event in pygame.event.get():  # event handling loop
            if event.type == QUIT:
                terminate()     #终止程序
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:  #终止程序
                    terminate() #终止程序
                else:
                    return #结束此函数, 重新开始游戏

# 开始游戏
def running_game(screen,snake_speed_clock):
    # 开始位置,在(3,map_width - 8)范围内找随机数
    startx = random.randint(3,map_width - 8)
    starty = random.randint(3,map_height - 8)
    snake_coords = [{'x': startx, 'y': starty},  #初始化贪吃蛇的位置
                   {'x': startx - 1, 'y': starty},
                   {'x': startx - 2, 'y': starty}]

    direction = RIGHT # 开始时向右移动
    food = get_random_location() # 食物随机位置

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        move_snake(direction,snake_coords)

        ret = snake_is_alive(snake_coords)
        if not ret:
            break # 游戏结束
        snake_is_eat_food(snake_coords,food)

        screen.fill(BG_COLOR)
        draw_snake(screen,snake_coords)
        draw_food(screen, food)
        draw_score(screen, len(snake_coords) - 3)
        pygame.display.update()
        snake_speed_clock.tick(snake_speed) #控制fps


# 食物的随机生成
def get_random_location():
    return {'x': random.randint(0, map_width - 1), 'y': random.randint(0, map_height - 1)}
 
# 移动贪吃蛇,即更新头部,删除尾部放在函数中
def move_snake(direction,snake_coords):
    if direction == UP:
        newHead = {'x':snake_coords[HEAD]['x'],'y':snake_coords[HEAD]['y'] - 1}
    elif direction == DOWN:
        newHead = {'x': snake_coords[HEAD]['x'], 'y': snake_coords[HEAD]['y'] + 1}
    elif direction == LEFT:
        newHead = {'x': snake_coords[HEAD]['x'] - 1, 'y': snake_coords[HEAD]['y']}
    elif direction == RIGHT:
        newHead = {'x': snake_coords[HEAD]['x'] + 1, 'y': snake_coords[HEAD]['y']}
    snake_coords.insert(0, newHead)

# 判断贪吃蛇是否gg
def snake_is_alive(snake_coords):
    tag = True
    # 碰壁
    if snake_coords[HEAD]['x'] == -1 or snake_coords[HEAD]['x'] == map_width or snake_coords[HEAD]['y'] == -1 or \
             snake_coords[HEAD]['y'] == map_height:
        tag = False

    # 碰自己
    for snake_body in snake_coords[1:]:
        if snake_coords[HEAD]['x'] == snake_body['x'] and snake_body['y'] == snake_coords[HEAD]['y']:
            tag = False
    return tag

# 判断贪吃蛇是否吃到食物
def snake_is_eat_food(snake_coords,food):
    if snake_coords[HEAD]['x'] == food['x'] and snake_coords[HEAD]['y'] == food['y']:
        food['x'] = random.randint(0, map_width - 1)
        food['y'] = random.randint(0, map_height - 1) # 实物位置重新设置
    else:
        del snake_coords[-1]  # 如果没有吃到实物, 就向前移动, 那么尾部一格删掉

# 画贪吃蛇
def draw_snake(screen, snake_coords):
    for coord in snake_coords:
        x = coord['x'] * cell_size
        y = coord['y'] * cell_size
        wormSegmentRect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, dark_blue, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(                #贪吃蛇身子里面的第二层亮蓝色色
            x + 4, y + 4, cell_size - 8, cell_size - 8)
        pygame.draw.rect(screen, blue, wormInnerSegmentRect)

#将食物画出来
def draw_food(screen, food):
    x = food['x'] * cell_size
    y = food['y'] * cell_size
    appleRect = pygame.Rect(x, y, cell_size, cell_size)
    pygame.draw.rect(screen, Red, appleRect)

#画成绩
def draw_score(screen,score):
    font = pygame.font.Font('simsun.ttc', 30)
    scoreSurf = font.render('得分: %s' % score, True, Green)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (window_width - 120, 10)
    screen.blit(scoreSurf, scoreRect)

#程序终止
def terminate():
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()

    snake_speed_clock = pygame.time.Clock() # 设置fps
    screen = pygame.display.set_mode((window_width,window_height)) # 创建窗口
    screen.fill(white) # 背景颜色填充

    pygame.display.set_caption("Python贪吃蛇小游戏") # 设置标题
    show_start_info(screen)  # 欢迎界面
    while True:
        running_game(screen, snake_speed_clock)
        show_gameover_info(screen)