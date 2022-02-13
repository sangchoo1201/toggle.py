import random
import pygame
import win32clipboard as clip

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


def click(x, y, reverse=False):
    global do

    functions = (flip, flip_u, flip_d, flip_l, flip_r,
                 flip_lu, flip_ru, flip_rd, flip_ld,
                 flip_l_r, flip_u_d, flip_lu_rd, flip_ru_ld,
                 rotate_cw, rotate_ccw, flip_diamond, flip_square,
                 mirror_lr, mirror_ud, shift_l, shift_r)

    num = level_code[1][y][x]
    if num == 0:
        return

    if reverse:
        if num in (13, 19):
            num += 1
        elif num in (14, 20):
            num -= 1
    functions[num](x, y)
    if not reverse:
        do.append((x, y))

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
    click(*move, True)
    click_count -= 1

def redo():
    global did, click_count

    if not did:
        return

    move = did.pop()
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


def generate(width, height, amount, shape_list):
    global x_max, y_max, do, did, click_count

    level_code[0] = (width, height)
    x_max, y_max = width, height
    shape_list = shape_list[:]

    level_code[1] = [[0 for _ in range(width)][:] for _ in range(height)]
    for i in range(y_max):
        for j in range(x_max):
            random.shuffle(shape_list)
            discard_list = []
            shape = None
            while True:
                if shape is not None:
                    discard_list.append(shape)
                shape = shape_list.pop() if shape_list else random.randint(0, 16)
                if j == 0 and shape in (3, 5, 8):
                    continue
                if j == width - 1 and shape in (4, 6, 7):
                    continue
                if i == 0 and shape in (1, 5, 6):
                    continue
                if i == height - 1 and shape in (2, 7, 8):
                    continue
                if (j, i) in ((0, height-1), (width-1, 0)) and shape == 11:
                    continue
                if (j, i) in ((0, 0), (width-1, height-1)) and shape == 12:
                    continue
                break
            level_code[1][i][j] = shape

    level_code[2] = [[0 for _ in range(width)][:] for _ in range(height)]
    li = list(range(width * height))
    random.shuffle(li)
    for _ in range(amount):
        i = li.pop()
        x, y = i%width, i//width
        while level_code[1][y][x] == 0:
            i = li.pop()
            x, y = i%width, i//width
        click(x, y, True)
    do, did = [], []
    click_count = 0

def v1_encode(author, name):  # unused function
    encoded_text = "".join(
        str(i) + spliter
        for i in (author, name, level_code[0][0], level_code[0][1])
    )

    for i, j in zip(sum(level_code[1], []), sum(level_code[2], [])):
        char = 64 + (j^1)*32 + i
        encoded_text += chr(char)
    return encoded_text

def v1_decode():
    global level_code, x_max, y_max, code

    x_max, y_max = codes[2], codes[3]
    level_code[0] = (x_max, y_max)

    level_code[1] = [[0 for _ in range(x_max)][:] for _ in range(y_max)]
    level_code[2] = [[0 for _ in range(x_max)][:] for _ in range(y_max)]
    for i in range(y_max):
        for j in range(x_max):
            a = ord(code[0])
            code = code[1:]
            level_code[1][i][j] = (a & 31)
            level_code[2][i][j] = 0 if (a & 32) else 1


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

def draw_text(text, size, pos):
    font = pygame.font.SysFont("consolas", size)
    img = font.render(text, True, (255, 255, 255))
    rect = img.get_rect()
    rect.center = pos
    screen.blit(img, rect)
    return rect


def set_mode(select):
    global mode, click_count, amount, level, do, did, run, code, codes

    mode = select
    if mode == "classic":
        click_count = 0
        amount = 3
        level = 1
        do, did = [], []
        generate(5, 5, amount, classic_shape)
    elif mode == "play":
        click_count = 0
        level = codes[1]
        do, did = [], []
        v1_decode()
    elif mode == "custom play":
        try:
            clip.OpenClipboard()
            codes = clip.GetClipboardData().split(spliter)
            assert len(codes) == 5
            codes[2] = int(codes[2])
            codes[3] = int(codes[3])
            assert len(codes[4]) == codes[2] * codes[3]
            code = codes[4]
            for i in range(64, 85):
                codes[4] = codes[4].replace(chr(i), "")
                codes[4] = codes[4].replace(chr(i+32), "")
            assert not codes[4]
            codes.pop()
        except:
            code = None
        finally:
            clip.CloseClipboard()
    elif mode == "exit":
        run = False


mode, click_count, amount, level, do, did, code, codes = [None]*8
selection_max = 3
modes = ["classic", "custom play", "exit"]
spliter = ":"
classic_shape = [0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 12, 13, 14, 15, 16]
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
        draw_text(logo, minimum//10, (screen_width//2, screen_height//2 - minimum//3))
        for i, text in enumerate(modes):
            position = (screen_width//2, screen_height//2 + minimum//8*i)
            draw_text(text, minimum//15, position)

    elif mode == "custom play":
        return_rect = draw_text("return to menu", minimum//20, (screen_width//2, screen_height//2 + minimum//5))
        if code:
            draw_text(f"{codes[1]}", minimum//15, (screen_width//2, screen_height//2 - minimum//4))
            draw_text(f"by {codes[0]}", minimum//20, (screen_width//2, screen_height//2 - round(minimum*0.17)))
            draw_text(f"size: {codes[2]}*{codes[3]}", minimum//20, (screen_width//2, screen_height//2))
            play_rect = draw_text("play!", minimum//20, (screen_width//2, screen_height//2 + round(minimum*0.3)))
        else:
            draw_text("No valid level", minimum//15, (screen_width//2, screen_height//2 - minimum//10))
            draw_text("in your clipboard!", minimum//15, (screen_width//2, screen_height//2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if return_rect.collidepoint(x, y):
                    set_mode("menu")
                if code and play_rect.collidepoint(x, y):
                    set_mode("play")
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                set_mode("menu")

    elif mode in ("classic", "play"):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pos()
                mx, my = pygame.mouse.get_pos()
                if 0 <= x < x_max and 0 <= y < y_max:
                    click(x, y)
                    if level_code[1][y][x] != 0:
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
            if mode == "classic":
                if level % 10 == 0:
                    amount += 1
                generate(5, 5, amount, classic_shape)
                level += 1
            elif mode == "play":
                set_mode("menu")

        score = f"level:{level}  click:{click_count}"
        position = (round(screen_width/2), round((screen_height-minimum*0.85)/2))
        draw_text(score, minimum // 20, position)

        texts = ("undo", "redo", "reset")
        for i, text in enumerate(texts):
            position = (round((screen_width/2)-(minimum/3.5)*(1-i)), round((screen_height + minimum*0.85)/2))
            draw_text(text, minimum // 20, position)

    pygame.display.flip()

pygame.quit()
