# Program Language: Python
# Development System: Visual Studio Code

# Team Members:
# Rashmika Srivastava
# Luke Chaney
# Xavian Kimbrough
# Mitchell Bergsma

# Dates: 09/23, 09/24, 11/04
# Date Submitted: (to be filled before submission)

# Class: 4500 - Software Profession

# Explanation of Program:
# This program prompts the user to enter up to 10 .txt files, ensuring they are valid and not duplicates.
# It reads each file, extracts words according to defined rules (case-insensitive, allows hyphenated words),
# and stores them for further analysis. The user can search for a word to see how many times it appears
# in each of the files. The program ends by displaying a summary of all searched words and their counts.

# Sources:
# Python documentation for string and os modules
# Stack Overflow discussions for text processing and file validation

# External Files:
# Up to 10 user-specified .txt files stored in the same directory as the script
 
import string
import os

def programexplaining():
    print("""
This program will do several things:
- It will ask you for up to 10 filenames that end with '.txt'.
- It will read the contents of each file, splitting them into words.
- A word is a sequence of letters or hyphenated letters.
- It will then prompt you to search for words and count their occurrences across all files.
- The program is case-insensitive and handles hyphenated words correctly.
- A summary table will be shown with your search history.
- Two new files will be created for a Concordance and Extra lists.
- Both the Concodance and Extra lists will be printed to the screen.
- The extra lists are Top Ten Words, Words in All Files, and Words in Only One File. 
    """)

def inputtextfile():
    file_paths = []
    max_files = 10

    while len(file_paths) < max_files:
        file_name = input("Please input text file name (must end in .txt): ").strip()

        if not file_name.lower().endswith(".txt"):
            print("Error: File must end in .txt (case insensitive).")
            continue

        if file_name in file_paths:
            print("Error: You have already added this file.")
            continue

        if not os.path.isfile(file_name):
            print("Error: File not found in directory.")
            continue

        file_paths.append(file_name)

        if len(file_paths) < max_files:
            while True:
                more = input("Do you want to add another file? [yes/no]: ").strip() 
                if more in ['Yes','yes','Y','y']:                          
                    break
                elif more in ['No','no','N','n']:
                    return file_paths
                else:
                    print("Invalid response. Please enter yes or no.")

    return file_paths

def extract_words_from_file(filename):
    words = []
    with open(filename, "r", encoding='utf-8') as f:
        lines = f.readlines()

    buffer = ""
    for line in lines:
        line = line.strip()
        if line.endswith("-") and not line.endswith(" -"):
            buffer += line[:-1]
            continue
        else:
            buffer += line

        word = ""
        for char in buffer:
            if char.isalpha() or char == '-':
                word += char
            else:
                if word:
                    words.append(word.lower())
                    word = ""
        if word:
            words.append(word.lower())
        buffer = ""

    return words

def process_files(file_paths):
    all_words = {}  # { filename: [list of words] }
    word_stats = {} # { filename: { word: count } }

    for file in file_paths:
        words = extract_words_from_file(file)
        all_words[file] = words
        stats = {}
        for word in words:
            stats[word] = stats.get(word, 0) + 1
        word_stats[file] = stats

    return all_words, word_stats

def display_file_summary(file_paths, all_words):
    file_max_length = max(len(f) for f in file_paths)
    print(file_max_length)
    print("\nFilename".ljust(file_max_length) + "Total Words".rjust(file_max_length*2) + "Distinct Words".rjust(file_max_length*2))
    print("-" * file_max_length*5)
    for file in file_paths:
        total = len(all_words[file])
        distinct = len(set(all_words[file]))
        print(f"{str(file).ljust(file_max_length)}{str(total).rjust(file_max_length*2)}{str(distinct).rjust(file_max_length*2)}")
    print()

def is_valid_word(word):
    legal_characters = set(string.ascii_letters + '-')
    if not word:
        return False, "Word cannot be empty."
    for idx, char in enumerate(word):
        if char not in legal_characters:
            return False, f"Illegal character '{char}' at position {idx + 1}."
    return True, ""

def prompt_for_word(): 
    while True:
        word = input("Enter a word to search (letters and hyphens only): ")
        is_valid, message = is_valid_word(word)
        if is_valid:
            return word.lower()
        else:
            print("Invalid word:", message)

def prompt_yes_no(question):
    while True:
        response = input(question + " [yes/no]: ").strip()
        if response in ['Yes', 'yes', 'y', 'Y]']:
            return True
        elif response in ['No', 'no', 'n', 'N']:
            return False
        else:
            print("Invalid input. Please enter The user is allowed to answer Yes, No, yes, no, y, Y, n, or N.")

