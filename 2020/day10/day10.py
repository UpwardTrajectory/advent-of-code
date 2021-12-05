from adapters import sample, sample2, jolt_adapters
import networkx as nx


def count_gaps(data):
    ada_options = sorted([int(x) for x in data.split("\n")])
    jolts = 0
    # The final jump to our device is always 3
    jolt_jump_counter = {0: 0, 1: 0, 2: 0, 3: 1}

    for ada in ada_options:
        jump = ada - jolts
        jolts += jump
        if jump not in jolt_jump_counter:
            raise ValueError(f"There's a problem getting to the {ada} jolt adapter.")
        jolt_jump_counter[jump] += 1

    return jolt_jump_counter[3] * jolt_jump_counter[1]


def build_graph(data):
    """Create a graph with a single point of entry, and a single point of exit"""
    ada_options = [-3, 0] + sorted([int(x) for x in data.split("\n")])
    ada_options.append(ada_options[-1] + 3)

    edges = set()
    for i, ada in enumerate(ada_options):
        next_3 = ada_options[i + 1 : i + 4]
        next_3_filtered = [x for x in next_3 if (x - ada) <= 3]
        next_3_filtered = [(ada, node) for node in next_3_filtered]
        edges.update(next_3_filtered)
    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


def find_entropy_zones(G):
    """Isolate the (start, stop) zones for any part of the graph containing 
    more than one possible path.
    
    return a list of these windows
    """
    nodes = sorted(G)
    prev_n_out = 0
    open_gate_to_chaos = nodes[0]
    zones_of_chaos = []

    for node in nodes:

        able_to_leave_chaos = (
            prev_n_out == 1
            and G.in_degree(node) == 1
            and open_gate_to_chaos != prev_node  # Skip single-paths
        )

        if able_to_leave_chaos:
            zones_of_chaos.append((open_gate_to_chaos, prev_node))
            open_gate_to_chaos = node

        prev_node, prev_n_out = node, G.out_degree(node)

    return set(zones_of_chaos)


def count_paths(data):
    """Find zones of chaos within the list of adapters
    (any section with more than one possible option forward)
    count the ways through that discrete section, and multiply as we go
    to find the count of all possible paths.
    
    If the count of all possible paths through looks like this:
    1 -> (4) -> 1 -> (3) -> 1 -> (7) -> 1
    
    zones of chaos are inside parens:  (num_ways_through)
    these are the numbers that will be multiplied for a total of 
    4 * 3 * 7 = 84 paths from start to finish
    """
    G = build_graph(data)
    zones_of_chaos = find_entropy_zones(G)
    total_paths = 1

    for chaos_window in zones_of_chaos:
        enter, depart = chaos_window
        ways_through = sum(
            [1 for _ in nx.all_simple_paths(G, source=enter, target=depart)]
        )
        total_paths *= ways_through

    return total_paths


assert count_gaps(sample) == 35, "first failed"
assert count_gaps(sample2) == 220, "second failed"
assert count_paths(sample) == 8, "Part 2: first failed"
assert count_paths(sample2) == 19208, "Part 2: second failed"


if __name__ == "__main__":
    print(count_gaps(jolt_adapters))
    print(count_paths(jolt_adapters))
