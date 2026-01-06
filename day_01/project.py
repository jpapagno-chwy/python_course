"""
🤖 Robot Name & Battery Estimator

This project teaches:
- Data types (strings, integers, floats)
- Basic math operations
- Formatting output with f-strings
- Writing functions with parameters and return values

Your Task:
----------
Complete the three functions below:

1. calculate_operating_hours(battery_capacity_wh, power_draw_w)
   - Calculate how long the robot can run

2. create_robot_name(base_name, model_number)
   - Combine the name parts into a full robot name

3. get_robot_summary(base_name, model_number, battery_capacity_wh, power_draw_w)
   - Use the above functions to build a complete robot spec summary

Formula:
--------
Operating hours = Battery capacity (Wh) / Power draw (W)

Example:
--------
If battery = 100 Wh and power draw = 25 W
Operating hours = 100 / 25 = 4.0 hours
"""


from ast import Pow


def calculate_operating_hours(battery_capacity_wh, power_draw_w):
    """
    Calculate how many hours a robot can operate.
    
    Args:
        battery_capacity_wh: Battery capacity in watt-hours (Wh)
        power_draw_w: Power consumption in watts (W)
    
    Returns:
        Operating hours as a float
    
    Example:
        calculate_operating_hours(100, 25) should return 4.0
    """
    # TODO: Implement the formula here
    operating_hours = float(battery_capacity_wh / power_draw_w)
    return  operating_hours
    
def create_robot_name(base_name, model_number):
    """
    Combine base name and model number into a full robot name.
    
    Args:
        base_name: The robot's base name (e.g., "Scout")
        model_number: The model number (e.g., "3000")
    
    Returns:
        Full robot name as a string (e.g., "Scout-3000")
    
    Example:
        create_robot_name("Scout", "3000") should return "Scout-3000"
    """
    # TODO: Combine base_name and model_number into a full name
    full_name =(f"{base_name}-{model_number}")
    return full_name


def get_robot_summary(base_name, model_number, battery_capacity_wh, power_draw_w):
    """
    Generate a complete summary of a robot's specs.
    
    This function should use create_robot_name() and calculate_operating_hours()
    to build a formatted summary string.
    
    Args:
        base_name: The robot's base name (e.g., "Scout")
        model_number: The model number (e.g., "3000")
        battery_capacity_wh: Battery capacity in watt-hours (Wh)
        power_draw_w: Power consumption in watts (W)
    
    Returns:
        A formatted string containing the robot's name, battery capacity,
        power draw, and calculated operating hours.
    
    Example:
        get_robot_summary("Scout", "3000", 100, 25) should return a string
        containing "Scout-3000", "100", "25", and "4.0" (or "4")
        example: 
        name: Scout-3000, battery: 100, power: 25, hours: 4
    """
    # TODO: Use create_robot_name() to get the full robot name
    # TODO: Use calculate_operating_hours() to get operating time
    robot_name = create_robot_name(base_name, model_number)
    operating_hours = calculate_operating_hours(battery_capacity_wh, power_draw_w)

    return (f"name: {robot_name}, battery: {battery_capacity_wh}, power: {power_draw_w}, hours: {operating_hours}")
    # TODO: Return a formatted summary string using f-strings
    
