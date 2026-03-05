"""
🤖 Debug the Data Pipeline — ROS to HuggingFace Dataset Converter

SCENARIO:
---------
An intern wrote this script to convert our robot's ROS sensor data into a
HuggingFace-compatible dataset for training a navigation model. The script
runs... but produces wrong and corrupt data.

This script has 10 BUGS! Your job is to find and fix every one.

The pipeline should:
1. Parse ROS timestamps (secs + nanoseconds → float seconds)
2. Normalize LIDAR scans to 0.0–1.0 range
3. Classify motor commands as "forward" / "turn" / "stop"
4. Filter messages by time range
5. Convert ROS messages → HuggingFace dataset rows
6. Build, validate, and split the dataset

After fixing all bugs, run tests.py — all tests should pass!

7 of the bugs are marked with "BUG" comments. 3 are unmarked — you'll
need to find those through the test output alone.

DEBUGGING TIPS:
- Add print() statements to see variable values
- Check each function one at a time
- Compare expected vs actual output
- Read the docstrings carefully — they describe correct behavior
- Use the debugger: breakpoint() or python -m pdb project.py
"""

import json
import math


# ============================================================
# DATA CLASSES
# ============================================================

class RosSensorMessage:
    """Represents a single ROS sensor message from the robot."""

    # BUG 3: Something wrong with the default parameter here
    def __init__(self, stamp, lidar_scan=[], linear_vel=0.0, angular_vel=0.0, frame_id=""):
        self.stamp = stamp                # {"secs": int, "nsecs": int}
        self.lidar_scan = lidar_scan      # List of float distances
        self.linear_vel = linear_vel      # Forward/backward speed
        self.angular_vel = angular_vel    # Turning speed
        self.frame_id = frame_id          # Camera frame identifier

    def __repr__(self):
        return f"RosSensorMessage(t={self.stamp}, lin={self.linear_vel}, ang={self.angular_vel})"


# ============================================================
# PARSING & CONVERSION FUNCTIONS
# ============================================================

def parse_ros_timestamp(stamp):
    """
    Convert a ROS timestamp to a float in seconds.

    ROS timestamps have two fields:
        - secs:  whole seconds since epoch
        - nsecs: additional nanoseconds (0 to 999,999,999)

    Args:
        stamp: dict with "secs" (int) and "nsecs" (int)

    Returns:
        Float timestamp in seconds

    Example:
        parse_ros_timestamp({"secs": 1000, "nsecs": 500000000})
        → 1000.5
    """
    # BUG 1: Is this the right divisor for nanoseconds?
    return stamp["secs"] + stamp["nsecs"] / 1_000_000


def normalize_lidar_scan(scan, max_range=12.0):
    """
    Normalize raw LIDAR readings to the 0.0–1.0 range.

    Each reading is divided by max_range, then clamped to a maximum of 1.0
    (readings beyond max_range are capped at 1.0).

    Args:
        scan: List of raw distance readings (floats, in meters)
        max_range: Maximum sensor range in meters (default 12.0)

    Returns:
        List of normalized readings, each between 0.0 and 1.0

    Example:
        normalize_lidar_scan([3.0, 6.0, 15.0], max_range=12.0)
        → [0.25, 0.5, 1.0]
    """
    normalized = []
    for reading in scan:
        value = reading / max_range
        # BUG 2: What should the clamp upper bound be?
        normalized.append(min(value, max_range))
    return normalized


def classify_action(linear_vel, angular_vel):
    """
    Classify the robot's action based on velocity commands.

    Classification rules (check in this order):
        1. "stop"    — both |linear| and |angular| < 0.05
        2. "turn"    — |angular| >= 0.05 (turning takes priority)
        3. "forward" — |linear| >= 0.05

    Args:
        linear_vel:  Forward/backward velocity (float)
        angular_vel: Rotational velocity (float)

    Returns:
        One of: "forward", "turn", "stop"

    Examples:
        classify_action(0.5, 0.3) → "turn"    (angular is significant)
        classify_action(0.5, 0.0) → "forward"
        classify_action(0.0, 0.0) → "stop"
    """
    if abs(linear_vel) < 0.05 and abs(angular_vel) < 0.05:
        return "stop"
    # BUG 4: Is this checking the right velocity first?
    elif abs(linear_vel) >= 0.05:
        return "forward"
    elif abs(angular_vel) >= 0.05:
        return "turn"
    else:
        return "stop"


