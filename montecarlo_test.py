from montecarlo import (
    Die,
    Game,
    Analyzer
)
import unittest

class DieTestSuite(unittest.TestCase):
    '''
    Test functions for testing the Die class.
    '''

    def test_1_change_weight(self):
        '''
        PURPOSE: tests the Die.change_weight() method

        OUTCOME:
        The row in the dataframe with the specified face should have the new weight value
        '''

        die = Die(faces = ['a', 'b', 'c'])
        new_weight = 3.0
        face_to_change = 'a'
        die.change_weight(face = face_to_change, weight = new_weight)

        sides = die.show_sides()
        changed_row = sides[(sides.face == face_to_change) & (sides.weight == new_weight)]

        self.assertTrue(len(changed_row) == 1, 'face weight not changed properly')
    
    def test_2_change_weight_invalid_inputs(self):
        '''
        PURPOSE: tests the invalid inputs for Die.change_weight() 

        OUTCOME:
        Weights of the Die should not change after passing invalid face and weight inputs
        '''

        faces = ['a', 'b', 'c']
        die = Die(faces = faces)
        invalid_new_weight = '3.0'
        new_weight = 3.0
        invalid_face_to_change = 'd'
        face_to_change = 'a'
        die.change_weight(face = invalid_face_to_change, weight = new_weight)
        die.change_weight(face = face_to_change, weight = invalid_new_weight)

        sides = die.show_sides()

        self.assertTrue(sides.weight.values.tolist() == [1.0] * len(faces), 'invalid inputs still changed weight of die face')
    
    def test_3_roll(self):
        '''
        PURPOSE: tests the Die.roll() method

        OUTCOMES:
        The unique resulting faces should be a subset of the initial list of faces AND
        The length of the resulting list should be equal to the total number of rolls
        '''

        faces = ['a', 'b', 'c']
        die = Die(faces = faces)
        rolls = 2
        roll_results = die.roll(rolls = rolls)

        is_subset = set(roll_results).issubset(set(faces))

        self.assertTrue(is_subset and (len(roll_results) == rolls), 'die did not roll properly')
    
    def test_4_show_sides(self):
        '''
        PURPOSE: tests the Die.show_sides() method

        OUTCOMES:
        The faces of the created Die object should be equal to the initial list of faces AND
        The weight of each side should be the default value of 1.0
        '''

        faces = ['a', 'b', 'c']
        default_weights = [1.0] * 3
        die = Die(faces = faces)
        sides = die.show_sides()
        side_faces = sides.face.values.tolist()
        side_weights = sides.weight.values.tolist()

        self.assertTrue(side_faces == faces and side_weights == default_weights, 'die sides not shown properly')

class GameTestSuite(unittest.TestCase):
    '''
    Test functions for testing the Game class.
    '''

    def test_1_play(self):
        '''
        PURPOSE: tests the Game.play() method

        OUTCOMES:
        The private attribute __play_result should not be accessible directly
        '''

        die = Die(faces = ['a', 'b', 'c'])
        game = Game(dice = [die] * 2)
        game.play()

        try:
            result = game.__play_result
            is_private = False
        except:
            is_private = True

        self.assertTrue(is_private, 'play_result attribute not set as private attribute')
    
    def test_2_show_play_results(self):
        '''
        PURPOSE: tests the Game.show_results() method

        OUTCOMES:
        The resulting wide dataframe should have a shape of M (rolls) rows x N (dice) columns
        '''

        die = Die(faces = ['a', 'b', 'c'])
        dice = [die] * 2
        game = Game(dice = dice)
        rolls = 5
        game.play(rolls = rolls)
        latest_results = game.show_play_results()

        self.assertTrue(latest_results.shape == (rolls, len(dice)), 'results returned an invalid play result')
    
    def test_3_show_play_results_inputs(self):
        '''
        PURPOSE: tests the valid inputs for the Game.show_results() method

        OUTCOMES:
        A 'wide' form dataframe should have 1 index AND
        A 'narrow' form dataframe should have 2 indices AND
        Any other form input should return None
        '''

        die = Die(faces = ['a', 'b', 'c'])
        game = Game(dice = [die] * 2)
        game.play()

        wide_play_results = game.show_play_results(form = 'wide')
        narrow_play_results = game.show_play_results(form = 'narrow')
        invalid_play_results = game.show_play_results(form = 'other string')

        self.assertTrue(len(wide_play_results.index.names) == 1 and len(narrow_play_results.index.names) == 2 and invalid_play_results is None, 'other')

class AnalyzerTestSuite(unittest.TestCase):
    '''
    Test functions for testing the Analyzer class.
    '''

    def test_1_jackpot(self):
        '''
        PURPOSE: tests the Analyzer.jackpot() method

        OUTPUTS:
        The jackpot method should return an int that is greater than or equal to 0
        '''

        die = Die(faces = ['a', 'b', 'c'])
        game = Game(dice = [die] * 2)
        game.play()
        analyzer = Analyzer(game = game)
        jackpot = analyzer.jackpot()

        self.assertTrue(isinstance(jackpot, int) and jackpot >= 0, 'jackpot returned an invalid value')
    
    def test_2_combo(self):
        '''
        PURPOSE: tests the Analyzer.combo() method

        OUTCOMES:
        The sum of the 'count' column should be equal to the total number of rolls AND
        The number of indices of the resulting dataframe should be equal to the number of dice
        '''

        faces = ['a', 'b', 'c']
        die = Die(faces = faces)
        dice = [die] * 5
        game = Game(dice = dice)
        rolls = 2
        game.play(rolls = rolls)
        analyzer = Analyzer(game)

        analyzer.combo()
        combos = analyzer.combos

        self.assertTrue(combos['count'].sum().item() == rolls and len(combos.index.names) == len(dice), 'combos attribute has an invalid value')
    
    def test_3_face_counts_per_roll(self):
        '''
        PURPOSE: tests the Analyzer.face_counts_per_roll() method

        OUTCOMES:
        The total sum of all face counts should be equal to the number of rolls x the number of dice AND
        The shape of the resulting dataframe should be M (rolls) rows x N (faces) columns
        '''

        faces = ['a', 'b', 'c']
        die = Die(faces = faces)
        dice = [die] * 5
        game = Game(dice = dice)
        rolls = 2
        game.play(rolls = rolls)
        analyzer = Analyzer(game)

        analyzer.face_counts_per_roll()
        face_counts = analyzer.face_counts
        self.assertTrue(face_counts.sum().sum().item() == (rolls * len(dice)) and face_counts.shape == (rolls, len(faces)), 'face_counts attribute has an invalid value')

if __name__ == '__main__':
    unittest.main(verbosity = 3)