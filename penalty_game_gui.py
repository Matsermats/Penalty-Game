import random
import pygame
from pathlib import Path

GOAL_MESSAGES = [
    'Goal!',
    'Fantastisch schot!',
    'Raak!',
    'Onhoudbaar!',
]

SAVE_MESSAGES = [
    'Wat een redding!',
    'Keeper pakt hem!',
    'Helaas gemist!',
]

WIDTH, HEIGHT = 600, 400
GOAL_Y = 50
GOAL_HEIGHT = 120
SECTIONS = 5
SUCCESS_CHANCES = [0.8, 0.6, 0.4, 0.2]

HIGHSCORE_FILE = Path("highscore.txt")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penalty Game")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# positions for ball and keeper
ball_start = (WIDTH // 2, HEIGHT - 50)
ball_pos = list(ball_start)
keeper_pos = [WIDTH // 2, GOAL_Y + GOAL_HEIGHT - 20]
GOLD = (255, 215, 0)
THIRD = WIDTH // 3
HALF = GOAL_HEIGHT // 2

SECTION_RECTS = [
    pygame.Rect(0, GOAL_Y, THIRD, HALF),
    pygame.Rect(0, GOAL_Y + HALF, THIRD, HALF),
    pygame.Rect(THIRD, GOAL_Y, THIRD, GOAL_HEIGHT),
    pygame.Rect(2 * THIRD, GOAL_Y, THIRD, HALF),
    pygame.Rect(2 * THIRD, GOAL_Y + HALF, THIRD, HALF),
]

BALL_TARGETS = [
    rect.center for rect in SECTION_RECTS
]

KEEPER_TARGETS = [
    (rect.centerx, rect.bottom) for rect in SECTION_RECTS
]

def load_highscore():
    try:
        return int(HIGHSCORE_FILE.read_text())
    except Exception:
        return 0


def save_highscore(score):
    try:
        HIGHSCORE_FILE.write_text(str(score))
    except Exception:
        pass


def run_game(highscore):
    score = 0
    ball_pos[:] = ball_start
    keeper_pos[0] = WIDTH // 2
    shooting = False
    ball_target = None
    keeper_target = None
    section_chosen = None
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return score, False
            elif event.type == pygame.MOUSEBUTTONDOWN and not shooting and score < 4:
                x, y = event.pos
                for idx, rect in enumerate(SECTION_RECTS):
                    if rect.collidepoint(x, y):
                        section_chosen = idx
                        ball_target = BALL_TARGETS[idx]
                        chance = SUCCESS_CHANCES[min(score, len(SUCCESS_CHANCES) - 1)]
                        if random.random() < chance:
                            choices = [i for i in range(SECTIONS) if i != idx]
                            keeper_target = random.choice(choices)
                        else:
                            keeper_target = idx
                        shooting = True
                        break

        if shooting:
            # move ball toward target
            for i in (0, 1):
                if ball_pos[i] < ball_target[i]:
                    ball_pos[i] += 10
                    if ball_pos[i] > ball_target[i]:
                        ball_pos[i] = ball_target[i]
                elif ball_pos[i] > ball_target[i]:
                    ball_pos[i] -= 10
                    if ball_pos[i] < ball_target[i]:
                        ball_pos[i] = ball_target[i]

            # move keeper toward target
            target_x, target_y = KEEPER_TARGETS[keeper_target]
            if keeper_pos[0] < target_x:
                keeper_pos[0] += 15
                if keeper_pos[0] > target_x:
                    keeper_pos[0] = target_x
            elif keeper_pos[0] > target_x:
                keeper_pos[0] -= 15
                if keeper_pos[0] < target_x:
                    keeper_pos[0] = target_x

            if keeper_pos[1] > target_y:
                keeper_pos[1] -= 15
                if keeper_pos[1] < target_y:
                    keeper_pos[1] = target_y
            elif keeper_pos[1] < target_y:
                keeper_pos[1] += 15
                if keeper_pos[1] > target_y:
                    keeper_pos[1] = target_y

            if (ball_pos[0], ball_pos[1]) == ball_target and (keeper_pos[0], keeper_pos[1]) == (target_x, target_y):
                if keeper_target == section_chosen:
                    msg = random.choice(SAVE_MESSAGES)
                    text = font.render(msg + f" Score: {score}", True, (255, 255, 255))
                    screen.blit(text, (20, HEIGHT - 40))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    return score, False
                else:
                    score += 1
                    if score >= 4:
                        msg = font.render("Gefeliciteerd, je hebt gewonnen!", True, (255, 255, 255))
                        screen.blit(msg, (20, HEIGHT - 40))
                        pygame.display.flip()
                        pygame.time.wait(1500)
                        return score, True
                    else:
                        ball_pos[:] = ball_start
                        keeper_pos[0] = WIDTH // 2
                        keeper_pos[1] = GOAL_Y + GOAL_HEIGHT - 20
                        shooting = False

        draw_field()
        draw_ball(gold=(score == 3))
        draw_keeper()
        if score == 3 and not shooting:
            gold_msg = font.render('Gouden bal!', True, GOLD)
            screen.blit(gold_msg, (WIDTH // 2 - gold_msg.get_width() // 2, HEIGHT - 70))
        score_text = font.render(f"Score: {score}", True, (255, 255, 0))
        hs_text = font.render(f"Highscore: {highscore}", True, (255, 255, 255))
        screen.blit(score_text, (10, HEIGHT - 30))
        screen.blit(hs_text, (WIDTH - hs_text.get_width() - 10, HEIGHT - 30))
        pygame.display.flip()
        clock.tick(30)

    return score, False


def draw_field():
    screen.fill((0, 128, 0))
    # goal frame
    pygame.draw.rect(screen, (255, 255, 255), (0, GOAL_Y, WIDTH, GOAL_HEIGHT), 5)
    # simple net
    for x in range(0, WIDTH, 30):
        pygame.draw.line(screen, (200, 200, 200), (x, GOAL_Y), (x, GOAL_Y + GOAL_HEIGHT), 1)
    for y in range(GOAL_Y, GOAL_Y + GOAL_HEIGHT + 1, 20):
        pygame.draw.line(screen, (200, 200, 200), (0, y), (WIDTH, y), 1)
    # show clickable sections
    for rect in SECTION_RECTS:
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)


def draw_ball(gold=False):
    color = GOLD if gold else (255, 255, 255)
    x, y = int(ball_pos[0]), int(ball_pos[1])
    pygame.draw.circle(screen, color, (x, y), 10)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 1)
    pygame.draw.line(screen, (0, 0, 0), (x - 5, y), (x + 5, y), 1)
    pygame.draw.line(screen, (0, 0, 0), (x, y - 5), (x, y + 5), 1)


def draw_keeper():
    x, y = int(keeper_pos[0]), int(keeper_pos[1])
    body_color = (0, 0, 255)
    head_color = (255, 224, 189)
    # body
    pygame.draw.line(screen, body_color, (x, y - 20), (x, y), 4)
    # arms
    pygame.draw.line(screen, body_color, (x, y - 15), (x - 10, y - 5), 4)
    pygame.draw.line(screen, body_color, (x, y - 15), (x + 10, y - 5), 4)
    # legs
    pygame.draw.line(screen, body_color, (x, y), (x - 8, y + 20), 4)
    pygame.draw.line(screen, body_color, (x, y), (x + 8, y + 20), 4)
    # head
    pygame.draw.circle(screen, head_color, (x, y - 28), 8)


def main():
    highscore = load_highscore()
    playing = True

    while playing:
        score, won = run_game(highscore)
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        msg = "Gefeliciteerd, je hebt gewonnen!" if won else random.choice(SAVE_MESSAGES)
        end_text = font.render(msg + f" Score: {score}", True, (255, 255, 255))
        screen.blit(end_text, (20, HEIGHT // 2 - 20))
        info = font.render("Klik om opnieuw te spelen of sluit het venster", True, (255, 255, 0))
        screen.blit(info, (20, HEIGHT // 2 + 20))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    playing = False
                elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    waiting = False

    pygame.quit()


if __name__ == "__main__":
    main()
