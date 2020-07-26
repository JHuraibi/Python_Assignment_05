# Author: Jamal Huraibi
# Assignment: 5
# Question: 1

import math
import random


# CRITICAL: Global precision value


class PopulationSpace:
    """Evolutionary Search. Candidate Solutions."""

    def __init__(self):
        self.current_gen = [[None] * 50, [None] * 50]
        self.range_lower_bound = -10
        self.range_upper_bound = 110
        self._initial_population()

    def __str__(self):
        pop_size = len(self.current_gen)
        for i in range(0, pop_size):
            print("{} ".format(self.current_gen[i]))
        print("\n")

    def _initial_population(self):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        for i in range(50):
            self.current_gen[i] = random.randint(-10, 100)

    def generate(self, next_gen):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        self.current_gen = next_gen

    def evaluate(self):
        """Evaluates the performance of the Population's individuals.
        Method defined as "obj()" in academic paper."""
        # TODO: floating point values
        pop_size = len(self.current_gen)
        for i in range(pop_size):                                               # Check value of each solution
            solution = float(self.current_gen[i])
            if solution > (100.0 + 1e-18):                                      # 100.000 000 000 000 000 000 0
                self.current_gen[i][1] = _larger_than_100(solution)                # x > 100
            else:
                self.current_gen[i] = _less_than_100(solution)                  # x <= 100

        self._rank()                                                            # Sort the new values



    def _rank(self):
        """Sorts the Population by their fitness score
        Fitness: piecewise function as defined by assignment instructions.
        Indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and [0 to (size * 0.2)] are the "Elites".
        """
        self.current_gen.sort()

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
        self.elites = [[], []]
        self.super_elite = [[], []]

    def update(self, elites):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values.
        "elites" is presorted (descending) by the Population class before being passed-in here."""
        self.elites = elites                                                    # Record the top-performers (plural)
        self.super_elite = elites[0]                                            # Record single, top performer (single)
        self.minima = elites[-1]                                                # Lowest value of the elites
        self.maxima = elites[0]                                                 # Highest value of the elites

    def influence(self, current_gen):
        """Generates the next generation's individuals using knowledge from the Belief Space."""
        pop_size = len(current_gen)                                             # Number of individuals in population

        next_gen = [None] * pop_size                                            # Redundant, but helps intuitive reading
        local_min = self.minima                                                 # Lower bound of current value range
        local_max = self.maxima                                                 # Upper bound of current value range

        for i in range(0, pop_size):
            solution = current_gen[i]                                           # Intermediate var.
            target = self.super_elite
            mutation_occurs = random.randint(0, 1)                              # 50% prob. of applying random value

            if mutation_occurs:
                next_gen[i] = self._mutation_value(local_min, local_max)        # Apply a randomized mutation value
                print("[DEBUG]: Mutation")
            elif self._greater_than(solution, target):
                next_gen[i] = solution - 1                                      # Tend downward to top score thus far
                print("[DEBUG]: MORE")
            elif self._less_than(solution, target):
                next_gen[i] = solution + 1                                      # Tend upward to top score thus far
                print("[DEBUG]: LESS")
            else:
                next_gen[i] = current_gen[i]                                    # Already equivalent to super-elite
                print("[DEBUG]: NONE")

        return next_gen                                                         # Return the new (influenced) generation

    @staticmethod
    def _mutation_value(minimum, maximum):
        """Returns a random value between minimum and maximum while accounting for decimal precision."""
        minimum = minimum * 1e20
        maximum = maximum * 1e20
        return random.randint(minimum, maximum) / 1e20

    @staticmethod
    def _greater_than(value, base_value):
        """Returns whether "value" is GREATER than "base_value".
        Built-in Python Rounding.
        Floating-point precision of 20."""
        value = round(value, 20)
        base_value = round(base_value, 20)
        return (value - base_value) > 1e-21

    @staticmethod
    def _less_than(value, base_value):
        """Returns whether "value" is LESSER than "base_value".
        Built-in Python Rounding.
        Floating-point precision of 20."""
        value = round(value, 20)
        base_value = round(base_value, 20)
        return (value - base_value) < -1e-21


def _larger_than_100(value):
    """Piecewise 1 of 2
    x = -exp(-1) + (x - 100)(x - 102)
    """
    # TODO: floating point values
    product = (value - 100) * (value - 102)                                     # (x - 100)(x - 102)
    return -(math.exp(-1)) + product                                            # -exp(-1) + (x - 100)(x - 102)

def _less_than_100(value):
    """Piecewise 2 of 2
    x = -exp(-(x / 100)^2))
    """
    inner = float(value / 100.0)                                                # (x / 100)
    inner = -(math.pow(inner, 2))                                               # -(x / 100)^2)
    return -(math.exp(inner))


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
        time = time + 1

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
#
# --| Overview of Major Methods |--
#
# evaluate() [i.e. obj()]
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



