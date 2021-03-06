import random
import pygame
import win32clipboard as clip
from typing import List, Tuple, Optional
import base64

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.init()

pygame.display.set_caption("Toggle.py")

level_code: list = [[], [], []]
x_max, y_max = 0, 0


def flip(x: int, y: int) -> None:
    level_code[2][y][x] ^= 1


def flip_u(x: int, y: int) -> None:
    for dy in range(y + 1):
        level_code[2][dy][x] ^= 1


def flip_d(x: int, y: int) -> None:
    for dy in range(y, y_max):
        level_code[2][dy][x] ^= 1


def flip_l(x: int, y: int) -> None:
    for dx in range(x + 1):
        level_code[2][y][dx] ^= 1


def flip_r(x: int, y: int) -> None:
    for dx in range(x, x_max):
        level_code[2][y][dx] ^= 1


def flip_lu(x: int, y: int) -> None:
    while x >= 0 and y >= 0:
        level_code[2][y][x] ^= 1
        x, y = x - 1, y - 1


def flip_ru(x: int, y: int) -> None:
    while x < x_max and y >= 0:
        level_code[2][y][x] ^= 1
        x, y = x + 1, y - 1


def flip_rd(x: int, y: int) -> None:
    while x < x_max and y < y_max:
        level_code[2][y][x] ^= 1
        x, y = x + 1, y + 1


def flip_ld(x: int, y: int) -> None:
    while x >= 0 and y < y_max:
        level_code[2][y][x] ^= 1
        x, y = x - 1, y + 1


def flip_l_r(x: int, y: int) -> None:
    flip_l(x, y)
    flip_r(x, y)
    flip(x, y)


def flip_u_d(x: int, y: int) -> None:
    flip_u(x, y)
    flip_d(x, y)
    flip(x, y)


def flip_lu_rd(x: int, y: int) -> None:
    flip_lu(x, y)
    flip_rd(x, y)
    flip(x, y)


def flip_ru_ld(x: int, y: int) -> None:
    flip_ru(x, y)
    flip_ld(x, y)
    flip(x, y)


def rotate_cw(x: int, y: int) -> None:
    positions = (
        (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)
    )
    li = [
        level_code[2][y + dy][x + dx]
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max
        else 0
        for dx, dy in positions
    ]
    li.insert(0, li.pop())
    for i, d in enumerate(positions):
        dx, dy = d
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max:
            level_code[2][y + dy][x + dx] = li[i]
    flip(x, y)


def rotate_ccw(x: int, y: int) -> None:
    positions = (
        (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)
    )
    li = [
        level_code[2][y + dy][x + dx]
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max
        else 0
        for dx, dy in positions
    ]
    li.append(li[0])
    del li[0]
    for i, d in enumerate(positions):
        dx, dy = d
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max:
            level_code[2][y + dy][x + dx] = li[i]
    flip(x, y)


def flip_diamond(x: int, y: int) -> None:
    flip_r(x, y)
    flip_l(x, y)
    flip_u(x, y)
    flip_d(x, y)
    flip(x, y)


def flip_square(x: int, y: int) -> None:
    positions = (
        (-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)
    )
    for dx, dy in positions:
        if 0 <= x + dx < x_max and 0 <= y + dy < y_max:
            flip(x + dx, y + dy)


def mirror_lr(x: int, y: int) -> None:
    for dy in range(y_max):
        a = 0 if x == 0 else level_code[2][dy][x - 1]
        b = 0 if x == x_max - 1 else level_code[2][dy][x + 1]
        if x > 0:
            level_code[2][dy][x - 1] = b
        if x < x_max - 1:
            level_code[2][dy][x + 1] = a
    flip(x, y)


def mirror_ud(x: int, y: int) -> None:
    for dx in range(x_max):
        a = 0 if y == 0 else level_code[2][y - 1][dx]
        b = 0 if y == y_max - 1 else level_code[2][y + 1][dx]
        if y > 0:
            level_code[2][y - 1][dx] = b
        if y < y_max - 1:
            level_code[2][y + 1][dx] = a
    flip(x, y)


# noinspection PyUnusedLocal
def shift_l(x: int, y: int) -> None:
    row = level_code[2][y]
    row.append(row[0])
    del row[0]
    level_code[2][y] = row


# noinspection PyUnusedLocal
def shift_r(x: int, y: int) -> None:
    row = level_code[2][y]
    row.insert(0, row.pop())
    level_code[2][y] = row


