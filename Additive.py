import sys
def convert(text): #converts text to ASCII representations for easier handling
    return [ord(i) for i in text]
def deconvert(numbers):
    return [chr(i) for i in numbers]
def additive(key, text):
    text = convert(text)
    key = key % 26
    for x in range(len(text)):
        if text[x] == 13 or text[x] == 32:  #32 for new line and 13 for space in ASCII
            continue
        text[x] =((text[x] + key) % 91)
        if text[x] < 65: text[x] = text[x] + 65 #to keep in ASCII range between A and Z
    text = deconvert(text) #convert back to textrepresentation
    return "".join(text)
def bruteforce(crypt):
    for i in range(26):
        solution = additive(-i, crypt)
        print("".join(solution))
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")
output.write(additive(sys.argv[3], input.read()))
input.close()
output.close()
