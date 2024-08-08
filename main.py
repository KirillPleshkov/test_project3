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


DIRECTIONS = {
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


def ant_movement(
    field_path: str,
    pos: Tuple[int, int] = (512, 512),
    direction: str = "top",
) -> int:
    with Image.open(field_path) as img:
        img.load()

    if img.mode != IMAGE_MONOCHROME_MODE:
        raise ValueError("Неверный формат изображения")

    count_black_dots = 0

    while check_pos_in_field_zone(img.size, pos):
        current_pixel = int(img.getpixel(pos))
        new_pixel = BLACK_COLOR if current_pixel != BLACK_COLOR else WHITE_COLOR
        count_black_dots += 1 if new_pixel == BLACK_COLOR else -1

        img.putpixel(pos, new_pixel)
        direction = new_direction(direction, current_pixel)
        pos = new_pos(pos, direction)

    img.save(RESULT_FIELD_SAVE_PATH, IMAGE_FORMAT)

    return count_black_dots


def check_pos_in_field_zone(field_size: Tuple[int, int], pos: Tuple[int, int]) -> bool:
    if 0 < pos[0] < field_size[0] and 0 < pos[1] < field_size[1]:
        return True
    return False


def new_pos(old_pos: Tuple[int, int], direction: str) -> Tuple[int, int]:
    return (
        old_pos[0] + DIRECTIONS[direction]["move_x"],
        old_pos[1] + DIRECTIONS[direction]["move_y"],
    )


def new_direction(old_direction, current_pixel: int) -> str:
    return (
        DIRECTIONS[old_direction]["turn_counterclockwise"]
        if current_pixel != BLACK_COLOR
        else DIRECTIONS[old_direction]["turn_clockwise"]
    )


def main():
    start_field_path = create_start_field()
    count_black_dots = ant_movement(start_field_path)
    print(f"Количество черных точек: {count_black_dots}")


if __name__ == "__main__":
    main()
