import pygame
from scenes.base import *
from data.cases import CASES

# World dimensions
WORLD_W      = 1400
WORLD_H      = 700
PLAYER_SPEED = 180   # px / sec
PLAYER_R     = 10    # half-size; player is 20x20
WALL_T       = 20

# Extra colours for world
C_FLOOR_OFF  = (218, 203, 178)
C_FLOOR_HALL = (200, 200, 192)
C_FLOOR_WAIT = (198, 213, 226)
C_FLOOR_EXAM = (210, 225, 210)   # exam room floor (light mint)
C_WALL_COL   = (68,  57,  46)
C_DESK_L     = (130, 90,  46)
C_PATIENT    = (192, 57,  43)
C_CHAIR      = (175, 135, 95)
C_LABEL_COL  = (110, 95,  80)
C_SKIN       = (240, 200, 168)
C_SKIN_DARK  = (200, 158, 128)
C_EXAM_TABLE = (220, 220, 215)   # exam table surface

# Shirt colour per patient slot (cycles if more patients than entries)
PATIENT_SHIRTS = [
    (70,  130, 180),   # steel blue
    (100, 155, 100),   # sage green
    (180, 115,  75),   # terracotta
    (140,  80, 160),   # purple
]

# Layout constants
CORRIDOR_Y1  = 300   # corridor top
CORRIDOR_Y2  = 420   # corridor bottom
EXAM_ROOM_W  = 200   # width of each exam room
N_EXAM_ROOMS = 4
EXAM_X0      = 580   # x start of exam/corridor/waiting section


