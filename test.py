import random


def read_file(filename: str) -> dict:
    """
    Read file with player information and return a dictionary of players.

    :param filename: Name of the file
    :return: Dictionary with player data
    """
    output = {}
    with open(filename, "r", encoding="utf-8") as file:
        next(file)
        for line in file:
            line = line.strip().split("|")
            line[2] = line[2].replace("Чоловік", "male").replace("Жінка", "female")
            line[3] = line[3].replace("Комп'ютерні науки", "CS").replace("IT та бізнес аналітика", "BA") \
                .replace("Право", "Law").replace("ЕПЕ", "EPE").replace("Історія", "History") \
                .replace("Філологія", "Philology").replace("Культурологія", "Culture") \
                .replace("Соціологія", "Sociology").replace("Соціальна робота", "SW") \
                .replace("Психологія", "Psychology")
            try:
                output.setdefault((f"{line[0]} {line[1]}", line[2], line[3]), (line[4], line[5], line[6], line[7]))
            except IndexError:
                output.setdefault((f"{line[0]} {line[1]}", line[2], line[3]), (line[4], line[5], line[6]))
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
    # Check if giver is the same as receiver
    if giver == receiver:
        return False

    # Check if giver and receiver are of the same gender
    giver_gender = players[giver][1]  # gender of the giver
    receiver_gender = players[receiver][1]  # gender of the receiver
    if giver_gender == receiver_gender:
        return False

    # Check if this pair has been made before
    if (giver[0], receiver[0]) in previous_pairs:
        return False

    return True


def shuffle_pairs(players: dict) -> dict:
    """
    Shuffle players to create pairs for Secret Santa with specific conditions.

    :param players: Dictionary of players
    :return: Dictionary with pairs of giver and receiver
    """
    givers = list(players.keys())
    receivers = givers.copy()
    pairs = {}
    previous_pairs = set()

    for giver in givers:
        possible_receivers = [receiver for receiver in receivers if
                              is_valid_pair(giver, receiver, previous_pairs, players)]
        if not possible_receivers:
            # Reset and re-run if valid pair could not be found
            return shuffle_pairs(players)
        receiver = random.choice(possible_receivers)
        pairs[giver] = receiver
        receivers.remove(receiver)
        previous_pairs.add((giver[0], receiver[0]))  # Store to avoid repeats in the future

    return pairs


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
            giver_name = giver[0]  # Giver's full name
            receiver_name = receiver[0]  # Receiver's full name
            receiver_info = list(players[receiver])

            # Make sure receiver_info has enough elements before using it
            while len(receiver_info) < 4:
                receiver_info.append("")  # Fill missing fields with empty strings

            # Format the output line with all details
            giver_info = f"{giver_name} -> {receiver_name} | {receiver_info[2]} | {receiver_info[0]} | {receiver_info[1]} | {receiver_info[2]} | {receiver_info[3]}"
            file.write(giver_info + "\n")


def main() -> None:
    """
    Main function to execute Secret Santa pairing.
    """
    # Read player data from the file
    players = read_file("data.csv")

    # Shuffle players and create pairs
    pairs = shuffle_pairs(players)

    # Write the pairs to the output file
    write_pairs_to_file(pairs, players, "secret_santa_pairs.csv")

    print("Pairs generated and saved to 'secret_santa_pairs.csv'.")


# Run the program
main()
