#Autor WaGjUb => (Daniel Costa Valerio)
import os
import pdb
import copy
import curses
from time import sleep
from curses import wrapper
from random import randint

def game(p):
    tick = "OFF"
    movements = 0
    stdscr = curses.initscr()
    game.a = stdscr
    curses.noecho()
    stdscr.keypad(True)
    character = None
    print("Digite [s/n] para guardar as estatisticas ou e para apenas gerar estatisticas:\r")
    character = stdscr.getkey()
    if character == "s":
        tick = "ON"
    elif character == 'e':  
        tick = 'ON'
        p.initial()
        for i in range(0,3):
            solve().aStarAndGreedy(p,solve().manhattanDistance, tick, True)
            solve().aStarAndGreedy(p,solve().manhattanDistance, tick)
            solve().aStarAndGreedy(p,solve().outOfPlace, tick, True)
            solve().aStarAndGreedy(p,solve().outOfPlace, tick)
            p.shuffle()
        print('\rEstatisticas geradas!')
        stdscr.getkey()
        exit()
    stdscr.clear()
    while (True):
        stdscr.clear()
        stdscr.refresh()
        p.printscene()
        curses.cbreak()
        character = stdscr.getkey()
        if (character == 'q'):
            break
        elif (character == 's'):
            p.shuffle()
            movements = 0
        elif (character == 'i'):
            p.initial()
            movements = 0
        elif(character == 'g' or character == 'a'):
            aStar = None
            if character == 'a':
                aStar = True
            else:
                aStar = False
            print("\rSelecione a heurística: m para manhattan e f para fora do lugar: \r")
            character = stdscr.getkey()
            print("\rDigite a velocidade de resolução em milisegundos:\r")
            curses.echo()
            speed = stdscr.getstr(0,0,5)
            #stdscr.clear()
            curses.noecho()
            result = []
            if (character == 'm'):
                result = solve().aStarAndGreedy(p,solve().manhattanDistance,tick, aStar)
            elif (character == 'f'):
                result = solve().aStarAndGreedy(p,solve().outOfPlace, tick, aStar)
            dictionary = {0:"KEY_RIGHT", 1:"KEY_LEFT", 2:"KEY_UP", 3:"KEY_DOWN"}
            movements = len(result)
            while len(result) > 0:
                stdscr.clear()
                stdscr.refresh()
                p.printscene()
                p.move(dictionary[result.pop(0)])
                sleep(float(speed)/1000.0)                
        else:
            movements += p.move(character)
        if (p.win() and movements != 0):
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

class node(object):
    def __init__(self, val):
        self.val = val
        self.sons = []
        self.father = None
        self.myLevel = None
class tree(object):
    def __init__(self, root):
        self.root = root
        root.myLevel = 0
    def leafs(self, node):
        if len(node.sons) == 0:
            return [node]
        else:
            leaf = []
            for n in node.sons:
                for l in self.leafs(n):
                    leaf.append(l)
            return leaf
    def nodesQnt(self, node):
        if len(node.sons) == 0:
            return 1
        else:
            count = 1
            for n in node.sons:
                count += self.nodesQnt(n)
            return count
    def fatherRouteQnt(self, node):
        
        if node is self.root:
            return 1
        else:
            count = 1 + self.fatherRouteQnt(node.father)
            return count

