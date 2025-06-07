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
GOAL_HEIGHT = 100
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
                if GOAL_Y <= y <= GOAL_Y + GOAL_HEIGHT:
                    section_chosen = x // (WIDTH // SECTIONS)
                    ball_target = (
                        section_chosen * WIDTH // SECTIONS + WIDTH // (2 * SECTIONS),
                        GOAL_Y + 10,
                    )
                    kans = SUCCESS_CHANCES[min(score, len(SUCCESS_CHANCES) - 1)]
                    if random.random() < kans:
                        choices = [i for i in range(SECTIONS) if i != section_chosen]
                        keeper_target = random.choice(choices)
                    else:
                        keeper_target = section_chosen
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
    # goal
    pygame.draw.rect(screen, (255, 255, 255), (0, GOAL_Y, WIDTH, GOAL_HEIGHT), 3)
    # divide goal into sections
    for i in range(1, SECTIONS):
        x = i * WIDTH // SECTIONS
        pygame.draw.line(screen, (255, 255, 255), (x, GOAL_Y), (x, GOAL_Y + GOAL_HEIGHT), 1)


def draw_ball(gold=False):
    color = GOLD if gold else (255, 255, 255)
    pygame.draw.circle(screen, color, (int(ball_pos[0]), int(ball_pos[1])), 10)


def draw_keeper():
    pygame.draw.rect(screen, (0, 0, 255), (int(keeper_pos[0]) - 15, int(keeper_pos[1]) - 20, 30, 40))


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
