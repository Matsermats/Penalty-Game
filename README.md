# Penalty-Game

This repository contains two versions of a simple penalty shootout game. Both versions keep track of your high score.

- **penalty_game.py** - command-line game where you shoot by entering a number for one of five corners.
- **penalty_game_gui.py** - Pygame variant where you click a corner to shoot and watch the keeper dive.

Install Pygame and start the GUI with:

```bash
pip install pygame
python3 penalty_game_gui.py
```

Use the mouse to click one of the five goal sections (links boven, links onder, midden, rechts boven, rechts onder). De grafische versie tekent nu een echt doel met net, een voetbal met zwart-wit patroon en een keeper met shirt en handschoenen. Elke goal maakt het lastiger om te scoren (80%, 60%, 40%, dan 20%). De vierde poging is de **gouden bal** en wordt goud getekend. Scoor vier keer achter elkaar om te winnen. Beide versies tonen willekeurige juich- of teleurstellingsteksten en slaan je hoogste score op in `highscore.txt`.