def click(x: int, y: int, reverse: Optional[bool] = False) -> None:
    global do

    functions = (
        flip, flip_u, flip_d, flip_l, flip_r,
        flip_lu, flip_ru, flip_rd, flip_ld,
        flip_l_r, flip_u_d, flip_lu_rd, flip_ru_ld,
        rotate_cw, rotate_ccw, flip_diamond, flip_square,
        mirror_lr, mirror_ud, shift_l, shift_r
    )

    num = level_code[1][y][x]
    if num == 0:
        return

    if reverse and num in (13, 19):
        num += 1
    elif reverse and num in (14, 20):
        num -= 1

    functions[num](x, y)
    if not reverse:
        do.append((x, y))


def pos() -> Tuple[int, int]:
    x, y = pygame.mouse.get_pos()
    tile_size = round(minimum * 0.7 / max(level_code[0]))
    x -= round(screen_width / 2 + (-(x_max - 1) / 2 - 0.5) * tile_size)
    x //= tile_size
    y -= round(screen_height / 2 + (-(y_max - 1) / 2 - 0.5) * tile_size)
    y //= tile_size
    return x, y


def undo() -> None:
    global do, did, click_count

    if not do:
        return

    move = do.pop()
    did.append(move)
    move = list(move)
    click(*move, True)
    click_count -= 1


def redo() -> None:
    global did, click_count

    if not did:
        return

    move = did.pop()
    click(*move)
    click_count += 1


def reset() -> None:
    global do, did, click_count

    while do:
        undo()
    did = []
    click_count = 0


def print_state() -> None:  # for debugging
    for row in level_code[2]:
        print(*row)


def print_shape() -> None:  # for debugging
    for row in level_code[1]:
        print(*row)


def generate(width: int, height: int, click_amount: int, shape_list: List[int]) -> None:
    global x_max, y_max, do, did, click_count

    level_code[0] = tuple((width, height))
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
                if not any((
                        j == 0 and shape in (3, 5, 8),
                        j == width - 1 and shape in (4, 6, 7),
                        i == 0 and shape in (1, 5, 6),
                        i == height - 1 and shape in (2, 7, 8),
                        (j, i) in ((0, height - 1), (width - 1, 0)) and shape == 11,
                        (j, i) in ((0, 0), (width - 1, height - 1)) and shape == 12
                )):
                    break
            level_code[1][i][j] = shape

    level_code[2] = [[0 for _ in range(width)][:] for _ in range(height)]
    li = list(range(width * height))
    random.shuffle(li)
    for _ in range(click_amount):
        i = li.pop()
        x, y = i % width, i // width
        while level_code[1][y][x] == 0:
            i = li.pop()
            x, y = i % width, i // width
        click(x, y, True)
    do, did = [], []
    click_count = 0


def v1_encode(author: str, name: str) -> str:  # unused function
    encoded_text = "".join(
        str(i) + spliter
        for i in (author, name, level_code[0][0], level_code[0][1])
    )

    for i, j in zip(sum(level_code[1], []), sum(level_code[2], [])):
        char = 64 + (j ^ 1) * 32 + i
        encoded_text += chr(char)
    return base64.b64encode(bytes(encoded_text)).decode()


def v1_decode() -> None:
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


