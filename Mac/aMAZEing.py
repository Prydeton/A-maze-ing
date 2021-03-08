#        __  __           ____________ _
#       |  \/  |   /\    |___  /  ____(_)
#   __ _| \  / |  /  \      / /| |__   _ _ __   __ _
#  / _` | |\/| | / /\ \    / / |  __| | | '_ \ / _` |
# | (_| | |  | |/ ____ \  / /__| |____| | | | | (_| |
#  \__,_|_|  |_/_/    \_\/_____|______|_|_| |_|\__, |
#                                               __/ |
#                                              |___/
# Created by Maxwell Reid 2019

import random
import pygame
import sys
import pygame.locals
import os
from time import sleep

pygame.init()

# Define global variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHTRED = (255, 69, 0)
FULLGREEN = (0, 255, 0)
GREEN = (34, 139, 34)
BLUE = (0, 0, 255)
LIGHTBLUE = (30, 144, 255)
GREY = (169, 169, 169)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (138, 43, 226)
width = 25
os.environ['SDL_VIDEO_CENTERED'] = "True"

# Defines removeWalls() function that is used to remove walls between two cells
# Takes current_cell
def removeWalls(current_cell: object, next_cell: object):
    # Checks which direction the next_cell is from the current_cell
    # and removes the two walls seperating them
    x = int(current_cell.x / width) - int(next_cell.x / width)
    y = int(current_cell.y / width) - int(next_cell.y / width)
    if x == -1:  # Right of current_cell
        current_cell.walls[1] = False
        next_cell.walls[3] = False
    elif x == 1:  # Left of current_cell
        current_cell.walls[3] = False
        next_cell.walls[1] = False
    elif y == -1:  # Down of current_cell
        current_cell.walls[2] = False
        next_cell.walls[0] = False
    elif y == 1:  # Uop of current_cell
        current_cell.walls[0] = False
        next_cell.walls[2] = False

# Defines PressedSkip() function that is used to wait until the user presses space
# before returning True
def pressedSkip():
    pygame.display.set_caption('Press SPACE to continue!')
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

# Defines readTime() function that is used to read the best time from a text file
def readTime(fileName: str):
    with open(os.getcwd() + "/" + fileName, "r") as file:
        contents = file.read()
        return contents.strip()

# Defines checkFinish() function that is used to check if the user has reached the end of the maze.
# Also will update the best time if the user is playing competative based on the existing scores
# If the user reaches the end of the maze
    # If the user is playing competative
        # Read the exisitng best time and compare to the current time and update if faster time
    # Wait for the user to press space until returning to menu
# Return False as the user hasn't reached the end
def checkFinish(x: int, y: int, rows: int, cols: int, competitive: bool, start_ticks: int, size: str="Not required"):
    if (x + 1) == rows and (y + 1) == cols:
        if competitive:
            attempt = ((pygame.time.get_ticks()-start_ticks)/1000)
            if size == "small":
                fileName = "smallBestTime.txt"
            elif size == "medium":
                fileName = "mediumBestTime.txt"
            elif size == "large":
                fileName = "largeBestTime.txt"
            record = readTime(fileName)
            if float(record) > float(attempt):
                with open(fileName, "w") as file:
                    file.write(str(attempt))
        return pressedSkip()
    else:
        return False

# Defines possible() function that is used to check if a directionis possible depending on the walls around a cell
# If the user is wanting to go up
    # Check the top wall of the current cell and the bottom wall of the above cell before returning True
# If the user is wanting to go right
    # Check the right wall of the current cell and the left wall of the right cell before returning True
# If the user is wanting to go down
    # Check the bottom wall of the current cell and the top wall of the down cell before returning True
# If the user is wanting to go left
    # Check the left wall of the current cell and the right wall of the left cell before returning True
