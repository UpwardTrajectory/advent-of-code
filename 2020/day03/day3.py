import numpy as np
from treemaps import sample, treemap


def treemap_to_array(treemap):
    """Convert string_blob treemap into numpy boolean array"""
    return np.array([[1 if c == "#" else 0 for c in row] for row in treemap.split("\n")])


def count_trees(treemap, delta_x, delta_y):
    """Starting from upper left corner, move toward the bottom of a treemap
    along the given slope (note delta_y must be positive to move downward)
    
    Count the number of trees encountered at the whole number "stops" of that slope
    Partial collisions or trees that are encountered part-way through a "slope-jump"
    are NOT counted. 
    i.e.  if given a slope of (8, 10) it will not count a tree @ (4, 5) even though
          a collision would have occured.
    """
    cur_x, cur_y = 0, 0
    tally = 0
    
    # Avoid infinite while loop
    if delta_y <= 0:
        raise ValueError("delta_y must be positive in order to move downhill.")
            
    while cur_y < len(treemap):
        if treemap[cur_y, cur_x]:
            tally += 1
        cur_x = (cur_x + delta_x) % treemap.shape[1]
        cur_y += delta_y
      
    return tally
      
    
# Testing
sample_arr = treemap_to_array(sample)
sample_tree_count = count_trees(sample_arr, 3, 1)
assert sample_tree_count == 7, f"should be 7, we got {sample_tree_count}"


if __name__ == "__main__":
    
    treemap_arr = treemap_to_array(treemap)
    tree_counts = {
        (1,1): None,
        (3,1): None,
        (5,1): None,
        (7,1): None,
        (1,2): None,
    }
    
    for slope in tree_counts:
        tree_counts[slope] = count_trees(treemap_arr, *slope)
        
    print(tree_counts[(3,1)])
    print(np.prod([float(x) for x in tree_counts.values()]))
    # Why float()?
    # https://numpy.org/doc/stable/reference/generated/numpy.prod.html
    # Arithmetic is modular when using integer types, and no error is raised on overflow.