class solve(object):
    def __init__(self):
        self.dictionary = {0:"KEY_RIGHT", 1:"KEY_LEFT", 2:"KEY_UP", 3:"KEY_DOWN"}
        self.dictionaryReversed = {0:"KEY_LEFT", 1:"KEY_RIGHT",2:"KEY_DOWN",3:"KEY_UP"} 
        self.log = []

       ###heuristicas
    def manhattanDistance(self,po):
        solve.manhattanDistance.nome = "Distância de Manhattan"
        p = copy.deepcopy(po)
        count = 0
        val = [0,0,0] #(valor, x, y)
        coordInit = []
        correctCoord = []
        for i in range(0,3):
            val[1] = (val[1]%3)+1
            for j in range(0,3):
                val[0] += 1
                val[2] = (val[2]%3)+1
                if ((p.scene[i][j] != str(val[0])) and (str(val[0]) != '9') and (p.scene[i][j] != '_')):
                    coordInit.append((p.scene[i][j],val[1],val[2]))
                elif((str(val[0]) == '9') and (p.scene[i][j] != '_' )):
                    coordInit.append((p.scene[i][j], val[1], val[2]))
                correctCoord.append((val[0], val[1], val[2])) #valor, x, y
        for i in coordInit:
            for c in correctCoord:
                if i[0] == str(c[0]):
                    count += ((i[1]-c[1]).__abs__() + (i[2]-c[2]).__abs__())
        return count
    
    def outOfPlace(self,p):
        solve.outOfPlace.nome = "Peças fora do lugar"
        count = 0
        val = 1
        for i in range(0,3):
            for j in range(0,3):
                if ((p.scene[i][j] != str(val)) and (str(val) != '9') and (p.scene[i][j] != '_')):
                    count += 1
                elif((str(val) == '9') and (p.scene[i][j] != '_')):
                    count += 1
                val += 1
        return count

    def nextLevelTree(self, p):
        pList = [(copy.deepcopy(p),0),(copy.deepcopy(p),1),(copy.deepcopy(p),2),(copy.deepcopy(p),3)]
        for i in range(0,4):
            pList[i][0].move(self.dictionary[pList[i][1]])
        keys = []
        for e in pList:
            adder = True
            for k in keys:
                if (e[0].scene == k[0].scene):
                    adder = False
            if adder and (e[0].scene != p.scene):
                keys.append(e)
        return keys #retorna tuplas (puzzle, movimento)

    def containsLog(self,p):

        print("\rNós no log: {0}".format(len(self.log)),end="")
        for idx, l in enumerate(self.log):
            if l[0].scene == p.scene:
                return idx 
        return -1 
    
    def aStarAndGreedy(self, p, hFunc, tick, aStar=False):
        Gtree = tree(node((p,None,hFunc(p)))) #tupla puzzle, None, heuristica na arvore
        pointer = Gtree.root
        movements = []
        estatistic = []
        iteration = 0
        #for a star algorithm
        gHeuristic = 0 
        while (pointer.val[0].win() is not True):
            if tick == 'ON':
                estatistic.append((iteration, Gtree.nodesQnt(Gtree.root), Gtree.fatherRouteQnt(pointer)))
                iteration += 1
            aux = self.containsLog(pointer.val[0])
            if aux == -1:
                self.log.append((copy.deepcopy(pointer.val[0]),0))
            else:
                self.log[aux] = (self.log[aux][0],self.log[aux][1]+1)
            nextLevel = self.nextLevelTree(pointer.val[0]) 
            heuristicCost = []
            for i in nextLevel:
                if aStar:
                    n = node([i[0], i[1], hFunc(i[0]) + (pointer.myLevel + 1)])
                else:
                    n = node([i[0], i[1], hFunc(i[0])])
                n.father = pointer
                n.myLevel = n.father.myLevel + 1 #gambs 
                heuristicCost.append(n)

            pointer.sons = heuristicCost
            leaf = Gtree.leafs(Gtree.root)
            leaf.sort(key=lambda x: x.val[2], reverse=False)
            verif = True
            returnMember = []
            for j in leaf:
                aux = self.containsLog(j.val[0])
                if aux == -1:
                    pointer = j
                    verif = False
                    break
                else:
                    returnMember.append((j,self.log[aux][1]))
            if verif == True:
                returnMember.sort(key=lambda x: x[1], reverse=False)
                pointer = returnMember[0][0]
        if tick == 'ON':
            estatistic.append((iteration, Gtree.nodesQnt(Gtree.root), Gtree.fatherRouteQnt(pointer)))
        while pointer.val[0].scene != p.scene:
            movements.insert(0,pointer.val[1])
            pointer = pointer.father
        if tick == 'ON':
            if not os.path.isdir("estatistica"):
                os.mkdir("estatistica")
            os.chdir("estatistica")
            filenum = 0
            while os.path.isfile("e{0}.txt".format(filenum)):
                filenum += 1
            f = open("e{0}.txt".format(filenum), 'w')
            f.write(str(p.printscene(False)))
            f.write("\n")
            if aStar:
                f.write("Algoritmo: A*\n")
            else:
                f.write("Algoritmo: Guloso\n")
            f.write("Heurística: {0}".format(hFunc.nome))
            f.write("\nQuantidade de movimentos necessários: {0}\n".format(len(movements)))
            f.write("\n")
            for e in estatistic:
                f.write("tick: {0}\nquantidade de nós: {1}\nnós na rota: {2}\n--------------------------------\n".format(e[0],e[1],e[2])) 
            f.close()
            os.chdir("../")
            self.log.clear()
        return movements
        
class puzzle(object):
    def __init__(self):
        self.pointer = [2,2] #aponta para a posicao do nulo
        self.scene = [['1','2','3'],['4','5','6'],['7','8','_']]
    def printscene(self, noPrint = True):
        strPrint = "{0}\n\r{1}\n\r{2}\r".format(" ".join(self.scene[0])," ".join(self.scene[1])," ".join(self.scene[2]))
        if noPrint:
            print(strPrint)
        return strPrint.replace("\r","")
        
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
        else:
            return 0
        return 1

    def shuffle(self):
        dictionary = {0:"KEY_RIGHT", 1:"KEY_LEFT", 2:"KEY_UP", 3:"KEY_DOWN"}
        for i in range(0,1000):
            self.move(dictionary[randint(0,3)])

    def win(self):
        if (self.scene == [['1','2','3'],['4','5','6'],['7','8','_']]):
            return True
        else:
            return False

    def initial(self): # inicial da aps
        self.scene = [['2','3','1'],['_','5','6'],['4','7','8']]
        self.pointer = [1,0]

#def main():
def main(stdscr):
    p = puzzle()
    game(p)
    p.initial()
    print(solve().greedy(p, solve().manhattanDistance))
wrapper(main)
#main()

