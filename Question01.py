# Author: Jamal Huraibi
# Assignment: 5
# Question: 1


class Population:
    """Evolutionary Search. Candidate Solutions."""
    population = None
    time = None

    def __init__(self):
        pass

    def update(self, ):
        pass


class Belief:
    """Knowledge. Information stored by ancestors, accessed by current generation."""
    range = None

    def __init__(self):
        pass

    @staticmethod
    def elevate_to_good_range():
        pass


if __name__ == '__main__':
    pass

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

