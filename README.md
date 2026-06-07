# Langton's Ant 🐜

A Python simulation of [Langton's Ant](https://en.wikipedia.org/wiki/Langton%27s_ant) — a cellular automaton that generates complex emergent patterns from two simple rules.

## How it works

The ant moves on an infinite grid following these rules:
- **White cell** → turn 90° right, flip cell to black, move forward
- **Black cell** → turn 90° left, flip cell to white, move forward

After ~10,000 steps, the ant spontaneously starts building an infinitely repeating diagonal "highway" — a classic example of emergent complexity from simple rules.

## Features

- Interactive GUI built with `tkinter`
- Step-by-step and continuous simulation modes
- Configurable grid size and simulation speed
- Support for extended multi-state rules (e.g. `LLRR`, `RLR`, ...)

## Getting Started

```bash
pip install tkinter
python "La Fourmi de Langton.py"
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3 | Core language |
| Tkinter | GUI framework |

## Authors

Ahmad Hatoum · Francesco Di Gennaro · Daniel Kebbous · Yasmine Faiz

*L1 Computer Science project — Université de Versailles Saint-Quentin-en-Yvelines*

