# Monte Carlo Simulator

### Metadata
- Project: Monte Carlo Simulator
- Version: 0.1.0
- Version Date: July 15, 2022
- Author: Eric Tria
- Email: ericmtria@gmail.com

### Synposis
This package implements a simple Monte Carlo simulator represented by a game of dice.
A set of classes are used to replicate a game of dice and analyze its outcomes.

#### Installing the Package
1. Fork the repository from [Git](https://github.com/erictria/montecarlo-sim)
2. Clone your forked repository
3. Go into the root directory and run *pip install -e .*

```bash
git clone https://github.com/erictria/montecarlo-sim.git
cd montecarlo-sim
pip install -e .
```

#### Importing the Package
- After installation, import the classes from *montecarlo*

```python
from montecarlo import (
    Die,
    Game,
    Analyzer
)
```

#### Creating Dice
1. Creating a Die object requires a list of either string or numeric types to represent the *faces*.
2. All faces have a default weight of 1.0. The weight can be changed per face.

```python
sample_die = Die(faces = ['a', 'b', 'c', 'd'])
sample_die.change_weight(face = 'c', weight = 2.5)
print(sample_die.show_sides())
```
```
  face  weight
0    a     1.0
1    b     1.0
2    c     2.5
3    d     1.0
```

#### Playing Games
1. A Game requires a list of Die objects with the **same** set of faces.
2. Specify the total number of rolls to play the Game.

```python
sample_die_2 = Die(faces = ['a', 'b', 'c', 'd'])

game = Game(dice = [sample_die, sample_die_2])
game.play(rolls = 2)
print(game.show_play_results())
```
```
die_number   0  1
roll_number      
0            c  d
1            c  b
```
#### Analyze a Game
1. Pass a Game object to an Analyzer to perform analyses.
2. The resulting dataframes can be accessed using the Analyzer class attributes.

```python
analyzer = Analyzer(game)

analyzer.face_counts_per_roll()
print(analyzer.face_counts)
```
```
face_value   a  b  c  d
roll_number            
0            0  0  1  1
1            0  1  1  0
```

### API Description

#### Die Class
- Replicates a die. A die has N faces, each with a defined weight. 
- Each face defaults to a weight of 1.0
- Attributes:
    1. **default_weight** - float value for the default weight for each face
- Constructor Parameters:
    1. **faces** - a list of string or numeric variables 
- Methods:
    1. **change_weight** - changes the weight of a face of the Die object
        - Parameters:
            1. *face* - string or numeric value that must match one of the current faces in the die
            2. *weight* - numeric value that will serve as the new weight
    2. **roll** - simulates rolling a die n times and returning the outcome
        - Parameters:
            1. *rolls* - integer value signifying the number of times a die will be rolled
        - Output:
            1. *outcomes* - list of string or numeric values representing the outcomes of rolling the die. Example:
                ```
                ['c', 'b']
                ```
    3. **show_sides** - returns all the sides of the die
        - Output:
            1. *sides* - pandas dataframe representing the faces and weights of the die. Example
                ```
                face  weight
                    0    a     1.0
                    1    b     1.0
                    2    c     2.5
                    3    d     1.0
                ```

#### Game Class
- Replicates a game of dice.
- Each game class has a list of dice with the **same** set of faces.
- Attributes:
    1. **dice** - a list of Die objects
    2. **faces** - a list of string or numeric values representing the faces of all the dice
- Methods:
    1. **play** - rolls each Die object n number of times
        - Parameters:
            1. *rolls* - integer value signifying the number of times each die will be rolled
    2. **show_play_results** - returns a pandas dataframe representing the latest results of a game
        - Parameters:
            1. *form* - string value signifying the format of the resulting dataframe. Valid values are 'wide' and 'narrow'
        - Output:
            1. *play_result* - pandas dataframe representing the latest results of a game. Example:
                ```
                # wide
                die_number   0  1
                roll_number      
                0            c  d
                1            b  b

                # narrow
                                    face_value
                roll_number die_number           
                0           0                   c
                            1                   d
                1           0                   b
                            1                   b
                ```

#### Analyzer Class
- Analyzes the results of a Game object.
- Attributes:
    1. **game** - a Game object
    2. **jackpots** - a pandas dataframe containing the number of times a roll resulted in all faces being identical. Example:
        ```
                     jackpot
        roll_number         
        0                  0
        1                  0
        ```
    3. **combos** - a pandas dataframe containing the frequency of distinct combinations rolled.
        - Note: this function generates **combinations**, meaning order does not matter. Different from permutations. [Reference](https://www.mathsisfun.com/combinatorics/combinations-permutations.html)
        - Example:

        ```
                       count
        face_1 face_2       
        a      d           1
        b      c           1
        ```
    4. **face_counts_per_roll** - a pandas dataframe containing the number of times a given face is rolled in each event. Example:
        ```
        face_value   a  b  c  d
        roll_number            
        0            1  0  0  1
        1            0  1  1  0
        ```
- Methods:
    1. **jackpot** - computes the jackpots of a game and stores it in a pandas dataframe
        - Output:
            1. *total_jackpots* - integer value representing the number of jackpots in a game
    2. **combo** - computes the combos of a game and stores it in a pandas dataframe
    3. **face_counts_per_roll** - computes the face counts per roll of a game and stores it in a pandas dataframe

### Manifest
```
montecarlo-sim/
    montecarlo/
        __init__.py
        montecarlo.py
        tests/
            montecarlo_test.py
            montecarlo_test_results.txt
    montecarlo_demo.ipynb
    final-project-submission.ipynb
    setup.py
    LICENSE
    README.md
    .gitignore
```
