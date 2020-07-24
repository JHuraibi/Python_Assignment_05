# Author: Jamal Huraibi
# Assignment: 5
# Question: 1

import math
import random


class PopulationSpace:
    """Evolutionary Search. Candidate Solutions."""

    def __init__(self):
        self.current_gen = []
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
        for solution in self.current_gen:
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
        # CRITICAL: Elites and super elite are not correctly being determined
        """Sorts the Population by their fitness score (DESCENDING!)
        Fitness: piecewise function as defined by assignment instructions.
        Sorting is reversed so that indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and 0 to [(size * 0.2)] are the Elites.
        """
        self.current_gen.sort(reverse=True)

    def accept(self):
        """Determines the individuals of the Population that will influence
        the Belief Space."""
        self._rank()

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

    def update(self, current_gen):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values."""
        # CHECK: will error occur when population is <2 ?

    def _record_elites(self, current_gen):
        low_bound = len(current_gen) * 0.2
        low_bound = math.ceil(low_bound)
        self.elites = current_gen[0:low_bound]
        self.super_elite = current_gen[0]

    def _record_extrema(self, current_gen):
        self.minima = current_gen[-1]
        self.maxima = current_gen[0]

    def influence(self, current_gen):
        """Generates the next generation's individuals using knowledge from the Belief Space."""
        # TODO: Move to Population class?
        next_gen = []                                                           # Redundant, but helps intuitive reading
        local_min = self.minima
        local_max = self.maxima

        for i in range(0, len(current_gen)):
            individual = current_gen[i]
            mutation_occurs = random.randint(0, 1)
            if mutation_occurs:
                next_gen[i] = random.randint(local_min, local_max)
            elif individual > self.super_elite:
                next_gen[i] = individual - 1
            elif individual < self.super_elite:
                next_gen[i] = individual + 1
            else:
                next_gen[i] = current_gen[i]

        return next_gen


if __name__ == '__main__':
    time = 0
    endTime = 100

    population = PopulationSpace()
    belief = BeliefSpace()

    while time < endTime:
        print("[Time: {}]\n".format(time))
        population.evaluate()
        belief.update(population.current_gen)
        time = time - 1

    print("\ndone\n")


# --| PseudoCode for Each Generation |--
#   Begin
#       t = 0
#       initialize Bt, Pt
#       repeat
#           evaluate Pt
#           update(Bt, accept(Pt))                  # ?staticmethod
#           generate(Pt, influence(Bt))             # ?staticmethod
#           t = t + 1;                              # update time
#           select Pt from Pt - 1                   # ?remove 1 solution
#           until(termination condition achieved)   # check loop condition
#   End

# def evaluate_router(self):
#     """Mimics a piecewise by routing to static method based on value passed-in.
#     Evaluates the performance of the Population's individuals.
#     Performance is a piecewise function as defined by assignment instructions."""
#     pass
