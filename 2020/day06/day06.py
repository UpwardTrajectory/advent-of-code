from questions import tests, all_answers


def count_answers(blob, func=set.union):
    parsed_qs = [[set(p) for p in grp.split("\n")] for grp in blob.split("\n\n")]
    return sum([len(func(*grp)) for grp in parsed_qs])


assert count_answers(tests, set.union) == 11
assert count_answers(tests, set.intersection) == 6


if __name__ == "__main__":
    print(count_answers(all_answers, set.union))
    print(count_answers(all_answers, set.intersection))
