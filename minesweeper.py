import random
from typing import List, Tuple, Set


class Cell:

    def __init__(self, around_mines: int = 0, mine: bool = False, fl_open: bool = False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = fl_open


class GamePole:

    def __init__(self, n: int, m: int):
        if m > n ** 2:
            raise ValueError("Количество мин на поле не может быть больше количества ячеек")
        self.pole_size = n  # Размер одной стороны поля
        self.mines_count = m  # Количество мин
        self.mines_matrix = set()  # Координаты всех мин
        self.pole: List[List[Cell]] = []  # Поле игры
        self.closed_cells = n ** 2  # Количество закрытых ячеек
        self.game_over = False  # Флаг для указания продолжается ли игра
        self.init()

    def init(self):
        r"""Инициализируем новую игру"""
        self.mines_matrix = self.generate_mines_matrix()
        self.pole = self.generate_pole()
        self.run()

    def generate_mines_matrix(self) -> Set[Tuple[int, int]]:
        r"""Генерирует координаты расположения мин на поле"""
        mines_matrix = set()
        while len(mines_matrix) < self.mines_count:
            mines_matrix.add((random.randint(0, self.pole_size - 1), random.randint(0, self.pole_size - 1)))
        return mines_matrix

    def scan_around_cell(self, coords: Tuple[int, int]):
        r"""Выдает координаты полей вокруг закрытой ячейки"""
        cells = set()
        for i in range(coords[0] - 1, coords[0] + 2):
            for j in range(coords[1] - 1, coords[1] + 2):
                if 0 <= i < self.pole_size and 0 <= j < self.pole_size and (
                        i, j
                ) != coords:  # Исключая само рассматриваемое поле
                    cells.add((i, j))
        return cells

    def generate_pole(self) -> List[List[Cell]]:
        r"""Генерирует игровое поле"""
        pole = []
        for y in range(self.pole_size):
            line = []
            for x in range(self.pole_size):
                scan_around = self.scan_around_cell((y, x))
                around_mines = len(self.mines_matrix.intersection(
                    scan_around))  # Количество пересечений соседних полей с координатами мин
                mine = False
                if (y, x) in self.mines_matrix:
                    mine = True
                cell = Cell(around_mines=around_mines, mine=mine)
                line.append(cell)
            pole.append(line)
        return pole

    def show(self):
        r"""Отображает игровое поле в консоли"""
        for line in self.pole:
            for cell in line:
                print("#" if cell.fl_open is False else "*" if cell.mine is True else
                0 if cell.around_mines == 0 else cell.around_mines, end=" ")
            print()

    # Методы управления

    def open_cell(self, coords: Tuple[int, int], user_action: bool = False):
        r"""Открывает ячейку с заданными координатами"""
        y = coords[0]  # y - номер строки
        x = coords[1]  # x - номер столбца
        if x >= self.pole_size or x < 0 or y >= self.pole_size or y < 0:
            return
        cell = self.pole[y][x]

        # Если клетка уже открыта никаких действий с полем не выполняется
        if cell.fl_open:
            if user_action:
                print("Эта клетка уже открыта!")
            return

        # Иначе открываем клетку
        cell.fl_open = True
        self.closed_cells -= 1  # Количество закрытых клеток уменьшается
        if self.closed_cells == self.mines_count:
            # Если количество закрытых клеток равно количеству мин, игра заканчивается - Победа
            self.game_over = True
        if cell.around_mines == 0 and cell.mine is not True:
            # Если вокруг нет мины, а сама клетка - не мина рекурсивно проходим по 8 клеткам вокруг
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if 0 <= i < self.pole_size and 0 <= j < self.pole_size and (i, j) != (y, x):
                        self.open_cell((i, j))
        else:
            if cell.mine:
                print("Взрыв!")
                self.game_over = True
            return

    def run(self):
        r"""Запуск игры"""
        self.show()
        if self.game_over:
            print("Игра завершена, спасибо!")
            action = input("Хотите сыграть еще? Y/N ")
            match action.lower():
                case "y":
                    return self.reset()
                case "n":
                    print("Хорошо! До свидания!")
                    return
                case _:
                    return self.run()
        action = input(
            "Введите координаты поля, которое хотите открыть. Номер строки и номер столбца через пробел: ").strip()
        print()
        try:
            y, x = action.split(' ')
            coords = (int(y) - 1, int(x) - 1)
            if 0 <= coords[0] < self.pole_size and 0 <= coords[1] < self.pole_size:
                self.open_cell(coords, user_action=True)
                return self.run()
            else:
                if coords[0] == 0 or coords[1] == 0:
                    print("\nПользователь, вы что, программист? У всех нормальных людей счет начинается с 1\n")
                else:
                    print("\nУказанные координаты находятся за пределами игрового поля\n")
                return self.run()
        except ValueError:
            print("Повторите попытку. Координаты должны быть двумя целыми числами")
            return self.run()

    def reset(self):
        self.mines_matrix = set()
        self.pole = []
        self.closed_cells = self.pole_size ** 2
        self.game_over = False
        self.init()


if __name__ == "__main__":
    pole_game = GamePole(10, 12)
