#!/usr/bin/env python3

import time
import random

class Agent:
    def __init__(self, x, y, character, environment):
        self.x = x
        self.y = y

        #Agent needs to be able to look at the environment to determine
        #what moves are possible
        self.environment = environment

        assert len(character) == 1,"Character must be a single printable character"
        self.character = character

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def move(self,direction):
        actionVector = [self.moveUp, self.moveDown, self.moveLeft, self.moveRight]
        assert direction >= 0 and direction <= 3,"Invalid direction provided. Must be integer in 0..3"
        actionVector[direction]()

    def moveUp(self):
        if self.getY() > 0:
            self.y = self.y - 1

    def moveDown(self):
        if self.getY() < self.environment.height - 1:
            self.y = self.y + 1

    def moveLeft(self):
        if self.getX() > 0:
            self.x = self.x - 1

    def moveRight(self):
        if self.getX() < self.environment.width - 1:
            self.x = self.x + 1

class Environment:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.world = [0 for x in range(0, self.width*self.height)]
        self.agent = Agent(self.width // 2,self.height // 2, 'A', self)
        self.food = Agent(0, 0, 'R', self)
        self.agentsList = [self.agent, self.food]

    def render(self):
        #Render the top border of the world
        topBorderString = "".join(["-" for x in range(0, self.width+2)])
        print(topBorderString)

        #print the stuff inside the environment
        for y in range(0, self.height):
            for x in range(0, self.width + 2):
                if x == 0 or x == self.width:
                    print("|", end="")

                charToPrint = ' '
                for a in self.agentsList:
                    if x == a.getX() and y == a.getY():
                        charToPrint = a.character

                #we print just one character so overlapping agents don't
                #mess up the display
                print(charToPrint, end="")

            print("", end="\n")


        #Bottom border string is the same as the top, so we can just
        #draw that again
        print(topBorderString)

    def resetAgent(self):
        pass

    #Returns a feature vector for a particular state that the
    #non-food agent is in. This is what our MDP will learn to
    #interpret.
    #It is assuming an environment with only one "food" item.  
    def getStateVector(self, as_string=False):
        sv = [0 for k in range(0, 8)]

        aX = self.agent.getX()
        aY = self.agent.getY()

        #upper left
        if self.food.getX() < aX and self.food.getY() < aY:
            sv[0] = 1
        #above
        if self.food.getX() == aX and self.food.getY() < aY:
            sv[1] = 1
        #upper right
        if self.food.getX() > aX and self.food.getY() < aY:
            sv[2] = 1
        #right
        if self.food.getX() > aX and self.food.getY() == aY:
            sv[3] = 1
        #lower right
        if self.food.getX() > aX and self.food.getY() > aY:
            sv[4] = 1
        #below
        if self.food.getX() == aX and self.food.getY() > aY:
            sv[5] = 1
        #lower left
        if self.food.getX() < aX and self.food.getY() > aY:
            sv[6] = 1
        #left
        if self.food.getX() < aX and self.food.getY() == aY:
            sv[7] == 1

        if as_string == False:
            return sv

        #otherwise, return string representation
        return "".join([str(c) for c in sv])

def tests():
    e = Environment()
    #e.render()

    #first food location is upper left
    assert e.getStateVector(as_string=True) == "10000000","State vector not as it should be!"

    #run a loop for a while that moves the agent around the environment,
    #just to observe the behavior
    for i in range(0,10):
        e.render()
        e.agent.move(random.randint(0,3))
        time.sleep(0.1)

if __name__ == "__main__":
    tests()