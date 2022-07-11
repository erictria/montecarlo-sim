import pandas as pd

class Die:
    '''
    Python class to replicate a die. A die has N faces, each with a defined weight. 
    Each face defaults to a weight of 1.0

    ATTRIBUTES:
    default_weight - float value for the default weight for each face
    __sides - private pandas dataframe containing the faces and weights of the die. Columns: ['face', 'weight']
    '''
    default_weight = 1.0

    def __init__(self, faces):
        self.__sides = pd.DataFrame({
            'face': faces,
            'weight': [self.default_weight] * len(faces)
        })
    
    def change_weight(self, face, weight):
        '''
        PURPOSE: changes the weight of a face of the die object

        INPUTS
        face - str or numeric; must match the current faces in the die
        weight - int or float
        '''
        if face in self.__sides['face'].values:
            if isinstance(weight, int) or isinstance(weight, float):
                float_weight = float(weight)
                self.__sides['weight'] = self.__sides[['face', 'weight']].apply(lambda x: float_weight if x['face'] == face else x['weight'], axis = 1)
            else:
                print('Error: Invalid weight value. Weight must be numeric.')
        else:
            print('Error: Invalid face value.')
    
    def roll(self, rolls = 1):
        '''
        PURPOSE: simulates rolling a die n times and returning the outcome

        INPUTS
        rolls - int

        OUTPUTS
        outcomes - int
        '''
        roll_result = self.__sides.sample(n = rolls, replace = True, weights = self.__sides.weight)
        outcomes = roll_result['face'].values.tolist()
        return outcomes
    
    def show_sides(self):
        '''
        PURPOSE: returns all the sides of the die.

        OUTPUTS
        sides - pandas dataframe
        '''
        return self.__sides

class Game:
    '''
    Python class to replicate a game of dice.
    A Game object has a list of Die objects.

    ATTRIBUTES:
    dice - list of Die objects
    __play_result - private pandas dataframe
    '''

    def __init__(self, dice):
        self.dice = dice
    
    def play(self, rolls = 1):
        '''
        PURPOSE: Rolls each Die object n number of times
        Latest results are saved in a private pandas dataframe __play_result

        INPUTS:
        rolls - int
        '''
        dice = self.dice
        roll_results = []
        for die_index, die in enumerate(dice):
            die_result = die.roll(rolls = rolls)
            for roll_index, roll_outcome in enumerate(die_result):
                roll_result = {
                    'roll_number': roll_index + 1,
                    'die_number': die_index,
                    'face_value': roll_outcome
                }
                roll_results.append(roll_result)
        self.__play_result = pd.DataFrame(roll_results).sort_values(['roll_number', 'die_number']).set_index('roll_number')
    
    def show_play_results(self, form = 'wide'):
        '''
        PURPOSE: Returns the private __play_result dataframe in eiher a wide or narrow format.
        Narrow - two-column index of 'roll_number' and 'die_number'; column for 'face_value'
        Wide - single column index of 'roll_number'; separate column for each die 'die_{n}'

        INPUTS:
        form - str; accepted values are 'wide' and 'narrow'; defaults to 'wide'

        OUTPUTS:
        __play_result - pandas dataframe
        '''
        if form == 'wide':
            # double check wide
            return self.__play_result
        elif form == 'narrow':
            return self.__play_result.reset_index().set_index(['roll_number', 'die_number'])
        else:
            print('Error: Invalid form.')

class Analyzer:
    '''
    Python class that analyzes the results of a Game object.
    Jackpot - number of times a game resulted in all faces being identical
    Combo - distinct combination of faces rolled
    Face Counts per Roll - Number of times a given face is rolled in each event

    ATTRIBUTES:
    game - Game object
    faces - list of str or numeric
    jackpots - pandas dataframe
    combos = pandas dataframe
    face_counts = pandas dataframe
    '''

    def __init__(self, game):
        self.game = game
        self.faces = game.dice[0].sides.face.values.tolist()
    
    def jackpot(self):
        '''
        PURPOSE: computes the number of times a game results with all faces being identical
        Tabular data is saved in the attribute 'jackpots'

        OUTPUTS:
        total_jackpots - int
        '''
        play_results = self.game.show_play_results()
        roll_unique_faces = play_results.groupby('roll_number')['face_value'].nunique()
        jackpot_results = []
        for i, r in roll_unique_faces.items():
            jackpot_results.append({
                'roll_number': i,
                'jackpot': 1 if r == 1 else 0
            })
        self.jackpots = pd.DataFrame(jackpot_results).set_index('roll_number')
        total_jackpots = self.jackpots.jackpot.sum().item()
        return total_jackpots
    
    def combo(self):
        '''
        PURPOSE: computes the distinct number of combinations rolled
        Tabular data is saved in the attribute 'combos'
        '''
        play_results = self.game.show_play_results()
        grouped = play_results.groupby('roll_number')['face_value'].agg(lambda x: sorted(list(x)))

        num_dice = len(self.game.dice)
        index_names = []
        for i in range(0, num_dice):
            index_names.append('face_{}'.format(i + 1))
        
        combos_df = pd.DataFrame(grouped.values.tolist(), columns = index_names)
        combos_df['count'] = 1
        self.combos = combos_df.groupby(index_names).sum()
    
    def face_counts_per_roll(self):
        '''
        PURPOSE: computes the number of times a given face is rolled in each event
        Tabular data is saved in the attribute 'face_counts'
        '''
        faces = self.game.faces
        play_results = self.game.show_play_results()

        all_faces = []
        for i in play_results.index.unique().tolist():
            for face in faces:
                all_faces.append({
                    'roll_number': i,
                    'face_value': face
                })
        all_faces_df = pd.DataFrame(all_faces).set_index('roll_number')

        face_counts_df = play_results.groupby(['roll_number', 'face_value'])\
            .count().reset_index()\
                .rename(columns = {'die_number': 'count'}).set_index('roll_number')
        
        self.face_counts = pd.merge(all_faces_df, face_counts_df, on = ['roll_number', 'face_value'], how = 'left')\
            .fillna(0).astype({'count': 'int32'})

if __name__ == '__main__':
    sample_die = Die(faces = ['a', 'b', 'c'])
    sample_die.change_weight(face = 'c', weight = 2.5)
    sample_die_2 = Die(faces = ['a', 'b', 'c'])

    game = Game([sample_die, sample_die_2])
    game.play(rolls = 2)

    print('---- play results narrow ----')
    print(game.show_play_results('narrow'))
    print('---- play results wide ----')
    print(game.show_play_results('wide'))
    analyzer = Analyzer(game)
    print('---- combo ----')
    analyzer.combo()
    print('---- face count ----')
    analyzer.face_counts_per_roll()
    print('---- jackpot ----')
    analyzer.jackpot()