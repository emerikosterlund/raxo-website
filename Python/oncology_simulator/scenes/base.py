import pygame

# --- Colours ---
BG           = (245, 245, 240)
OFFICE_WALL  = (210, 195, 170)
OFFICE_FLOOR = (180, 160, 130)
DESK_COLOR   = (101, 67, 33)
BLUE         = (41, 128, 185)
BLUE_DARK    = (31, 97, 141)
GREEN        = (39, 174, 96)
GREEN_DARK   = (30, 132, 73)
RED          = (231, 76, 60)
RED_DARK     = (192, 57, 43)
WHITE        = (255, 255, 255)
TEXT         = (30, 30, 30)
HEADER_COL   = (52, 73, 94)
PANEL_BORDER = (200, 200, 200)
GRAY         = (150, 150, 150)
LIGHT_GRAY   = (230, 230, 230)
SELECTED     = (52, 152, 219)
CORRECT_BG   = (212, 237, 218)
WRONG_BG     = (248, 215, 218)


def wrap_text(text, font, max_width):
    words = text.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        if font.size(test)[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines


class Button:
    def __init__(self, rect, text, color=None, hover_color=None,
                 text_color=WHITE, font=None):
        self.rect       = pygame.Rect(rect)
        self.text       = text
        self.color      = color or BLUE
        self.hover_color = hover_color or BLUE_DARK
        self.text_color = text_color
        self.font       = font

    def draw(self, surface):
        mouse = pygame.mouse.get_pos()
        col = self.hover_color if self.rect.collidepoint(mouse) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        surf = self.font.render(self.text, True, self.text_color)
        surface.blit(surf, surf.get_rect(center=self.rect.center))

    def is_clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))
