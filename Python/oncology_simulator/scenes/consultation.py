import pygame
from scenes.base import *

PHASE_HISTORY  = 'history'
PHASE_QUESTION = 'question'


class ConsultationScene:
    def __init__(self, screen, case, player_pos=None):
        self.screen      = screen
        self.W, self.H   = screen.get_size()
        self.case        = case
        self.player_pos  = player_pos
        self.phase       = PHASE_HISTORY
        self.q_index  = 0
        self.answers  = []   # list of (selected_idx, correct_idx)
        self.selected = None
        self.scroll_y = 0

        self.font_title  = pygame.font.SysFont('segoeui', 26, bold=True)
        self.font_header = pygame.font.SysFont('segoeui', 20, bold=True)
        self.font_body   = pygame.font.SysFont('segoeui', 17)
        self.font_small  = pygame.font.SysFont('segoeui', 15)
        self.font_btn    = pygame.font.SysFont('segoeui', 18, bold=True)

        self.btn_proceed = Button(
            rect=(self.W // 2 - 135, self.H - 68, 270, 46),
            text="Proceed to Questions  \u2192",
            font=self.font_btn,
        )
        self.btn_confirm = Button(
            rect=(self.W // 2 - 110, self.H - 68, 220, 46),
            text="Confirm Answer  \u2192",
            font=self.font_btn,
        )

        self._build_history_lines()

    # ------------------------------------------------------------------
    # Pre-render history into individual wrapped lines
    # ------------------------------------------------------------------
    def _build_history_lines(self):
        max_w = self.W - 110
        self.history_lines = []   # list of (kind, text)

        p = self.case['patient']
        self.history_lines.append(('header',   f"{p['name']}  |  Age {p['age']}  |  {p['sex']}"))
        self.history_lines.append(('subheader', f"Stage: {self.case['stage']}"))
        self.history_lines.append(('spacer',    ''))

        self.history_lines.append(('label', 'Chief Complaint'))
        for line in wrap_text(p['presenting_complaint'], self.font_body, max_w - 40):
            self.history_lines.append(('body', line))
        self.history_lines.append(('spacer', ''))

        self.history_lines.append(('label', 'History'))
        for line in wrap_text(self.case['history'], self.font_body, max_w - 40):
            self.history_lines.append(('body', line))
        self.history_lines.append(('spacer', ''))

        self.history_lines.append(('label', 'Investigations'))
        for inv in self.case['investigations']:
            for line in wrap_text(f"\u2022  {inv}", self.font_body, max_w - 40):
                self.history_lines.append(('body', line))

    _LINE_H = {'header': 34, 'subheader': 26, 'label': 30, 'spacer': 14, 'body': 22}

    def _total_history_h(self):
        return sum(self._LINE_H.get(k, 22) for k, _ in self.history_lines)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event):
        if self.phase == PHASE_HISTORY:
            if event.type == pygame.MOUSEWHEEL:
                max_scroll = max(0, self._total_history_h() - (self.H - 160))
                self.scroll_y = max(0, min(self.scroll_y - event.y * 25, max_scroll))
            if self.btn_proceed.is_clicked(event):
                self.phase    = PHASE_QUESTION
                self.scroll_y = 0
                self.selected = None

        elif self.phase == PHASE_QUESTION:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, rect in enumerate(self._option_rects()):
                    if rect.collidepoint(event.pos):
                        self.selected = i

            if self.selected is not None and self.btn_confirm.is_clicked(event):
                q = self.case['questions'][self.q_index]
                self.answers.append((self.selected, q['correct']))
                self.q_index += 1
                self.selected = None
                if self.q_index >= len(self.case['questions']):
                    from scenes.debrief import DebriefScene
                    return DebriefScene(self.screen, self.case, self.answers, self.player_pos)

        return None

    def update(self, dt):
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BG)
        if self.phase == PHASE_HISTORY:
            self._draw_history()
        else:
            self._draw_question()

    def _draw_history(self):
        # Header bar
        pygame.draw.rect(self.screen, HEADER_COL, (0, 0, self.W, 68))
        title = self.font_title.render(
            f"Patient File  \u2014  {self.case['patient']['name']}", True, WHITE)
        self.screen.blit(title, (28, 18))

        # Clip scrollable content
        self.screen.set_clip(pygame.Rect(0, 68, self.W, self.H - 128))
        y = 82 - self.scroll_y
        for kind, text in self.history_lines:
            if   kind == 'header':
                surf = self.font_title.render(text, True, HEADER_COL)
                self.screen.blit(surf, (50, y))
            elif kind == 'subheader':
                surf = self.font_header.render(text, True, BLUE)
                self.screen.blit(surf, (50, y))
            elif kind == 'label':
                surf = self.font_header.render(text, True, HEADER_COL)
                self.screen.blit(surf, (50, y))
                pygame.draw.line(self.screen, PANEL_BORDER,
                                 (50, y + 26), (self.W - 50, y + 26), 1)
            elif kind == 'body':
                surf = self.font_body.render(text, True, TEXT)
                self.screen.blit(surf, (62, y))
            y += self._LINE_H.get(kind, 22)
        self.screen.set_clip(None)

        # Scrollbar
        total_h = self._total_history_h()
        visible_h = self.H - 128
        if total_h > visible_h:
            bar_h = max(30, int(visible_h / total_h * visible_h))
            bar_y = 68 + int(self.scroll_y / (total_h - visible_h) * (visible_h - bar_h))
            pygame.draw.rect(self.screen, LIGHT_GRAY,  (self.W - 9, 68, 7, visible_h))
            pygame.draw.rect(self.screen, GRAY, (self.W - 9, bar_y, 7, bar_h), border_radius=3)

        self.btn_proceed.draw(self.screen)

    def _option_rects(self):
        q = self.case['questions'][self.q_index]
        rects, y = [], 260
        for _ in q['options']:
            rects.append(pygame.Rect(70, y, self.W - 140, 68))
            y += 80
        return rects

    def _draw_question(self):
        q      = self.case['questions'][self.q_index]
        total  = len(self.case['questions'])
        p      = self.case['patient']

        # Header bar
        pygame.draw.rect(self.screen, HEADER_COL, (0, 0, self.W, 68))
        hdr = self.font_header.render(
            f"{p['name']}  \u2014  Question {self.q_index + 1} of {total}", True, WHITE)
        self.screen.blit(hdr, (28, 22))

        # Question text
        y = 95
        for line in wrap_text(q['text'], self.font_header, self.W - 100):
            surf = self.font_header.render(line, True, HEADER_COL)
            self.screen.blit(surf, (50, y))
            y += 30

        # Options
        mouse = pygame.mouse.get_pos()
        for i, (opt, rect) in enumerate(zip(q['options'], self._option_rects())):
            hover = rect.collidepoint(mouse)
            if self.selected == i:
                bg, tc = SELECTED, WHITE
            elif hover:
                bg, tc = (220, 236, 252), TEXT
            else:
                bg, tc = WHITE, TEXT

            pygame.draw.rect(self.screen, bg, rect, border_radius=8)
            pygame.draw.rect(self.screen, PANEL_BORDER, rect, 2, border_radius=8)

            letter_col = WHITE if self.selected == i else BLUE
            letter = self.font_header.render(f"{chr(65 + i)}.", True, letter_col)
            self.screen.blit(letter, (rect.x + 16, rect.y + 20))

            for j, ol in enumerate(wrap_text(opt, self.font_body, rect.width - 58)[:2]):
                surf = self.font_body.render(ol, True, tc)
                self.screen.blit(surf, (rect.x + 52, rect.y + 14 + j * 22))

        # Bottom controls
        if self.selected is not None:
            self.btn_confirm.draw(self.screen)
        else:
            hint = self.font_small.render("Select an answer above", True, GRAY)
            self.screen.blit(hint, (self.W // 2 - hint.get_width() // 2, self.H - 52))
