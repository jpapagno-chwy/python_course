"""
🤖 Robot Patrol Route Generator

This project teaches:
- Lists and indexing
- The random module (random.choice, random.shuffle, random.randint)
- For loops and range()
- Building strings from lists

Your Task:
----------
Complete the five functions below:

1. get_random_waypoint(waypoints)
   - Pick a random waypoint from a list using random.choice()

2. shuffle_route(waypoints)
   - Randomize the order of waypoints using random.shuffle()

3. generate_patrol_route(waypoints, num_stops)
   - Build a patrol route by randomly selecting waypoints

4. calculate_total_steps(route)
   - Use a for loop to count total steps in a route

5. format_route_report(route)
   - Use a for loop to build a formatted route report string

Waypoints:
----------
Waypoints are represented as tuples: (name, steps_to_reach)
Example: ("Entrance", 0), ("Lab A", 15), ("Storage", 22)

The 'steps_to_reach' represents how many steps from the starting point.
"""

import random


# Available waypoints for patrol routes
WAYPOINTS = [
    ("Entrance", 0),
    ("Lab A", 15),
    ("Lab B", 28),
    ("Storage Room", 42),
    ("Server Room", 55),
    ("Break Room", 33),
    ("Loading Dock", 67),
    ("Security Office", 20),
]


def get_random_waypoint(waypoints):
    """
    Select a random waypoint from the list.
    
    Args:
        waypoints: A list of waypoint tuples [(name, steps), ...]
    
    Returns:
        A single randomly chosen waypoint tuple
    
    Example:
        waypoints = [("Lab A", 15), ("Lab B", 28), ("Storage", 42)]
        get_random_waypoint(waypoints) might return ("Lab B", 28)
    
    Hint: Use random.choice()
    """
    # TODO: Use random.choice() to return a random waypoint
    return random.choice(waypoints)
    pass


def shuffle_route(waypoints):
    """
    Create a shuffled copy of the waypoints list.
    
    Args:
        waypoints: A list of waypoint tuples to shuffle
    
    Returns:
        A NEW list with the same waypoints in random order
        (Do not modify the original list!)
    
    Example:
        waypoints = [("A", 1), ("B", 2), ("C", 3)]
        shuffle_route(waypoints) might return [("C", 3), ("A", 1), ("B", 2)]
    
    Hint: Make a copy first, then use random.shuffle() on the copy
    """
    # TODO: Create a copy of the list, shuffle it, and return it
    waypoints_copy = waypoints.copy()
    random.shuffle(waypoints_copy)
    return waypoints_copy


def generate_patrol_route(waypoints, num_stops):
    """
    Generate a patrol route with a specified number of stops.
    
    Args:
        waypoints: A list of available waypoint tuples
        num_stops: How many stops to include in the route (integer)
    
    Returns:
        A list of randomly chosen waypoints (can have repeats)
    
    Example:
        waypoints = [("Lab A", 15), ("Lab B", 28)]
        generate_patrol_route(waypoints, 3) might return:
        [("Lab A", 15), ("Lab A", 15), ("Lab B", 28)]
    
    Hint: Use a for loop with range() and random.choice()
    """
    # TODO: Use a for loop to build a list of num_stops random waypoints
    route = []
    for i in range(num_stops):
        route.append(get_random_waypoint(waypoints))
    return route


def calculate_total_steps(route):
    """
    Calculate the total steps for a patrol route.
    
    Args:
        route: A list of waypoint tuples [(name, steps), ...]
    
    Returns:
        The sum of all steps values in the route (integer)
    
    Example:
        route = [("Lab A", 15), ("Lab B", 28), ("Storage", 42)]
        calculate_total_steps(route) should return 85 (15 + 28 + 42)
    
    Hint: Use a for loop to add up the steps from each waypoint
    """
    # TODO: Use a for loop to sum all the steps values
    total_steps = 0
    for waypoint in route:
        total_steps += waypoint[1]
    return total_steps


def format_route_report(route):
    """
    Create a formatted report of the patrol route.
    
    Args:
        route: A list of waypoint tuples [(name, steps), ...]
    
    Returns:
        A string listing each stop with its number, like:
        "Stop 1: Lab A (15 steps)\nStop 2: Lab B (28 steps)\n..."
    
    Example:
        route = [("Lab A", 15), ("Lab B", 28)]
        format_route_report(route) should return:
        "Stop 1: Lab A (15 steps)\nStop 2: Lab B (28 steps)"
    
    Hint: Use a for loop with enumerate() or range(len(route))
    """
    # TODO: Use a for loop to build a formatted string
    # Each line should be "Stop X: Name (Y steps)"
    report = ""
    for i, waypoint in enumerate(route):
        report += f"Stop {i+1}: {waypoint[0]} ({waypoint[1]} steps)\n"
    return report

