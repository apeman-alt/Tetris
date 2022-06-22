#Josh Muszka
#Started June 20, 2022
#Last Updated June 22, 2022
#Tetris:
#current version can spawn two types of pieces with different colors
#player can move, stack, and rotate pieces
#pieces have border detection

#point-earning system / full-row-clearing to be added
#more types of pieces to be added 

import pygame, sys, time, random

pygame.init()
pygame.display.set_caption('Tetris')

current_time = time.time()
prev_time = time.time()

width = 400
height = 2*width
size = width, height
screen = pygame.display.set_mode(size)

refresh = 144

background_color = 255,255,255
grid_color = 200,200,200

GRID = []
GRID_X = 10
GRID_Y = 20

tile_size = width/GRID_X

#BLOCK OBJECTS
class Block:
    x = 3*tile_size
    y = 1*tile_size
    color = 0xFF, 0x0, 0x0
    adj_blocks = [[2*tile_size,1*tile_size], [1*tile_size,1*tile_size], [4*tile_size,1*tile_size]]

block = Block()

#randomly choose which type of block to start off with
num = random.randint(0,1)

if num == 0: #horizontal line block
    block.adj_blocks = [[block.x-1*tile_size, block.y - 0*tile_size], [block.x-2*tile_size,block.y - 0*tile_size], [block.x+1*tile_size,block.y+0*tile_size]]
    block.color = 255, 0, 0
elif num == 1: #vertical line block
    block.adj_blocks = [[block.x+0*tile_size, block.y-1*tile_size], [block.x+0*tile_size,block.y+1*tile_size], [block.x+0*tile_size,block.y+2*tile_size]]
    block.color = 0, 0, 255

block_list = []

def move_blocks_vertical():
    global prev_time, current_time
    current_time = time.time()
    if current_time-prev_time > 0.8:
        
        #if block.y < height-tile_size: block.y+=tile_size

        adj_blocks_floating = True
        for x, y in block.adj_blocks:
            if not y < height-tile_size: adj_blocks_floating = False

        if block.y < height-tile_size and adj_blocks_floating:
            block.y+=tile_size
            for i in block.adj_blocks:
                #increase y value of adjactent block by 1 tile
                i[1] += tile_size
        prev_time = time.time()

def move_blocks_horizontal(key):
    global tile_size

    #check if piece is bordering on right wall
    right = False
    if not block.x < width-tile_size: right = True
    for i in block.adj_blocks:
        for i in block.adj_blocks:
            x= i[0]
            y=i[1]
            if not x < width-tile_size: right = True
    
    #check if piece is bordering on left wall
    left = False
    if not block.x > 0: left = True
    for i in block.adj_blocks:
        for i in block.adj_blocks:
            x= i[0]
            y=i[1]
            if not x > 0: left = True


    #move left unless against left border, or at bottom of floor
    #move right unless against right border, or at bottom of floor
    #move down unless at bottom of floor
    if key == pygame.K_LEFT and not left: 
        block.x -= tile_size
        for i in block.adj_blocks: i[0] -= tile_size
    if key == pygame.K_RIGHT and not right: 
        block.x += tile_size
        for i in block.adj_blocks: i[0] += tile_size
    if key == pygame.K_DOWN: 
        block.y += tile_size
        for i in block.adj_blocks: i[1] += tile_size

def release_new_block():
    global block
    global block_list

    #check to see if the current block is directly above another block
    above_another_block = False
    for b in block_list:
        if not block.y < b.y-tile_size and block.x == b.x: above_another_block = True
        for i in block.adj_blocks:
            x= i[0]
            y=i[1]
            if not y < b.y-tile_size and x == b.x: above_another_block = True

    #check to see if the current block is directly above ground
    on_ground = False
    if not block.y < height-tile_size: on_ground = True
    for i in block.adj_blocks:
        y = i[1]
        if not y < height-tile_size: on_ground = True

    #if block hits ground, add it to the block list and create a new block, or if block is above a pre-existing block
    if on_ground or above_another_block:
        block_list.append(block)
        
        #convert adjacent blocks into block objects
        for i in block.adj_blocks:
            b = Block()
            b.x = i[0]
            b.y = i[1]
            b.color = block.color
            block_list.append(b)


        block = Block()

        #randomly choose which type of block
        num = random.randint(0,1)

        if num == 0: #horizontal line block
            block.adj_blocks = [[block.x-1*tile_size, block.y - 0*tile_size], [block.x-2*tile_size,block.y - 0*tile_size], [block.x+1*tile_size,block.y+0*tile_size]]
            block.color = 255, 0, 0
        elif num == 1: #vertical line block
            block.adj_blocks = [[block.x+0*tile_size, block.y-1*tile_size], [block.x+0*tile_size,block.y+1*tile_size], [block.x+0*tile_size,block.y+2*tile_size]]
            block.color = 0, 0, 255

def rotate_blocks(key):

    #if z is pressed
    if key == pygame.K_z:
        x1 = block.x//tile_size
        y1 = block.y//tile_size

        for i in block.adj_blocks:
            x2 = i[0]//tile_size
            y2= i[1]//tile_size
            dx = x1-x2
            dy = y1-y2

            if dx == 0 and not dy == 0:
                i[0] += dy*tile_size
                i[1] += dy*tile_size
            elif not dx == 0 and dy == 0:
                i[0] += dx*tile_size
                i[1] -= dx*tile_size

def draw_blocks():
    #draw anchored block
    pygame.draw.rect(screen, block.color, pygame.Rect(block.x,block.y,tile_size,tile_size))

    #draw adjacent blocks
    for x, y in block.adj_blocks:
        pygame.draw.rect(screen, block.color, pygame.Rect(x,y,tile_size,tile_size))

    #draw already-placed blocks
    for b in block_list:
        pygame.draw.rect(screen, b.color, pygame.Rect(b.x,b.y,tile_size,tile_size))

    #draw grid lines
    for i in range(GRID_X):
        for j in range(GRID_Y):
            pygame.draw.line(screen, grid_color, (i*tile_size, 0), (i*tile_size, height))
            pygame.draw.line(screen, grid_color, (0, j*tile_size), (width, j*tile_size))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            move_blocks_horizontal(event.key)
            rotate_blocks(event.key)

    screen.fill(background_color)
    move_blocks_vertical()
    release_new_block()
    draw_blocks()

    time.sleep(1/refresh)
    pygame.display.update()