def _draw_person(surface, cx, cy, shirt, scale=1.0, hair_col=None):
    """Bird's-eye person: large head dominates, small shirt shoulders below."""
    hr  = max(5, int(12 * scale))
    bw  = max(4, int(15 * scale))
    bh  = max(2, int(7  * scale))
    hair = hair_col if hair_col is not None else (55, 38, 18)

    pygame.draw.ellipse(surface, shirt,
                        (cx - bw // 2, cy + hr - 4, bw, bh))
    pygame.draw.circle(surface, hair,      (cx, cy), hr)
    pygame.draw.circle(surface, C_SKIN,    (cx, cy + hr // 5), int(hr * 0.88))
    pygame.draw.circle(surface, C_SKIN_DARK, (cx, cy), hr, 1)
    eo = max(2, hr // 4)
    er = max(1, hr // 5)
    ey = cy + hr // 3
    pygame.draw.circle(surface, (30, 20, 10), (cx - eo, ey), er)
    pygame.draw.circle(surface, (30, 20, 10), (cx + eo, ey), er)


def _draw_chair(surface, cx, cy, back='N'):
    """Bird's-eye chair. back = 'N'|'S'|'E'|'W' (which side the backrest is on)."""
    seat_col = (195, 158, 110)
    back_col = (138, 100, 52)
    sw, sh = 30, 26
    bt = 7

    if   back == 'N': br = (cx - sw//2, cy - sh//2 - bt, sw, bt)
    elif back == 'S': br = (cx - sw//2, cy + sh//2,       sw, bt)
    elif back == 'W': br = (cx - sw//2 - bt, cy - sh//2,  bt, sh)
    else:             br = (cx + sw//2, cy - sh//2,        bt, sh)

    pygame.draw.rect(surface, back_col, br, border_radius=3)
    pygame.draw.rect(surface, seat_col, (cx - sw//2, cy - sh//2, sw, sh), border_radius=4)
    pygame.draw.rect(surface, back_col, (cx - sw//2, cy - sh//2, sw, sh), 1, border_radius=4)


def _draw_exam_table(surface, cx, cy):
    """Bird's-eye exam table: white padded surface with metal frame."""
    tw, th = 50, 90
    # Metal frame
    pygame.draw.rect(surface, (160, 160, 155),
                     (cx - tw//2 - 2, cy - th//2 - 2, tw + 4, th + 4), border_radius=4)
    # Padded surface
    pygame.draw.rect(surface, C_EXAM_TABLE,
                     (cx - tw//2, cy - th//2, tw, th), border_radius=3)
    # Pillow at top
    pygame.draw.rect(surface, (235, 235, 230),
                     (cx - tw//2 + 4, cy - th//2 + 4, tw - 8, 22), border_radius=3)
    # Paper strip down centre
    pygame.draw.rect(surface, (248, 248, 248),
                     (cx - 6, cy - th//2 + 28, 12, th - 34), border_radius=1)


# ---------------------------------------------------------------------------
# Walls + furniture (used for collision AND rendering)
# ---------------------------------------------------------------------------
WALL_RECTS = [
    # --- Office outer walls ---
    pygame.Rect(0,    0,   580, WALL_T),    # N
    pygame.Rect(0,    680, 580, WALL_T),    # S
    pygame.Rect(0,    0,   WALL_T, 700),    # W
    pygame.Rect(580,  0,   WALL_T, CORRIDOR_Y1),          # E-upper (adjacent to exam room 1)
    pygame.Rect(580,  CORRIDOR_Y2, WALL_T, 700 - CORRIDOR_Y2),  # E-lower (adjacent to waiting room)

    # --- Exam rooms: outer shell ---
    pygame.Rect(EXAM_X0, 0,   800, WALL_T),               # N wall (all 4 rooms)
    pygame.Rect(1380,    0,   WALL_T, CORRIDOR_Y1),        # E wall (exam rooms)

    # --- Exam room internal dividers ---
    pygame.Rect(780,  WALL_T, WALL_T, CORRIDOR_Y1 - WALL_T),   # divider 1|2
    pygame.Rect(980,  WALL_T, WALL_T, CORRIDOR_Y1 - WALL_T),   # divider 2|3
    pygame.Rect(1180, WALL_T, WALL_T, CORRIDOR_Y1 - WALL_T),   # divider 3|4

    # --- Corridor north wall (south wall of exam rooms) with door gaps ---
    # Room 1 gap: x 650-710
    pygame.Rect(580, CORRIDOR_Y1,  70, WALL_T),
    pygame.Rect(710, CORRIDOR_Y1,  70, WALL_T),
    # Room 2 gap: x 850-910
    pygame.Rect(780, CORRIDOR_Y1,  70, WALL_T),
    pygame.Rect(910, CORRIDOR_Y1,  70, WALL_T),
    # Room 3 gap: x 1050-1110
    pygame.Rect(980,  CORRIDOR_Y1, 70, WALL_T),
    pygame.Rect(1110, CORRIDOR_Y1, 70, WALL_T),
    # Room 4 gap: x 1250-1310
    pygame.Rect(1180, CORRIDOR_Y1, 70, WALL_T),
    pygame.Rect(1310, CORRIDOR_Y1, 70, WALL_T),

    # --- Corridor south wall (north wall of waiting room) with central door gap ---
    # Gap: x 830-1010 (180 px)
    pygame.Rect(580,  CORRIDOR_Y2, 250, WALL_T),   # left of gap
    pygame.Rect(1010, CORRIDOR_Y2, 370, WALL_T),   # right of gap

    # --- Waiting room outer walls ---
    pygame.Rect(580,  680, 800, WALL_T),            # S
    pygame.Rect(1380, CORRIDOR_Y2, WALL_T, 700 - CORRIDOR_Y2),  # E
]

# Furniture collision rects (also used for drawing by index)
FURNITURE = [
    pygame.Rect(180,  290, 220, 80),    # [0] office desk
    pygame.Rect(130,  150,  55, 120),   # [1] bookshelf
    pygame.Rect(276,  388,  30,  26),   # [2] office chair
    # Exam tables (one per room, centred in each room)
    pygame.Rect(655,   85,  50,  90),   # [3] room 1 exam table
    pygame.Rect(855,   85,  50,  90),   # [4] room 2 exam table
    pygame.Rect(1055,  85,  50,  90),   # [5] room 3 exam table
    pygame.Rect(1255,  85,  50,  90),   # [6] room 4 exam table
]

SOLID = WALL_RECTS + FURNITURE

# Floor areas (visual only)
FLOORS = [
    (pygame.Rect(WALL_T, WALL_T, 560,  660), C_FLOOR_OFF),   # office
    (pygame.Rect(580, CORRIDOR_Y1, 800, 120), C_FLOOR_HALL),  # corridor
    # Exam rooms (draw each individually for visual separation)
    (pygame.Rect(600, WALL_T, 180, CORRIDOR_Y1 - WALL_T), C_FLOOR_EXAM),   # room 1
    (pygame.Rect(800, WALL_T, 180, CORRIDOR_Y1 - WALL_T), C_FLOOR_EXAM),   # room 2
    (pygame.Rect(1000, WALL_T, 180, CORRIDOR_Y1 - WALL_T), C_FLOOR_EXAM),  # room 3
    (pygame.Rect(1200, WALL_T, 180, CORRIDOR_Y1 - WALL_T), C_FLOOR_EXAM),  # room 4
    (pygame.Rect(600, CORRIDOR_Y2, 780, 680 - CORRIDOR_Y2), C_FLOOR_WAIT), # waiting room
]

# Exam room centres (x, y) — patients sit here on exam tables
EXAM_ROOM_CENTRES = [(680, 150), (880, 150), (1080, 150), (1280, 150)]


# ---------------------------------------------------------------------------
# Patient NPC
# ---------------------------------------------------------------------------
class Patient:
    R = 18

    def __init__(self, case, x, y):
        self.case = case
        self.x    = x
        self.y    = y

    def near(self, px, py):
        return abs(px - self.x) < 75 and abs(py - self.y) < 75


# ---------------------------------------------------------------------------
# WorldScene
# ---------------------------------------------------------------------------
class WorldScene:
    def __init__(self, screen, player_pos=None):
        self.screen   = screen
        self.SW, self.SH = screen.get_size()

        self.f_room = pygame.font.SysFont('segoeui', 20, bold=True)
        self.f_name = pygame.font.SysFont('segoeui', 14)
        self.f_hint = pygame.font.SysFont('segoeui', 19, bold=True)
        self.f_ui   = pygame.font.SysFont('segoeui', 15)

        px0, py0 = player_pos or (100, 500)
        self.px   = float(px0)
        self.py   = float(py0)

        # Place one patient per exam room (up to N_EXAM_ROOMS)
        self.patients = [
            Patient(case, *EXAM_ROOM_CENTRES[i])
            for i, case in enumerate(CASES[:N_EXAM_ROOMS])
        ]

        self._near = None

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_e, pygame.K_SPACE):
            if self._near:
                from scenes.consultation import ConsultationScene
                return ConsultationScene(
                    self.screen,
                    self._near.case,
                    player_pos=(self.px, self.py),
                )
        return None

    # ------------------------------------------------------------------
    def update(self, dt):
        keys  = pygame.key.get_pressed()
        speed = PLAYER_SPEED * dt / 1000.0

        dx = dy = 0.0
        if keys[pygame.K_LEFT]  or keys[pygame.K_a]: dx -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx += 1
        if keys[pygame.K_UP]    or keys[pygame.K_w]: dy -= 1
        if keys[pygame.K_DOWN]  or keys[pygame.K_s]: dy += 1

        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071

        self._slide(dx * speed, 0)
        self._slide(0, dy * speed)

        self.px = max(float(PLAYER_R), min(self.px, float(WORLD_W - PLAYER_R)))
        self.py = max(float(PLAYER_R), min(self.py, float(WORLD_H - PLAYER_R)))

        self._near = next(
            (p for p in self.patients if p.near(self.px, self.py)), None
        )

    def _slide(self, dx, dy):
        self.px += dx
        self.py += dy
        pr = self._prect()
        for solid in SOLID:
            if pr.colliderect(solid):
                if dx > 0: self.px = float(solid.left   - PLAYER_R)
                if dx < 0: self.px = float(solid.right  + PLAYER_R)
                if dy > 0: self.py = float(solid.top    - PLAYER_R)
                if dy < 0: self.py = float(solid.bottom + PLAYER_R)
                pr = self._prect()

    def _prect(self):
        return pygame.Rect(
            int(self.px) - PLAYER_R, int(self.py) - PLAYER_R,
            PLAYER_R * 2, PLAYER_R * 2,
        )

    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(C_WALL_COL)

        cx = int(max(0, min(self.px - self.SW / 2, WORLD_W - self.SW)))

        def ws(wx, wy):
            return (wx - cx, wy)

        def sr(rect):
            return rect.move(-cx, 0)

        # --- Floors ---
        for rect, col in FLOORS:
            pygame.draw.rect(self.screen, col, sr(rect))

        # Subtle stripe between exam rooms (visual only, makes rooms feel distinct)
        for room_x in [780, 980, 1180]:
            rx = room_x - cx
            pygame.draw.line(self.screen, (175, 185, 175), (rx, WALL_T), (rx, CORRIDOR_Y1), 1)

        # --- Office furniture ---

        # Desk
        dr = sr(FURNITURE[0])
        pygame.draw.rect(self.screen, (148, 98, 50), dr, border_radius=3)
        pygame.draw.rect(self.screen, (100, 64, 28),
                         (dr.x, dr.bottom - 8, dr.width, 8), border_radius=3)
        mon = pygame.Rect(dr.x + dr.width // 2 - 14, dr.y + 10, 28, 20)
        pygame.draw.rect(self.screen, (38, 40, 46), mon, border_radius=2)
        pygame.draw.rect(self.screen, (60, 62, 70), mon, 1, border_radius=2)
        kbd = pygame.Rect(dr.x + dr.width // 2 - 22, dr.y + 36, 44, 14)
        pygame.draw.rect(self.screen, (175, 175, 168), kbd, border_radius=2)
        pygame.draw.ellipse(self.screen, (175, 175, 168),
                            (dr.x + dr.width // 2 + 26, dr.y + 37, 10, 14))

        # Bookshelf
        sf = sr(FURNITURE[1])
        pygame.draw.rect(self.screen, (88, 60, 28), sf, border_radius=3)
        book_cols = [(200,55,55),(55,100,200),(55,175,75),(200,170,45),
                     (180,80,200),(200,140,50),(80,160,160)]
        bw_each = (sf.width - 8) // len(book_cols)
        for i, c in enumerate(book_cols):
            pygame.draw.rect(self.screen, c,
                             (sf.x + 4 + i * bw_each, sf.y + 4, bw_each - 2, sf.height - 8),
                             border_radius=1)

        # Office chair
        ch = sr(FURNITURE[2])
        _draw_chair(self.screen, ch.centerx, ch.centery, back='N')

        # --- Exam tables (one per room) ---
        for idx in range(3, 7):
            t = sr(FURNITURE[idx])
            _draw_exam_table(self.screen, t.centerx, t.centery)

        # --- Waiting room: a few chairs along the north wall ---
        for wx in [700, 820, 940, 1060, 1180]:
            _draw_chair(self.screen, wx - cx, CORRIDOR_Y2 + 35, back='S')

        # --- Room labels ---
        labels = [
            ('OFFICE',       300,  350),
            ('EXAM ROOM 1',  680,   28),
            ('EXAM ROOM 2',  880,   28),
            ('EXAM ROOM 3', 1080,   28),
            ('EXAM ROOM 4', 1280,   28),
            ('WAITING ROOM', 920,  450 + (680 - CORRIDOR_Y2) // 2),
        ]
        for txt, wx, wy in labels:
            surf = self.f_room.render(txt, True, C_LABEL_COL)
            self.screen.blit(surf, ws(wx - surf.get_width() // 2, wy))

        # --- Corridor direction arrow hint ---
        arrow_surf = self.f_ui.render('↑  Exam Rooms', True, (140, 140, 130))
        self.screen.blit(arrow_surf, ws(780 - arrow_surf.get_width() // 2, CORRIDOR_Y1 + 10))

        # --- Patients on exam tables ---
        for i, p in enumerate(self.patients):
            sx, sy = ws(p.x, p.y)

            # Glow ring when in range
            if p is self._near:
                glow = pygame.Surface((p.R * 4, p.R * 4), pygame.SRCALPHA)
                pygame.draw.circle(glow, (41, 128, 185, 70), (p.R * 2, p.R * 2), p.R * 2)
                self.screen.blit(glow, (sx - p.R * 2, sy - p.R * 2))

            # Patient sits on exam table, facing south (toward corridor door)
            shirt = PATIENT_SHIRTS[i % len(PATIENT_SHIRTS)]
            is_female = p.case['patient'].get('sex', '').lower() == 'female'
            hair_col = (195, 155, 90) if is_female else None
            _draw_person(self.screen, sx, sy, shirt=shirt, scale=1.0, hair_col=hair_col)

            # Name tag above
            ns = self.f_name.render(p.case['patient']['name'], True, TEXT)
            self.screen.blit(ns, (sx - ns.get_width() // 2, sy - 30))

        # --- Player (doctor in white coat) ---
        pr = self._prect().move(-cx, 0)
        _draw_person(self.screen, pr.centerx, pr.centery,
                     shirt=(230, 230, 230), scale=1.0)

        # --- HUD: controls reminder ---
        ctrl = self.f_ui.render("WASD / Arrows to move   \u2022   E to interact", True, (185, 185, 185))
        self.screen.blit(ctrl, (10, 10))

        # --- HUD: interaction hint ---
        if self._near:
            txt  = f"Press E  \u2014  {self._near.case['patient']['name']}"
            hint = self.f_hint.render(txt, True, WHITE)
            hw   = hint.get_width() + 28
            hh   = hint.get_height() + 14
            hx   = self.SW // 2 - hw // 2
            hy   = self.SH - 56
            bg   = pygame.Surface((hw, hh), pygame.SRCALPHA)
            bg.fill((15, 15, 15, 180))
            pygame.draw.rect(bg, (255, 255, 255, 35), (0, 0, hw, hh), 1, border_radius=8)
            self.screen.blit(bg,   (hx, hy))
            self.screen.blit(hint, (hx + 14, hy + 7))
