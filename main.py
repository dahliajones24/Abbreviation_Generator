import logging
import re

# DEFINE FUNCTION 'READ_NAMES' TO TAKE FILE PATH AS AN ARGUMENT
def read_names(file_path):
    # ERROR HANDLING
    try:
        with open(file_path, 'r') as file:
            return [name.strip() for name in file.readlines()]
    except FileNotFoundError:
        logging.error(f"Error: FILE NOT FOUND AT {file_path}")
        return []

# DEFINE FUNCTION 'READ_VALUES' TO READ VALUES FROM VALUES.TXT
def read_values(file_path):
    try:
        with open(file_path, 'r') as file:
            return {letter: int(score) for line in file for letter, score in [line.strip().split()]}
    except FileNotFoundError:
        logging.error(f"Error: FILE NOT FOUND AT {file_path}")
        return {}

# CALCULATE SCORE FOR AN ABBREVIATION
def calculate_score(abbreviation, word, values):
    score = 0

    for i, letter in enumerate(abbreviation):
        if i == 0:
            continue  # RULE: FIRST LETTER HAS A SCORE OF 0
        elif i == 1 and letter == word[-1]:
            score += 20 if letter == 'E' else 5
        else:
            position_value = 1 if i == 1 else 2 if i == 2 else 3
            score += position_value + values.get(letter.upper(), 0)

    return score

# Updated generate_abbreviations function
def generate_abbreviations(names, values):
    abbreviations = {}

    for name in names:
        # RULE: IGNORE APOSTROPHES AND GET FIRST LETTER
        first_letter = re.sub(r'[^a-zA-Z]', '', name)[0].upper()
        words = [word.strip("'") for word in name.split()]

        # Create a set to track used letters for the current name
        used_letters = set()

        abbreviation = first_letter
        for word in words:
            for i, letter in enumerate(word):
                if i == 0:
                    continue  # Skip the first letter in a word
                if i == len(word) - 1:
                    score = 20 if letter == 'E' else 5
                else:
                    position_value = 1 if i == 1 else 2 if i == 2 else 3
                    score = position_value + values.get(letter.upper(), 0)

                if letter not in used_letters:
                    abbreviation += letter.upper()
                    used_letters.add(letter)
                    break

        # Ensure the abbreviation is at least 3 letters long
        while len(abbreviation) < 3 and len(name) > 1:
            for letter in name[1:]:
                if letter not in used_letters:
                    abbreviation += letter.upper()
                    used_letters.add(letter)
                    break

        score = calculate_score(abbreviation, name, values)

        if abbreviation not in abbreviations or score > abbreviations[abbreviation][1]:
            abbreviations[abbreviation] = (name, score)

    return abbreviations


# GENERATE THREE-LETTER ABBREVIATIONS FOR EACH NAME
def generate_abbreviations(names, values):
    abbreviations = {}

    for name in names:
        # RULE: IGNORE APOSTROPHES AND GET FIRST LETTER
        first_letter = re.sub(r'[^a-zA-Z]', '', name)[0].upper()
        words = [word.strip("'") for word in name.split()]

        # Create a set to track used letters for the current name
        used_letters = set()
        
        abbreviation = first_letter
        for word in words:
            for letter in word[1:]:
                if letter not in used_letters:
                    abbreviation += letter.upper()
                    used_letters.add(letter)
                    break

        # For single-letter words, if the abbreviation is less than 3 letters, add additional letters
        while len(abbreviation) < 3:
            for letter in name[1:]:
                if letter not in used_letters:
                    abbreviation += letter.upper()
                    used_letters.add(letter)
                    break

        score = calculate_score(abbreviation, name, values)

        if abbreviation not in abbreviations or score > abbreviations[abbreviation][1]:
            abbreviations[abbreviation] = (name, score)

    return abbreviations

# PRINT ABBREVIATIONS AND CORRESPONDING NAMES
def print_abbreviations(abbreviations):
    for abbreviation, (name, score) in abbreviations.items():
        print(f"{abbreviation}:{name} (Score: {score})")

# EXECUTE THE PROGRAM
def main():
    logging.basicConfig(level=logging.INFO)

    # SPECIFYING FILE PATHS
    file_path = "trees.txt"
    values_file_path = "values.txt"

    # REMOVE SPACES FROM FILE PATHS
    file_path = file_path.replace(" ", "")
    values_file_path = values_file_path.replace(" ", "")

    names = read_names(file_path)
    values = read_values(values_file_path)
    abbreviations = generate_abbreviations(names, values)

    # RULE: PRINT ABBREVIATIONS WITHOUT APOSTROPHES
    print_abbreviations(abbreviations)

if __name__ == "__main__":
    main()