import random

def secret_santa_pairing(filename: str, max_attempts: int = 1000) -> list:
    """
    Generate Secret Santa pairs with prioritized conditions:
    1. Pair each male with a female.
    2. Ensure pairs are from different programs if possible.
    3. If conditions are not met within max_attempts, pair remaining players without conditions.
    
    :param filename: Path to the file containing player information.
    :param max_attempts: Maximum number of pairing attempts before relaxing conditions.
    :return: List of pairs [(giver, receiver), ...]
    """
    # Read player data
    players = []
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip().split(",")
            name, gender, program = f"{line[0]} {line[1]}", line[2], line[3]
            players.append((name, gender, program))
    
    # Attempt pairing with prioritized conditions
    for attempt in range(max_attempts):
        givers = players[:]
        receivers = givers.copy()
        pairs = []
        
        # Try to pair each male with a female from a different program
        for giver in givers[:]:
            if giver[1] == "male":  # Check for males
                valid_females = [rec for rec in receivers if rec[1] == "female" and rec[2] != giver[2]]
                if valid_females:
                    receiver = random.choice(valid_females)
                    pairs.append((giver, receiver))
                    receivers.remove(receiver)
                    givers.remove(giver)
        
        # Pair remaining players, prioritizing different programs
        for giver in givers[:]:
            valid_receivers = [rec for rec in receivers if rec != giver and rec[2] != giver[2]]
            if not valid_receivers:
                valid_receivers = [rec for rec in receivers if rec != giver]  # Relax condition if needed
            if valid_receivers:
                receiver = random.choice(valid_receivers)
                pairs.append((giver, receiver))
                receivers.remove(receiver)
                givers.remove(giver)
        
        # If all players are paired, return the pairs
        if not givers and not receivers:
            return pairs  # Successfully generated pairs

    # If all attempts fail, pair remaining players without conditions
    print("Unable to generate valid pairs within prioritized conditions. Pairing without restrictions.")
    random.shuffle(players)
    pairs = [(players[i], players[i + 1]) for i in range(0, len(players), 2)]
    
    return pairs

# Example Usage
pairs = secret_santa_pairing("data.csv")
for giver, receiver in pairs:
    print(f"{giver[0], giver[2]} -> {receiver[0], receiver[2]}")


with open("pairs.txt", "w", encoding="utf-8") as f:
    pairs = secret_santa_pairing("data.csv")
    for giver, receiver in pairs:
        f.write(f"{giver[0], giver[2]} -> {receiver[0], receiver[2]}\n")