import pandas as pd


def calc_final_position(fname: str) -> int:
    df = pd.read_csv(fname, sep=" ", names=['dir', 'dist'])
    horiz = df.loc[df['dir'] == 'forward', 'dist'].sum()
    gross_down = df.loc[df['dir'] == 'down', 'dist'].sum()
    gross_up = df.loc[df['dir'] == 'up', 'dist'].sum()
    return horiz * (gross_down - gross_up)


def calc_aim(fname: str) -> int:
    df = pd.read_csv(fname, sep=" ", names=['dir', 'dist'])
    forward_mask = df['dir'] == 'forward'
    up_mask = df['dir'] == 'up'
    df.loc[up_mask, 'dist'] = -df.loc[up_mask, 'dist']
    aims = df.loc[~forward_mask, 'dist'].cumsum()
    df['aim'] = None
    df.loc[~forward_mask, 'aim'] = aims
    df['aim'] = df['aim'].fillna(method='ffill').fillna(0)
    df.loc[forward_mask, 'depth'] = df['aim'] * df['dist']
    
    return int(df['depth'].sum() * df.loc[forward_mask, 'dist'].sum())
    

tests = (
    (calc_final_position('test.txt'), 150),
    (calc_aim('test.txt'), 900)
)

for test_num, test_case in enumerate(tests):
    pred, actual = test_case
    assert pred == actual, f"test #{test_num} failed. got {pred} instead of {actual}"
    
print("All tests passed.")


if __name__ == "__main__":
    p1 = calc_final_position("inputs.txt")
    print(p1)
    p2 = calc_aim("inputs.txt")
    print(p2)