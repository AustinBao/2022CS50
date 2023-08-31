import csv
import sys


def main():

    file_to_str = ""
    database_to_dict = {}

    # checks user input
    if len(sys.argv) != 3:
        print("file.csv, file.text")
        return
    else:
        file_csv = sys.argv[1]
        file_name = sys.argv[2]

    database = open(file_csv, "r")
    csv_reader = csv.reader(database)

    # first row of csv file
    dna_types = next(csv_reader)

    # gets rid of "name" in dna_types
    dna_types.pop(0)

    # reads csv into dictionary
    for row in csv_reader:
        database_to_dict[row[0]] = row[1:]

    # reads txt file into list
    actual_file = open(file_name, "r")
    for dna in actual_file.read():
        file_to_str += dna

    # finds the longest for each STR
    longest = []
    for dna in dna_types:
        index = 0
        max = 0
        curr = 0
        while index < len(file_to_str):
            STR = file_to_str[index: index + len(dna)]

            if STR == dna:
                curr += 1
                index += len(STR)
            else:
                if curr > max:
                    max = curr

                curr = 0
                index += 1

        longest.append(str(max))

    # Checks database for matching profiles
    for keys in database_to_dict:
        if database_to_dict[keys] == longest:
            print(keys)
            return

    print("No match")
    return


main()
