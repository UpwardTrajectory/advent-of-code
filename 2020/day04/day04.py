from passports import sample, valid, invalid, batched_passports
import re


def parse_multiple(passports):
    """Convert text blob into list of dictionaries
    No validation is performed in this step
    """
    as_strings = [
        row.replace(" ", ",").replace("\n", ",") for row in passports.split("\n\n")
    ]

    parsed_passports = []
    for passport in as_strings:
        parsed_pp = {}
        for attribute in passport.split(","):
            k, v = attribute.split(":")
            parsed_pp[k] = v
        parsed_passports.append(parsed_pp)
    return parsed_passports


def validate_one(pp):
    """byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.
    """
    try:
        # TO-DO: convert to dictionary unpacking from the inputs
        byr = pp["byr"]
        iyr = pp["iyr"]
        eyr = pp["eyr"]
        hgt = pp["hgt"]
        hcl = pp["hcl"]
        ecl = pp["ecl"]
        pid = pp["pid"]

        all_necessary_attributes = {
            "byr": check_yr(byr, 1920, 2002),
            "iyr": check_yr(iyr, 2010, 2020),
            "eyr": check_yr(eyr, 2020, 2030),
            "hgt": check_height(hgt),
            "hcl": check_hcl(hcl),
            "ecl": check_ecl(ecl),
            "pid": check_pid(pid),
        }
        return True if sum(all_necessary_attributes.values()) == 7 else False
    except KeyError:
        # silence predictable errors
        return False
    except Exception as e:
        raise e


def check_yr(yr, low, high):
    """Verify yr is 4 digits and inside acceptable range.
    Decimal years (ie. 1982.5) are not allowed and will return False
    """
    yr = float(yr)
    return (yr == int(yr)) & (low <= yr <= high)


def check_height(hgt):
    """hgt (Height) - a number followed by either cm or in:
    If cm, the number must be at least 150 and at most 193.
    If in, the number must be at least 59 and at most 76.
    """
    num, unit = hgt[:-2], hgt[-2:]

    if unit == "cm" and (150 <= float(num) <= 193):
        return True
    if unit == "in" and (59 <= float(num) <= 76):
        return True
    return False


def check_hcl(hcl):
    return bool(re.search(r"^#(?:[0-9a-f]{3}){1,2}$", hcl))


def check_ecl(ecl):
    return ecl in ("amb", "blu", "brn", "gry", "grn", "hzl", "oth")


def check_pid(pid):
    return bool(re.search(r"^\s*(?:[0-9]{9})\s*$", pid))


def validate_keys(parsed_pp):
    """Ensure 7 essential keys are in a passport.
    'ecl', 'pid', 'eyr', 'hcl', 'byr', 'iyr', 'hgt'
    """
    necessary_keys = set(["ecl", "pid", "eyr", "hcl", "byr", "iyr", "hgt"])
    current_keys = set(parsed_pp.keys())
    current_keys.discard("cid")
    return current_keys == necessary_keys


def count_valid_from_batch(passports, validate_func):
    return sum(validate_func(pp) for pp in parse_multiple(passports))


assert (
    count_valid_from_batch(sample, validate_keys) == 2
), f"sample failed: 2 vs {count_valid_from_batch(sample)}"
assert (
    count_valid_from_batch(sample, validate_one) == 2
), f"sample failed: 2 vs {count_valid_from_batch(sample)}"
assert count_valid_from_batch(invalid, validate_one) == 0, "invalid failed"
assert (
    count_valid_from_batch(valid, validate_one) == 4
), f"valid failed: 4 vs {count_valid_from_batch(valid)}"


if __name__ == "__main__":
    print(count_valid_from_batch(batched_passports, validate_keys))
    print(count_valid_from_batch(batched_passports, validate_one))
