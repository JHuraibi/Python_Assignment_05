# Author: Jamal Huraibi, fh1328
# Assignment []
# Question []

from decimal import *

if __name__ == '__main__':

    value = 100 + Decimal(1e-20)
    test = 100.00000000000000000004

    decTest = Decimal(test)

    if test > (100 + Decimal(1e-20)):
        print("TRUE")

    if decTest > (100 + Decimal(1e-20)):
        print("TRUE")

    # print(value)
