import copy
import random
import time
import pygame
import math
import copy
import os

width, height = 700, 700
window = pygame.display.set_mode((width, height))

global lost, won, flags_used
lost = False
won = False
flags_used = 0

# assets
bomb = pygame.image.load(os.path.join("assets", "bomb.png"))
bomb = pygame.transform.scale(bomb, (80, 80))

flag = pygame.image.load(os.path.join("assets", "flag.png"))
flag = pygame.transform.scale(flag, (55, 55))

restart = pygame.image.load(os.path.join("assets", "restart2.png"))
restart = pygame.transform.scale(restart, (100, 100))
restart_surface = pygame.Surface((restart.get_width(), restart.get_height()), pygame.SRCALPHA)
restart_rect = restart.get_rect()
restart_rect.topright = (width, 0)

lost_text = pygame.image.load(os.path.join("assets", "lost.png"))
ratio = lost_text.get_width() / lost_text.get_height()
lost_text = pygame.transform.scale(lost_text, (100 * ratio, 100))

won_text = pygame.image.load(os.path.join("assets", "won.png"))
ratio = won_text.get_width() / won_text.get_height()
won_text = pygame.transform.scale(won_text, (100 * ratio, 100))



# numbers
numbers_list = []

for i in range(10):
    number = pygame.image.load(os.path.join("numbers", f"{i}.png"))
    number = pygame.transform.scale(number, (55, 55))
    numbers_list.append(number)


# colors
uncovered_hexagon_color = 	(64,69,78)
background_hexagon_color = 	(50, 55, 63)

mine_color = (76,82,101)

background_color = (41, 46, 53)
hidden_hexagon_color = background_color


global grid

grid = [
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
]
grid_width = len(grid[0])


def draw_cell(surface, color, x, y, cell_size, corner_diameter = 30):
    cell_width = pygame.Rect(x, y + corner_diameter / 2, cell_size[0], cell_size[1] - corner_diameter)
    cell_height = pygame.Rect(x + corner_diameter / 2, y, cell_size[0] - corner_diameter, cell_size[1])

    pygame.draw.rect(surface, color, cell_width)
    pygame.draw.rect(surface, color, cell_height)

    corner_left =  x + corner_diameter / 2
    corner_right = x - corner_diameter / 2 + cell_size[0]
    corner_top = y + corner_diameter / 2
    corner_bottom = y - corner_diameter / 2 + cell_size[1]
    corners = [(corner_right, corner_top), (corner_right, corner_bottom), (corner_left, corner_bottom),
               (corner_left, corner_top)]
    for corner in corners:
        pygame.draw.circle(surface, color, corner, corner_diameter / 2)


def generate_hexagon(color, width, radius = 16, third_radius = False):

    hexagon = pygame.Surface((width * 2, width * 2), pygame.SRCALPHA)

    hex_width = width
    hex_height = hex_width * math.sqrt(3) + 2

    hex_width += radius / (2 + third_radius)

    # rects = []

    rotated_surface0 = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)
    # rotated_surface0.fill(color)
    draw_cell(rotated_surface0, color, 0, 0, (rotated_surface0.get_width(), rotated_surface0.get_height()), radius)
    rotated_hex0 = rotated_surface0.get_rect()
    rotated_hex0.center = (width, width)

    # rects.append(rotated_hex0)

    hexagon.blit(rotated_surface0, rotated_hex0)


    rotated_surface = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)
    # rotated_surface.fill(color)
    draw_cell(rotated_surface, color, 0, 0, (rotated_surface.get_width(), rotated_surface.get_height()), radius)
    rotated_surface = pygame.transform.rotate(rotated_surface, 60)
    rotated_hex = rotated_surface.get_rect()
    rotated_hex.center = (width, width)

    # rects.append(rotated_hex)

    hexagon.blit(rotated_surface, rotated_hex)

    rotated_surface1 = pygame.Surface((hex_width, hex_height), pygame.SRCALPHA)
    # rotated_surface1.fill(color)
    draw_cell(rotated_surface1, color, 0, 0, (rotated_surface1.get_width(), rotated_surface1.get_height()), radius)
    rotated_surface1 = pygame.transform.rotate(rotated_surface1, -60)
    rotated_hex1 = rotated_surface1.get_rect()
    rotated_hex1.center = (width, width)

    # rects.append(rotated_hex1)


    hexagon.blit(rotated_surface1, rotated_hex1)

    return hexagon # , hexagon.get_rect()]



