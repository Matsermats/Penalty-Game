# Penalty-Game

This repository contains two versions of a simple penalty shootout game. Both versions keep track of your highscore.

- **penalty_game.py** – command line version where you choose one of five corners using the number keys.
- **penalty_game_gui.py** – Pygame version where you click inside the goal to shoot and watch the keeper dive.

Install the required dependency and run the graphical game with:

```bash
pip install pygame
python3 penalty_game_gui.py
```

Use the mouse to click one of the five sections of the goal. With every goal you score the keeper becomes more likely to pick the correct corner (80%, 60%, 40%, then 20% chance to score). The last shot is the **gouden bal** and is drawn in gold. Als je vier keer op rij scoort win je. Daarna kun je opnieuw beginnen door ergens te klikken. De command-line versie werkt hetzelfde en meldt het wanneer je de gouden bal bereikt.

Beide versies tonen nu willekeurige juich- of teleurstellende teksten na elke poging om het spel levendiger te maken.

Your best score is stored in `highscore.txt`.
