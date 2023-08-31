import math


def readability():
    text = input("Text: ")

    # IMPORTANT: set word counter = 1 since we don't account for the last word in the sentence since there are no more white spaces afterwards.
    letter_counter = 0
    word_counter = 1
    sentence_counter = 0

    for letter in text:

        if letter.isalpha() == True:
            letter_counter += 1

        if letter.isspace() == True:
            word_counter += 1

        if letter == "." or letter == "!" or letter == "?":
            sentence_counter += 1

    average_letters = float(letter_counter / word_counter * 100)
    average_sentences = float(sentence_counter / word_counter * 100)

    index = round(0.0588 * average_letters - 0.296 * average_sentences - 15.8)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")


readability()
