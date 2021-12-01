import math
from homework import samples, sample_answers, sample_answers_p2, problems
    
    
def parenthetic_contents(string, func):
    """Generate parenthesized contents in string as pairs (level, contents).
    source:  https://stackoverflow.com/a/4285211/14083170
    """
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            s = string[start: i+1]
            if len(stack) == 2:
                yield (len(stack), (s, func(s)))
            else:
                yield (len(stack), s)

                
def prep_simple_str(s):
    s = s.strip()
    only_outer_parens = (s[0] == "(") & (s[-1] == ")") & (s[1:-1].count("(") == 0)
    if only_outer_parens:
        return prep_simple_str(s[1:-1])
    
    if "(" in s:
        raise ValueError("No parens allowed.")
    
    s = s.replace(")", " )").split(" ")
    fixed_s = []
    for c in s:
        try:
            fixed_s.append(int(c))
        except ValueError:
            fixed_s.append(c)
    return fixed_s
    
            
def sans_parens(s):
    """Perform left -> right math.  Input should not have spaces. 
    Exit when either a ')' is found or the end of the string is reached.
    """
    s = prep_simple_str(s)
    
    total = s[0]
    
    for c in s[1:]:
        if c == ")":
            return total
        elif c == "*":
            op = lambda a,b: a * b
        elif c == "+":
            op = lambda a,b: a + b
        else:
            total = op(total, c)
    return total


def advanced_math_sans_parens(s):
    if isinstance(s, str):
        s = prep_simple_str(s)
    
    if '+' in s:
        add_loc = s.index("+")
        prelude = s[: max(0, add_loc-1)]
        new_sum = s[add_loc-1] + s[add_loc+1]
        s = prelude + [new_sum] + s[add_loc+2:]
        return advanced_math_sans_parens(s)
    
    s = [c for c in s if c not in {"*", ")"}]
    return math.prod(s)
    

def compute_all(problems, func=sans_parens):
    """Evaluate all math problems, using the 'Order of Operations' defined in func."""
    all_answers = []
    for s in problems.split("\n"):
        s = "( " + s + " )"
        row = list(parenthetic_contents(s, func))
        inners = [d for lvl, d in row if lvl == 2]
        outers = [d for lvl, d in row if lvl == 1]
        final = [d for lvl, d in row if lvl == 0][0]
        
        # Replace inner parens with their evaluated values
        if inners:
            filled_outers = []
            for outer_s in outers:
                result = outer_s
                for d in inners:
                    inner_s, new_val = d[0], d[1]
                    result = result.replace(inner_s, str(new_val))
                filled_outers.append((outer_s, func(result)))
        else:
            filled_outers = [(outer_s, func(outer_s)) for outer_s in outers]

        # Replace outer parens with their evaluated values
        result = final
        if filled_outers:
            for d in filled_outers:
                outer_s, new_val = d[0], d[1]
                result = result.replace(outer_s, str(new_val))
        all_answers.append(func(result))

    return all_answers    


preds = compute_all(samples)
for pred, ans in zip(preds, sample_answers):
    assert pred == ans, f"Predicted {pred} != {ans} (the true value)"
    
preds = compute_all(samples, advanced_math_sans_parens)
for pred, ans in zip(preds, sample_answers_p2):
    assert pred == ans, f"Predicted {pred} != {ans} (the true value)"
    
    
if __name__ == "__main__":
    print(sum(compute_all(problems)))
    print(sum(compute_all(problems, advanced_math_sans_parens)))


                
            
       