# Spaceship TSP KP

This program is a approach for the combination between Travelling Salesman Problem and Knapsack Problem.
The representation consists in a Spaceship that visits Planets and collects resources from them.
The visited Planets are randomly chosen from a planets.json file that contains hundreds of them.

## Imports

The modules used in the code are:

1. json: for parsing the planets.json file
2. random: for choosing the random planets
3. typing (NamedTuple, List, Tuple): for the program classes
4. math: for distance measurement

## Classes

There are 4 classes in the program:
- Coordinate
- Resource
- Planet
- Spaceship

The Coordinate, Resource and Planet classes inherit from the NamedTuple class, the idea is having them working like C Structs

### Coordinate

The Coordinate class contain 3 attributes: x, y, z.
It's purpose is to put all the coordinates of an object in a single variable

### Resource

The Resource class contains info about a resource found in a Planet:
- name: string
- weight: float
- value: float

### Planet

The Planet class contains info about the Planet's name, location and resources:
- name: string
- coord: Coordinate
- resources: List[Resource]

### Spaceship

The Spaceship class is the core of the program. Inside it, the optimal path will be calculated by trying to maximize the value carried by the Spaceship.
This class contains the following attributes:
- max_weight: float
- current_weight: float
- current_value: float
- resources: List[Resource]
- base: Coordinate

And it contains the following methods:
- __init__
- __str__
- load_resources -> bool
- _calculate_distance -> float
- _simulate_path_value -> float
- analyze_path -> Tuple[Planet, ...]

The __init__ methods is the class initializer and __str__ formats the Spaceship as a string.

#### load_resources

The load_resources method takes a list of Planets as parameter and returns a boolean.
It is a Fractional Knapsack Problem solution that uses a greedy algorithm approach.
It returns False if no resources could be loaded and True if all resources were loaded (or partially loaded).

#### _calculate_distance

This method takes two coordinates as arguments and returns the Euclidean Distance between them.

#### _simulate_path_value

The _simulate_path_value takes a list of Planets as parameter and returns a float.
This method calculates the value that will be collected in a path without actually loading the Spaceship. It creates a temporary spaceship to simulate the value and is used inside the analyze_path method.

#### analyze_path

The analyze_path method takes a list of Planets as parameter and returns a tuple of Planets.
It is a Travelling Salesman Problem that uses a greedy algorithm approach.
It uses the _calculate_distance, _simulate_path_value and load_resources methods to maximize the value carried by the Spaceship when it visits the Planets on the list.
The tuple of Planets returned is in visit order.

## Functions

The only function in the program is the json parser for the Planet class. It takes a filename as parameter and returns a list of Planets.

## Main code

The main code of the program does the following tasks, in order:
1. Load the json file that contains the Planets
2. Generate a random number N from 5 to 50
3. Select N random planets from the json file
4. Creates a Spaceship with 150 as the default max weight
5. Uses the Spaceship's methods to choose the best path
6. Outputs the visited planets and the Spaceship's final status