# Otherwise return False
def possible(direction: str, x: int, y: int, grid: list):
    if direction == "Up" and grid[x][y].walls[0] is False and grid[x - 1][y].visited is False:
        return True
    elif direction == "Right" and grid[x][y].walls[1] is False and grid[x][y + 1].visited is False:
        return True
    elif direction == "Down" and grid[x][y].walls[2] is False and grid[x + 1][y].visited is False:
        return True
    elif direction == "Left" and grid[x][y].walls[3] is False and grid[x][y - 1].visited is False:
        return True
    else:
        return False

# Defines resetVisited() which is used to loop through each of the cells and set their 'visited' property to False
# and colours them white
def resetVisited(rows: int, cols: int, grid: list, screen: object):
    for y in range(rows):
        for x in range(cols):
            grid[x][y].visited = False
            grid[x][y].draw(screen)

# Defines revealPath() which is used to reveal the optimal path once the maze has been solved automatically
# For each of the instructions in the last item of the path list
    # Modify the x or y co-ordinate depending on the instruction
    # Set the 'path' property of current cell to True
    # Draws the cell to reveal the path
def revealPath(path: list, grid: list):
    x = 0
    y = 0
    for direction in path[-1]:
        if direction == "Up":
            x = x - 1
        elif direction == "Right":
            y = y + 1
        elif direction == "Down":
            x = x + 1
        elif direction == "Left":
            y = y - 1
        current_cell = grid[x][y]
        current_cell.path = True
        current_cell.visited = False
        current_cell.current = False
        current_cell.draw(screen, direction)
        pygame.display.update()

