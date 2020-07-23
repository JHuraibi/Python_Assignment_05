# Author: Jamal Huraibi
# Assignment: 5
# Question: 1


class Algorithm:
    def __init__(self):
        pass

    def select(self):
        pass

    def accept(self):
        pass

    def influence(self):
        pass


class PopulationSpace:
    """Evolutionary Search. Candidate Solutions."""
    population = None
    time = None

    def __init__(self):
        pass

    def update(self):
        pass


class BeliefSpace:
    """Knowledge. Information stored by ancestors, accessed by current generation."""
    range = None
    # Accepted Range (Normative Knowledge)
    #   if (situational > lower bound) && (situational < upper bound)

    # Exemplar Value (Situational Knowledge)
    #   if (actual - situational) >= [tbd value]

    def __init__(self):
        pass

    @staticmethod
    def elevate_to_good_range():
        pass


def evaluate(population):
    pass


def update(beliefObj, popObj):
    pass
    # popObj.accept()
    #
    # for individual in List population
    #   if (not acceptable, pop(counter))
    #       counter = counter + 1


def generate(beliefObj, popObj):
    pass
    # beliefObj.influence()


if __name__ == '__main__':
    time = 0


# PseudoCode from Instructions:
#   Begin
#       t = 0
#       initialize Bt, Pt
#       repeat
#           evaluate Pt
#           update(Bt, accept(Pt))
#           generate(Pt, influence(Bt))
#           t = t + 1;
#           select Pt from Pt - 1
#           until(termination condition achieved)
#   End

# --| Functions |--
#   - When an individual is to be modified: select ONE knowledge source to modify
#       the individual. Selection is done by
#   - Functions:
#       accept() - selects the individual experiences that will be used to update
#                       the belief space at each generation.
#       update() - method in which knowledge sources communicate with each other
#       influence() - determines how knowledge can influence the population
#       select() - done via roulette wheel selection
#   - Example for handling infeasible solutions:
#       if (individual satisfies all constrains)
#         fitness = obj(individual)
#       else
#         fitness = IN_FEASIBLE_VALUE
#       endif
