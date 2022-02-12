import random
import pygame

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.init()

pygame.display.set_caption("Toggle.py")

level_code = [0, 0, 0]
x_max, y_max = 0, 0


def flip(x, y):
    level_code[2][y][x] ^= 1

def flip_u(x, y):
    for dy in range(y+1):
        level_code[2][dy][x] ^= 1

def flip_d(x, y):
    for dy in range(y, y_max):
        level_code[2][dy][x] ^= 1

def flip_l(x, y):
    for dx in range(x+1):
        level_code[2][y][dx] ^= 1

def flip_r(x, y):
    for dx in range(x, x_max):
        level_code[2][y][dx] ^= 1

def flip_lu(x, y):
    while x >= 0 and y >= 0:
        level_code[2][y][x] ^= 1
        x, y = x-1, y-1

def flip_ru(x, y):
    while x < x_max and y >= 0:
        level_code[2][y][x] ^= 1
        x, y = x+1, y-1

def flip_rd(x, y):
    while x < x_max and y < y_max:
        level_code[2][y][x] ^= 1
        x, y = x+1, y+1

def flip_ld(x, y):
    while x >= 0 and y < y_max:
        level_code[2][y][x] ^= 1
        x, y = x-1, y+1

def flip_l_r(x, y):
    flip_l(x, y)
    flip_r(x, y)
    flip(x, y)

def flip_u_d(x, y):
    flip_u(x, y)
    flip_d(x, y)
    flip(x, y)

def flip_lu_rd(x, y):
    flip_lu(x, y)
    flip_rd(x, y)
    flip(x, y)

def flip_ru_ld(x, y):
    flip_ru(x, y)
    flip_ld(x, y)
    flip(x, y)

def rotate_cw(x, y):
    pos = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
    li = []
    for dx, dy in pos:
        if not (0 <= x+dx < x_max and 0 <= y+dy < y_max):
            li.append(0)
        else:
            li.append(level_code[2][y+dy][x+dx])
    li.insert(0, li.pop())
    for i, d in enumerate(pos):
        dx, dy = d
        if 0 <= x+dx < x_max and 0 <= y+dy < y_max:
            level_code[2][y+dy][x+dx] = li[i]
    flip(x, y)

def rotate_ccw(x, y):
    pos = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))
    li = []
    for dx, dy in pos:
        if not (0 <= x+dx < x_max and 0 <= y+dy < y_max):
            li.append(0)
        else:
            li.append(level_code[2][y+dy][x+dx])
    li.append(li[0])
    del li[0]
    for i, d in enumerate(pos):
        dx, dy = d
        if 0 <= x+dx < x_max and 0 <= y+dy < y_max:
            level_code[2][y+dy][x+dx] = li[i]
    flip(x, y)

def flip_diamond(x, y):
    flip_r(x, y)
    flip_l(x, y)
    flip_u(x, y)
    flip_d(x, y)
    flip(x, y)

def flip_square(x, y):
    pos = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1))
    for dx, dy in pos:
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max:
            flip(x+dx, y+dy)

def mirror_lr(x, y):
    for dy in range(y_max):
        a = 0 if x == 0 else level_code[2][dy][x-1]
        b = 0 if x == x_max-1 else level_code[2][dy][x+1]
        if x > 0:
            level_code[2][dy][x-1] = b
        if x < x_max-1:
            level_code[2][dy][x+1] = a
    flip(x, y)

def mirror_ud(x, y):
    for dx in range(x_max):
        a = 0 if y == 0 else level_code[2][y-1][dx]
        b = 0 if y == y_max-1 else level_code[2][y+1][dx]
        if y > 0:
            level_code[2][y-1][dx] = b
        if y < y_max-1:
            level_code[2][y+1][dx] = a
    flip(x, y)

# noinspection PyUnusedLocal
def shift_l(x, y):
    row = level_code[2][y]
    row.append(row[0])
    del row[0]
    level_code[2][y] = row

# noinspection PyUnusedLocal
def shift_r(x, y):
    row = level_code[2][y]
    row.insert(0, row.pop())
    level_code[2][y] = row


def click(x, y, shape=None):
    global do

    functions = (flip, flip_u, flip_d, flip_l, flip_r,
                 flip_lu, flip_ru, flip_rd, flip_ld,
                 flip_l_r, flip_u_d, flip_lu_rd, flip_ru_ld,
                 rotate_cw, rotate_ccw, flip_diamond, flip_square,
                 mirror_lr, mirror_ud, shift_l, shift_r)

    num = level_code[1][y][x]
    if shape:
        functions[shape](x, y)
    elif num != 0:
        functions[num](x, y)
        do.append((x, y, num))

def pos():
    x, y = pygame.mouse.get_pos()
    tile_size = round(minimum * 0.7 / max(level_code[0]))
    x -= round(screen_width/2 + (-(x_max-1)/2 - 0.5) * tile_size)
    x //= tile_size
    y -= round(screen_height/2 + (-(y_max-1)/2 - 0.5) * tile_size)
    y //= tile_size
    return x, y


def undo():
    global do, did, click_count

    if not do:
        return

    move = do.pop()
    did.append(move)
    move = list(move)
    if move[2] in (13, 14, 19, 20):
        move[2] ^= 1
    click(*move)
    click_count -= 1

def redo():
    global did, click_count

    if not did:
        return

    move = did.pop()
    do.append(move)
    click(*move)
    click_count += 1

def reset():
    global do, did, click_count

    while do:
        undo()
    did = []
    click_count = 0


def print_state():  # for debugging
    for row in level_code[2]:
        print(*row)

