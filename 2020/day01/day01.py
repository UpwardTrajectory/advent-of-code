import numpy as np
import itertools


with open("inputs.txt", "r") as f:
    expense_report = f.read()

expense_report = [float(x) for x in expense_report.split("\n")]


def get_result(
    expense_report, tally=2020, in_operation=np.sum, out_operation=np.prod, n=2
):
    """Given an expense_report : list
    get all combinations of expense_report repeated n times
    use in_operation() : must operate on an array
    to find the tally : something that in_operation can yield
    then return the out_operation() on the successful combo
    """
    possible = itertools.combinations(expense_report, n)

    for group in possible:
        if in_operation(group) == tally:
            return int(out_operation(group))
    return None


if __name__ == "__main__":

    for n in [2, 3]:
        print(get_result(expense_report, n=n))
