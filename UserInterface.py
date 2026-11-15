# Imports
import sys
import pygame
import numpy as np

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 20)

objects = []


class Button():
    def __init__(self, x, y, width, height, buttonText='Button',
                 onclickFunction=lambda *args: None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])

        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()          # fires every frame while held
                elif not self.alreadyPressed:
                    self.onclickFunction()          # fires once per click
                    self.alreadyPressed = True
            else:
                self.buttonSurface.fill(self.fillColors['normal'])
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)
        
class Toggle:
    def __init__(self, x, y, width, height, buttonText='Toggle'):
        self.state = False          
        self.held = False           
        self.hovered = False

        self.fillColors = {
            'normal':  '#ffffff',
            'hover':   '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((width, height))
        self.buttonRect = pygame.Rect(x, y, width, height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        self.buttonSurfRect = self.buttonSurf.get_rect()

        objects.append(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.buttonRect.collidepoint(event.pos):
                self.held = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.held and self.buttonRect.collidepoint(event.pos):
                self.state = not self.state   # toggle only on valid click
            self.held = False

    def process(self):
        self.hovered = self.buttonRect.collidepoint(pygame.mouse.get_pos())

        if self.held:
            color = self.fillColors['pressed']
        elif self.hovered:
            color = self.fillColors['hover']
        else:
            color = self.fillColors['normal']

        self.buttonSurface.fill(color)
        self.buttonSurface.blit(
            self.buttonSurf,
            self.buttonSurfRect.move(
                (self.buttonRect.width  - self.buttonSurfRect.width)  // 2,
                (self.buttonRect.height - self.buttonSurfRect.height) // 2,
            ),
        )
        screen.blit(self.buttonSurface, self.buttonRect)

class TextBox():
    def __init__(self, x, y, width, height, numeric=True, defaultText=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.numeric = numeric
        self.text = defaultText
        self.active = False
        self.maxChars = 12

        self.textRect = pygame.Rect(x, y, width, height)
        self.textSurface = pygame.Surface((width, height))

        objects.append(self)

    # ---- event handling -------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # click inside -> focus, click outside -> unfocus
            self.active = self.textRect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.active = False
            elif event.key == pygame.K_ESCAPE:
                self.text = ''
                self.active = False
            else:
                char = event.unicode
                if char and len(self.text) < self.maxChars and self._is_valid(char):
                    self.text += char

    def _is_valid(self, char):
        if not self.numeric:
            return char.isprintable()
        if char.isdigit():
            return True
        if char in '+-' and self.text == '':       # sign only at the start
            return True
        if char == '.' and '.' not in self.text:   # one decimal point
            return True
        return False

    # ---- value access ---------------------------------------------------
    def get_value(self, default=0):
        try:
            return float(self.text)
        except ValueError:          # empty box or just "-" or "."
            return default

    # ---- drawing --------------------------------------------------------
    def process(self):
        self.textSurface.fill((255, 255, 255))
        border = (0, 120, 215) if self.active else (0, 0, 0)
        pygame.draw.rect(self.textSurface, border, self.textSurface.get_rect(), 2)

        textSurf = font.render(self.text, True, (20, 20, 20))

        # clip so long input doesn't spill out of the box
        self.textSurface.set_clip(pygame.Rect(4, 0, self.width - 8, self.height))
        self.textSurface.blit(textSurf, (6, self.height/2 - textSurf.get_height()/2))

        # blinking caret
        if self.active and (pygame.time.get_ticks() // 500) % 2 == 0:
            cx = 6 + textSurf.get_width()
            pygame.draw.line(self.textSurface, (20, 20, 20),
                             (cx, 10), (cx, self.height - 10), 2)
        self.textSurface.set_clip(None)

        screen.blit(self.textSurface, self.textRect)


class InteractiveMatrix:
    def __init__(self, x, y, size, matrix=None):
        if matrix is None:
            matrix = np.zeros((3, 3))
        self.x, self.y = x, y
        self.matrix = matrix

        unit = size / 8
        self.TextBoxes = np.empty((3, 3), dtype=object)
        for i in range(3):
            for j in range(3):
                self.TextBoxes[i, j] = TextBox(
                    x + j * 3 * unit,
                    y + i * 3 * unit,
                    2 * unit, 2 * unit,
                    defaultText=str(matrix[i, j]),
                )

        self.Button = Button(x + 1 * unit, y + 9 * unit,
                             6 * unit, 2 * unit,
                             'Commit', self.commit)

    def commit(self):                      # real method, reachable as self.commit
        for i in range(3):
            for j in range(3):
                self.matrix[i, j] = self.TextBoxes[i, j].get_value()

        print(self.matrix)

    def handle_event(self, event):
        for i in range(3):
            for j in range(3):
                self.TextBoxes[i, j].handle_event(event)

    def process(self):
        for i in range(3):
            for j in range(3):
                self.TextBoxes[i, j].process()
        self.Button.process()

