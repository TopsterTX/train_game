import os
import time
import keyboard
import math
from utils import convert_hex_to_ansi


class Train:
    def __init__(self, hex_color, position, max_speed):
        self.hex_color = hex_color
        self._position = position
        self._max_speed = max_speed
        self._accelerate = 0
        self._speed = 0
        self.segment_count = abs(position[1] - position[0])
        self.max_speed = max_speed

    @property
    def accelerate(self):
        return self._accelerate

    @property
    def max_speed(self):
        return self._max_speed

    @max_speed.setter
    def max_speed(self, new_max_speed):
        self._max_speed = new_max_speed

    @accelerate.setter
    def accelerate(self, new_accelerate):
        self._accelerate = new_accelerate
        while self.speed < self.max_speed:
            self.speed = self.speed + self.accelerate

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed


class Road:
    def __init__(self, symbol="=", count=round(os.get_terminal_size().columns - 10)):
        if count < 40:
            raise Exception("Count must be greater than 40. Please change the terminal size.")

        self.symbol = symbol
        self.count = count
        self.elements = []
        for i in range(count):
            self.elements.append(symbol)

    def change_element(self, index, symbol):
        self.elements[index] = symbol


class Game:
    def __init__(self, road: Road = Road(), train: Train = None):
        self.road = road
        self.train = train
        pass

    def __update_train_position(self):
        new_position_x = self.train.position[0] + self.train.speed
        new_position_y = self.train.position[1] + self.train.speed
        print(f"x:{new_position_x} y:{new_position_y}")
        position_x = new_position_x if new_position_x < self.road.count else 0
        position_y = new_position_y if new_position_y < self.road.count else 0

        self.train.position = [position_x, position_y]

    def __render_road(self):
        for i in range(self.road.count):
            self.road.change_element(i, self.road.symbol)

    def __render_train(self, train: Train = None):
        train = train or self.train

        road_length = self.road.count
        [start_pos, end_pos] = train.position
        int_start_pos = math.floor(start_pos)
        int_end_pos = math.floor(end_pos)
        print(f"rl:{road_length} ps:{int_start_pos} pe:{int_end_pos} tl:{train.segment_count} st:{train.speed}")

        if int_start_pos < int_end_pos:
            for i in range(int_start_pos, int_end_pos):
                self.road.change_element(i, convert_hex_to_ansi(train.hex_color))
        else:
            for i in [*range(int_start_pos, road_length), *range(0, int_end_pos)]:
                self.road.change_element(i, convert_hex_to_ansi(train.hex_color))

    def draw(self):
        print(*self.road.elements, sep="")

    def update(self):
        self.__update_train_position()
        self.__render_road()
        self.__render_train()


road = Road()
game = Game(road, train=Train(max_speed=1, hex_color="#257ca3", position=[4, 20]))

# Game tick
while True:
    if keyboard.is_pressed("esc"):
        break

    if keyboard.is_pressed("a"):
        new_speed = game.train.speed - 0.02
        game.train.speed = new_speed if new_speed > 0 else 0

    if keyboard.is_pressed("d"):
        new_speed = game.train.speed + 0.02
        game.train.speed = new_speed if new_speed < game.train.max_speed else game.train.max_speed

    game.draw()
    game.update()
    time.sleep(.01)
    os.system("clear")
