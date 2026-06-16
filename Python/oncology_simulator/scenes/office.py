import pygame
from scenes.base import *


class OfficeScene:
    def __init__(self, screen):
        self.screen = screen
        self.W, self.H = screen.get_size()

        self.font_title = pygame.font.SysFont('segoeui', 32, bold=True)
        self.font_body  = pygame.font.SysFont('segoeui', 18)
        self.font_btn   = pygame.font.SysFont('segoeui', 20, bold=True)

        self.btn_waiting = Button(
            rect=(self.W - 225, self.H - 110, 185, 50),
            text="Enter Clinic  \u2192",
            font=self.font_btn,
        )

    def handle_event(self, event):
        if self.btn_waiting.is_clicked(event):
            from scenes.world import WorldScene
            return WorldScene(self.screen)
        return None

    def update(self, dt):
        pass

    def draw(self):
        # Walls
        self.screen.fill(OFFICE_WALL)

        # Floor
        pygame.draw.rect(self.screen, OFFICE_FLOOR,
                         (0, int(self.H * 0.62), self.W, self.H))

        # Desk surface
        desk = pygame.Rect(self.W // 2 - 210, int(self.H * 0.52), 420, 75)
        pygame.draw.rect(self.screen, DESK_COLOR, desk, border_radius=6)
        # Desk front panel
        pygame.draw.rect(self.screen, (75, 46, 18),
                         (desk.x + 10, desk.bottom - 18, desk.width - 20, 18),
                         border_radius=4)

        # Window (back wall)
        win = pygame.Rect(80, 80, 210, 185)
        pygame.draw.rect(self.screen, (135, 206, 235), win)
        pygame.draw.rect(self.screen, (100, 78, 48), win, 6)
        pygame.draw.line(self.screen, (100, 78, 48), (80, 172), (290, 172), 4)
        pygame.draw.line(self.screen, (100, 78, 48), (185, 80), (185, 265), 4)

        # Bookshelf (back wall, right)
        shelf = pygame.Rect(self.W - 170, 75, 130, 210)
        pygame.draw.rect(self.screen, (120, 88, 48), shelf)
        book_cols = [(210, 50, 50), (50, 100, 200), (50, 175, 80),
                     (220, 175, 50), (150, 50, 200), (200, 120, 50)]
        for i, c in enumerate(book_cols):
            pygame.draw.rect(self.screen, c,
                             (shelf.x + 8 + i * 19, shelf.y + 10, 15, 85),
                             border_radius=2)

        # Door (right wall)
        door = pygame.Rect(self.W - 155, int(self.H * 0.32), 105, 175)
        pygame.draw.rect(self.screen, (140, 100, 58), door, border_radius=4)
        pygame.draw.rect(self.screen, (80, 54, 24), door, 3, border_radius=4)
        pygame.draw.circle(self.screen, (218, 178, 50),
                           (door.x + 18, door.centery + 10), 7)

        # "Clinic" label above door
        lbl = self.font_body.render("Clinic", True, HEADER_COL)
        self.screen.blit(lbl, (self.W - 158, door.bottom + 8))

        # Title
        title = self.font_title.render("Your Office", True, HEADER_COL)
        self.screen.blit(title, (30, 22))

        self.btn_waiting.draw(self.screen)
