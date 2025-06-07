import random
from pathlib import Path

GOAL_MESSAGES = [
    'Goal!',
    'Wat een schot!',
    'Binnenkant paal en erin!',
    'Onhoudbaar!',
]

SAVE_MESSAGES = [
    'Keeper pakt hem!',
    'Wat een redding!',
    'Geen goal deze keer!',
]

HIGHSCORE_FILE = Path("highscore.txt")


def load_highscore():
    try:
        return int(HIGHSCORE_FILE.read_text())
    except Exception:
        return 0


def save_highscore(score: int) -> None:
    try:
        HIGHSCORE_FILE.write_text(str(score))
    except Exception:
        pass


def penalty_game():
    opties = [
        'links boven',
        'links onder',
        'midden',
        'rechts boven',
        'rechts onder',
    ]
    kansen = [0.8, 0.6, 0.4, 0.2]  # kans om te scoren per doelpoging
    highscore = load_highscore()
    print('Welkom bij de Penalty Game!')
    print(f'Huidige highscore: {highscore}')
    print(
        'Typ 1 voor links boven, 2 voor links onder, 3 voor midden, '
        '4 voor rechts boven, 5 voor rechts onder. q om te stoppen.'
    )

    while True:  # speel meerdere rondes
        score = 0
        while True:
            if score >= 4:
                print('Gefeliciteerd, je hebt gewonnen!')
                if score > highscore:
                    print('Nieuwe highscore!')
                    save_highscore(score)
                break

            if score == 3:
                print('*** Gouden bal! ***')
            keuze = input('Kies je hoek (1/2/3/4/5/q): ').strip().lower()
            if keuze == 'q':
                print(f'Eindscore: {score}')
                if score > highscore:
                    print('Nieuwe highscore!')
                    save_highscore(score)
                break
            if keuze not in ['1', '2', '3', '4', '5']:
                print('Ongeldige invoer. Probeer opnieuw.')
                continue

            speler_index = int(keuze) - 1
            speler_hoek = opties[speler_index]

            # kans dat keeper de juiste hoek kiest neemt toe per doelpoging
            kans_scoren = kansen[min(score, len(kansen) - 1)]
            if random.random() < kans_scoren:
                keuzes_over = [i for i in range(len(opties)) if i != speler_index]
                keeper_index = random.choice(keuzes_over)
            else:
                keeper_index = speler_index

            keeper_hoek = opties[keeper_index]

            print(f'Je trapte naar {speler_hoek}. Keeper dook naar {keeper_hoek}.')
            if speler_index == keeper_index:
                print(random.choice(SAVE_MESSAGES))
                print(f'Je eindscore is {score} doelpunt(en).')
                if score > highscore:
                    print('Nieuwe highscore!')
                    save_highscore(score)
                break
            else:
                score += 1
                print(random.choice(GOAL_MESSAGES), f'Totaal gescoord: {score}')

        again = input('Nog een keer spelen? (j/n): ').strip().lower()
        if again != 'j':
            break

if __name__ == '__main__':
    penalty_game()
