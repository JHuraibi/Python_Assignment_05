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
        self.evaluate_solution()                                                         # Calculate and set y-value

    def __str__(self):
        x = format(self.x, '.21f')
        y = format(self.y, '.21f')
        return "x = %-.21s, y = %-.21s" % (x, y)

    def evaluate_solution(self):
        """Evaluates the performance of the Population's individuals.
        Method defined as "obj()" in academic paper."""
        # CHECK: floating point values
        if self.x > (100.0 + 1e-18):
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

    def __getitem__(self, item):
        return population[item]

    def _initial_population(self):
        """Generates the initial 50 random solutions (i.e. the population).
        Values range from -10 to 110."""
        for i in range(50):
            random_value = random.randint(-10, 100)                             # Random value -10 to 100
            initial_solution = Solution(random_value)                           # Initialize the solution with the value
            self.current_gen.append(initial_solution)                           # Add to the initial generation

    def generate(self, next_gen):
        """Sets the current generation equal to the influenced and updated next generation."""
        self.current_gen = next_gen                                             # Store the new generation of solutions

    def evaluate(self):
        """Indirectly evaluates the solutions (via each solution's evaluate() method.)"""
        # TODO: floating point values
        for solution in self.current_gen:                                       # Check value of each solution
            solution.evaluate_solution()                                        # Invoke class Solution evaluate method

        self._rank()                                                            # "Rank" the new values (i.e. sort)

    def _rank(self):
        """Sorts the Population by their fitness score (i.e. their y-value)
        Fitness determined by piecewise function as defined by assignment instructions."""
        self.current_gen = sorted(self.current_gen, key=lambda solution: solution.y)    # Sort by solution y-values

    def accept(self):
        """Determines the individuals of the Population that will influence the Belief Space (i.e. the Elites).
        The Population is already sorted/ranked beforehand.
        If population is static at 50, then will always be 10."""
        elite_threshold = len(self.current_gen) * 0.2                           # 20% of population size
        elite_threshold = math.ceil(elite_threshold)
        return self.current_gen[0:elite_threshold]


