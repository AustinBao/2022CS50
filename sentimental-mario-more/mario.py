

height = input("Height: ")

while height.isnumeric() == False or int(height) > 8 or int(height) < 1:
    height = input("Height: ")


h = int(height)

for i in range(1, h + 1):
    print((h - i) * " " + i * "#" + "  " + i * "#")