def print_shape():  # for debugging
    for row in level_code[1]:
        print(*row)


def generate(width, height, amount):
    global x_max, y_max, do, did, click_count

    level_code[0] = (width, height)
    x_max, y_max = width, height

    shape = [[0 for _ in range(width)][:] for _ in range(height)]
    shape[random.randrange(height)][random.randrange(width)] = 15
    for x in range(width):
        for y in range(height):
            li = set(range(13))
            if x == 0:
                li -= set((3, 5, 8))
            if x == width-1:
                li -= set((4, 6, 7))
            if y == 0:
                li -= set((1, 5, 6))
            if y == height-1:
                li -= set((2, 7, 8))
            if (x, y) in ((0, height-1), (width-1, 0)):
                li.discard(11)
            if (x, y) in ((0, 0), (width-1, height-1)):
                li.discard(12)
            if shape[y][x] != 15:
                shape[y][x] = random.choice(list(li))
    level_code[1] = shape

    level_code[2] = [[0 for _ in range(width)][:] for _ in range(height)]
    li = list(range(width * height))
    random.shuffle(li)
    for _ in range(amount):
        i = li.pop()
        x, y = i%width, i//width
        while level_code[1][y][x] == 0:
            i = li.pop()
            x, y = i%width, i//width
        click(x, y)
    do, did = [], []
    click_count = 0

def v1_encode():  # unused function
    encoded_text = f"{level_code[0][0]}:{level_code[0][1]}:"
    for i, j in zip(sum(level_code[1], []), sum(level_code[2], [])):
        char = 64 + (j^1)*32 + i
        encoded_text += chr(char)
    return encoded_text


def draw():
    imgs = (0, "u", "d", "l", "r",
            "lu", "ru", "rd", "ld",
            "l_r", "u_d", "lu_rd", "ru_ld",
            "cw", "ccw", "diamond", "square",
            "vertical", "horizontal", "shl", "shr")
    gray = (127, 127, 127)
    yellow = (255, 255, 0)
    tile_size = round(min(screen_width, screen_height) * 0.7 / max(level_code[0]))
    for x in range(x_max):
        for y in range(y_max):
            dx = round(screen_width/2 + (x - (x_max-1)/2 - 0.5) * tile_size)
            dy = round(screen_height/2 + (y - (y_max-1)/2 - 0.5) * tile_size)
            color = yellow if level_code[2][y][x] else gray
            rect = (dx+1, dy+1, tile_size-2, tile_size-2)
            pygame.draw.rect(screen, color, rect)

            if level_code[1][y][x] == 0:
                continue
            src = f"img/{imgs[level_code[1][y][x]]}.png"
            img = pygame.image.load(src)
            img = pygame.transform.scale(img, (tile_size//3*2, tile_size//3*2))
            screen.blit(img, (dx+tile_size//6, dy+tile_size//6))

def draw_text(text, size, pos, option=None):
    font = pygame.font.SysFont("consolas", size)
    img = font.render(text, True, (255, 255, 255))
    rect = img.get_rect()
    if option is None:
        rect.x, rect.y = pos
    elif option == "center":
        rect.center = pos
    screen.blit(img, rect)


def set_mode(select):
    global mode, click_count, amount, level, do, did, run

    mode = select
    if mode == "classic":
        click_count = 0
        amount = 3
        level = 1
        do, did = [], []
        generate(5, 5, amount)
    elif mode == "exit":
        run = False


mode, click_count, amount, level, do, did = [None]*6
selection_max = 2
modes = ["classic", "exit"]
set_mode("menu")

run = True
while run:
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen_width, screen_height))
    minimum = min(screen_width, screen_height)

    if mode == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if not screen_width//2 - minimum//6 <= x <= screen_width//2 + minimum//6:
                    continue
                y -= screen_height//2
                y = round(y/(minimum//8))
                if 0 <= y < selection_max:
                    set_mode(modes[y])
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                run = False

        logo = "TOGGLE.py"
        draw_text(logo, minimum//10, (screen_width//2, screen_height//2 - minimum//3), "center")
        for i, text in enumerate(modes):
            position = (screen_width//2, screen_height//2 + minimum//8*i)
            draw_text(text, minimum//15, position, "center")

    elif mode == "classic":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pos()
                mx, my = pygame.mouse.get_pos()
                if 0 <= x < x_max and 0 <= y < y_max:
                    click(x, y)
                    did = []
                    click_count += 1
                    continue
                elif not round((screen_height + minimum*0.78)/2) <= my <= round((screen_height + minimum*0.92)/2):
                    continue
                for i, func in enumerate((undo, redo, reset)):
                    center_x = round((screen_width/2)-(minimum/3.5)*(1-i))
                    if center_x - minimum*0.07 <= mx <= center_x + minimum*0.07:
                        func()
                        break

            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                set_mode("menu")
            if event.key == pygame.K_z:
                undo()
            if event.key == pygame.K_x:
                redo()
            if event.key == pygame.K_r:
                reset()

        draw()
        if not any(sum(level_code[2], [])):
            if level % 10 == 0:
                amount += 1
            generate(5, 5, amount)
            level += 1

        score = f"level:{level}  click:{click_count}"
        position = ((screen_width-minimum)//2+2, (screen_height-minimum)//2+2)
        draw_text(score, minimum // 20, position)

        texts = ("undo", "redo", "reset")
        for i, text in enumerate(texts):
            position = (round((screen_width/2)-(minimum/3.5)*(1-i)), round((screen_height + minimum*0.85)/2))
            draw_text(text, minimum // 20, position, "center")

    pygame.display.flip()

pygame.quit()
