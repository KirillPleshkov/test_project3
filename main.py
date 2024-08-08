from typing import Tuple
from PIL import Image

WHITE_COLOR = 1
BLACK_COLOR = 0
IMAGE_MONOCHROME_MODE = "1"
START_FIELD_SAVE_PATH = "start_field.png"
RESULT_FIELD_SAVE_PATH = "result_field.png"
IMAGE_FORMAT = "PNG"


def create_start_field(size: Tuple[int, int] = (1024, 1024)) -> str:
    img = Image.new(IMAGE_MONOCHROME_MODE, size, color=WHITE_COLOR)
    img.save(START_FIELD_SAVE_PATH, IMAGE_FORMAT)
    return START_FIELD_SAVE_PATH


class Ant:

    directions = {
        "top": {
            "move_x": 0,
            "move_y": -1,
            "turn_counterclockwise": "left",
            "turn_clockwise": "right",
        },
        "right": {
            "move_x": 1,
            "move_y": 0,
            "turn_counterclockwise": "top",
            "turn_clockwise": "bottom",
        },
        "bottom": {
            "move_x": 0,
            "move_y": 1,
            "turn_counterclockwise": "right",
            "turn_clockwise": "left",
        },
        "left": {
            "move_x": -1,
            "move_y": 0,
            "turn_counterclockwise": "bottom",
            "turn_clockwise": "top",
        },
    }

    def __init__(
        self,
        field_path: str,
        start_pos: Tuple[int, int] = (512, 512),
        start_direction: str = "top",
    ):
        self.__field_path = field_path
        self.__pos = start_pos
        self.__direction = start_direction
        self.__count_black_dots = 0

    def movement_trajectory(self):
        with Image.open(self.__field_path) as img:
            img.load()

        if img.mode != IMAGE_MONOCHROME_MODE:
            raise ValueError("Неверный формат изображения")

        while self.check_pos_in_field(img.size):
            current_pixel = int(img.getpixel(self.__pos))
            new_pixel = BLACK_COLOR if current_pixel != BLACK_COLOR else WHITE_COLOR
            self.__count_black_dots += 1 if new_pixel == BLACK_COLOR else -1

            img.putpixel(self.__pos, new_pixel)
            self.rotate(current_pixel)
            self.move()

        img.save(RESULT_FIELD_SAVE_PATH, IMAGE_FORMAT)

        return self.__count_black_dots

    def check_pos_in_field(self, field_size: Tuple[int, int]):
        x_len = field_size[0]
        y_len = field_size[1]
        x_pos = self.__pos[0]
        y_pos = self.__pos[1]
        if 0 < x_pos < x_len and 0 < y_pos < y_len:
            return True
        return False

    def move(self):
        self.__pos = (
            self.__pos[0] + self.directions[self.__direction]["move_x"],
            self.__pos[1] + self.directions[self.__direction]["move_y"],
        )

    def rotate(self, current_pixel: int):
        self.__direction = (
            self.directions[self.__direction]["turn_counterclockwise"]
            if current_pixel != BLACK_COLOR
            else self.directions[self.__direction]["turn_clockwise"]
        )


def main():
    start_field_path = create_start_field()
    ant = Ant(start_field_path)
    count_black_dots = ant.movement_trajectory()
    print(f"Количество черных точек: {count_black_dots}")


if __name__ == "__main__":
    main()
