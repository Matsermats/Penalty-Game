# Penalty-Game

This repository contains two versions of a simple penalty shootout game. Both versions keep track of your high score.

- **penalty_game.py** - command-line game where you shoot by entering a number for one of five corners.
- **penalty_game_gui.py** - Pygame variant where you click a corner to shoot and watch the keeper dive.

Install Pygame and start the GUI with:

```bash
pip install pygame
python3 penalty_game_gui.py
```

Use the mouse to click one of the five goal sections. Each goal you score makes it harder to score again (80%, 60%, 40%, then 20%). The last shot is the **gouden bal** and is drawn in gold. Score four times in a row to win. Both versions show random celebrations or disappointments, and your best score is stored in `highscore.txt`.
