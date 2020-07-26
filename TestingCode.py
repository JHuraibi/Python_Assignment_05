# Author: Jamal Huraibi, fh1328
# Assignment 5
# Testing: Expression as List item

import random
from decimal import *

class Solution():
    def __init__(self, x):
        self.x = x
        self.y = random.randint(0, 100)


if __name__ == '__main__':
    population = [Solution] * 50
    for i in range(50):
        solution = Solution(i)
        population[i] = solution
        print(population[i].y, end=" ")

    # print(population[0].y)
    population = sorted(population, key=lambda solution: solution.y)
    # population.sort()
    print()
    for i in range(50):
        print(population[i].y, end=" ")
    print()
    print("DONE")

    # def evaluate(self):
    #     value = self.x
    #     if value > (100.0 + 1e-18):  # 100.000 000 000 000 000 000 0
    #         self.y = _larger_than_100(solution)  # x > 100
    #     else:
    #         self.current_gen[i] = _less_than_100(solution)  # x <= 100