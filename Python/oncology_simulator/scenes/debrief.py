import pygame
from scenes.base import *


class DebriefScene:
    def __init__(self, screen, case, answers, player_pos=None):
        self.screen     = screen
        self.W, self.H  = screen.get_size()
        self.case       = case
        self.answers    = answers   # list of (selected_idx, correct_idx)
        self.player_pos = player_pos
        self.scroll_y   = 0

        self.font_title  = pygame.font.SysFont('segoeui', 28, bold=True)
        self.font_header = pygame.font.SysFont('segoeui', 19, bold=True)
        self.font_body   = pygame.font.SysFont('segoeui', 17)
        self.font_small  = pygame.font.SysFont('segoeui', 15)
        self.font_btn    = pygame.font.SysFont('segoeui', 18, bold=True)

        self.score = sum(1 for sel, cor in answers if sel == cor)
        self.total = len(answers)

        self.btn_office = Button(
            rect=(self.W // 2 - 140, self.H - 66, 280, 46),
            text="\u2190  Return to Office",
            font=self.font_btn,
        )

        self._build_lines()

    # ------------------------------------------------------------------
    # Pre-wrap all content into individual lines
    # ------------------------------------------------------------------
    def _build_lines(self):
        self.lines = []   # list of (kind, text)
        max_w = self.W - 130

        for i, (sel, cor) in enumerate(self.answers):
            q       = self.case['questions'][i]
            correct = sel == cor

            mark = '\u2713 Correct' if correct else '\u2717 Incorrect'
            self.lines.append(('q_header', f"Question {i + 1}  \u2014  {mark}", correct))

            for line in wrap_text(q['text'], self.font_body, max_w):
                self.lines.append(('q_text', line, None))

            for j, opt in enumerate(q['options']):
                label = f"{chr(65 + j)}.  {opt}"
                if j == cor == sel:
                    tag = 'correct_chosen'
                elif j == cor:
                    tag = 'correct_unchosen'
                elif j == sel:
                    tag = 'wrong_chosen'
                else:
                    tag = 'option'
                for line in wrap_text(label, self.font_body, max_w - 10):
                    self.lines.append((tag, line, None))

            self.lines.append(('exp_label', 'Explanation', None))
            for line in wrap_text(q['explanation'], self.font_body, max_w - 20):
                self.lines.append(('exp_body', line, None))

            self.lines.append(('spacer', '', None))

    _LINE_H = {
        'q_header': 34, 'q_text': 22,
        'correct_chosen': 24, 'correct_unchosen': 24,
        'wrong_chosen': 24, 'option': 24,
        'exp_label': 30, 'exp_body': 22, 'spacer': 18,
    }

    def _total_h(self):
        return sum(self._LINE_H.get(k, 22) for k, _, _ in self.lines)

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            visible_h = self.H - 160
            max_scroll = max(0, self._total_h() - visible_h)
            self.scroll_y = max(0, min(self.scroll_y - event.y * 25, max_scroll))

        if self.btn_office.is_clicked(event):
            from scenes.world import WorldScene
            return WorldScene(self.screen, self.player_pos)
        return None

    def update(self, dt):
        pass

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------
    def draw(self):
        self.screen.fill(BG)

        # Header bar
        pygame.draw.rect(self.screen, HEADER_COL, (0, 0, self.W, 98))
        title = self.font_title.render("Case Debrief", True, WHITE)
        self.screen.blit(title, (28, 12))

        score_col = GREEN if self.score == self.total else (RED if self.score == 0 else (220, 140, 0))
        score_surf = self.font_title.render(
            f"Score: {self.score} / {self.total}", True, score_col)
        self.screen.blit(score_surf, (28, 52))

        # Scrollable content
        visible_h = self.H - 158
        self.screen.set_clip(pygame.Rect(0, 98, self.W, visible_h))
        x0 = 58
        y  = 112 - self.scroll_y

        for kind, text, meta in self.lines:
            lh = self._LINE_H.get(kind, 22)

            if kind == 'q_header':
                correct = meta
                col = GREEN if correct else RED
                surf = self.font_header.render(text, True, col)
                self.screen.blit(surf, (x0, y))

            elif kind == 'q_text':
                surf = self.font_body.render(text, True, TEXT)
                self.screen.blit(surf, (x0, y))

            elif kind in ('correct_chosen', 'correct_unchosen', 'wrong_chosen', 'option'):
                if kind in ('correct_chosen', 'correct_unchosen'):
                    bg, tc = CORRECT_BG, GREEN_DARK
                elif kind == 'wrong_chosen':
                    bg, tc = WRONG_BG, RED_DARK
                else:
                    bg, tc = None, GRAY

                if bg:
                    pygame.draw.rect(self.screen, bg,
                                     (x0 - 4, y - 1, self.W - x0 * 2 + 8, lh), border_radius=4)
                surf = self.font_body.render(text, True, tc)
                self.screen.blit(surf, (x0 + 4, y + 2))

            elif kind == 'exp_label':
                surf = self.font_header.render("Explanation:", True, BLUE)
                self.screen.blit(surf, (x0, y))

            elif kind == 'exp_body':
                surf = self.font_body.render(text, True, TEXT)
                self.screen.blit(surf, (x0 + 12, y))

            elif kind == 'spacer':
                pygame.draw.line(self.screen, PANEL_BORDER,
                                 (x0, y + 8), (self.W - x0, y + 8), 1)

            y += lh

        self.screen.set_clip(None)

        # Scrollbar
        total_h = self._total_h()
        if total_h > visible_h:
            bar_h = max(30, int(visible_h / total_h * visible_h))
            bar_y = 98 + int(self.scroll_y / max(1, total_h - visible_h) * (visible_h - bar_h))
            pygame.draw.rect(self.screen, LIGHT_GRAY, (self.W - 9, 98, 7, visible_h))
            pygame.draw.rect(self.screen, GRAY, (self.W - 9, bar_y, 7, bar_h), border_radius=3)

        self.btn_office.draw(self.screen)