# Defines textObjects() function that is used to get the perimters of a given text
def textObjects(text: str, font: str):
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# Defines button() which is used to create buttons on the screen given peramiters
# and returns true when the button has been clicked
def button(display_surface: object, msg: str, x: int, y: int, w: int, h: int, ic: int, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    pygame.draw.rect(display_surface, ic, (x, y, w, h))
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        if click[0] == 1 and action is not None:
            return action()
    subText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = textObjects(msg, subText)
    textRect.center = ((x+(w/2)), (y+(h/2)))
    display_surface.blit(textSurf, textRect)

# Defines returnTrue() which is used within the button function to return True when the button is pressed
def returnTrue():
    return True

# Defines menu() which is used to render the menu including buttons and labels
# and returns peramiters based on the selected options which dictate which mode function is selected
# and which size is passed too the function
def menu():
    menuX = 600
    menuY = 400
    x = ""
    y = ""
    size = ""
    mode = ""
    go = False
    display_surface = pygame.display.set_mode((menuX, menuY))
    pygame.display.set_caption('Maze')
    titleFont = pygame.font.Font('freesansbold.ttf', 32)
    subHeadingFont = pygame.font.Font('freesansbold.ttf', 20)
    titleLbl = titleFont.render('Maze Solver/Generator', True, BLACK, WHITE)
    sizeLbl = subHeadingFont.render('Select Maze Size', True, BLACK, WHITE)
    modeLbl = subHeadingFont.render('Select Solving Method', True, BLACK, WHITE)
    smallBestTimeLbl = subHeadingFont.render('Small Best Time: ' + readTime("smallBestTime.txt"), True, BLACK, WHITE)
    mediumBestTimeLbl = subHeadingFont.render('Medium Best Time: ' + readTime("mediumBestTime.txt"), True, BLACK, WHITE)
    largeBestTimeLbl = subHeadingFont.render('Large Best Time: ' + readTime("largeBestTime.txt"), True, BLACK, WHITE)
    titleTextRect = titleLbl.get_rect()
    sizeTextRect = sizeLbl.get_rect()
    modeTextRect = modeLbl.get_rect()
    smallTextRect = smallBestTimeLbl.get_rect()
    mediumTextRect = mediumBestTimeLbl.get_rect()
    largeTextRect = largeBestTimeLbl.get_rect()
    titleTextRect.center = (menuX // 2, 35)
    sizeTextRect.center = (menuX // 2, 90)
    modeTextRect.center = (menuX // 2, 200)
    smallTextRect.center = (2 * menuX // 3, 300)
    mediumTextRect.center = (2 * menuX // 3, 325)
    largeTextRect.center = (2 * menuX // 3, 350)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            display_surface.fill(WHITE)
            display_surface.blit(titleLbl, titleTextRect)
            display_surface.blit(sizeLbl, sizeTextRect)
            display_surface.blit(modeLbl, modeTextRect)
            display_surface.blit(smallBestTimeLbl, smallTextRect)
            display_surface.blit(mediumBestTimeLbl, mediumTextRect)
            display_surface.blit(largeBestTimeLbl, largeTextRect)

            if size == "small":
                small = button(display_surface, "Small", menuX // 5 - 50, 110, 130, 50, GREEN, returnTrue)
            else:
                small = button(display_surface, "Small", menuX // 5 - 50, 110, 130, 50, LIGHTBLUE, returnTrue)

            if size == "medium":
                medium = button(display_surface, "Medium", 2 * menuX // 5, 110, 130, 50, GREEN, returnTrue)
            else:
                medium = button(display_surface, "Medium", 2 * menuX // 5, 110, 130, 50, LIGHTBLUE, returnTrue)

            if size == "large":
                large = button(display_surface, "Large", 3 * menuX // 5 + 50, 110, 130, 50, GREEN, returnTrue)
            else:
                large = button(display_surface, "Large", 3 * menuX // 5 + 50, 110, 130, 50, LIGHTBLUE, returnTrue)

            if mode == "auto":
                auto = button(display_surface, "Automatic", menuX // 5 - 50, 220, 130, 50, GREEN, returnTrue)
            else:
                auto = button(display_surface, "Automatic", menuX // 5 - 50, 220, 130, 50, LIGHTBLUE, returnTrue)

            if mode == "manual":
                manual = button(display_surface, "Manual", 2 * menuX // 5, 220, 130, 50, GREEN, returnTrue)
            else:
                manual = button(display_surface, "Manual", 2 * menuX // 5, 220, 130, 50, LIGHTBLUE, returnTrue)

            if mode == "competitive":
                competitive = button(display_surface, "Competitive", 3 * menuX // 5 + 50, 220, 130, 50, GREEN, returnTrue)
            else:
                competitive = button(display_surface, "Competitive", 3 * menuX // 5 + 50, 220, 130, 50, LIGHTBLUE, returnTrue)

            if small:
                size = "small"
                x = 300
                y = 300
            elif medium:
                size = "medium"
                x = 600
                y = 600
            elif large:
                size = "large"
                x = 1000
                y = 1000

            if auto:
                mode = "auto"
            elif manual:
                mode = "manual"
            elif competitive:
                mode = "competitive"

            if mode != "" and size != "":
                go = button(display_surface, "Go!", 100, 300, 100, 50, GREEN, returnTrue)
            else:
                button(display_surface, "Go!", 100, 300, 100, 50, GREY, returnTrue)

            if go:
                return mode, x, y, size

            pygame.display.update()

# Defines generate() function which is used to generate the maze based on a given size.
def generate(maze_width: int, maze_height: int):
    size = (int(maze_width), int(maze_height))
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maze')
    done = False
    cols = int(size[0] / width)  # Defines number of columns
    rows = int(size[1] / width)  # Defines number of rows
    stack = []
    grid = []

    for y in range(rows):
        grid.append([])
        for x in range(cols):
            grid[y].append(Cell(x, y))

    current_cell = grid[0][0]
    next_cell = 0
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        screen.fill(WHITE)
        current_cell.visited = True
        current_cell.current = True

        for y in range(rows):
            for x in range(cols):
                grid[y][x].draw(screen)

        # Randomly selects the next cell based on which cells in the neighbores havn't been visited
        next_cell = current_cell.checkNeighbors(rows, cols, grid, screen)
        if next_cell:  # If atleast one of the neighbores hasnt been visited yet
            current_cell.neighbors = []

            stack.append(current_cell)

            removeWalls(current_cell, next_cell)

            current_cell.current = False

            current_cell = next_cell

            if current_cell == grid[rows-1][cols-1]:
                current_cell.end = True

            current_cell.draw(screen)

        elif len(stack) > 0:
            current_cell.current = False
            current_cell = stack.pop()

        elif len(stack) == 0:
            done = True
        pygame.display.update()
    return rows, cols, grid, screen

# Defines autoSolve() which is used to solve the generated maze
# ALGORITHM
# Pop the first item from a path list
# Loop through 'Up', 'Down', 'Left', 'Right'
    # Append the direction to the first item
    # Loop though each of the directions in the path
    # Check if each direction is valid marking each cell as marked
        # If all the directions are valid, append the new path to the end of the path list
        # If any of the directions are not valid, move on to the next option
    # Check if the end has been reached
def autoSolve(rows: int, cols: int, grid: list, screen: object):
    solved = False
    path = []
    first = ""
    finished = False
    while not solved:
        if len(path) >= 1:
            first = path.pop(0)
        for option in [["Up"], ["Right"], ["Down"], ["Left"]]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    solved = True
                    pygame.quit()
                    break
            resetVisited(rows, cols, grid, screen)
            x = 0
            y = 0
            grid[0][0].visited = True
            current = []
            if solved:
                break
            if first != "":
                current += first
            current += option
            valid = True
            for direction in current:
                if direction == "Up" and possible(direction, x, y, grid):
                    x = x - 1
                elif direction == "Right" and possible(direction, x, y, grid):
                    y = y + 1
                elif direction == "Down" and possible(direction, x, y, grid):
                    x = x + 1
                elif direction == "Left" and possible(direction, x, y, grid):
                    y = y - 1
                else:
                    valid = False
                current_cell = grid[x][y]
                current_cell.visited = True
                if current_cell.end:
                    solved = True
            if valid and not finished:
                path.append(current)
                current_cell.current = True
                current_cell.draw(screen)
                pygame.display.update()
            if current_cell == grid[rows-1][cols-1]:
                finshed = True
    for y in range(rows):
        for x in range(cols):
            current_cell = grid[x][y]
            current_cell.current = False
            current_cell.visited = True
            current_cell.draw(screen)
            pygame.display.update()
    print(path)
    revealPath(path, grid)
    solved = checkFinish(x, y, rows, cols, False, 0)

# Defines manualSolve() which is used for when the user wishes to solve the maze manually
# Loops through the following until the maze has been solved
    # Checks if W Key has been pressed and if there is no wall stopping it from moving
        # If so: Increment x by -1
    # Checks if A Key has been pressed and if there is no wall stopping it from moving
        # If so: Increment y by -1
    # Checks if S Key has been pressed and if there is no wall stopping it from moving
        # If so: Increment x by 1
    # Checks if D Key has been pressed and if there is no wall stopping it from moving
        # If so: Increment y by 1
    # Checks if the maze has been solved
        # If so: Updates fastest time etc
def manualSolve(rows: int, cols: int, grid: list, screen: object, competative: bool, size: str):
    solved = False
    x = 0
    y = 0
    move_count = 0
    current_cell = grid[x][y]
    start_ticks = pygame.time.get_ticks()

    while not solved:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                solved = True
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                move_count += 1
                current_cell.current = False
                current_cell.draw(screen)
                if event.key == pygame.K_s:
                    if not current_cell.walls[2]:
                        x += 1

                elif event.key == pygame.K_a:
                    if not current_cell.walls[3]:
                        y -= 1

                elif event.key == pygame.K_w:
                    if not current_cell.walls[0]:
                        x -= 1

                elif event.key == pygame.K_d:
                    if not current_cell.walls[1]:
                        y += 1
                current_cell = grid[x][y]
                current_cell.current = True
                current_cell.draw(screen)
                pygame.display.update()
                solved = checkFinish(x, y, rows, cols, competative, start_ticks, size)


# Cell class used for each of the cells in the maze
# Used when refering to the properties of each square of the maze
class Cell():

    # Defines __init__() which sets the initial conditions of each cell
    def __init__(self: object, x: int, y: int):
        global width
        self.x = x * width
        self.y = y * width

        self.visited = False
        self.current = False
        self.end = False
        self.path = False

        self.walls = [True, True, True, True]  # Top, Right, Bottom, Left

        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    # Defines draw() function which checks the property of a cell and colours in correctly as well as the walls.
    def draw(self: object, screen: object, direction: str="No Direction"):
        if self.current:
            pygame.draw.rect(screen, RED, (self.x, self.y, width, width))
        elif self.visited and not self.end:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, width, width))
        elif self.end:
            pygame.draw.rect(screen, BLUE, (self.x, self.y, width, width))
        elif self.path:
            if direction == "Up":
                pygame.draw.rect(screen, PURPLE, (self.x + 5, self.y + 5, width - 10, width - 0))
            elif direction == "Down":
                pygame.draw.rect(screen, PURPLE, (self.x + 5, self.y - 5, width - 10, width - 0))
            elif direction == "Right":
                pygame.draw.rect(screen, PURPLE, (self.x - 5, self.y + 5, width - 0, width - 10))
            elif direction == "Left":
                pygame.draw.rect(screen, PURPLE, (self.x + 5, self.y + 5, width - 0, width - 10))

        if self.walls[0]:
            pygame.draw.line(screen, BLACK, (self.x, self.y),
                ((self.x + width), self.y), 1)  # Top wall
        if self.walls[1]:
            pygame.draw.line(screen, BLACK, ((self.x + width), self.y),
                ((self.x + width), (self.y + width)), 1)  # Right Wall
        if self.walls[2]:
            pygame.draw.line(screen, BLACK,
                ((self.x + width), (self.y + width)), (self.x, (self.y + width)), 1)  # Bottom Wall
        if self.walls[3]:
            pygame.draw.line(screen, BLACK, (self.x, (self.y + width)),
            (self.x, self.y), 1)  # Left Wall

    # Defines checkNeighbors() which is used to assign neighbores to the cell
    # If the neighboure is past the bounds of the grid it is not assigned to the cell
    def checkNeighbors(self: object, rows: int, cols: int, grid: list, screen: object):
        if int(self.y / width) - 1 >= 0:
            self.top = grid[int(self.y / width) - 1][int(self.x / width)]
        if int(self.x / width) + 1 <= cols - 1:
            self.right = grid[int(self.y / width)][int(self.x / width) + 1]
        if int(self.y / width) + 1 <= rows - 1:
            self.bottom = grid[int(self.y / width) + 1][int(self.x / width)]
        if int(self.x / width) - 1 >= 0:
            self.left = grid[int(self.y / width)][int(self.x / width) - 1]

        # Checks which sides have been visited, if the side has been visited its value is appended
        if self.top != 0:
            if not self.top.visited:
                self.neighbors.append(self.top)
        if self.right != 0:
            if not self.right.visited:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if not self.bottom.visited:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if not self.left.visited:
                self.neighbors.append(self.left)

        # If there is atleast 1 neighbour randomly select a neightbour else makes the cell backtrack
        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(
                0, len(self.neighbors))]
            return self.next_cell
        else:
            pygame.draw.rect(screen, GREEN, (self.x, self.y, width, width))
            return False

if __name__ == "__main__":
    while True:
        mode, x, y, size = menu()
        rows, cols, grid, screen = generate(x, y)
        if mode == "auto":
            autoSolve(rows, cols, grid, screen)
        elif mode == "manual":
            manualSolve(rows, cols, grid, screen, False, size)
        elif mode == "competitive":
            manualSolve(rows, cols, grid, screen, True, size)