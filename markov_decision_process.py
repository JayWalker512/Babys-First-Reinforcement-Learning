#!/usr/bin/env python3
import random

class MarkovDecisionProcess:
    def __init__(self):
        self.possible_actions = [] #expected to be a list of ints
        self.state_actions= {}

    def set_possible_actions(self,list_of_actions):
        self.possible_actions = list_of_actions

    #NOT USED?!
    def get_action_weights(self, state):
        if state in self.state_actions:
            return self.state_actions[state]

        #each action is equally probable if we haven't seen this state previously.
        return {x:0 for x in self.possible_actions} 

    #Returns which action should be taken in the current state.
    #epsilon is a hyperparameter defining how "explorative" the 
    #MDP training process should be. If you only want to get the
    #most probable action, set epsilon=0. If you want 100%
    #exploration regardless of probability, set epsilon=1.
    #For training, it should be somewhere in between and for 
    #inference 0 is the most sensible value.
    def get_predicted_action(self, state, epsilon=0.2):
        if state not in self.state_actions:
            self.state_actions[state] = {x:0 for x in self.possible_actions}
            #The state->action pair was not present before, so any action is equally likely
            return self.possible_actions[random.randint(0,len(self.possible_actions) - 1)]

        #Otherwise we need to determine the action to return (depends on epsilon as well!)
        random_choice = random.random()
        if random_choice > epsilon: #choose current best option

            #TODO FIXME if there are multiple maximums, this only selects the first one.
            #Perhaps any maximum weight action should be chosen at random?
            best_action = self.possible_actions[0]
            best_weight = 0 #don't allow negative weights, so 0 is fine lowest
            for a in self.state_actions[state]:
                if self.state_actions[state][a] > best_weight:
                    best_weight = self.state_actions[state][a]
                    best_action = a

            #Are there any other actions with the same maximum weight? 
            #We must choose between them with equal probability.
            best_actions = [best_action]
            for a in self.state_actions[state]:
                if self.state_actions[state][a] == best_weight:
                    best_actions.append(a)

            return best_actions[random.randint(0, len(best_actions) - 1)]

        else: #otherwise pick an action at random
            random_index = random.randint(0, len(self.possible_actions) - 1)
            return self.possible_actions[random_index]

    #Increase the probability of taking an action in a particular state in the future.
    #We allow setting an "amount" because maybe some actions should be encouraged more
    #than others. Note that setting "amount" negative is equivalent to discouraging an action.
    def encourage(self, state, action, amount=1):
        if state not in self.state_actions:
            #this just ensures that the state->action pair is initialized since it wasn't prior to being encouraged
            self.get_predicted_action(state) 

        self.state_actions[state][action] += amount
        if self.state_actions[state][action] < 0:
            self.state_actions[state][action] = 0

def tests():
    mdp = MarkovDecisionProcess()
    mdp.set_possible_actions([0,7,9,13])
    assert mdp.possible_actions == [0,7,9,13],"possible_actions vector not as expected."
    mdp.get_predicted_action("00000000")
    assert mdp.state_actions == {"00000000":{0:0, 7:0, 9:0, 13:0}},"state_actions dictionary not as expected."
    assert mdp.get_predicted_action("00000000") in mdp.possible_actions,"Predicted action is not possible!" #will be some action at random
    mdp.encourage("00000000", 13)
    assert mdp.get_predicted_action("00000000", epsilon=0) == 13,"Predicted action not as expected!"

if __name__ == "__main__":
    tests()