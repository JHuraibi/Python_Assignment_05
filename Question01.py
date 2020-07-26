# Author: Jamal Huraibi, fh1328
# Assignment: 5
# Question: 1

# TODO: Normative knowledge
# TODO: Global precision value
# TODO: Comments
# If time: Global SIZE for population size
# If time: Fix purpose of docstrings
# SIZE = 50


import math
import random


class Solution:
    """The Individuals of each Generation."""
    def __init__(self, x):
        self.x = x                                                              # Set x value
        self.y = None                                                           # Declare y variable
        self.evaluate()                                                         # Calculate and set y-value

    def evaluate(self):
        """Evaluates the performance of the Population's individuals.
        Method defined as "obj()" in academic paper."""
        # TODO: floating point values
        if self.x > (100.0 + 1e-18):                                            # 100.000 000 000 000 000 000 0
            self.y = self._larger_than_100(self.x)                              # x > 100
        else:
            self.y = self._less_than_100(self.x)                                # x <= 100

    @staticmethod
    def _larger_than_100(value):
        """Piecewise 1 of 2
        x = -exp(-1) + (x - 100)(x - 102)
        """
        # TODO: floating point values
        product = (value - 100) * (value - 102)  # (x - 100)(x - 102)
        return -(math.exp(-1)) + product  # -exp(-1) + (x - 100)(x - 102)

    @staticmethod
    def _less_than_100(value):
        """Piecewise 2 of 2
        x = -exp(-(x / 100)^2))
        """
        inner = float(value / 100.0)  # (x / 100)
        inner = -(math.pow(inner, 2))  # -(x / 100)^2)
        return -(math.exp(inner))


class PopulationSpace:
    """Evolutionary Search. Candidate Solutions."""
    def __init__(self):
        self.current_gen = []
        self.range_lower_bound = -10
        self.range_upper_bound = 110
        self._initial_population()

    def __str__(self):
        for solution in self.current_gen:
            print("{} ".format(solution.y))
        print("\n")

    def _initial_population(self):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        for i in range(50):
            random_value = random.randint(-10, 100)
            initial_solution = Solution(random_value)
            self.current_gen.append(initial_solution)

    def generate(self, next_gen):
        """Sets the current generation equal to the influenced and updated next generation."""
        self.current_gen = next_gen

    def evaluate(self):
        """Indirectly evaluates the solutions (via each solution's evaluate() method.)"""
        # TODO: floating point values
        for solution in self.current_gen:                                       # Check value of each solution
            solution.evaluate()

        self._rank()                                                            # "Rank" the new values (i.e. sort)

    def _rank(self):
        """Sorts the Population by their fitness score (i.e. their y-value)
        Fitness determined by piecewise function as defined by assignment instructions.
        Note: Indexes can also intuitively associate a Solution's fitness.
        e.g. index 0 is always the "Super Elite" and [0 to (size * 0.2)] are the "Elites".
        """
        self.current_gen = sorted(self.current_gen, key=lambda solution: solution.y)    # Sort by Solutions' y-values

    def accept(self):
        """Determines the individuals of the Population that will influence the Belief Space (i.e. the Elites).
        The Population is already sorted/ranked beforehand."""
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
        self.minima_y = None
        self.maxima_y = None
        self.minima_x = None
        self.maxima_x = None
        self.elites = []
        self.super_elite = None

    def update(self, elites):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values.
        "elites" is pre-sorted before being passed-in here."""
        self.elites = elites                                                    # Record the top-performers
        self.super_elite = elites[0]                                            # Record single, top performer
        self.minima_x = elites[-1].x                                            # X-value of lowest value
        self.minima_y = elites[-1].y                                            # Y-value of lowest value
        self.maxima_x = elites[0].x                                             # X-value of highest value
        self.maxima_y = elites[0].y                                             # Y-value of highest value

    def influence(self, current_gen):
        """Generates the next generation's individuals using knowledge from the Belief Space."""
        # CHECK: Local min and max
        next_generation = []                                                    # Redundant, but helps intuitive reading
        x_local_min = self.minima_x                                             # X of lower bound of current range
        x_local_max = self.maxima_x                                             # X of upper bound of current range

        for solution in current_gen:
            target = self.super_elite.y                                         # Best solution this generation
            mutation_occurs = random.randint(0, 1)                              # 50% prob. of applying random value
            solution_value = solution.y

            if mutation_occurs:
                mutation = self._mutation_value(x_local_min, x_local_max)       # Generate a randomized mutation value
                solution.x = mutation                                           # Store the mutated value
                next_generation.append(solution)                                # Add mutated individual to next gen.
                # print("[DEBUG]: Mutation")
            elif solution_value > target:
                solution.y = solution.y - 1                                     # Tend DOWNWARD to best score thus far
                next_generation.append(solution)                                # Add updated individual to next gen.
                # print("[DEBUG]: MORE")
            elif solution_value < target:
                solution.y = solution.y - 1                                     # Tend UPWARD to best score thus far
                next_generation.append(solution)                                # Add updated individual to next gen.
                # print("[DEBUG]: LESS")
            else:
                next_generation.append(solution)                                # Individual is already at best value
                # print("[DEBUG]: NONE")

        return next_generation                                                  # Return the new (influenced) generation

    @staticmethod
    def _mutation_value(minimum, maximum):
        """Returns a random value between the previous generation's minimum and maximum x-values.
        Able to handle min/max ranges containing negatives and/or decimals."""
        # TODO: Use same range record
        # TODO: Need seed?
        value_range = abs(maximum - minimum)                                    # Absolute distance between min and max
        random_float = random.random()                                          # Get a random float [0.0, 1.0)

        random_offset = value_range * random_float                              # "Map" the range to the random float

        return minimum + random_offset                                          # Return the random number in the range


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



