# Penalty-Game

This repository contains two versions of a simple penalty shootout game. Both versions keep track of your high score.

- **penalty_game.py** - command-line game where you shoot by entering a number for one of five corners.
- **penalty_game_gui.py** - Pygame variant where you click a corner to shoot and watch the keeper dive.

Install Pygame and start the GUI with:

```bash
python3 -m pip install pygame  # use the pip alias if available
python3 penalty_game_gui.py
```

Use the mouse to click one of the five goal sections (links boven, links onder, midden, rechts boven, rechts onder). De grafische versie tekent nu een echt doel met fijn net, een voetbal met meer patroon en een keeper die tijdens het duiken draait. De bal volgt een boog en wordt goud bij de vierde poging. Elke goal maakt scoren moeilijker (80%, 60%, 40%, dan 20%). Scoor vier keer achter elkaar om te winnen. Beide versies tonen willekeurige juich- of teleurstellingsteksten en slaan je hoogste score op in `highscore.txt`.
