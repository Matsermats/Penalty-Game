import random


def penalty_game():
    opties = ['links', 'midden', 'rechts']
    score = 0
    print('Welkom bij de Penalty Game!')
    print('Typ l voor links, m voor midden, r voor rechts. q om te stoppen.')
    while True:
        keuze = input('Kies je hoek (l/m/r/q): ').strip().lower()
        if keuze == 'q':
            print(f'Eindscore: {score}')
            break
        if keuze not in ['l', 'm', 'r']:
            print('Ongeldige invoer. Probeer opnieuw.')
            continue
        speler_hoek = {'l': 'links', 'm': 'midden', 'r': 'rechts'}[keuze]
        keeper_hoek = random.choice(opties)
        print(f'Je trapte naar {speler_hoek}. Keeper dook naar {keeper_hoek}.')
        if speler_hoek == keeper_hoek:
            print('Keeper heeft de bal!')
            print(f'Je eindscore is {score} doelpunt(en).')
            break
        else:
            score += 1
            print(f'Goal! Totaal gescoord: {score}')

if __name__ == '__main__':
    penalty_game()
