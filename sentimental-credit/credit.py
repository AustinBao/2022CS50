def CardChecker():
    creditcard = input("Number: ")

    while creditcard.isnumeric() == False or len(creditcard) > 16 or len(creditcard) < 13:
        return "INVALID"

    sum = 0
    card_len = len(creditcard)

    # takes care of all digits starting from the end
    j = -2
    for i in range(0, card_len // 2):

        num = int(creditcard[j]) * 2
        j -= 2

        if len(str(num)) > 1:
            for digit in str(num):
                sum += int(digit)
        else:
            sum += num

    # takes care of all digits directly after the end
    k = -1
    if card_len % 2 != 0:
        for i in range(0, card_len // 2 + 1):

            sum += int(creditcard[k])
            k -= 2
    else:
        for i in range(0, card_len // 2):

            sum += int(creditcard[k])
            k -= 2

    if int(str(sum)[-1]) == 0:
        print(cardType(creditcard))
        return 0
    else:
        print("INVALID")
        return 1


def cardType(cc):

    firsttwo = cc[0:2]

    if firsttwo == "34" or firsttwo == "37":
        if len(cc) == 15:
            return "AMEX"

    # if firsttwo == "51" or firsttwo == "52" or firsttwo == "53" or firsttwo == "54" or firsttwo == "55":

    if int(firsttwo) in range(51, 55 + 1):
        if len(cc) == 16:
            return "MASTERCARD"

    if firsttwo[0] == "4":
        if len(cc) in range(13, 16 + 1):
            return "VISA"

    return "INVALID"


print(CardChecker())
