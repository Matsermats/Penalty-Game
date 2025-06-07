import random
codex/maak-penalty-spel-met-keeper-en-random-duiken
import math
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
GOAL_Y = 60
GOAL_HEIGHT = 140
GOAL_LEFT = WIDTH // 5
GOAL_WIDTH = WIDTH - GOAL_LEFT * 2
GOAL_RIGHT = GOAL_LEFT + GOAL_WIDTH
SECTIONS = 5
SUCCESS_CHANCES = [0.8, 0.6, 0.4, 0.2]

HIGHSCORE_FILE = Path("highscore.txt")

import pygame

WIDTH, HEIGHT = 600, 400
GOAL_Y = 50
GOAL_HEIGHT = 100
SECTIONS = 3
main

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penalty Game")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

codex/maak-penalty-spel-met-keeper-en-random-duiken
# animation helpers
ball_progress = 0.0
keeper_progress = 0.0
keeper_angle = 0.0

# positions for ball and keeper
ball_start = (WIDTH // 2, HEIGHT - 60)
ball_pos = list(ball_start)
keeper_pos = [WIDTH // 2, GOAL_Y + GOAL_HEIGHT - 10]
GOLD = (255, 215, 0)
THIRD = GOAL_WIDTH // 3
HALF = GOAL_HEIGHT // 2

SECTION_RECTS = [
    pygame.Rect(GOAL_LEFT, GOAL_Y, THIRD, HALF),
    pygame.Rect(GOAL_LEFT, GOAL_Y + HALF, THIRD, HALF),
    pygame.Rect(GOAL_LEFT + THIRD, GOAL_Y, THIRD, GOAL_HEIGHT),
    pygame.Rect(GOAL_LEFT + 2 * THIRD, GOAL_Y, THIRD, HALF),
    pygame.Rect(GOAL_LEFT + 2 * THIRD, GOAL_Y + HALF, THIRD, HALF),
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
    global ball_progress, keeper_progress, keeper_angle

    score = 0
    ball_pos[:] = ball_start
    keeper_pos[0] = WIDTH // 2
    keeper_pos[1] = GOAL_Y + GOAL_HEIGHT - 10
    ball_progress = 0.0
    keeper_progress = 0.0
    keeper_angle = 0.0
    shooting = False
    ball_target = None
    keeper_target = None
    section_chosen = None
    ball_start_pos = ball_start
    keeper_start = keeper_pos[:]
    angle_target = 0
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
                        ball_start_pos = tuple(ball_pos)
                        keeper_start = keeper_pos[:]
                        chance = SUCCESS_CHANCES[min(score, len(SUCCESS_CHANCES) - 1)]
                        if random.random() < chance:
                            choices = [i for i in range(SECTIONS) if i != idx]
                            keeper_target = random.choice(choices)
                        else:
                            keeper_target = idx
                        angle_target = -40 if keeper_target in (0, 1) else 40 if keeper_target in (3, 4) else 0
                        ball_progress = 0.0
                        keeper_progress = 0.0
                        shooting = True
                        break

        if shooting:
            # smooth animation using progress variables
            ball_progress = min(ball_progress + 0.05, 1.0)
            keeper_progress = min(keeper_progress + 0.07, 1.0)

            t = ball_progress
            bx = ball_start_pos[0] + (ball_target[0] - ball_start_pos[0]) * t
            by = ball_start_pos[1] + (ball_target[1] - ball_start_pos[1]) * t
            arc = -60 * math.sin(math.pi * t)
            ball_pos[:] = [bx, by + arc]

            target_x, target_y = KEEPER_TARGETS[keeper_target]
            kx = keeper_start[0] + (target_x - keeper_start[0]) * keeper_progress
            ky = keeper_start[1] + (target_y - keeper_start[1]) * keeper_progress
            keeper_pos[:] = [kx, ky]
            keeper_angle = angle_target * keeper_progress

            if ball_progress >= 1.0 and keeper_progress >= 1.0:
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
                        keeper_pos[1] = GOAL_Y + GOAL_HEIGHT - 10
                        ball_start_pos = ball_start
                        keeper_start = keeper_pos[:]
                        keeper_angle = 0
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
    screen.fill((34, 139, 34))
    # penalty spot
    pygame.draw.circle(screen, (255, 255, 255), (WIDTH // 2, HEIGHT - 70), 3)
    # goal frame
    pygame.draw.rect(screen, (255, 255, 255), (GOAL_LEFT, GOAL_Y, GOAL_WIDTH, GOAL_HEIGHT), 5)
    # net
    for x in range(GOAL_LEFT, GOAL_RIGHT + 1, 10):
        pygame.draw.line(screen, (200, 200, 200), (x, GOAL_Y), (x, GOAL_Y + GOAL_HEIGHT), 1)
    for y in range(GOAL_Y, GOAL_Y + GOAL_HEIGHT + 1, 10):
        pygame.draw.line(screen, (200, 200, 200), (GOAL_LEFT, y), (GOAL_RIGHT, y), 1)
    # show clickable sections
    for rect in SECTION_RECTS:
        pygame.draw.rect(screen, (255, 255, 255), rect, 1)


def draw_ball(gold=False):
    color = GOLD if gold else (255, 255, 255)
    x, y = int(ball_pos[0]), int(ball_pos[1])
    radius = 12
    pygame.draw.circle(screen, color, (x, y), radius)
    pygame.draw.circle(screen, (0, 0, 0), (x, y), radius, 2)
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        end = (x + int(radius * 0.6 * math.cos(rad)), y + int(radius * 0.6 * math.sin(rad)))
        pygame.draw.line(screen, (0, 0, 0), (x, y), end, 1)
    for angle in range(30, 360, 60):
        rad = math.radians(angle)
        outer = (x + int(radius * 0.8 * math.cos(rad)), y + int(radius * 0.8 * math.sin(rad)))
        inner = (x + int(radius * 0.3 * math.cos(rad)), y + int(radius * 0.3 * math.sin(rad)))
        pygame.draw.line(screen, (0, 0, 0), outer, inner, 1)


def draw_keeper():
    angle = keeper_angle
    surf = pygame.Surface((80, 80), pygame.SRCALPHA)
    x, y = 40, 50
    jersey = (0, 0, 220)
    skin = (255, 224, 189)
    pygame.draw.rect(surf, jersey, (x - 12, y - 28, 24, 28))
    pygame.draw.line(surf, jersey, (x - 12, y - 20), (x - 24, y - 10), 5)
    pygame.draw.line(surf, jersey, (x + 12, y - 20), (x + 24, y - 10), 5)
    pygame.draw.circle(surf, skin, (x - 24, y - 10), 4)
    pygame.draw.circle(surf, skin, (x + 24, y - 10), 4)
    pygame.draw.line(surf, jersey, (x - 4, y), (x - 12, y + 22), 5)
    pygame.draw.line(surf, jersey, (x + 4, y), (x + 12, y + 22), 5)
    pygame.draw.circle(surf, skin, (x, y - 34), 10)
    pygame.draw.circle(surf, (0, 0, 0), (x, y - 34), 10, 1)
    rotated = pygame.transform.rotate(surf, angle)
    rect = rotated.get_rect(center=(int(keeper_pos[0]), int(keeper_pos[1])))
    screen.blit(rotated, rect)


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

# positions for ball and keeper
ball_start = (WIDTH // 2, HEIGHT - 50)
ball_pos = list(ball_start)
keeper_pos = [WIDTH // 2, GOAL_Y + GOAL_HEIGHT - 20]

score = 0
running = True
shooting = False
ball_target = None
keeper_target = None
section_chosen = None


def draw_field():
    screen.fill((0, 128, 0))
    # goal
    pygame.draw.rect(screen, (255, 255, 255), (0, GOAL_Y, WIDTH, GOAL_HEIGHT), 3)
    # divide goal into sections
    for i in range(1, SECTIONS):
        x = i * WIDTH // SECTIONS
        pygame.draw.line(screen, (255, 255, 255), (x, GOAL_Y), (x, GOAL_Y + GOAL_HEIGHT), 1)


def draw_ball():
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_pos[0]), int(ball_pos[1])), 10)


def draw_keeper():
    pygame.draw.rect(screen, (0, 0, 255), (int(keeper_pos[0]) - 15, int(keeper_pos[1]) - 20, 30, 40))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not shooting:
            x, y = event.pos
            if GOAL_Y <= y <= GOAL_Y + GOAL_HEIGHT:
                section_chosen = x // (WIDTH // SECTIONS)
                ball_target = (section_chosen * WIDTH // SECTIONS + WIDTH // (2 * SECTIONS), GOAL_Y + 10)
                keeper_target = random.randint(0, SECTIONS - 1)
                shooting = True

    if shooting:
        # move ball
        ball_pos[1] -= 10
        if ball_pos[1] < ball_target[1]:
            ball_pos[1] = ball_target[1]
        # move keeper
        target_x = keeper_target * WIDTH // SECTIONS + WIDTH // (2 * SECTIONS)
        if keeper_pos[0] < target_x:
            keeper_pos[0] += 15
            if keeper_pos[0] > target_x:
                keeper_pos[0] = target_x
        elif keeper_pos[0] > target_x:
            keeper_pos[0] -= 15
            if keeper_pos[0] < target_x:
                keeper_pos[0] = target_x

        if ball_pos[1] == ball_target[1] and keeper_pos[0] == target_x:
            if keeper_target == section_chosen:
                msg = font.render(f"Keeper pakt de bal! Score: {score}", True, (255, 255, 255))
                screen.blit(msg, (20, HEIGHT - 40))
                pygame.display.flip()
                pygame.time.wait(1500)
                running = False
            else:
                score += 1
                ball_pos[:] = ball_start
                keeper_pos[0] = WIDTH // 2
                shooting = False

    draw_field()
    draw_ball()
    draw_keeper()
    score_text = font.render(f"Score: {score}", True, (255, 255, 0))
    screen.blit(score_text, (10, HEIGHT - 30))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
main
