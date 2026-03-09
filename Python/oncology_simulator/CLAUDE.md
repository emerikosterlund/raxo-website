# Oncology Simulator - CLAUDE.md

## Project Overview

An interactive educational medical training game built with Pygame. Players act as a doctor navigating a clinic, selecting patients, reviewing clinical histories, and answering evidence-based oncology questions. Designed to teach cancer case management through realistic scenarios.

## Running the Project

```bash
cd oncology_simulator
pip install pygame
python main.py
```

- Resolution: 1024×768, 60 FPS
- Controls: WASD/Arrow keys to move, E or SPACE to interact with patients

## Project Structure

```
oncology_simulator/
├── main.py               # Entry point: pygame init, game loop, scene manager
├── data/
│   └── cases.py          # All clinical case data (patients, questions, explanations)
└── scenes/
    ├── base.py           # Shared colors, Button class, wrap_text()
    ├── world.py          # Main interactive clinic world (player movement, NPCs)
    ├── office.py         # Doctor's office intro scene
    ├── waiting_room.py   # Patient selection list
    ├── consultation.py   # History review + multiple-choice questions
    └── debrief.py        # Score display and answer explanations
```

## Scene Architecture

Every scene implements three methods — this is the core contract:

```python
def handle_event(self, event) -> Scene | None:  # Return new scene to transition, None to stay
def update(self, dt: float) -> None             # dt is seconds since last frame
def draw(self) -> None                          # Render to self.screen
```

`main.py` drives the loop: calls `handle_event` → `update` → `draw` each frame. Scene transitions happen by returning a new scene object from `handle_event`.

## Adding a New Patient Case

All case data lives in [data/cases.py](data/cases.py). Append a new dict to the `CASES` list:

```python
{
    "id": 3,                         # Unique integer
    "patient": {
        "name": "Full Name",
        "age": 45,
        "sex": "F",                  # "M" or "F"
        "presenting_complaint": "..."
    },
    "history": "Multi-line clinical narrative...",
    "investigations": [              # Bullet-pointed findings shown in consultation
        "Finding one",
        "Finding two",
    ],
    "stage": "Stage IIB ...",
    "questions": [
        {
            "text": "Question text?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct": 0,            # 0-indexed
            "explanation": "Evidence-based rationale citing trials..."
        }
    ]
}
```

The waiting room and world scene automatically pick up new cases — no other code changes needed.

## Key Implementation Details

**world.py** is the largest file (~430 lines). It handles:
- Bird's-eye clinic layout with collision rects for walls/furniture
- Player stick-figure rendering and WASD movement (speed: 180 px/s)
- Diagonal movement normalized by 1/√2
- Camera: horizontal panning that follows the player
- Patient NPCs in the waiting room area; interaction triggers within 75px

**consultation.py** runs two sequential phases:
1. `PHASE_HISTORY` — scrollable patient file
2. `PHASE_QUESTION` — one question at a time, records `(selected_idx, correct_idx)` per question

**base.py** defines the full color palette as module-level constants (e.g., `COLORS["header"]`, `COLORS["success"]`). Always import colors from here rather than hardcoding RGB values.

## Clinical Content Standards

- Reference real RCTs when writing explanations (e.g., PACIFIC trial for NSCLC, CLEOPATRA for HER2+ breast cancer)
- Include molecular markers (EGFR, ALK, HER2, HR status), TNM staging, and performance status where relevant
- Explanations should justify why wrong answers are wrong, not just why the correct answer is right

## No Tests / No Config Files

There is no test suite and no external config. All settings (screen size, FPS, colors) are hardcoded. To change resolution, edit `SCREEN_W`/`SCREEN_H` in `main.py`.
