class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        qValue = 0.0
        features = self.featExtractor.getFeatures(state, action)
        for key in features.keys():
            qValue += (self.weights[key] * features[key])
        print(qValue, 'the q value')
        return(qValue)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        features = self.featExtractor.getFeatures(state, action)
        possibleStateQValues = []
        for act in self.getLegalActions(state):
            possibleStateQValues.append(self.getQValue(state, act))
        for key in features.keys():
            self.weights[key] += self.alpha * (reward + self.discount * (
                        (1 - self.epsilon) * self.getValue(nextState) + (self.epsilon / len(possibleStateQValues)) * (
                    sum(possibleStateQValues))) - self.getQValue(state, action)) * features[key]


def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass