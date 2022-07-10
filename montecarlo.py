import pandas as pd

class Die:
    default_weight = 1.0

    def __init__(self, faces):
        # check if need to validate faces
        self.sides = pd.DataFrame({
            'face': faces,
            'weight': [self.default_weight] * len(faces)
        })
    
    def change_weight(self, face, weight):
        if face in self.sides['face'].values:
            if isinstance(weight, int) or isinstance(weight, float):
                float_weight = float(weight)
                self.sides['weight'] = self.sides[['face', 'weight']].apply(lambda x: float_weight if x['face'] == face else x['weight'], axis = 1)
            else:
                print('Error: Invalid weight value. Weight must be numeric.')
        else:
            print('Error: Invalid face value.')
    
    def roll(self, rolls = 1):
        roll_result = self.sides.sample(n = rolls, replace = True, weights = self.sides.weight)
        outcomes = roll_result['face'].values.tolist()
        return outcomes
    
    def show_sides(self):
        return self.sides

class Game:
    def __init__(self, dice):
        # check if need to validate dice
        self.dice = dice
    
    def play(self, rolls = 1):
        dice = self.dice
        roll_results = []
        for idx, die in enumerate(dice):
            die_result = die.roll(rolls = rolls)
            for i, r in enumerate(die_result):
                roll_result = {
                    'roll_number': i + 1,
                    'die_number': idx,
                    'result_face': r
                }
                roll_results.append(roll_result)
        self.__play_result = pd.DataFrame(roll_results).set_index('roll_number')
    
    def show_play_results(self, form = 'wide'):
        if form == 'wide':
            return self.__play_result
        elif form == 'narrow':
            return self.__play_result.reset_index().set_index(['roll_number', 'die_number'])
        else:
            print('Error: Invalid form.')

class Analyzer:
    def __init__(self, game):
        self.game = game
    
    def jackpot(self):
        play_results = self.game.show_play_results()
        roll_unique_faces = play_results.groupby('roll_number')['result_face'].nunique()
        jackpot_results = []
        for i, r in roll_unique_faces.items():
            jackpot_results.append({
                'roll_number': i,
                'jackpot': 1 if r == 1 else 0
            })
        self.jackpots = pd.DataFrame(jackpot_results)
        return self.jackpots.jackpot.sum()
    
    # def combo(self):




if __name__ == '__main__':
    sample_die = Die(faces = ['a', 'b', 'c'])
    # print(sample_die.roll(5))
    # print(sample_die.show_sides())
    # sample_die.change_weight(face = 5, weight = 3)
    # sample_die.change_weight(face = 'c', weight = 'z')
    sample_die.change_weight(face = 'c', weight = 3.5)
    # print(sample_die.show_sides())

    sample_die_2 = Die(faces = ['a', 'b', 'c'])
    game = Game([sample_die, sample_die_2])
    game.play(rolls = 2)
    # print(game.show_play_results('narrow'))
    # print(game.show_play_results('widez'))
    analyzer = Analyzer(game)
    print(analyzer.jackpot())