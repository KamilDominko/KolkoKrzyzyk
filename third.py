import pygame as pg
import sys, random

RED = (255, 000, 000)
GREEN = (000, 255, 000)
BLACK = (000, 000, 000)
WHITE = (255, 255, 255)

winnning_condictions = [[1, 1, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 1, 1, 1, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 1, 1, 1],
                        [1, 0, 0, 1, 0, 0, 1, 0, 0],
                        [0, 1, 0, 0, 1, 0, 0, 1, 0],
                        [0, 0, 1, 0, 0, 1, 0, 0, 1],
                        [1, 0, 0, 0, 1, 0, 0, 0, 1],
                        [0, 0, 1, 0, 1, 0, 1, 0, 0]]

win_con = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class Box:
    number = 0

    def __init__(self, x, y, width, height):
        self.rect = pg.Rect(x, y, width, height)
        self.color = BLACK
        self.token = None
        self.number = Box.number
        self.available = True
        Box.number += 1

    def set_token(self, xo):
        if self.available:
            self.token = xo
            self.available = False

    def reset(self):
        self.token = None
        self.available = True

    def draw(self, surface):
        if self.token == "X":
            pg.draw.line(surface, self.color, self.rect.topleft, self.rect.bottomright, 4)
            pg.draw.line(surface, self.color, self.rect.topright, self.rect.bottomleft, 4)
        elif self.token == "O":
            pg.draw.ellipse(surface, self.color, self.rect, 4)
        else:
            pass