def draw() -> None:
    imgs = (
        "", "u", "d", "l", "r",
        "lu", "ru", "rd", "ld",
        "l_r", "u_d", "lu_rd", "ru_ld",
        "cw", "ccw", "diamond", "square",
        "vertical", "horizontal", "shl", "shr"
    )
    gray = (127, 127, 127)
    yellow = (255, 255, 0)
    tile_size = round(min(screen_width, screen_height) * 0.7 / max(level_code[0]))
    for x in range(x_max):
        for y in range(y_max):
            dx = round(screen_width / 2 + (x - (x_max - 1) / 2 - 0.5) * tile_size)
            dy = round(screen_height / 2 + (y - (y_max - 1) / 2 - 0.5) * tile_size)
            color = yellow if level_code[2][y][x] else gray
            rect = (dx + 1, dy + 1, tile_size - 2, tile_size - 2)
            pygame.draw.rect(screen, color, rect)

            if level_code[1][y][x] == 0:
                continue
            src = f"img/{imgs[level_code[1][y][x]]}.png"
            img = pygame.image.load(src)
            img = pygame.transform.scale(img, (tile_size // 3 * 2, tile_size // 3 * 2))
            screen.blit(img, (dx + tile_size // 6, dy + tile_size // 6))


def draw_text(value: str, size: int, positions: Tuple[int, int]) -> pygame.rect:
    font = pygame.font.SysFont("consolas", size)
    img = font.render(value, True, (255, 255, 255))
    rect = img.get_rect()
    rect.center = positions
    screen.blit(img, rect)
    return rect


def set_mode(select: str) -> None:
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
            codes = list(base64.b64decode(clip.GetClipboardData()).decode().split(spliter))
            assert len(codes) == 5
            codes[2] = int(codes[2])
            codes[3] = int(codes[3])
            assert len(codes[4]) == codes[2] * codes[3]
            code = codes[4]
            for i in range(64, 85):
                codes[4] = codes[4].replace(chr(i), "")
                codes[4] = codes[4].replace(chr(i + 32), "")
            assert not codes[4]
            codes.pop()
        except:
            code = None
        finally:
            clip.CloseClipboard()
    elif mode == "exit":
        run = False


mode, click_count, amount, level, do, did, code, codes = [None] * 8
selection_max = 3
modes = [
    "classic", "custom play", "exit"
]
spliter = ":"
classic_shape = [
    0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 10, 11, 12, 13, 14, 15, 16
]
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
                px, py = pygame.mouse.get_pos()
                if not screen_width // 2 - minimum // 6 <= px <= screen_width // 2 + minimum // 6:
                    continue
                py -= screen_height // 2
                py = round(py / (minimum // 8))
                if 0 <= py < selection_max:
                    set_mode(modes[py])
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                run = False

        logo = "TOGGLE.py"
        draw_text(logo, minimum // 10, (screen_width // 2, screen_height // 2 - minimum // 3))
        for index, text in enumerate(modes):
            position = (screen_width // 2, screen_height // 2 + minimum // 8 * index)
            draw_text(text, minimum // 15, position)

    elif mode == "custom play":
        return_rect = draw_text(
            "return to menu",
            minimum // 20,
            (screen_width // 2, screen_height // 2 + minimum // 5)
        )
        if code:
            draw_text(
                f"{codes[1]}",
                minimum // 15,
                (screen_width // 2, screen_height // 2 - minimum // 4)
            )
            draw_text(
                f"by {codes[0]}",
                minimum // 20,
                (screen_width // 2, screen_height // 2 - round(minimum * 0.17))
            )
            draw_text(
                f"size: {codes[2]}*{codes[3]}",
                minimum // 20,
                (screen_width // 2, screen_height // 2)
            )
            play_rect = draw_text(
                "play!",
                minimum // 20,
                (screen_width // 2, screen_height // 2 + round(minimum * 0.3))
            )
        else:
            draw_text(
                "No valid level",
                minimum // 15,
                (screen_width // 2, screen_height // 2 - minimum // 10)
            )
            draw_text(
                "in your clipboard!",
                minimum // 15,
                (screen_width // 2, screen_height // 2)
            )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                px, py = pygame.mouse.get_pos()
                if return_rect.collidepoint(px, py):
                    set_mode("menu")
                if code and play_rect.collidepoint(px, py):
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
                px, py = pos()
                mx, my = pygame.mouse.get_pos()
                if 0 <= px < x_max and 0 <= py < y_max:
                    click(px, py)
                    if level_code[1][py][px] != 0:
                        did = []
                        click_count += 1
                    continue
                elif not round((screen_height + minimum * 0.78) / 2) \
                        <= my \
                        <= round((screen_height + minimum * 0.92) / 2):
                    continue
                for index, func in enumerate((undo, redo, reset)):
                    center_x = round((screen_width / 2) - (minimum / 3.5) * (1 - index))
                    if center_x - minimum * 0.07 <= mx <= center_x + minimum * 0.07:
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
        position = (
            round(screen_width / 2),
            round((screen_height - minimum * 0.85) / 2)
        )
        draw_text(score, minimum // 20, position)

        texts = (
            "undo", "redo", "reset"
        )
        for index, text in enumerate(texts):
            position = (
                round((screen_width / 2) - (minimum / 3.5) * (1 - index)),
                round((screen_height + minimum * 0.85) / 2)
            )
            draw_text(text, minimum // 20, position)

    pygame.display.flip()

pygame.quit()
