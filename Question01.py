# Author: Jamal Huraibi
# Assignment: 5
# Question: 1

import math
import random


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
        for solution in self.population:
            if solution > 100:
                solution = self._larger_than_100(solution)
            else:
                solution = self._less_than_100(solution)

    @staticmethod
    def _larger_than_100(value):
        """Piecewise 1 of 2
        x = -exp(-1) + (x - 100)(x - 102)
        """
        product = (value - 100) * (value - 102)                                 # (x - 100)(x - 102)
        return -(math.exp(-1)) + product                                        # -exp(-1) + (x - 100)(x - 102)

    @staticmethod
    def _less_than_100(value):
        """Piecewise 2 of 2
        x = -exp(-(x / 100)^2))
        """
        inner = float(value / 100)                                              # x / 100
        inner = -(math.pow(inner, 2))                                           # -(x / 100)^2)
        return -(math.exp(inner))

    def _rank(self):
        """Sorts the Population by their fitness score (DESCENDING!)
        Fitness: piecewise function as defined by assignment instructions.
        Sorting is reversed so that indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and 0 to [(size * 0.2)] are the Elites.
        """
        self.population.sort(reverse=True)

    def accept(self):
        """Determines the individuals of the Population that will influence
        the Belief Space."""
        self._rank()
        self._filter()

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
    def __init__(self):
        self.minima = -10
        self.maxima = 110
        self.elites = []
        self.super_elite = -10

    def update(self, current_generation):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values."""
        # CHECK: will error occur when population is <2 ?

    def _record_elites(self, current_generation):
        low_bound = len(current_generation) * 0.2
        low_bound = math.ceil(low_bound)
        self.elites = current_generation[0:low_bound]
        self.super_elite = current_generation[0]

    def _record_extrema(self, current_generation):
        self.minima = current_generation[-1]
        self.maxima = current_generation[0]

    def influence(self, current_generation):
        """Selects the next generation's individuals using knowledge (influence)
         from the Belief Space.
         i.e. modifies each individual in the """
        # TODO: Move to Population class?
        next_generation = current_generation                                    # Redundant, but helps intuitive reading
        for solution in next_generation:
            mutation_occurs = random.randint(0, 1)
            if mutation_occurs:
                solution = random.randint(-10, 100)
            elif solution > self.super_elite:
                solution = solution - 1
            elif solution < self.super_elite:
                solution = solution + 1

        return next_generation



def check_termination_condition():
    """Controls program termination. In this case, when time=100. [UPDATE]"""
    # [?] if population == 1
    pass


if __name__ == '__main__':
    TIME = 0

    population = PopulationSpace()
    population.obj()

    belief = BeliefSpace(x)

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