def search_words_loop(file_paths, word_stats):
    searched_words = []
    while True:
        word = prompt_for_word()
        searched_words.append(word)
        print(f"\nOccurrences of '{word}':")
        for file in file_paths:
            count = word_stats[file].get(word.lower(), 0)
            print(f"{file.rjust(25)} : {count}")
        print()

        if not prompt_yes_no("Do you want to enter another word?"):
            break

    return searched_words

# ------------------- SG2 ADDITIONS -------------------
def build_concordance(file_paths):
    concordance = {}
    for f_index, filename in enumerate(file_paths, start=1):
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for l_index, line in enumerate(lines, start=1):
            words = []
            buffer = ""
            line = line.strip()
            if line.endswith("-") and not line.endswith(" -"):
                buffer += line[:-1]
                continue
            else:
                buffer += line
            word = ""
            for char in buffer:
                if char.isalpha() or char == '-':
                    word += char
                else:
                    if word:
                        words.append(word.lower())
                        word = ""
            if word:
                words.append(word.lower())

            for w_index, word in enumerate(words, start=1):
                if word not in concordance:
                    concordance[word] = []
                concordance[word].append(f"{f_index}.{l_index}.{w_index}")
    return concordance

def write_concordance(concordance):
    sorted_words = sorted(concordance.keys())
    with open("CONCORDANCE.TXT", "w", encoding="utf-8") as out:
        for word in sorted_words:
            places = "; ".join(sorted(concordance[word], key=lambda x: list(map(int, x.split('.'))))) + "."
            line = f"{word} {places}"
            print(line)
            out.write(line + "\n")

def generate_extra_lists(file_paths, concordance):
    from collections import Counter
    # Flatten word data
    word_counts = Counter()
    file_occurrences = {word: set() for word in concordance}

    for word, locations in concordance.items():
        for loc in locations:
            fnum = int(loc.split(".")[0])
            file_occurrences[word].add(fnum)
            word_counts[word] += 1

    # Top 10
    top_ten = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))[:10]

    # Words in all files
    words_in_all = [w for w, files in file_occurrences.items() if len(files) == len(file_paths)]

    # Words only in one file
    words_in_one = [(w, list(files)[0]) for w, files in file_occurrences.items() if len(files) == 1]

    return top_ten, words_in_all, words_in_one, file_occurrences

def write_extra_lists(top_ten, words_in_all, words_in_one, file_occurrences):
    with open("ExtraLists.txt", "w", encoding="utf-8") as out:
        # Top Ten
        header = f"{'WORD':>20} {'COUNT':>10} {'FILES':>10}"
        print("\nTOP TEN WORDS:\n" + header)
        out.write("TOP TEN WORDS:\n" + header + "\n")

        for word, count in top_ten:
            files = (len(file_occurrences[word])) #was "files = "?"" 
            print(f"{word:>20} {count:>10} {files:>10}")
            out.write(f"{word:>20} {count:>10} {files:>10}\n")


        # Words in all files
        print("\nWORDS IN ALL FILES:")
        out.write("\n\nWORDS IN ALL FILES:\n")
        for w in sorted(words_in_all):
            print(f"{w:>20}")
            out.write(f"{w:>20}\n")

        # Words in one file
        print("\nWORDS THAT APPEAR IN ONLY ONE FILE:\n")
        out.write("\n\nWORDS THAT APPEAR IN ONLY ONE FILE:\n")
        print(f"{'WORD':>20} {'FILE':>10}")
        out.write(f"{'WORD':>20} {'FILE':>10}\n")
        for w, fnum in sorted(words_in_one, key=lambda x: (x[1], x[0])):
            print(f"{w:>20} {fnum:>10}")
            out.write(f"{w:>20} {fnum:>10}\n")

# ------------------- MODIFY END OF SG1 -------------------

def display_summary(file_paths, word_stats, searched_words):
    print("\nSummary of all searched words:\n")
    header = "Word".ljust(20)
    for file in file_paths:
        header += file.rjust(20)
    print(header)
    print("-" * len(header))

    for word in searched_words:
        line = word.ljust(20)
        for file in file_paths:
            count = word_stats[file].get(word.lower(), 0)
            line += str(count).rjust(20)
        print(line)

    input("\nPress ENTER to continue to concordance and extra lists...")

    # NEW SG2 SECTION
    concordance = build_concordance(file_paths)
    write_concordance(concordance)

    top_ten, words_in_all, words_in_one, file_occurrences = generate_extra_lists(file_paths, concordance)
    write_extra_lists(top_ten, words_in_all, words_in_one, file_occurrences)

    print("\nAll reports written successfully. Program complete.")
    
#----------- MAIN PROGRAM EXECUTION --------------
def main():
    programexplaining()
    file_paths = inputtextfile()
    all_words, word_stats = process_files(file_paths)
    display_file_summary(file_paths, all_words)
    searched_words = search_words_loop(file_paths, word_stats)
    display_summary(file_paths, word_stats, searched_words)
    
if __name__ == "__main__":
    main()

