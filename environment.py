#!/usr/bin/env python3

import time
import random

class Agent:
    def __init__(self, x, y, character, environment):
        self.x = x
        self.y = y
        self.action_vector = [self.move_up, self.move_down, self.move_left, self.move_right]

        #Agent needs to be able to look at the environment to determine
        #what moves are possible
        self.environment = environment

        assert len(character) == 1,"Character must be a single printable character"
        self.character = character

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    #This returns a list of valid directions that can be passed to the move() method.
    #Note that running into a wall is considered a valid move, this makes no assumptions of intent.
    def get_possible_movement_directions(self):
        return [x for x in range(0, len(self.action_vector))]

    def move(self,direction):
        assert direction >= 0 and direction <= len(self.action_vector),"Invalid direction provided. Must be integer in 0..3"
        self.action_vector[direction]()

    def move_up(self):
        if self.gety() > 0:
            self.y = self.y - 1

    def move_down(self):
        if self.gety() < self.environment.height - 1:
            self.y = self.y + 1

    def move_left(self):
        if self.getx() > 0:
            self.x = self.x - 1

    def move_right(self):
        if self.getx() < self.environment.width - 1:
            self.x = self.x + 1

class Environment:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.world = [0 for x in range(0, self.width*self.height)]
        self.agent = Agent(self.width // 2,self.height // 2, 'A', self)
        self.food = Agent(0, 0, 'R', self)
        self.agents_list = [self.agent, self.food]

    def render(self):
        #Render the top border of the world
        top_border_string = "".join(["-" for x in range(0, self.width+2)])
        print(top_border_string)

        #print the stuff inside the environment
        for y in range(0, self.height):
            for x in range(0, self.width + 2):
                if x == 0 or x == self.width:
                    print("|", end="")

                char_to_print = ' '
                for a in self.agents_list:
                    if x == a.getx() and y == a.gety():
                        char_to_print = a.character

                #we print just one character so overlapping agents don't
                #mess up the display
                print(char_to_print, end="")

            print("", end="\n")


        #Bottom border string is the same as the top, so we can just
        #draw that again
        print(top_border_string)

    def reset_agent(self):
        pass

    #Move the food to a random spot, make sure it's not on top of the agent
    def reset_food(self):
        newx = self.agent.getx()
        newy = self.agent.gety()
        while newx == self.agent.getx() and newy == self.agent.gety():
            newx = random.randint(0, self.width-1)
            newy = random.randint(0, self.height-1)

        self.food.x = newx
        self.food.y = newy

    #returns True if agent is on top of food, otherwise false
    def has_agent_food_collision(self):
        if self.agent.getx() == self.food.getx() and self.agent.gety() == self.food.gety():
            return True

        return False

    #Returns a feature vector for a particular state that the
    #non-food agent is in. This is what our MDP will learn to
    #interpret.
    #It is assuming an environment with only one "food" item.  
    def get_state_vector(self, as_string=False):
        sv = [0 for k in range(8)]

        ax = self.agent.getx()
        ay = self.agent.gety()

        #upper left
        if self.food.getx() < ax and self.food.gety() < ay:
            sv[0] = 1
        #above
        if self.food.getx() == ax and self.food.gety() < ay:
            sv[1] = 1
        #upper right
        if self.food.getx() > ax and self.food.gety() < ay:
            sv[2] = 1
        #right
        if self.food.getx() > ax and self.food.gety() == ay:
            sv[3] = 1
        #lower right
        if self.food.getx() > ax and self.food.gety() > ay:
            sv[4] = 1
        #below
        if self.food.getx() == ax and self.food.gety() > ay:
            sv[5] = 1
        #lower left
        if self.food.getx() < ax and self.food.gety() > ay:
            sv[6] = 1
        #left
        if self.food.getx() < ax and self.food.gety() == ay:
            sv[7] = 1

        if as_string == False:
            return sv

        #otherwise, return string representation
        return "".join([str(c) for c in sv])

def tests():
    e = Environment()
    #e.render()

    #first food location is upper left
    assert e.get_state_vector(as_string=True) == "10000000","State vector not as it should be!"

    #run a loop for a while that moves the agent around the environment,
    #just to observe the behavior
    for i in range(0,10):
        e.render()
        e.agent.move(random.randint(0,3))
        time.sleep(0.1)

if __name__ == "__main__":
    tests()