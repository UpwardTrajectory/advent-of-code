passwords = """1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc"""


def parse_and_test_input(raw_pw_str, sep=",", test_func=test_record_min_max):
    """Parse a string blob where each row is a record of password + rules
    then determine if the password meets the rule specifications using test_func
    
    return the total number of correct passwords
    """
    total = 0
    for row in passwords.split("\n"):
        rules, pw = row.split(":")
        record = {}
        record["pw"] = pw[1:]

        parsed_rules = []

        for rule in rules.split(sep):
            one_rule = {}
            nums, char = rule.split(" ")
            low, high = nums.split("-")
            one_rule["low"] = int(low)
            one_rule["high"] = int(high)
            one_rule["char"] = char
            parsed_rules.append(one_rule)

        record["rules"] = parsed_rules
        total += test_func(record)
    return total


def test_record_min_max(record):
    """Determine whether the desired char is represented a certain number of times
    (inclusively between a given min & max)
    """
    pw = record["pw"]

    for rule in record["rules"]:
        true_num = pw.count(rule["char"])
        if (true_num < rule["low"]) | (true_num > rule["high"]):
            return False
    return True


assert parse_and_test_input(passwords) == 2, print(f"Should be 2")


def test_record_position(record, num_repeats=1):
    """Determine whether the desired character appears exactly num_repeats times
    in the desired indices (BEWARE: starting @ 1 not 0)
    """
    pw = record["pw"]

    for rule in record["rules"]:
        # Silly indexing starting @ 1 in the problem
        true_positions = set(i + 1 for i in find_offsets(pw, rule["char"]))
        desired_positions = set([rule["low"], rule["high"]])

        if len(true_positions & desired_positions) == num_repeats:
            return True
    return False


def find_offsets(haystack, needle):
    """
    Find the start of all (possibly-overlapping) instances of needle in haystack
    TY: https://stackoverflow.com/a/11122388/14083170
    """
    offs = -1
    while True:
        offs = haystack.find(needle, offs + 1)
        if offs == -1:
            break
        else:
            yield offs


assert parse_and_test_input(passwords, test_func=test_record_position) == 1, print(
    f"Part 2 should be 1"
)


if __name__ == "__main__":

    with open("inputs.txt", "r") as f:
        passwords = f.read()

    for f in [test_record_min_max, test_record_position]:
        print(parse_and_test_input(passwords, test_func=f))