global hexagons
hexagons = []

flagged_hexagon = generate_hexagon(hidden_hexagon_color, 30)
flagged_hexagon.blit(flag, flag.get_rect(center=flagged_hexagon.get_rect().center))

hidden_hexagon = generate_hexagon(hidden_hexagon_color, 30)
hidden_hexagon_rect = hidden_hexagon.get_rect()

for y, row in enumerate(grid):
    for x, column in enumerate(row):
        if column == 1:
            hexagon = [hidden_hexagon, pygame.Rect(0, 0, hidden_hexagon_rect.width, hidden_hexagon_rect.height)]
            dist = 60
            hexagon[1].center = (90 + x * dist * math.sqrt(3) / 2, 200 + y * dist - x * dist / 2)
            hexagon += [0, False, False]
            hexagons.append(hexagon)
        else:
            hexagons.append(None)


background_hexagon = generate_hexagon(background_hexagon_color, 345, 90, True)
background_hexagon = pygame.transform.rotate(background_hexagon, 90)

background_hexagon_center = background_hexagon.get_rect().center
background_hexagon_center = (width / 2 - background_hexagon_center[0], height / 2 - background_hexagon_center[1])

def mouse_clicked(pos, flag):
    closest = math.inf
    final_index = None
    for index, hexagon in enumerate(hexagons):
        if hexagon:
            rect = hexagon[1]
            if rect.collidepoint(pos):
                point = rect.center

                point_x = point[0]
                point_y = point[1]

                mouse_x = pos[0]
                mouse_y = pos[1]

                x_power = (point_x - mouse_x) * (point_x - mouse_x)
                y_power = (point_y - mouse_y) * (point_y - mouse_y)

                distance = math.sqrt(x_power + y_power)

                if distance < closest:
                    closest = distance
                    final_index = index

    if final_index is not None:
        if flag:
            flagged(final_index)
        else:
            uncover_hex(final_index)


def flagged(index):
    global mines_placed
    global flags_used

    hexagon = hexagons[index]

    if hexagon[3]:
        return


    if not hexagon[4] and flags_used < mines_placed:
        hexagon[4] = True
        flags_used += 1
        hexagon[0] = flagged_hexagon
        check_win()
    elif hexagon[4]:
        hexagon[4] = False
        flags_used -= 1
        hexagon[0] = hidden_hexagon


def check_win():
    global mines_placed
    correct = 0
    for hexagon in hexagons:
        if hexagon:
            if hexagon[2] == "mine" and hexagon[4] == True:
                correct += 1


    if correct == mines_placed:
        global won
        won = True


def get_neighbours(index):
    neighbours = [
        index - 1 - grid_width,
        index - grid_width,
        index - 1,
        index + 1,
        index + grid_width,
        index + 1 + grid_width
    ]

    final_list = []

    for neighbour in neighbours:
        y = neighbour // grid_width
        if not y < 0 and len(hexagons) > neighbour:
            final_list.append(neighbour)

    return final_list


def draw_mine_number():
    global flags_used, mines_placed
    nr = mines_placed - flags_used
    nr = str(nr)
    for i, num in enumerate(nr):
        window.blit(numbers_list[int(num)], (20 * i, 0))


