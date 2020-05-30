import sys
def convert(text): #converts text to ASCII representations for easier handling
    return [ord(i) for i in text]
def deconvert(numbers):
    return [chr(i) for i in numbers]
def additive(key, text,mode):
    text = convert(text)
    key = key % 26
    if mode == "D":	#for decrypt set "D" as 4th Argument
        key = -key
    for x in range(len(text)):
        if text[x] == ord(" ") or text[x] == ord("\n"):  #ignore newline and space
            continue
        text[x] =((text[x] - 65 + key)% 26 + 65 )  
    text = deconvert(text) #convert back to textrepresentation
    return "".join(text)
def bruteforce(crypt):
    for i in range(26):
        solution = additive(-i, crypt)
        print("".join(solution))
input = open(sys.argv[1], "r")
output = open(sys.argv[2], "w")
output.write(additive(int(sys.argv[3]), input.read(), sys.argv[4]))
input.close()
output.close()