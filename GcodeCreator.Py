import random

# Page params
LineSpacing = 8.06
NumOfLines = 27
MaxLen = 165

# Randomization params
MinLetterSpacing = 0
MaxLetterSpacing = 0
MinLetterYOfst = 0
MaxLetterYOfst = 0
MaxWordSpacing = 5
MinWordSpacing = 2
LetterVersions = ["1", "2", "3"]

# Gcode params
PenUpCode = "G0 Z3.5\n"
PenDownCode = "G0 Z0\n"
PageTurnCode = "PAUSE\n"
StartGcode = "G90\nG1 F30000\n"
EndGcode = "G1 X0 Y0"


class Page:
    def __init__(self):
        self.LineNum = NumOfLines
        self.Xmax = 0
        self.YatXmax = 0
        self.FinalX = 0
        self.FinalY = 0
        self.XJP = 0
        self.FinalXJP = 0
        self.Xpos = 0
        self.Ypos = self.LineNum * LineSpacing
        self.GcodeBuffer = ""
        self.LetterXOfst = 0
        self.LetterYOfst = 0

    def RandomizeLetterXY(self):
        self.LetterXOfst = -P.XJP
        self.LetterYOfst = round(random.uniform(MinLetterYOfst, MaxLetterYOfst), 4)

    def NewLine(self):
        if self.LineNum > 0:
            self.LineNum -= 1
        else:
            output.write(PageTurnCode)
            self.LineNum = NumOfLines
        self.Xpos = 0
        self.Ypos = P.LineNum * LineSpacing


def CalcCursiveSpace(P, RefLine):
    Words = RefLine.split()
    for Word in Words:
        if "X" in Word:
            Word = Word[1:]
            X = float(Word)
        elif "Y" in Word:
            Word = Word[1:]
            Y = float(Word)
            if abs(P.FinalY - Y) < 0.5 and X < P.XJP:
                P.XJP = X
                print("XJP =", P.XJP)


def ExtractFinalXY(P, RefLine):
    Words = RefLine.split()
    for Word in Words:
        if "X" in Word:
            Word = Word[1:]
            P.FinalX = float(Word)
        elif "Y" in Word:
            Word = Word[1:]
            P.FinalY = float(Word)


def CheckWrite(P, Word):
    if P.Xpos > MaxLen:
        P.NewLine()
        P.GcodeBuffer = ""
        ProcessWord(P, Word)
    else:
        output.write(P.GcodeBuffer)
        P.GcodeBuffer = ""


def ProcessGcodeLine(P, RefLine):
    if RefLine == "U\n":
        P.GcodeBuffer += PenUpCode
    elif RefLine == "D\n":
        P.GcodeBuffer += PenDownCode
    else:
        Words = RefLine.split()
        X = 0
        Y = 0
        for Word in Words:
            if "X" in Word:
                Word = Word[1:]
                X = float(Word)
                Xtotal = X + P.Xpos + P.LetterXOfst
                Xtotal = round(Xtotal, 4)
                Word = "X" + str(Xtotal)
            elif "Y" in Word:
                Word = Word[1:]
                Y = float(Word)
                Ytotal = Y + P.Ypos + P.LetterYOfst
                Y = round(Ytotal, 4)
                Word = "Y" + str(Ytotal)
            if X > P.Xmax:
                P.Xmax = X
                P.YatXmax = Y
        P.GcodeBuffer += Word + " "
    P.GcodeBuffer += "\n"


def ProcessWord(P, Word):
    for Letter in Word:
        P.XJP = 100
        P.RandomizeLetterXY()
        LetterChoice = random.choice(LetterVersions)
        LetterTag = Letter + LetterChoice + "<\n"
        print("LetterTag= ", LetterTag)
        print_content = False
        reference.seek(0)
        content = []
        print("Xpos = ", P.Xpos)
        for line in reference:
            if line == LetterTag:
                print_content = True
                continue
            elif line == ">\n":
                print_content = False
            if print_content:
                content.append(line)
        for line in content:
            CalcCursiveSpace(P, line)
        P.Xpos = P.Xpos - P.XJP
        P.Xpos = round(P.Xpos, 4)
        for line in content:
            ProcessGcodeLine(P, line)
        ExtractFinalXY(P, content[-2])
        print("Final X= ", P.FinalX)
        print("Final Y= ", P.FinalY)
        P.Xpos = P.Xpos + P.FinalX
        P.Xpos = round(P.Xpos, 4)
        P.Xmax = 0
    CheckWrite(P, Word)
    Space = round(random.uniform(MinWordSpacing, MaxWordSpacing), 4)
    P.Xpos += Space


def CentreWrite():
    i = 0


def ProcessLine(P, InputLine):
    if InputLine == ":p:\n":
        output.write(PageTurnCode)
        P.Xpos = 0
        P.LineNum = NumOfLines
        P.Ypos = P.LineNum * LineSpacing
    elif InputLine == ":c:\n":
        InputLine = input.readline()
    else:
        Words = InputLine.split()
        for Word in Words:
            ProcessWord(P, Word)


with open("input.txt", encoding='utf-8') as input, open("SM2.txt", encoding='utf-8') as reference, open("output.gcode", 'w',
                                                                                                     encoding='utf-8') as output:
    P = Page()
    output.write(StartGcode)
    while True:
        Line = input.readline()
        if not Line:
            break
        ProcessLine(P, Line)
        P.NewLine()
    output.write(EndGcode)
