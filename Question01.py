# Author: Jamal Huraibi
# Assignment: 5
# Question: 1

import math
import random


class PopulationSpace:
    """Evolutionary Search. Candidate Solutions."""

    def __init__(self):
        self.current_gen = []
        self.range_lower_bound = -10
        self.range_upper_bound = 110
        self._initial_population()

    def __str__(self):
        pop_size = len(self.current_gen)
        for i in range(0, pop_size):
            print("{} ".format(self.current_gen[i]))
        print('\n')

    def _initial_population(self):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        for i in range(50):
            self.current_gen.append(random.randint(-10, 100))

    def generate(self, next_gen):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        self.current_gen = next_gen

    def evaluate(self):
        """Evaluates the performance of the Population's individuals.
        Method defined as "obj()" in academic paper."""
        # TODO: floating point values
        for i in range(0, len(self.current_gen)):                               # Check value of each solution
            solution = self.current_gen[i]
            if solution > 100:
                self.current_gen[i] = self._larger_than_100(solution)           # x > 100
            else:
                self.current_gen[i] = self._less_than_100(solution)             # x <= 100

        self._rank()                                                            # Sort the new values

    @staticmethod
    def _larger_than_100(value):
        """Piecewise 1 of 2
        x = -exp(-1) + (x - 100)(x - 102)
        """
        # TODO: floating point values
        product = (value - 100) * (value - 102)                                 # (x - 100)(x - 102)
        return -(math.exp(-1)) + product                                        # -exp(-1) + (x - 100)(x - 102)

    @staticmethod
    def _less_than_100(value):
        """Piecewise 2 of 2
        x = -exp(-(x / 100)^2))
        """
        inner = float(value / 100.0)                                            # (x / 100)
        inner = -(math.pow(inner, 2))                                           # -(x / 100)^2)
        return -(math.exp(inner))

    def _rank(self):
        # CRITICAL: Are elites and super elite correctly being determined?System.out.println();
        """Sorts the Population by their fitness score (DESCENDING!)
        Fitness: piecewise function as defined by assignment instructions.
        Sorting is reversed so that indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and 0 to [(size * 0.2)] are the Elites.
        """
        self.current_gen.sort(reverse=True)

    def accept(self):
        """Determines the individuals of the Population that will influence
        the Belief Space."""
        low_bound = len(self.current_gen) * 0.2
        low_bound = math.ceil(low_bound)
        return self.current_gen[0:low_bound]
        # self.super_elite = self.current_gen[0]

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

    def update(self, elites):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values.
        "elites" is presorted (descending) by the Population class before being passed-in here."""
        # CHECK: will error occur when population is <2 ?
        self.elites = elites                                                    # Record the top-performers (plural)
        self.super_elite = elites[0]                                            # Record single, top performer (single)
        self.minima = elites[-1]                                                # Lowest value of the elites
        self.maxima = elites[0]                                                 # Highest value of the elites

    def influence(self, current_gen):
        """Generates the next generation's individuals using knowledge from the Belief Space."""
        # TODO: Check precision of value of tending toward super elite
        next_gen = current_gen                                                  # Redundant, but helps intuitive reading
        local_min = math.floor(self.minima)
        local_max = math.ceil(self.maxima)

        for i in range(0, len(current_gen)):
            solution = current_gen[i]
            mutation_occurs = random.randint(0, 1)
            if mutation_occurs:
                next_gen[i] = random.randint(local_min, local_max)              # Apply a randomized mutation value
            elif solution > self.super_elite:
                next_gen[i] = solution - 1                                      # Tend downward to top score thus far
            elif solution < self.super_elite:
                next_gen[i] = solution + 1                                      # Tend upward to top score thus far

        return next_gen                                                         # Return the new (influenced) generation


if __name__ == '__main__':
    time = 0
    endTime = 100

    population = PopulationSpace()
    belief = BeliefSpace()

    while time < endTime:
        print("[Time: {}]\n".format(time))
        population.evaluate()
        belief.update(population.accept())
        influenced = belief.influence(population.current_gen)
        population.generate(influenced)
        time = time - 1

        print(population)

    print("\nfin\n")


# --| PseudoCode for Each Generation |--
#   Begin
#       t = 0                                       #
#       initialize Bt, Pt                           #
#       repeat
#           evaluate Pt                             #
#           update(Bt, accept(Pt))                  # ?staticmethod
#           generate(Pt, influence(Bt))             # ?staticmethod
#           t = t + 1;                              # update time
#           select Pt from Pt - 1                   # ?remove 1 solution
#           until(termination condition achieved)   # check loop condition
#   End
#
#
# --| Overview of Major Methods |--
# evaluate()/obj()
#   - Evaluate each solution and find their fitness score
#   - Rank solutions based on their fitness score f(x)
#
# accept()
#   - Select 20% of the top-performing individuals(Elites)
#
# update()
#   - Update the Belief Space using top-performing individuals
#       - record the top-performing individuals (situational knowledge)
#       - record max, min, and range of variable x (normative knowlege)
#
# influence()
#   - Use the domain knowledge in the Belief Space to influence/evolve the population
#       - compare each solution to the super elite(the best solution)and take one step toward that.
#       - With a probability of 50% introduce a mutation to a solution by changing
#           the value randomly within the recorded min and max.



