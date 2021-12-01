import pandas as pd


def count_increased_depths(filename: str) -> int:
    """Tally the number of times a depth increased compared to the previous
    depth reading. Iterate over the inputs only once (during initial file read)
    and perform calculations simultaneously.
    """
    prev_depth = 0
    # ignore the initial jump from 0 -> first_value
    total_increased = -1
    
    with open(filename, 'r') as f:
        
        for depth in f.readlines():
            cur_depth = int(depth)
            if cur_depth > prev_depth:
                total_increased += 1
            prev_depth = cur_depth
    return total_increased


def count_increased_with_pandas(filename: str) -> int:
    df = pd.read_csv(filename, names=['depths'])
    return (df['depths'].shift(-1) > df['depths']).sum()
     
    
def count_rolling_increased_depths(filename: str) -> int:
    df = pd.read_csv(filename, names=['depths'])
    df['rolling'] = df['depths'].rolling(3).sum()
    df['increased'] = df['rolling'].shift(-1) > df['rolling']
    return df['increased'].sum()
    

tests = (
    (count_increased_depths('test1.txt'), 7),
    (count_increased_with_pandas('test1.txt'), 7),
    (count_rolling_increased_depths('test1.txt'), 5)
)

for test_num, test_case in enumerate(tests):
    test, correct = test_case
    assert test == correct, f"Test #{test_num} failed, got {test} instead of {correct}."


print('All tests passed.')


if __name__ == "__main__":
    total_increased = count_increased_depths('depths.txt')
    print("part 1:", total_increased)
    
    rolling_increased = count_rolling_increased_depths('depths.txt')
    print("part 2:", rolling_increased)