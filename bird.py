from pico2d import get_canvas_width, load_image

import game_framework


# 원본의 자세는 위에서부터 5개, 5개, 4개로 배치되어 있다.
COLUMN_EDGES = (0, 180, 362, 545, 727, 918)
ROW_EDGES = (506, 326, 151, 0)  # pico2d 이미지 좌표는 아래에서 시작한다.
BIRD_WIDTH, BIRD_HEIGHT = 110, 100
FRAME_COUNT = 14
FLAP_CYCLE_SECONDS = 1.2  # 날갯짓 한 주기에 걸리는 시간
FLAP_FRAMES_PER_SECOND = FRAME_COUNT / FLAP_CYCLE_SECONDS

# 강의의 화면 축척: 화면의 10픽셀을 실제 거리 0.3m로 정한다.
PIXEL_PER_METER = 10.0 / 0.3
FLIGHT_SPEED_KMPH = 13.0  # 학습용으로 정한 새의 속력
FLIGHT_SPEED_MPM = FLIGHT_SPEED_KMPH * 1000.0 / 60.0
FLIGHT_SPEED_MPS = FLIGHT_SPEED_MPM / 60.0
FLIGHT_SPEED_PPS = FLIGHT_SPEED_MPS * PIXEL_PER_METER


class Bird:
    image = None

    def __init__(self, x, y, direction=1, frame=0):
        if Bird.image is None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y = x, y
        self.direction = direction
        self.frame = float(frame)

    def update(self):
        self.frame = (self.frame + FLAP_FRAMES_PER_SECOND * game_framework.frame_time) % FRAME_COUNT
        # 이동 거리 = 초당 이동 거리 × 지난 시간
        self.x += self.direction * FLIGHT_SPEED_PPS * game_framework.frame_time

        # 경계를 넘은 거리만큼 반대 방향으로 되돌린다.
        left = BIRD_WIDTH / 2
        right = get_canvas_width() - BIRD_WIDTH / 2
        while self.x < left or self.x > right:
            if self.x > right:
                self.x = right - (self.x - right)
                self.direction = -1
            elif self.x < left:
                self.x = left + (left - self.x)
                self.direction = 1

    def draw(self):
        row, column = divmod(int(self.frame), 5)
        x = COLUMN_EDGES[column]
        y = ROW_EDGES[row + 1]
        width = COLUMN_EDGES[column + 1] - x
        height = ROW_EDGES[row] - y
        flip = '' if self.direction == 1 else 'h'
        Bird.image.clip_composite_draw(
            x, y, width, height,
            0, flip, self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT
        )
