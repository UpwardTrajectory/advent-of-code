import numpy as np
import networkx as nx
from corrupted_msgs import sample, msg


def parse_msg(data: str):
    rules, candidates = data.split("\n\n")

    parsed_rules = {}
    for row in rules.split("\n"):
        num, rule = row.split(": ")
        rule = np.array(
            [
                [num_or_char(x) for x in single_rule.split(" ")]
                for single_rule in rule.split(" | ")
            ]
        )
        if isinstance(rule[0][0], str):
            rule = rule[0][0]
        parsed_rules[int(num)] = rule

    candidates = candidates.split("\n")
    return parsed_rules, candidates


def num_or_char(x: str):
    try:
        return int(x)
    except ValueError:
        return x.strip('"')


def check(rules):
    ends = {k: v for k, v in rules.items() if isinstance(v, str)}
    middles = {
        k: v for k, v in rules.items() if any([end in v.ravel() for end in endpoints])
    }
    starts = {
        k: v
        for k, v in rules.items()
        if all([v not in endpoints.values() for v in rules.values()])
    }
    return starts, middles, ends


rules, candidates = parse_msg(sample)