# ============================================================
# FILTERING
# ============================================================

def filter_by_time_range(messages, start_time, end_time):
    """
    Filter messages to only include those within a time range.

    Args:
        messages: List of RosSensorMessage objects
        start_time: Start of range (float seconds)
        end_time: End of range (float seconds)

    Returns:
        A new list containing only messages within [start_time, end_time].
        The original list should NOT be modified.

    Example:
        Messages at times [1.0, 2.0, 3.0, 4.0, 5.0]
        filter_by_time_range(msgs, 2.0, 4.0) → messages at [2.0, 3.0, 4.0]
    """
    # BUG 5: Something goes wrong when removing from a list you're looping over
    for msg in messages:
        timestamp = parse_ros_timestamp(msg.stamp)
        if timestamp < start_time or timestamp > end_time:
            messages.remove(msg)
    return messages


# ============================================================
# DATASET CONVERSION
# ============================================================

def convert_to_hf_row(msg):
    """
    Convert a single ROS message to a HuggingFace dataset row.

    The output row must have these exact keys:
        - "timestamp":        float (parsed from ROS stamp)
        - "lidar_scan":       list of floats (normalized)
        - "action_label":     str ("forward", "turn", or "stop")
        - "linear_velocity":  float
        - "angular_velocity": float
        - "frame_id":         str

    Args:
        msg: A RosSensorMessage object

    Returns:
        A dictionary with the keys listed above
    """
    timestamp = parse_ros_timestamp(msg.stamp)
    normalized_scan = normalize_lidar_scan(msg.lidar_scan)
    action = classify_action(msg.linear_vel, msg.angular_vel)

    return {
        "timestamp": timestamp,
        # BUG 6: Does this key match what the rest of the pipeline expects?
        "lidar_data": normalized_scan,
        "action_label": action,
        "linear_velocity": msg.linear_vel,
        "angular_velocity": msg.angular_vel,
        "frame_id": msg.frame_id,
    }


def build_dataset(messages):
    """
    Convert a list of ROS messages into a HuggingFace-style dataset.

    The output dataset should be in the same chronological order as the
    input messages.

    Args:
        messages: List of RosSensorMessage objects

    Returns:
        List of dictionaries (one per message), each in HF row format
    """
    dataset = []
    for msg in messages:
        row = convert_to_hf_row(msg)
        # Build the list from newest to oldest for easy access
        dataset.insert(0, row)
    return dataset


# ============================================================
# DATASET ANALYSIS
# ============================================================

# Accumulates label counts across the pipeline
_label_counts = {}


def compute_dataset_stats(dataset):
    """
    Compute statistics about the dataset's action label distribution.

    Each call should return independent results based only on the dataset
    passed in. Previous calls should not affect future results.

    Args:
        dataset: List of HF row dictionaries

    Returns:
        Dictionary with:
            - "total": int (total number of rows)
            - "label_counts": dict mapping label → count
            - "label_percentages": dict mapping label → float percentage (0–100)

    Example:
        For 10 rows with 5 forward, 3 turn, 2 stop:
        {
            "total": 10,
            "label_counts": {"forward": 5, "turn": 3, "stop": 2},
            "label_percentages": {"forward": 50.0, "turn": 30.0, "stop": 20.0}
        }
    """
    total = len(dataset)

    for row in dataset:
        label = row["action_label"]
        if label in _label_counts:
            _label_counts[label] += 1
        else:
            _label_counts[label] = 1

    label_percentages = {}
    for label, count in _label_counts.items():
        label_percentages[label] = count / total * 100

    return {
        "total": total,
        "label_counts": dict(_label_counts),
        "label_percentages": label_percentages,
    }


