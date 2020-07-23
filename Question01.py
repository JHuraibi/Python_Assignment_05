# Author: Jamal Huraibi
# Assignment: 5
# Question: 1

import math


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

    def __init__(self):
        self.population = []
        self.elites = []
        self.pop_size = 0
        self.range_lower_bound = -10
        self.range_upper_bound = 110
        pass

    def _generate(self):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        pass

    def evaluate(self):
        """Evaluates the performance of the Population's individuals.
        Method defined as "obj()" in academic paper."""
        for solValue in self.population:
            if solValue > 100:
                solValue = self._larger_than_100(solValue)
            else:
                solValue = self._less_than_100(solValue)

    @staticmethod
    def _larger_than_100(value):
        """Piecewise 1 of 2
        x = -exp(-1) + (x - 100)(x - 102)
        """
        product = (value - 100) * (value - 102)
        return -(math.exp(-1)) + product

    @staticmethod
    def _less_than_100(value):
        """Piecewise 2 of 2
        x = -exp(-(x / 100)^2))
        """
        inner = float(value / 100)
        inner = -(math.pow(inner, 2))
        return -(math.exp(inner))

    def _rank(self):
        """Sorts the Population by their fitness score (DESCENDING!)
        Fitness: piecewise function as defined by assignment instructions.
        Sorting is reversed so that indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and 0 to [(size * 0.2)] are the Elites.
        """
        self.population.sort(reverse=True)

    def _filter(self):
        """Selects the top 20% of scores (i.e. the elites)."""
        # CHECK: will error occur when population is <2
        low_bound = len(self.population) * 0.2
        low_bound = math.ceil(low_bound)
        self.elites = self.population[0:low_bound]

    def accept(self):
        """Determines the individuals of the Population that will influence
        the Belief Space."""
        self._rank()
        self._filter()

    def influence(self):
        """Selects the next generation's individuals using knowledge (influence)
         from the Belief Space."""
        pass

    def _normative_knowledge(self, value):
        """Checks if the value is a new min or max"""
        pass

    def _update_range(self):
        """Updates the current range of the solution values"""
        # TODO: Remove either min/max or the bound variables (redundant)
        self.range_lower_bound = self.min
        self.range_upper_bound = self.max


class BeliefSpace:
    """Information of ancestors (i.e knowledge), accessed by current/future generations."""
    range = None

    # Accepted Range (Normative Knowledge)
    #   if (situational > lower bound) && (situational < upper bound)

    # Exemplar Value (Situational Knowledge)
    #   if (actual - situational) >= [tbd value]

    def __init__(self):
        pass

    def update(self):
        """Adds the experiences of the accepted individuals of the Population."""
        # popObj.accept()
        #
        # for individual in List population
        #   if (not acceptable, pop(counter))
        #       counter = counter + 1
        pass


def check_termination_condition():
    """Controls program termination. In this case, when time=100. [UPDATE]"""
    # [?] if population == 1
    pass


if __name__ == '__main__':
    TIME = 0

    population = PopulationSpace()
    population.obj()

# --| PseudoCode for Each Generation |--
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

# def evaluate_router(self):
#     """Mimics a piecewise by routing to static method based on value passed-in.
#     Evaluates the performance of the Population's individuals.
#     Performance is a piecewise function as defined by assignment instructions."""
#     pass
