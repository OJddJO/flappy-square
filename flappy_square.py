from kandinsky import fill_rect as fRect,draw_string as dStr,get_pixel as gCol
from ion import *
from time import sleep
from random import randint

def dSquare(x, y, length, color):
    fRect(int(x-length/2), int(y-length/2), length, length, color)

light = [(190, 230, 255), (220, 240, 255), (0, 240, 0), (0, 0, 0)]
dark = [(20, 40, 65), (20, 20, 45), (0, 40, 0), (255, 255, 255)]
selCol = light


class UI:
    
    def __init__(self):

        self.optionList = ["    Play    ", "    Exit    ", "   Bright   ", "[OK] to jump"]
        self.modifiedList = []
        self.select = 0
        self.draw()


    def draw(self):
        fRect(0, 0, 320, 222, selCol[0])
        dStr("Flappy Square", 95, 80, (200, 50, 70), selCol[0])
        dStr("by OJd_dJO", 110, 98, (200, 50, 70), selCol[0])


    def update(self):
        global selCol
        self.modifiedList = []
        for element in self.optionList:
            if element == self.optionList[self.select]:
                self.modifiedList.append("> "+element+" <")
            else:
                self.modifiedList.append("  "+element+"  ")
        i = 0
        for element in self.modifiedList:
            yMod = 18*i
            length = len(element)*10
            if element == self.modifiedList[self.select]:
              dStr(element, 160-int(length/2), 140+yMod, selCol[3], selCol[1])
            else:
              dStr(element, 160-int(length/2), 140+yMod, selCol[3], selCol[0])
            i += 1
        if keydown(KEY_DOWN):
            self.select += 1
            if self.select == 4:
                self.select = 0
            while keydown(KEY_DOWN):
                pass
        elif keydown(KEY_UP):
            self.select -= 1
            if self.select == -1:
                self.select = 3
            while keydown(KEY_UP):
                pass

        if keydown(KEY_OK):
            if self.select == 0:
                game = Game()
                run = True
                while run:
                    run = game.run()
                    sleep(1/120)
                while keydown(KEY_OK):
                    pass
                return True
            if self.select == 1:
                fRect(0, 0, 320, 222, selCol[0])
                return False
            if self.select == 2:
                if self.optionList[2] == "   Bright   ":
                    self.optionList[2] = "    Dark    "
                    selCol = dark
                    self.draw()
                elif self.optionList[2] == "    Dark    ":
                    self.optionList[2] = "   Bright   "
                    selCol = light
                    self.draw()
                while keydown(KEY_OK):
                    pass
            if self.select == 3:
                pass
        return True

class Game:
    
    def __init__(self):
        self.player = Player()
        self.obsList = []
        self.tick = 0
        self.score = 0
        fRect(0, 0, 320, 222, selCol[0])


    def testLose(self):
        run = True
        if self.player.pos[1] > 222:
            run = False
        if self.player.pos[1] < 0:
            run = False
        if self.player.gameOver:
            run = False
        if not run:
            dStr("Game Over !", 110, 100, selCol[3], selCol[0])
            while not keydown(KEY_OK):
                pass
            return False
        return True


    def addObs(self):
        if self.tick == 0:
            self.obsList.append(Obstacle(randint(40, 160), int(self.score/10)))
            self.tick = 60
        else:
            self.tick -= 1
        for element in self.obsList:
            element.changePos()
            element.draw()
            if element.destroy:
                self.obsList.remove(element)
            self.score += element.score()


    def run(self):
        self.player.update()
        self.addObs()
        dStr("Score: "+str(self.score), 200, 10, selCol[3], selCol[0])
        return self.testLose()


class Player:

    def __init__(self):
        self.col = (240, 0, 0)
        self.pos = [40, 111]
        self.yVel = 0
        self.yMinVel, self.yMaxVel = -4, 4
        self.yFlapVel = -4
        self.flapped = False
        self.gameOver = False


    def gravity(self):
        if not self.flapped and self.yVel < self.yMaxVel:
            self.yVel += 0.1 + ((self.yVel**2)/20)
        elif self.flapped:
            if self.yVel < 0:
                self.yVel += 0.1 + (1/abs(self.yVel))/10
            elif self.yVel >= 0:
                self.flapped = False
        if self.yVel > self.yMaxVel:
            self.yVel == self.yMaxVel


    def flap(self):
        self.flapped = True
        self.yVel = self.yFlapVel


    def collider(self):
        for i in range(11):
            if gCol(self.pos[0]-5+i, self.pos[1]-6) == selCol[2]:
                self.gameOver = True
        for i in range(11):
            if gCol(self.pos[0]-5+i, self.pos[1]+6) == selCol[2]:
                self.gameOver = True
        for i in range(10):
            if gCol(self.pos[0]+6, self.pos[1]-5+i) == selCol[2]:
                self.gameOver = True


    def draw(self):
        dSquare(self.pos[0], self.pos[1], 10, self.col)
        if self.yVel == 0:
            return
        if self.yVel < 0:
            fRect(self.pos[0]-5, self.pos[1]+5, 10, abs(int(self.yVel)), selCol[0])
        elif self.yVel > 0:
            fRect(self.pos[0]-5, self.pos[1]-5, 10, -abs(int(self.yVel)), selCol[0])


    def update(self):
        if keydown(KEY_OK):
            self.flap()
        self.gravity()
        self.pos[1] += int(self.yVel)
        self.draw()
        self.collider()


class Obstacle:

    def __init__(self, y, modifier):
        self.x = 320
        self.y = y
        self.col = selCol[2]
        self.destroy = False
        self.modifier = modifier


    def draw(self):
        fRect(self.x, 0, 20, self.y-60+self.modifier, self.col)
        fRect(self.x , self.y+30-self.modifier, 20, 222, self.col)
        fRect(self.x-5, self.y-60+self.modifier, 30, 20, self.col)
        fRect(self.x-5, self.y+30-self.modifier, 30, 20, self.col)

        fRect(self.x+20, 0, 2, self.y-60+self.modifier, selCol[0])
        fRect(self.x+20, self.y+50-self.modifier, 2, 222, selCol[0])
        fRect(self.x+25, self.y-60+self.modifier, 2, 20, selCol[0])
        fRect(self.x+25, self.y+30-self.modifier, 2, 20, selCol[0])

    
    def score(self):
        if self.x == 0:
            return 1
        else:
            return 0


    def changePos(self):
        self.x -= 2
        if self.x < -25:
            self.destroy = True


ui = UI()
run = True
while run:
    run = ui.update()

