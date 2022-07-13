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
        outcomes - list of str or numeric
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
    faces - list of str or numeric
    __play_result - private pandas dataframe
    '''

    def __init__(self, dice):
        self.dice = dice
        self.faces = dice[0].show_sides().face.values.tolist()
    
    def play(self, rolls = 1):
        '''
        PURPOSE: Rolls each Die object n number of times
        Latest results are saved in a private pandas dataframe __play_result
        __play_result - index: ['roll_number']; columns: different die numbers; shape: M (rolls) rows x N (dice) columns

        INPUTS:
        rolls - int
        '''
        dice = self.dice
        roll_results = []
        for die_index, die in enumerate(dice):
            die_result = die.roll(rolls = rolls)
            for roll_index, roll_outcome in enumerate(die_result):
                roll_result = {
                    'roll_number': roll_index,
                    'die_number': die_index,
                    'face_value': roll_outcome
                }
                roll_results.append(roll_result)
        self.__play_result = pd.DataFrame(roll_results).pivot(index = 'roll_number', columns = 'die_number', values = 'face_value')
    
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
            return self.__play_result
        elif form == 'narrow':
            return self.__play_result.stack().to_frame('face_value')
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
    jackpots - pandas dataframe
    combos = pandas dataframe
    face_counts = pandas dataframe
    '''

    def __init__(self, game):
        self.game = game
    
    def jackpot(self):
        '''
        PURPOSE: computes the number of times a game results with all faces being identical
        Tabular data is saved in the attribute 'jackpots'

        PROCESS:
        1. Group the play results of the game by roll number to get the unique count of resulting faces
        2. If the unique count is 1, tag 'jackpot' as 1. Otherwise, tag it as 0.
        3. The dataframe would have 'roll_number' as an index and 'jackpot' as a column.
        4. Get the sum of the 'jackpot' column to get the number of total jackpots.

        OUTPUTS:
        total_jackpots - int
        '''
        play_results = self.game.show_play_results(form = 'narrow')
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

        PROCESS:
        1. Group the play results of the game by roll number and combine all resulting faces into a sorted list 
            ['face_value_1', 'face_value_2', ...]
        2. Create a list of new column names based on the number of dice in the game.
        3. Create a dataframe using the lists from step 1 and the column names from step 2.
        4. Aggregate the new dataframe to get the total 'count' per combination
        '''
        play_results = self.game.show_play_results(form = 'narrow')
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

        PROCESS:
        1. Create a dataframe of all the possible face results per roll.
        2. Create a dataframe of the total count of each face result per roll.
        3. Merge the dataframes from step 1 and step 2 and fill the NaN values with 0s.
        '''
        faces = self.game.faces
        play_results = self.game.show_play_results(form = 'narrow').reset_index(level = 'die_number')

        all_faces = []
        for i in play_results.index.unique().tolist():
            for face in faces:
                all_faces.append({
                    'roll_number': i,
                    'face_value': face
                })
        all_faces_df = pd.DataFrame(all_faces).set_index('roll_number')

        face_counts_df = play_results.groupby(['roll_number', 'face_value'])\
            .count().reset_index(level = 'face_value')\
                .rename(columns = {'die_number': 'count'})
        
        self.face_counts = pd.merge(all_faces_df, face_counts_df, on = ['roll_number', 'face_value'], how = 'left')\
            .fillna(0).astype({'count': 'int32'})\
                .pivot(columns = 'face_value', values = 'count')

if __name__ == '__main__':
    sample_die = Die(faces = ['a', 'b', 'c', 'd'])
    sample_die.change_weight(face = 'c', weight = 2.5)
    sample_die_2 = Die(faces = ['a', 'b', 'c', 'd'])

    game = Game([sample_die, sample_die_2])
    game.play(rolls = 2)

    analyzer = Analyzer(game)

    print('---- Die.roll() ----')
    print(sample_die.roll(rolls = 2))

    print('\n---- Die.show_sides() ----')
    print(sample_die.show_sides())

    print('\n---- Game.show_play_results("narrow") ----')
    print(game.show_play_results('narrow'))

    print('\n---- Game.show_play_results("wide") ----')
    print(game.show_play_results('wide'))

    print('\n---- Analyzer.jackpot() ----')
    print(analyzer.jackpot())

    print('\n---- Analyzer.combo() ----')
    analyzer.combo()
    print(analyzer.combos)

    print('\n---- Analyzer.face_counts_per_roll() ----')
    analyzer.face_counts_per_roll()
    print(analyzer.face_counts)