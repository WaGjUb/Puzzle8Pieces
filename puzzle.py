#Autor WaGjUb => (Daniel Costa Valerio)
import curses
from random import randint
def game(p):
    movements = 0
    stdscr = curses.initscr()
    curses.noecho()
    stdscr.keypad(True)
    character = None
    while (True):
        stdscr.clear()
        stdscr.refresh()
        p.printscene()
        curses.cbreak()
        character = stdscr.getkey()
       # print(character)
        if (character == 'q'):
            break
        elif (character == 's'):
            p.shuffle()
        else:
            p.move(character)
            movements += 1
            if (p.win()):
                stdscr.clear()
                stdscr.refresh()
                p.printscene()
                print("Você ganhou com {0} movimentos!".format(movements))
                stdscr.getkey()
                break
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    exit()


class puzzle(object):
    def __init__(self):
        self.pointer = [2,2] #aponta para a posicao do nulo
        self.scene = [['1','2','3'],['4','5','6'],['7','8','_']]
    def printscene(self):
        print("{0}\n\r{1}\n\r{2}\r".format(" ".join(self.scene[0])," ".join(self.scene[1])," ".join(self.scene[2])))
    def move(self, orientation):
        if ((orientation == "KEY_RIGHT") and (self.pointer[1] < 2)):
            aux = self.scene[self.pointer[0]][self.pointer[1]+1] #pega o valor da direita para trocar
            self.scene[self.pointer[0]][self.pointer[1]+1] = "_" #apaga o valor antigo
            self.scene[self.pointer[0]][self.pointer[1]] = aux #coloca o valor na posição anterior do _
            self.pointer[1] += 1 # muda o ponteiro
        elif ((orientation == "KEY_LEFT") and (self.pointer[1] > 0)):
            aux = self.scene[self.pointer[0]][self.pointer[1]-1] #pega o valor da esquerda para trocar
            self.scene[self.pointer[0]][self.pointer[1]-1] = "_" #apaga o valor antigo
            self.scene[self.pointer[0]][self.pointer[1]] = aux #coloca o valor na posição anterior do _
            self.pointer[1] -= 1 # muda o ponteiro
        elif ((orientation == "KEY_UP") and (self.pointer[0] > 0)):
            aux = self.scene[self.pointer[0]-1][self.pointer[1]] #coloca o valor de cima em aux
            self.scene[self.pointer[0]-1][self.pointer[1]] = "_" #inverte os valores
            self.scene[self.pointer[0]][self.pointer[1]] = aux #"                "
            self.pointer[0] -= 1
        elif ((orientation == "KEY_DOWN") and (self.pointer[0] < 2)):
            aux = self.scene[self.pointer[0]+1][self.pointer[1]] #coloca o valor de baixo em aux
            self.scene[self.pointer[0]+1][self.pointer[1]] = "_" #inverte os valores
            self.scene[self.pointer[0]][self.pointer[1]] = aux #"                "
            self.pointer[0] += 1
    def shuffle(self):
        dictionary = {0:"KEY_RIGHT", 1:"KEY_LEFT", 2:"KEY_UP", 3:"KEY_DOWN"}
        for i in range(0,1000):
            self.move(dictionary[randint(0,3)])
    def win(self):
        if (self.scene == [['1','2','3'],['4','5','6'],['7','8','_']]):
            return True
        else:
            return False
        
def main():
    p = puzzle()
    #p.shuffle()
    game(p)
    p.printscene()
    p.move("KEY_LEFT")
    p.printscene()


main()
