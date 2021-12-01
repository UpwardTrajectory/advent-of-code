from typing import List
from dataclasses import dataclass
from initial_states import sample, starting_decks


@dataclass
class Deck(dict):
    name: str
    cards: List[int]
        
    @staticmethod
    def build(data):
        data = data.split("\n")
        name_out = data[0].replace(":", "")
        deck_out = [int(x) for x in data[1:]]
        return Deck(name_out, deck_out)
    
    def replicate_trimmed_self(self):
        name_out = "_" + self.name
        deck_out = self.cards[1: self.top+1]
        return Deck(name_out, deck_out)
    
    @property
    def top(self):
        return self.cards[0]
    
    @property
    def starts_recursion(self):
        if self.top <= len(self.cards[1:]):
            return True
        return False
        
    def win(self, loot):
        deck = self.cards[1:]
        self.cards = deck + [self.top, loot]
        return 
    
    def loss(self):
        self.cards.pop(0)
        return 
    
    @property
    def score(self):
        score = [(i+1)*val for i, val in enumerate(self.cards[::-1])]
        return sum(score)
            
    
def combat(p1, p2):
    if p1.top > p2.top:
        winner, loser = p1, p2

    elif p2.top > p1.top:
        winner, loser = p2, p1

    else:
        raise NotImplementedError("TIE: not sure what to do. Hopefully we never get here.")
    winner.win(loser.top)
    loser.loss()
    return p1, p2
    
    
@dataclass
class RecursiveCombat(dict):
    """Part 2: Remember all previous game-states & recursively play
    until a winner is found, or the game returns to a previously seen
    game-state.
    """
    p1: Deck
    p2: Deck
    deck_histories: set 
    meta_lvl: str
        
    @staticmethod
    def build(data):
        myself, friendly_crab = data.split("\n\n")
    
        player_1 = Deck.build(myself)
        player_2 = Deck.build(friendly_crab)
        return RecursiveCombat(p1=player_1, p2=player_2, deck_histories=set(), meta_lvl="|")
    
    def replicate_trimmed_self(self, meta_lvl):
        player_1 = self.p1.replicate_trimmed_self()
        player_2 = self.p2.replicate_trimmed_self()
        meta_out = meta_lvl + "_"
        return RecursiveCombat(p1=player_1, p2=player_2, deck_histories=set(), meta_lvl=meta_out)
        
    def resolve_meta_winner(self, meta_winner, parents):
        
        if parents['p1'].name in meta_winner.name:
            winner, loser = parents['p1'], parents['p2']
        elif parents['p2'].name in meta_winner.name:
            loser, winner = parents['p1'], parents['p2']
        else:
            print("Parents:", parents['p1'].name, parents['p2'].name)
            print("Children:", meta_winner.name)
            raise ValueError(f'MetaWinner: {meta_winner.name} was not cloned from original players {[self.p1.name, self.p2.name]}') 
        winner.win(loser.top)
        loser.loss()
        return parents
        
    def play_game(self):
        
        p1 = self.p1
        p2 = self.p2
        meta_lvl = self.meta_lvl
        
        just_exited_recursion = False
        i = 0
        while p1.cards and p2.cards:
#             print(meta_lvl + str(i+1))
#             print(f"{meta_lvl}  {p1.cards}\n{meta_lvl}  {p2.cards}")
            game_state = tuple([tuple(p1.cards), tuple(p2.cards)])
            
            if (game_state in self.deck_histories) and not just_exited_recursion:
#                 print(f"{meta_lvl}Infinite Loop Avoided on round {i} -- Forced Exit with Victory to {self.p1.name}.")
                if meta_lvl == "|":
                    print(f"Outermost Game found revisited state on round {i}. {p1.name} wins.")
                return p1
            else:
                self.deck_histories.add(game_state)
            
            if p1.starts_recursion and p2.starts_recursion:
                cached_meta_lvl = meta_lvl
                meta_lvl += "_"             
                parents = {"p1": p1, "p2": p2}
                nested_game = self.replicate_trimmed_self(meta_lvl=meta_lvl)
                meta_winner = nested_game.play_game()
#                 print(f"Starting recursive game on round {i}")
#                 print(f"{i}: Parents: {p1.name}, {p2.name}  --  Children:  {meta_p1.name}, {meta_p2.name}")
                parents = self.resolve_meta_winner(meta_winner, parents)
                p1 = parents['p1']
                p2 = parents['p2']
                meta_lvl = cached_meta_lvl
                just_exited_recursion = True
                
            else:
                p1, p2 = combat(p1, p2)
                just_exited_recursion = False
            if i > 590 and (meta_lvl == "|"):
                print(f"{p1.cards}, {p2.cards}")
            i += 1

        winner = sorted([p1, p2], key=lambda x: len(x.cards))[-1]  
        if meta_lvl == "|":
            print(f"{winner.name} WON! Finished after {i} rounds.")
        return winner
    
                           
def play_game(data):
    """Part 1: Read raw data, split into two players, and play Combat. 
    Print the winner & number of rounds it took.
    Return the winning score.
    """
    myself, friendly_crab = data.split("\n\n")
    
    player_1 = Deck.build(myself)
    player_2 = Deck.build(friendly_crab)
    
    i = 0
    while player_1.cards and player_2.cards:
        combat(player_1, player_2)
        i += 1
        if i > 1000:
            print("Avoiding infinite loop -- Forced exit.")
            break
            
    winner = sorted([player_1, player_2], key=lambda x: len(x.cards))[-1]
    print(f"{winner.name} WON! Finished after {i} rounds.")
    return winner.score


pred = play_game(sample)
assert pred == 306

rec_game = RecursiveCombat.build(sample) 
winner = rec_game.play_game()
assert winner.score == 291


if __name__ == "__main__":
    winning_score = play_game(starting_decks)
    print(winning_score)
    
    rec_game = RecursiveCombat.build(starting_decks)
    winner = rec_game.play_game()
    print(winner.score)
