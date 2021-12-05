import numpy as np
from chairs import sample, sample2, waiting_area


def map_area(data):
    return np.array(
        [[np.nan if c == "." else 0 for c in row] for row in data.split("\n")]
    )


def analyze_chairs(m):
    """Iterate through the room & build two lists of indices.
    Use a rolling window to search for empty chairs w/ no-one seated nearby
     -- add to 'going_to_sit'
    Simultainesouly look for filled chairs that ALSO have 4+ neighbors
     -- add to 'going_to_leave'
    
    return (arrive_rows, arrive_cols), (leave_rows, leave_cols)
    which can be used later to slice into 'm'
    """
    arrive_rows, arrive_cols = [], []
    leave_rows, leave_cols = [], []
    row_dim, col_dim = m.shape

    for row, one_row in enumerate(m):
        for col, val in enumerate(one_row):
            r_min = max(0, row - 1)
            r_max = min(row_dim, row + 2)
            c_min = max(0, col - 1)
            c_max = min(col_dim, col + 2)
            rolling_window = m[r_min:r_max, c_min:c_max]
            # Will someone sit down?
            if (val == 0) and (np.nansum(rolling_window) == 0):
                arrive_rows.append(row)
                arrive_cols.append(col)
            # Will this chair vacate?  (cutoff @ 5 because of counting self)
            if (val == 1) and (np.nansum(rolling_window) >= 5):
                leave_rows.append(row)
                leave_cols.append(col)

    return (arrive_rows, arrive_cols), (leave_rows, leave_cols)


def analyze_sightline(m):
    """Iterate through the room & build two lists of indices.
    
     -- add to 'going_to_sit'
    Simultainesouly look for filled chairs that ALSO have 5+ neighbors
     -- add to 'going_to_leave'
    
    return (arrive_rows, arrive_cols), (leave_rows, leave_cols)
    which can be used later to slice into 'm'
    """
    m = np.pad(m, pad_width=2, mode="constant", constant_values=0)
    arrive_rows, arrive_cols = [], []
    leave_rows, leave_cols = [], []
    row_dim, col_dim = m.shape
    flipped_m = np.fliplr(m)

    for i, one_row in enumerate(m[2:-2]):
        for j, val in enumerate(one_row[2:-2]):
            if val in [0, 1]:
                # Account for the border offset
                row, col = i + 2, j + 2
                viewable = count_viewable(row, col, m, flipped_m)
                # Will someone sit down?
                if (val == 0) and (viewable == 0):
                    arrive_rows.append(i)
                    arrive_cols.append(j)
                # Will this chair vacate?
                if (val == 1) and (viewable >= 5):
                    leave_rows.append(i)
                    leave_cols.append(j)

    return (arrive_rows, arrive_cols), (leave_rows, leave_cols)


def count_viewable(row, col, m, flipped_m):
    """Before coming in, should pad with a border of 2
    This allows np.diagonal() to work.
    
    m = np.pad(m, pad_width=2, mode='constant', constant_values=0)
    row, col = row+2, col+2
    """
    val = m[row, col]
    n_rows, n_cols = m.shape

    up = m[:row, col][::-1]
    down = m[row + 1 :, col]
    left = m[row, :col][::-1]
    right = m[row, col + 1 :]

    d1u = m[:row, :col].diagonal(offset=col - row)[::-1]
    d2u = flipped_m[:row, : (n_cols - col)].diagonal(offset=n_cols - col - row - 1)[
        ::-1
    ]
    d1d = m[row + 1 :, col + 1 :].diagonal()
    d2d = flipped_m[row + 1 :, (n_cols - col) :].diagonal()

    total_seen = 0

    for view in [up, down, left, right, d1u, d2u, d1d, d2d]:
        view = view[~np.isnan(view)]
        total_seen += view[0]

    return total_seen


def cycle_once(m, func=analyze_chairs):
    """Analyze a seating map (m) and change it in place.
    Return the updated map, and a flag for whether the room is still unstable
    """
    going_to_sit, going_to_leave = func(m)

    print(
        f"Arrived  {len(going_to_sit[0])} | {len(going_to_leave[0])}  Left  |  Current  {int(np.nansum(m))}"
    )

    if going_to_sit == going_to_leave:
        print("No changes!  Exiting . . . ")
        return m, False

    m[going_to_sit] = 1
    m[going_to_leave] = 0

    return m, True


def stabalize_room(data, func=analyze_chairs):
    """Parse the raw data, then alternate between filling & vacating
    chairs in the waiting room.
    
    When no more changes can occur, exit the cycle & return the total 
    number of seated visitors.
    """
    m, still_in_flux = map_area(data), True

    while still_in_flux:
        m, still_in_flux = cycle_once(m, func)

    return int(np.nansum(m))


def show_room(m):
    """NOT USED: Helper function to visualize using original characters"""
    view_map = {np.nan: ".", 0: "L", 1: "#"}
    z = np.vectorize(view_map.get)(m)
    z = np.vectorize({"None": ".", "L": "L", "#": "#"}.get)(z)
    z_printout = "\n".join("".join(row) for row in z)
    return z_printout


print(sample)
assert stabalize_room(sample) == 37
assert stabalize_room(sample, analyze_sightline) == 26


if __name__ == "__main__":
    print(stabalize_room(waiting_area))
    print(stabalize_room(waiting_area, analyze_sightline))
