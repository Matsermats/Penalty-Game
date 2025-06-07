import random
import pygame

WIDTH, HEIGHT = 600, 400
GOAL_Y = 50
GOAL_HEIGHT = 100
SECTIONS = 3

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Penalty Game")
font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

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
