from typing import List

SAMPLE = "0,3,6"
ELVES_HAVE_SPOKEN = "11,0,1,10,5,19"


# def speak_next(nums: List, shout=False):
#     """DEPRECIATED
#     Somewhat naive searching through a list in reverse order.
#     """
#     most_recent, others_reversed = nums[-1], nums[-2::-1]
#     shouting = f"Turn {len(nums)+1}:  {most_recent}"
    
#     if most_recent not in others_reversed:
#         saying = 0
#         shouting += " not found. Saying 0"
#     else:
#         found = False
#         steps = 0
#         while not found:
#             if others_reversed[steps] == most_recent:
#                 saying = steps + 1
#                 shouting += f" found. Saying {saying}"
#                 found = True
#             steps += 1

#     if shout is True:
#         print(shouting)
#     nums.append(saying)
#     return nums


def speak_next(most_recent: int, turn_num: int, nums_spoken: dict):
    """
    If you want to optimize something in Python, 
    it probably involves dictionaries or tuples.
                     ~ My friend Miles
    """
    if most_recent not in nums_spoken:
        saying = 0
    else:
        saying = turn_num - nums_spoken[most_recent]

    nums_spoken[most_recent] = turn_num
    turn_num += 1
    return saying, turn_num, nums_spoken
    

def play_game(data: str, max_n: int=2020, shout=False) -> int:
    """Play a game according to: https://adventofcode.com/2020/day/15
    Initializes by building a dict until the 2nd to last turn of inputs
    then starts the loop by 'saying' the final number from the inputs.
    """
    starting_nums = [int(x) for x in data.split(",")]

    saying = starting_nums[-1]
    turn_num = len(starting_nums)
    nums_spoken = {int(x): i+1 for i, x in enumerate(starting_nums[:-1])}
   
    for n in range(max_n - len(starting_nums)):
        saying, turn_num, nums_spoken = speak_next(saying, turn_num, nums_spoken)
    
    return saying
    

assert play_game(SAMPLE) == 436


if __name__ == "__main__":
    print(play_game(ELVES_HAVE_SPOKEN))
    
    import time
    t = time.time()
    
    print(play_game(ELVES_HAVE_SPOKEN, 30000000))
    
    elapsed = round(time.time() - t, 3)
    print(f"\nPart 2 took: {elapsed} seconds.")