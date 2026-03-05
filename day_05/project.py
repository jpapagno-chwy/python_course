"""
🤖 Robot Inventory & Config Manager

This project teaches:
- Dictionaries and key-value pairs
- Nested dictionaries
- Functions that return values
- Working with lists of dictionaries
- Dictionary operations (get, update, keys, values)

Your Task:
----------
Complete the six functions below:

1. create_robot_config(name, motor_count, sensor_count, battery_wh)
   - Create and return a robot configuration dictionary

2. get_total_power_draw(robot)
   - Calculate total power draw from a robot's config

3. add_sensor(robot, sensor_name, sensor_range)
   - Add a new sensor to a robot's sensors dictionary

4. find_robot_by_name(fleet, name)
   - Search a list of robots and return the matching one

5. get_fleet_summary(fleet)
   - Calculate summary statistics for a fleet of robots

6. get_most_capable_robot(fleet)
   - Find the robot with the highest sensor count

Robot Config Structure:
-----------------------
{
    "name": "Scout-3000",
    "motors": {
        "count": 4,
        "power_per_motor": 25  # watts
    },
    "sensors": {
        "lidar": 10.0,    # range in meters
        "camera": 5.0,
        "ultrasonic": 3.0
    },
    "battery_wh": 100
}
"""


def create_robot_config(name, motor_count, sensor_count, battery_wh):
    """
    Create a robot configuration dictionary.
    
    Args:
        name: Robot name (string)
        motor_count: Number of motors (integer)
        sensor_count: Number of sensors (integer)
        battery_wh: Battery capacity in watt-hours (integer)
    
    Returns:
        A dictionary with the robot's configuration:
        {
            "name": name,
            "motors": {"count": motor_count, "power_per_motor": 25},
            "sensors": {},  # empty dict, sensors added later
            "battery_wh": battery_wh,
            "sensor_count": sensor_count
        }
    
    Example:
        create_robot_config("Scout", 4, 3, 100) returns:
        {"name": "Scout", "motors": {"count": 4, "power_per_motor": 25}, 
         "sensors": {}, "battery_wh": 100, "sensor_count": 3}
    """
    # TODO: Create and return the robot config dictionary
    return  {
            "name": name,
            "motors": {"count": motor_count, "power_per_motor": 25},
            "sensors": {},  # empty dict, sensors added later
            "battery_wh": battery_wh,
            "sensor_count": sensor_count
        }
    pass


def get_total_power_draw(robot):
    """
    Calculate the total power draw of a robot.
    
    Power draw = motor count × power per motor
    
    Args:
        robot: A robot configuration dictionary
    
    Returns:
        Total power draw in watts (integer)
    
    Example:
        robot = {"motors": {"count": 4, "power_per_motor": 25}, ...}
        get_total_power_draw(robot) returns 100 (4 × 25)
    
    Hint: Access nested dict with robot["motors"]["count"]
    """
    # TODO: Calculate and return motor_count * power_per_motor
    return robot["motors"]["count"] * robot["motors"]["power_per_motor"]
    pass


def add_sensor(robot, sensor_name, sensor_range):
    """
    Add a new sensor to a robot's sensors dictionary.
    
    Args:
        robot: A robot configuration dictionary
        sensor_name: Name of the sensor (string, e.g., "lidar")
        sensor_range: Range of the sensor in meters (float)
    
    Returns:
        The updated robot dictionary
    
    Example:
        robot = {"sensors": {}, ...}
        add_sensor(robot, "lidar", 10.0)
        # robot["sensors"] is now {"lidar": 10.0}
    
    Hint: robot["sensors"][sensor_name] = sensor_range
    """
    # TODO: Add the sensor to robot["sensors"] and return robot
    robot["sensors"][sensor_name] = sensor_range
    return robot
    pass


def find_robot_by_name(fleet, name):
    """
    Find a robot in a fleet by its name.
    
    Args:
        fleet: A list of robot configuration dictionaries
        name: The name to search for (string)
    
    Returns:
        The robot dictionary if found, None if not found
    
    Example:
        fleet = [{"name": "Scout"}, {"name": "Guard"}]
        find_robot_by_name(fleet, "Scout") returns {"name": "Scout"}
        find_robot_by_name(fleet, "Unknown") returns None
    
    Hint: Loop through fleet and check each robot["name"]
    """
    # TODO: Loop through fleet and return matching robot
    for robot in fleet:
        if robot["name"] == name:
            return robot
    return None
    pass


def get_fleet_summary(fleet):
    """
    Calculate summary statistics for a fleet of robots.
    
    Args:
        fleet: A list of robot configuration dictionaries
    
    Returns:
        A dictionary with fleet statistics:
        {
            "total_robots": number of robots,
            "total_battery_wh": sum of all battery capacities,
            "total_motors": sum of all motor counts
        }
    
    Example:
        fleet = [
            {"battery_wh": 100, "motors": {"count": 4}},
            {"battery_wh": 150, "motors": {"count": 6}}
        ]
        get_fleet_summary(fleet) returns:
        {"total_robots": 2, "total_battery_wh": 250, "total_motors": 10}
    
    Hint: Use a loop to sum up the values
    """
    # TODO: Calculate and return the fleet summary dictionary
    out = {
        "total_robots": 0,
        "total_battery_wh": 0,
        "total_motors": 0
    }
    for robot in fleet:
        out["total_robots"] += 1
        out["total_battery_wh"] += robot["battery_wh"]
        out["total_motors"] += robot["motors"]["count"]
    return out
    
    pass


def get_most_capable_robot(fleet):
    """
    Find the robot with the highest sensor count.
    
    Args:
        fleet: A list of robot configuration dictionaries
    
    Returns:
        The name of the robot with the most sensors (string)
        Returns None if fleet is empty
    
    Example:
        fleet = [
            {"name": "Scout", "sensor_count": 3},
            {"name": "Guard", "sensor_count": 5},
            {"name": "Worker", "sensor_count": 2}
        ]
        get_most_capable_robot(fleet) returns "Guard"
    
    Hint: Track the best robot as you loop through
    """
    # TODO: Find and return the name of the robot with most sensors
    max_sensor_count = 0
    max_sensor_robot = None
    for robot in fleet:
        if robot["sensor_count"] > max_sensor_count:
            max_sensor_count = robot["sensor_count"]
            max_sensor_robot = robot
    return max_sensor_robot["name"] if max_sensor_robot else None
    pass