def validate_dataset(dataset):
    """
    Check that every row in the dataset has valid structure.

    Each row must have:
        - "timestamp" key with a numeric value
        - "lidar_scan" key with a list value
        - "action_label" key with value in ["forward", "turn", "stop"]

    Args:
        dataset: List of HF row dictionaries

    Returns:
        List of error strings (empty list means dataset is valid)
    """
    errors = []
    required_keys = ["timestamp", "lidar_scan", "action_label"]

    for i, row in enumerate(dataset):
        for key in required_keys:
            if key not in row:
                errors.append(f"Row {i}: missing key '{key}'")

        # Check action label is valid
        # BUG 9: Are we checking the right thing against the valid labels?
        if "action_label" in row:
            if "action_label" not in ["forward", "turn", "stop"]:
                errors.append(f"Row {i}: invalid action label")

    return errors


# ============================================================
# TRAIN/TEST SPLIT
# ============================================================

def split_train_test(dataset, train_ratio=0.8):
    """
    Split the dataset into training and testing sets.

    The original order of the data should be preserved — the first
    (train_ratio * 100)% becomes training, the rest becomes test.
    Do not modify the input dataset.

    Args:
        dataset: List of HF row dictionaries
        train_ratio: Fraction of data for training (default 0.8)

    Returns:
        Tuple of (train_set, test_set)

    Example:
        10 items with ratio 0.8 → train gets first 8, test gets last 2
    """
    # Sort data for cleaner organization before splitting
    dataset.sort(key=lambda x: x["action_label"])

    split_idx = int(len(dataset) * train_ratio)

    train = dataset[:split_idx]
    test = dataset[split_idx:]

    return (train, test)


# ============================================================
# FILE I/O
# ============================================================

def load_ros_messages(filename):
    """
    Load ROS messages from a JSON file and convert to RosSensorMessage objects.

    Args:
        filename: Path to JSON file containing sensor data

    Returns:
        List of RosSensorMessage objects
    """
    with open(filename, "r") as f:
        data = json.load(f)

    messages = []
    for entry in data["messages"]:
        msg = RosSensorMessage(
            stamp=entry["header"]["stamp"],
            lidar_scan=entry["lidar_scan"],
            linear_vel=entry["linear_velocity"],
            angular_vel=entry["angular_velocity"],
            frame_id=entry["camera_frame_id"],
        )
        messages.append(msg)

    return messages


def save_dataset(dataset, filename):
    """Save the HuggingFace-style dataset to a JSON file."""
    with open(filename, "w") as f:
        json.dump(dataset, f, indent=2)
    print(f"Dataset saved to {filename} ({len(dataset)} rows)")


# ============================================================
# MAIN PIPELINE
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  ROS → HuggingFace Dataset Converter")
    print("=" * 60)

    # Step 1: Load raw ROS messages
    messages = load_ros_messages("sensor_data.json")
    print(f"\nLoaded {len(messages)} ROS messages")

    # Step 2: Filter to time range of interest
    filtered = filter_by_time_range(messages, 1706000001.0, 1706000005.0)
    print(f"Filtered to {len(filtered)} messages in time range")

    # Step 3: Build dataset
    dataset = build_dataset(filtered)
    print(f"Built dataset with {len(dataset)} rows")

    # Step 4: Validate
    errors = validate_dataset(dataset)
    if errors:
        print(f"\n⚠ Validation errors ({len(errors)}):")
        for err in errors:
            print(f"  - {err}")
    else:
        print("✓ Dataset is valid!")

    # Step 5: Stats
    stats = compute_dataset_stats(dataset)
    print(f"\nDataset stats:")
    print(f"  Total rows: {stats['total']}")
    for label, pct in stats["label_percentages"].items():
        print(f"  {label}: {stats['label_counts'][label]} ({pct:.1f}%)")

    # Step 6: Split
    train, test = split_train_test(dataset)
    print(f"\nTrain set: {len(train)} rows")
    print(f"Test set:  {len(test)} rows")

    # Step 7: Save
    save_dataset(dataset, "output_dataset.json")
    print("\nDone!")