class BeliefSpace:
    """Information, or knowledge, of ancestors. Influenced by current generations and accessed by future generations."""
    def __init__(self):
        self.elites = []
        self.super_elite = None
        self.minima_y = None                                                    # Lowest solution value of the Elites
        self.maxima_y = None                                                    # Highest solution value of the Elites
        self.lower_bound_x = -10                                                # Lowest x-value of the Elites (so far)
        self.upper_bound_x = 110                                                # Highest x-value of the Elites (so far)
        self.step = 1.0                                                         # Amount to tend x toward super elite

    def update(self, elites):
        """Adds the experiences of the accepted individuals of the Population by:
        1. Recording the current generation's top performers (elites).
        2. Recording the current generation's minimum and maximum values.
        3. Update the Belief Space's normative knowledge.
        List "elites" is pre-sorted before being passed-in."""
        self.elites = elites                                                    # Record the top-performers
        self.super_elite = elites[0]                                            # Record single, top performer
        self.minima_y = elites[-1].y                                            # Lowest solution value of elites
        self.maxima_y = elites[0].y                                             # Highest solution value of elites
        self._update_normative_knowledge(elites)                                # Update x-value range of elites

    def _update_normative_knowledge(self, new_elites):
        """Updates the x-values of the "good range" of solutions."""
        new_elites = sorted(new_elites, key=lambda solution: solution.x)        # Sort the new elites by their x-values
        new_elites_upper_x = new_elites[-1].x                                   # Highest x-value of the new elites
        new_elites_lower_x = new_elites[0].x                                    # Lowest x-value of the new elites

        if new_elites_upper_x > self.upper_bound_x:
            self.upper_bound_x = new_elites_upper_x                             # Highest x of new elites is new highest

        if new_elites_lower_x < self.lower_bound_x:
            self.lower_bound_x = new_elites_lower_x                             # Lowest x of new elites is new lowest

    def influence(self, current_gen):
        """Generates the next generation's individuals using knowledge from the Belief Space."""
        next_generation = []                                                    # Redundant, but helps intuitive reading
        step = self.step

        for solution in current_gen:
            mutation_occurs = random.randint(0, 1)                              # 50% prob. of applying random value

            if mutation_occurs:
                mutation = self._mutation_value()                               # Generate a randomized mutation value
                solution.x = mutation                                           # Store the mutated value
                next_generation.append(solution)                                # Add mutated individual to next gen.
            elif self._out_of_good_range(solution.x):
                solution.x = self._good_range_value(solution.x)                 # Put x-value into the "good range"
                next_generation.append(solution)                                # Add updated individual to next gen.
            else:
                solution.x = self._tend_toward_super_elite(solution.x)
                next_generation.append(solution)                                # Individual is already at best value

        self._update_step_amount()                                              # Update the step
        return next_generation                                                  # Return the new (influenced) generation

    def _mutation_value(self):
        """Returns a random value between the previous generation's minimum and maximum x-values.
        Able to handle min/max ranges containing negatives and/or decimals."""
        minimum = self.lower_bound_x                                            # Current local minimum
        maximum = self.upper_bound_x                                            # Current local maximum
        value_range = abs(maximum - minimum)                                    # Absolute distance between min and max

        random_float = random.random()                                          # Get a random float [0.0, 1.0)
        random_offset = value_range * random_float                              # "Map" the range to the random float

        return minimum + random_offset                                          # Return the random number in the range

    def _out_of_good_range(self, x_value):
        """Checks if the x-value is out of the "good range"."""
        # CHECK: Precision. Possibly use same method as _mutation_value.
        return x_value < self.lower_bound_x or x_value > self.upper_bound_x     # Is x_value within the "good range"?

    def _good_range_value(self, x_value):
        """Returns the boundary value of the "good range" that x_value is closest to.
        Allows solution x-values to "jump into the good range". """
        distance_to_lower_bound = abs(x_value - self.lower_bound_x)             # How much x_value is from lowest x
        distance_to_upper_bound = abs(x_value - self.upper_bound_x)             # How much x_value is from highest x

        if distance_to_lower_bound < distance_to_upper_bound:                   # x_value closer to upper or lower x?
            return self.lower_bound_x                                           # Was closer to lower, return lower
        else:
            return self.upper_bound_x                                           # Was closer to upper, return upper

    def _tend_toward_super_elite(self, x_value):
        """Returns an adjusted x-value. Adjust is to tend toward the x-value of the super elite's."""
        target = self.super_elite.x                                             # x-value of best solution (super elite)
        if x_value > target:
            return x_value - self.step                                          # Tend DOWNWARD to best score thus far
        else:
            return x_value + self.step                                          # Tend UPWARD to best score thus far

    def _update_step_amount(self):
        """Fine-tunes the value that Solution x-values will be adjusted by next generation."""
        self.step = self.step / 2.0                                             # Halve the step amount


if __name__ == '__main__':
    time = 0                                                                    # t
    endTime = 100                                                               # How many "generations" to run

    population = PopulationSpace()                                              # Initialize Pt (t = 0)
    belief = BeliefSpace()                                                      # Initialize Bt (t = 0)

    # --| Evolution loop |--
    while time < endTime:
        population.evaluate()                                                   # Evaluate Pt (t = time). AKA obj()
        belief.update(population.accept())                                      # Update Bt using accepted Pt values
        influenced = belief.influence(population.current_gen)                   # Influence next gen. using Bt knowledge
        population.generate(influenced)                                         # Generate the next generation
        time = time + 1                                                         # Increment time/generation
    # --| End Evolution loop |--

    print("Final Values\n")
    print("[Best]   ", end="")
    print(population.current_gen[0])                                            # Super elite (1)

    for j in range(1, 10):                                                      # Remaining Elites (2 - 10)
        if j + 1 < 10:
            print(" ", end="")                                                  # (Extra space when j is single-digit)

        print("  [%i]   " % (j + 1), end="")                                    # Line number
        print(population.current_gen[j])                                        # x and y value of individual solution

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