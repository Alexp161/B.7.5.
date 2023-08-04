# Определяем класс для представления точки на игровой доске
class Point:
    def __init__(self, row, col):
        self.row = row
        self.col = col

# Определяем класс для корабля
class Ship:
    def __init__(self, points):
        self.points = points
        self.hits = set()

    def is_sunk(self):
        return set(self.points) == self.hits

    def hit(self, point):
        self.hits.add(point)

# Определяем класс для игровой доски
class Board:
    def __init__(self):
        self.ships = []

    def add_ship(self, ship):
        self.ships.append(ship)

    def is_valid_move(self, point):
        # Проверяем, что ход не был сделан ранее
        for ship in self.ships:
            if point in ship.hits:
                return False
        return True

    def make_move(self, point):
        # Выполняем ход и проверяем, было ли попадание
        for ship in self.ships:
            if point in ship.points:
                ship.hit(point)
                return True
        return False

import random

def place_ship(board, length):
    while True:
        orientation = random.choice(['horizontal', 'vertical'])
        if orientation == 'horizontal':
            row = random.randint(1, 6)
            col = random.randint(1, 7 - length)
            points = [Point(row, col+i) for i in range(length)]
        else:
            row = random.randint(1, 7 - length)
            col = random.randint(1, 6)
            points = [Point(row+i, col) for i in range(length)]

        if all(is_valid_point(p) for p in points) and not any(is_adjacent(p) for p in points):
            ship = Ship(points)
            board.add_ship(ship)
            break

def is_valid_point(point):
    return 1 <= point.row <= 6 and 1 <= point.col <= 6

def is_adjacent(point):
    return any(p in points for ship in board.ships for p in ship.points)

# Создаем игровую доску и размещаем корабли на ней
board = Board()
for length in [3, 2, 2, 1, 1, 1, 1]:
    place_ship(board, length)

# Игровой цикл
while True:
    # Выводим игровую доску в консоль
    print("   | 1 | 2 | 3 | 4 | 5 | 6 |")
    for row in range(1, 7):
        print(f"{row} | " + " | ".join(get_symbol(Point(row, col)) for col in range(1, 7)) + " |")

    # Ход игрока
    while True:
        try:
            row = int(input("Введите номер строки (от 1 до 6): "))
            col = int(input("Введите номер столбца (от 1 до 6): "))
            move = Point(row, col)
            if not is_valid_point(move):
                raise ValueError("Неверные координаты!")
            if not board.is_valid_move(move):
                raise ValueError("Вы уже стреляли в эту клетку!")
            break
        except ValueError as e:
            print(e)

    # Выполняем ход игрока
    if board.make_move(move):
        print("Попадание!")
    else:
        print("Промах!")

    # Проверяем, завершилась ли игра
    if all(ship.is_sunk() for ship in board.ships):
        print("Поздравляем! Вы победили!")
        break

    # Ход компьютера (случайный выбор клетки)
    while True:
        computer_move = Point(random.randint(1, 6), random.randint(1, 6))
        if board.is_valid_move(computer_move):
            break

    # Выполняем ход компьютера
    if board.make_move(computer_move):
        print("Компьютер попал!")
    else:
        print("Компьютер промахнулся!")

    # Проверяем, завершилась ли игра
    if all(ship.is_sunk() for ship in board.ships):
        print("Компьютер победил!")
        break