def draw():
    window.fill(background_color)
    window.blit(background_hexagon, background_hexagon_center)
    window.blit(restart_surface, restart_surface.get_rect(center=restart_rect.center))

    draw_mine_number()

    for hexagon in hexagons:
        if hexagon:
            rect = hexagon[1]
            window.blit(hexagon[0], rect)

    global lost, won
    if lost:
        window.blit(lost_text, lost_text.get_rect(center=(width / 2, lost_text.get_height() / 2)))
    elif won:
        window.blit(won_text, won_text.get_rect(center=(width / 2, won_text.get_height() / 2)))

    pygame.display.update()


def add_mines(final_amount):
    no_no_zone = [4, 5, 16, 17]
    loop = True
    mines = 0
    while loop:
        index = random.randint(0, grid_width * len(grid) - 1)
        if index in no_no_zone:
            ...
        elif hexagons[index]:
            if hexagons[index][2] != "mine":
                mines += 1
                hexagons[index][2] = "mine"
                neighbours = get_neighbours(index)
                for x in neighbours:
                    cell = hexagons[x]
                    if cell:
                        if isinstance(cell[2], int):
                            cell[2] += 1

        if mines == final_amount:
            loop = False


def color_hexagons():
    for hexagon in hexagons:
        if hexagon:
            if hexagon[2] == "mine":
                hexagon[0] = generate_hexagon((255, 0, 0), 30)
            else:
                intensity = 255 - hexagon[2] * 60
                intensity = max(0, intensity)
                hexagon[0] = generate_hexagon((intensity, intensity, intensity), 30)


def uncover_hex(index):
    hexagon = hexagons[index]

    if not hexagon:
        return

    if hexagon[3] or hexagon[4]:
        return

    hexagon[3] = True

    if hexagon[2] == "mine":
        hexagon[0] = generate_hexagon(background_hexagon_color, 30)
        hexagon[0].blit(bomb, bomb.get_rect(center=hexagon[0].get_rect().center))
        global lost
        lost = True
        return
    else:
        hexagon[0] = generate_hexagon(uncovered_hexagon_color, 30)
        if hexagon[2] != 0:
            number = numbers_list[hexagon[2]]

            surface_center = hexagon[0].get_rect().center

            hexagon[0].blit(number, number.get_rect(center=surface_center))
        else:
            cells = get_neighbours(index)
            for i in cells:
                uncover_hex(i)


global restart_angle, restart_clicked
restart_angle = 0
restart_clicked = False

def check_reset():
    pos = pygame.mouse.get_pos()
    global restart, restart_angle, restart_surface, restart_clicked

    if restart_rect.collidepoint(pos):
        if pygame.mouse.get_pressed()[0] and not restart_clicked:
            restart_game()
            restart_clicked = True
        elif not pygame.mouse.get_pressed()[0]:
            restart_clicked = False

        if abs(restart_angle) < 85:
            restart_surface = pygame.transform.rotate(restart_surface, int((-90 - restart_angle) / 2))
            restart_angle += int((-90 - restart_angle) / 2)
        else:
            restart_surface = pygame.transform.rotate(restart, 90)
    else:
        restart_surface = pygame.transform.rotate(restart_surface, int((0 - restart_angle) / 2))
        restart_angle += int((0 - restart_angle) / 2)

        if abs(restart_angle) < 5:
            restart_surface = pygame.transform.rotate(restart, 0)


def restart_game():
    global mines_placed, flags_used, won, lost
    won = lost = False
    flags_used = 0
    for hexagon in hexagons:
        if hexagon:
            hexagon[0] = hidden_hexagon
            hexagon[2] = 0
            hexagon[3] = False
            hexagon[4] = False

    add_mines(mines_placed)


def main():
    mouse_down = False

    global mines_placed
    mines_placed = 17

    add_mines(mines_placed)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False


        if not (lost or won):
            if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
                if not mouse_down:
                    mouse_clicked(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[2])
                    mouse_down = True
            else:
                mouse_down = False

        check_reset()
        draw()


if __name__ == "__main__":
    main()