from math import prod
import networkx as nx
from bag_rules import sample, sample_2, nested_sample, rules


def parse_row(row):
    """For a single rule (row), create acceptable input for nx.build_edges_from()"""
    parent, children = row.split(" bags contain ")
    parsed_children = []
    if children != "no other bags.":
        children = children.replace("bags", "").split(", ")
        for child in children:
            num, adj, color = child.split(" ")[:3]
            name = adj + " " + color
            parsed_children.append((parent, name, {"max_count": int(num)}))
    return {parent: parsed_children}


def parse_all(text_blob):
    """Iterate over all given rules (text_blob) and build nodes & edges 
    in a format that is acceptable for: 
        nx.add_nodes_from(nodes)
        nx.add_edges_from(edges)
    """
    parsed_rules = {}
    for row in text_blob.split("\n"):
        parsed_rules.update(parse_row(row))
    edges = []
    for grp in parsed_rules.values():
        edges += grp
    return edges


def build_graph(edges):
    """Create a directed graph between all bag colors
    also contains 'max_count' data
    """
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def count_total_bags_contained_in(bag, G):
    sink_nodes = [node for node, n_out in G.out_degree(G.nodes()) if n_out == 0]
    all_paths = [
        p
        for sink in sink_nodes
        for p in nx.all_simple_paths(G, source=bag, target=sink)
    ]
    total = 0
    already_seen = set()
    for path in all_paths:
        for parent, child in zip(path[:-1], path[1:]):
            partial_path = tuple(path[: path.index(child) + 1])

            if partial_path not in already_seen:
                par_chld_pairs = zip(partial_path[:-1], partial_path[1:])
                multipliers = [
                    G.get_edge_data(par, ch)["max_count"] for par, ch in par_chld_pairs
                ]
                total += prod(multipliers)
                already_seen.add(partial_path)
    return total


# { answer : text_blob}  for P1: key is str(answer)  for P2 it is just a nomral number
# WARNING: Cannot have multiple different text_blobs w/ the same numerical answer
tests = {"4": sample, 32: sample, 126: sample_2, 35653: nested_sample}

for i, (ans, text_blob) in enumerate(tests.items()):
    G = build_graph(parse_all(text_blob))
    # Part 1 : How many ultimate parent bags evenutally can hold 'shiny gold'?
    if isinstance(ans, str):
        pred = len(nx.algorithms.ancestors(G, "shiny gold"))
        assert pred == int(
            ans
        ), f"Test #0 Failed\n\t\tTrue =>  {ans} != {pred}  <= Predicted"
    # Part 2: How many bags can a 'shiny gold' bag hold (with all filled to capacity)?
    else:
        pred = count_total_bags_contained_in("shiny gold", G)
        assert pred == ans, f"#{i} Failed\n\t\tTrue =>  {ans} != {pred}  <= Predicted"


if __name__ == "__main__":
    G = build_graph(parse_all(rules))
    # Part 1
    print(len(nx.algorithms.ancestors(G, "shiny gold")))
    # Part 2
    print(count_total_bags_contained_in("shiny gold", G))
