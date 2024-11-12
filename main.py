"""Module to shuffle people in Secret Santa game"""


import random

def read_file(filename: str) -> dict:
    """
    Read file

    :param filename:
    :return:
    """
    output = {}
    with (open(filename, "r", encoding="utf-8") as file):
        next(file)
        for line in file:
            line = line.strip().split("|")
            line[2] = line[2].replace("Чоловік", "male").replace("Жінка", "female")
            line[3] = line[3].replace("Комп'ютерні науки", "CS")
            line[3] = line[3].replace("IT та бізнес аналітика", "BA")
            line[3] = line[3].replace("Право", "Law")
            line[3] = line[3].replace("ЕПЕ", "EPE")
            line[3] = line[3].replace("Історія", "History")
            line[3] = line[3].replace("Філологія", "Philology")
            line[3] = line[3].replace("Культурологія", "Culture")
            line[3] = line[3].replace("Соціологія", "Sociology")
            line[3] = line[3].replace("Соціальна робота", "SW")
            line[3] = line[3].replace("Психологія", "Psychology")
            try:
                output.setdefault((f"{line[0]} {line[1]}", line[2], line[3]), (line[4], line[5], line[6], line[7]))
            except IndexError:
                output.setdefault((f"{line[0]} {line[1]}", line[2], line[3]), (line[4], line[5], line[6]))
        return output


def shuffle_pairs(players: dict) -> dict:
    """
    Shuffl pairs

    :param players:
    :return:
    """
    ...


def write_file(pairs: dict, filename: str) -> None:
    """
    Write pairs to file

    :param pairs:
    :return:
    """
    ...


def main() -> None:
    """
    Main func

    :return:
    """
    ...


print(read_file("data.csv"))