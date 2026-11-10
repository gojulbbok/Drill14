from pico2d import *
from random import randint

import game_framework
import game_world
from bird import Bird, BIRD_HEIGHT


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    for index in range(10):
        x = 160 + (index % 5) * 320
        # 이미지가 위아래 경계를 벗어나지 않는 범위에서 높이를 정한다.
        y = randint(BIRD_HEIGHT // 2, get_canvas_height() - BIRD_HEIGHT // 2)
        direction = 1 if index % 2 == 0 else -1
        game_world.add_oject(Bird(x, y, direction, index))


def pause():
    pass


def resume():
    pass


def finish():
    game_world.clear()


def update():
    game_world.update()


def render():
    clear_canvas()
    game_world.render()
    update_canvas()