class Program:
    def __init__(self):
        self.win_line = False
        self.p1 = None
        self.p2 = None
        self.clock = pg.time.Clock()
        self.FPS = 59
        self.screen_width = 960
        self.screen_height = 960
        self.running = False
        self.state = ""
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height))
        pg.display.set_caption("Kolko i Krzyzyk")
        self.game_font = None

        self.boxes = self.create_boxes()
        self.token = None
        self.player_token = None
        self.enemy_token = None
        self.winner = None
        self.prepare_game()

    def prepare_game(self):
        for box in self.boxes:
            box.reset()
        self.win_line = False
        self.p1 = None
        self.p2 = None
        self.winner = None
        self.token = random.choice(("O", "X"))
        self.player_token = random.choice(("O", "X"))
        if self.player_token == "O":
            self.enemy_token = "X"
        elif self.player_token == "X":
            self.enemy_token = "O"

    def change_token(self):
        if self.token == "O":
            self.token = "X"
        elif self.token == "X":
            self.token = "O"

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1 and self.state == "play":
                    self.check_collision(self.boxes, 1)
                if event.button == 1 and self.state == "reset":
                    self.prepare_game()
                    self.state = "play"
                if event.button == 3:
                    self.check_collision(self.boxes, 3)

    def draw_bg(self):
        self.screen.fill(WHITE)

    def create_lines(self):
        x = self.screen_width // 3
        y = self.screen_height // 3
        vertical_pnt1 = (x, 0)
        vertical_pnt2 = (x, self.screen_height)
        vertical_pnt3 = (2 * x, 0)
        vertical_pnt4 = (2 * x, self.screen_height)
        horizontal_pnt1 = (0, y)
        horizontal_pnt2 = (self.screen_width, y)
        horizontal_pnt3 = (0, y * 2)
        horizontal_pnt4 = (self.screen_width, y * 2)
        lines_points = []
        lines_points.append((vertical_pnt1, vertical_pnt2))
        lines_points.append((vertical_pnt3, vertical_pnt4))
        lines_points.append((horizontal_pnt1, horizontal_pnt2))
        lines_points.append((horizontal_pnt3, horizontal_pnt4))
        return lines_points

    def draw_lines(self, lines_points):
        for line in lines_points:
            pg.draw.line(self.screen, BLACK, line[0], line[1], 4)

    def create_boxes(self):
        x = self.screen_width / 3
        y = self.screen_height / 3
        boxes = []

        for i in range(3):
            for j in range(3):
                box = Box(j * x + 1 * j, i * y, x, y)
                boxes.append(box)
        return boxes

    def check_collision(self, boxes, mouse_btn):
        mouse_pos = pg.mouse.get_pos()
        for box in boxes:
            if box.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                if mouse_btn == 1:
                    if box.available:
                        box.set_token(self.player_token)
                        self.check_winner(self.player_token)
                        self.change_token()
                # elif mouse_btn == 3:
                # box.token = "O"
                # box.color = (000, 000, 255)

    def draw_boxes(self):
        for box in self.boxes:
            box.draw(self.screen)

    def enemy_move(self):
        available_moves = self.get_available_moves()
        moved = False
        if not moved:
            for move in available_moves:
                predict_move = self.get_yours_moves(self.enemy_token)
                predict_move[move] = 1

                for i in win_con:
                    ar = []
                    for j in range(3):
                        ar.append(predict_move[i[j]])
                    if ar == [1, 1, 1] and not moved:
                        self.boxes[move].set_token(self.enemy_token)
                        moved = True
                        break
        if not moved:
            for move in available_moves:
                predict_move = self.get_yours_moves(self.player_token)
                predict_move[move] = 1

                for i in win_con:
                    ar = []
                    for j in range(3):
                        ar.append(predict_move[i[j]])
                    if ar == [1, 1, 1] and not moved:
                        self.boxes[move].set_token(self.enemy_token)
                        moved = True
                        break
        if not moved:
            if len(available_moves) > 0:
                random_move = random.choice(available_moves)
                self.boxes[random_move].set_token(self.enemy_token)
                moved = True
            else:
                print("nie")

    def get_available_moves(self):
        available_moves = []
        for box in self.boxes:
            if box.available:
                available_moves.append(box.number)
        return available_moves

    def get_yours_moves(self, token):
        your_moves = []
        for box in self.boxes:
            if box.token == token:
                your_moves.append(1)
            else:
                your_moves.append(0)
        return your_moves

    def draw_boxes_no(self):
        for box in self.boxes:
            text = self.game_font.render(f"{box.number}", True, RED)
            x = box.rect.centerx - text.get_rect().width / 2
            y = box.rect.centery - text.get_rect().height / 2
            self.screen.blit(text, (x, y))

    def draw_win(self):
        self.game_font = pg.font.Font("freesansbold.ttf", 62)
        text = self.game_font.render(f"{self.winner} HAS WON", True, GREEN)
        x = self.screen_width / 2 - text.get_rect().width / 2
        y = self.screen_height / 2 - text.get_rect().height / 2
        self.screen.blit(text, (x, y))

    def check_winner(self, token):
        current_moves = self.get_yours_moves(token)

        for i in win_con:
            ar = []
            for j in range(3):
                ar.append(current_moves[i[j]])
            if ar == [1, 1, 1]:
                self.p1 = self.boxes[i[0]].rect.center
                self.p2 = self.boxes[i[2]].rect.center
                self.win_line = True
                self.winner = token
                self.state = "reset"

        available_moves = self.get_available_moves()
        if len(available_moves) == 0:
            self.winner = "draft"



    def start(self):
        pg.init()
        self.game_font = pg.font.Font("freesansbold.ttf", 62)
        lines_points = self.create_lines()
        self.running = True
        self.state = "play"
        while self.running:
            if self.token == self.player_token:
                self.check_events()
            elif self.token != self.player_token:
                self.enemy_move()
                self.check_winner(self.enemy_token)
                self.change_token()

            # DRAWING
            self.draw_bg()
            self.draw_boxes()
            self.draw_lines(lines_points)
            if self.win_line:
                pg.draw.line(self.screen, RED, self.p1, self.p2, 8)
                self.draw_win()
            if self.winner == "draft":
                self.state = "reset"
            # self.draw_boxes_no()

            pg.display.flip()
            self.clock.tick(self.FPS)


gra = Program()
gra.start()
