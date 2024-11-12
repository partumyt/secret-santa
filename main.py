"""Temp"""


import random


def read_file(filename: str) -> dict:
    """
    Read file with player information and return a dictionary of players.

    :param filename: Name of the file
    :return: Dictionary with player data
    """
    output = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(",")
            line[2] = line[2].replace("Чоловік", "male").replace("Жінка", "female")
            line[3] = line[3].replace("Комп'ютерні науки", "CS").replace("IT та бізнес аналітика", "BA") \
                .replace("Право", "Law").replace("ЕПЕ", "EPE").replace("Історія", "History") \
                .replace("Філологія", "Philology").replace("Культурологія", "Culture") \
                .replace("Соціологія", "Sociology").replace("Соціальна робота", "SW") \
                .replace("Психологія", "Psychology")
            try:
                output.append((f"{line[0]} {line[1]}", line[2], line[3]))
            except IndexError:
                output.append((f"{line[0]} {line[1]}", line[2], line[3]))
        return output


def is_valid_pair(giver, receiver, previous_pairs, players):
    """
    Check if a pair of giver and receiver is valid.

    :param giver: Tuple containing giver details
    :param receiver: Tuple containing receiver details
    :param previous_pairs: Set of previously used pairs
    :param players: Dictionary of players with all information
    :return: Boolean, True if pair is valid, otherwise False
    """
    if giver == receiver:
        return False
    giver_gender = giver[1]
    receiver_gender = receiver[1]
    if giver_gender == receiver_gender:
        return False
    if (giver[0], receiver[0]) in previous_pairs:
        return False
    return True


def shuffle_pairs(players: list, max_attempts: int = 1000) -> list:
    """
    Shuffle players to create pairs for Secret Santa with specific conditions.

    :param players: List of players
    :param max_attempts: Maximum attempts to create valid pairs
    :return: List with pairs of giver and receiver, or empty if unsuccessful
    """
    for attempt in range(max_attempts):
        givers = players[:]
        receivers = givers.copy()
        pairs = []
        previous_pairs = set()

        for giver in givers:
            possible_receivers = [rec for rec in receivers if
                                  is_valid_pair(giver, rec, previous_pairs, players)]
            if not possible_receivers:
                break
            receiver = random.choice(possible_receivers)
            pairs.append((giver, receiver))
            receivers.remove(receiver)
            previous_pairs.add((giver[0], receiver[0]))
    
    missing = []
    paired_players = {pair[0] for pair in pairs}.union({pair[1] for pair in pairs})

    for player in players:
        if player not in paired_players:
            missing.append(player)

    print(pairs)
    print("\n")
    print("\n")
    print(missing)
        
    return pairs

    # If all attempts fail, return an empty list or a failure message
    print("Unable to generate valid pairs within the maximum number of attempts.")
    return []


def write_pairs_to_file(pairs: dict, players: dict, filename: str) -> None:
    """
    Write the pairs to a file with details of the receiver.

    :param pairs: Dictionary of Secret Santa pairs
    :param players: Dictionary with all player data
    :param filename: Name of the output file
    """
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Giver -> Receiver|Program|Likes|Dislikes|Wishlist|Additional\n")
        for giver, receiver in pairs.items():
            giver_name = giver[0]
            receiver_name = receiver[0]
            receiver_info = list(players[receiver])
            while len(receiver_info) < 4:
                receiver_info.append("")
            giver_info = f"{giver_name} -> {receiver_name}"
            file.write(giver_info + "\n")


def main() -> None:
    """
    Main function to execute Secret Santa pairing.
    """
    players = read_file("data.csv")
    pairs = shuffle_pairs(players)
    # write_pairs_to_file(pairs, players, "secret_santa_pairs.csv")
    # print("Pairs generated and saved to 'secret_santa_pairs.csv'.")

main()
