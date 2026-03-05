"""
🧪 Tests for the ROS → HuggingFace Data Pipeline

Run with:  python tests.py

Each test targets a specific bug. Fix the bugs one at a time
and re-run to check your progress!
"""

from project import (
    RosSensorMessage,
    parse_ros_timestamp,
    normalize_lidar_scan,
    classify_action,
    filter_by_time_range,
    convert_to_hf_row,
    build_dataset,
    compute_dataset_stats,
    validate_dataset,
    split_train_test,
)


# ============================================================
# TEST 1: Timestamp Parsing
# ============================================================

def test_1_timestamp_parsing():
    """ROS timestamps should convert nanoseconds correctly."""
    # 500,000,000 nanoseconds = 0.5 seconds
    stamp = {"secs": 1000, "nsecs": 500000000}
    result = parse_ros_timestamp(stamp)
    assert result == 1000.5, (
        f"parse_ros_timestamp({stamp}) should be 1000.5, got {result}.\n"
        f"  Hint: 500,000,000 nanoseconds = 0.5 seconds. Check your divisor."
    )

    # 250,000,000 nanoseconds = 0.25 seconds
    stamp2 = {"secs": 0, "nsecs": 250000000}
    result2 = parse_ros_timestamp(stamp2)
    assert result2 == 0.25, (
        f"parse_ros_timestamp({stamp2}) should be 0.25, got {result2}"
    )

    print("  ✓ Test 1 passed: Timestamp parsing")


# ============================================================
# TEST 2: LIDAR Normalization
# ============================================================

def test_2_lidar_normalization():
    """Normalized LIDAR values should be between 0.0 and 1.0."""
    scan = [3.0, 6.0, 15.0]
    result = normalize_lidar_scan(scan, max_range=12.0)
    expected = [0.25, 0.5, 1.0]
    assert result == expected, (
        f"normalize_lidar_scan({scan}, max_range=12.0) should be {expected}, got {result}.\n"
        f"  Hint: 15.0 / 12.0 = 1.25, but should be clamped to 1.0."
    )

    # All zeros should stay zero
    assert normalize_lidar_scan([0.0, 0.0], max_range=10.0) == [0.0, 0.0]

    # Exact max_range should normalize to 1.0
    assert normalize_lidar_scan([12.0], max_range=12.0) == [1.0]

    print("  ✓ Test 2 passed: LIDAR normalization")


# ============================================================
# TEST 3: Mutable Default Argument
# ============================================================

def test_3_mutable_default():
    """Each RosSensorMessage should have its OWN lidar_scan list."""
    msg1 = RosSensorMessage(stamp={"secs": 0, "nsecs": 0})
    msg2 = RosSensorMessage(stamp={"secs": 1, "nsecs": 0})

    # Modify msg1's scan
    msg1.lidar_scan.append(99.9)

    # msg2 should NOT be affected
    assert msg2.lidar_scan == [], (
        f"msg2.lidar_scan should be [], got {msg2.lidar_scan}.\n"
        f"  Hint: msg1 and msg2 shouldn't share the same list object.\n"
        f"        Look up 'mutable default arguments' in Python."
    )

    print("  ✓ Test 3 passed: No shared mutable default")


# ============================================================
# TEST 4: Action Classification
# ============================================================

def test_4_action_classification():
    """Turning should take priority when robot is moving AND turning."""
    # Pure stop
    assert classify_action(0.0, 0.0) == "stop", (
        "classify_action(0.0, 0.0) should be 'stop'"
    )

    # Pure forward
    assert classify_action(0.5, 0.0) == "forward", (
        "classify_action(0.5, 0.0) should be 'forward'"
    )

    # Pure turn
    assert classify_action(0.0, 0.5) == "turn", (
        "classify_action(0.0, 0.5) should be 'turn'"
    )

    # Moving AND turning → should be "turn" (turning takes priority!)
    result = classify_action(0.5, 0.3)
    assert result == "turn", (
        f"classify_action(0.5, 0.3) should be 'turn', got '{result}'.\n"
        f"  Hint: Read the docstring — turning takes priority over forward.\n"
        f"        Check the order of your elif conditions."
    )

    # Negative angular velocity is still a turn
    assert classify_action(0.0, -0.3) == "turn"

    print("  ✓ Test 4 passed: Action classification")


# ============================================================
# TEST 5: Filter By Time Range
# ============================================================

def test_5_filter_by_time_range():
    """Filtering should return correct results and not mutate the input."""
    messages = [
        RosSensorMessage(stamp={"secs": 1, "nsecs": 0}, lidar_scan=[1.0]),
        RosSensorMessage(stamp={"secs": 2, "nsecs": 0}, lidar_scan=[2.0]),
        RosSensorMessage(stamp={"secs": 3, "nsecs": 0}, lidar_scan=[3.0]),
        RosSensorMessage(stamp={"secs": 4, "nsecs": 0}, lidar_scan=[4.0]),
        RosSensorMessage(stamp={"secs": 5, "nsecs": 0}, lidar_scan=[5.0]),
    ]

    original_len = len(messages)
    result = filter_by_time_range(messages, 3.0, 5.0)

    # Should get exactly 3 messages (t=3, t=4, t=5)
    assert len(result) == 3, (
        f"Expected 3 messages in range [3.0, 5.0], got {len(result)}.\n"
        f"  Hint: Are elements being skipped during iteration?"
    )

    # Original list should not be modified
    assert len(messages) == original_len, (
        f"Original list was modified (was {original_len}, now {len(messages)}).\n"
        f"  Hint: Build a NEW list instead of removing from the original.\n"
        f"        Never modify a list while iterating over it."
    )

    print("  ✓ Test 5 passed: Time range filtering")


# ============================================================
# TEST 6: HuggingFace Row Keys
# ============================================================

def test_6_hf_row_keys():
    """Converted rows must have the exact key names the pipeline expects."""
    msg = RosSensorMessage(
        stamp={"secs": 1000, "nsecs": 0},
        lidar_scan=[6.0],
        linear_vel=0.5,
        angular_vel=0.0,
        frame_id="cam_001",
    )
    row = convert_to_hf_row(msg)

    expected_keys = {"timestamp", "lidar_scan", "action_label",
                     "linear_velocity", "angular_velocity", "frame_id"}

    assert "lidar_scan" in row, (
        f"Row is missing key 'lidar_scan'. Got keys: {list(row.keys())}.\n"
        f"  Hint: Check the key names in convert_to_hf_row().\n"
        f"        Do they match the docstring?"
    )

    assert set(row.keys()) == expected_keys, (
        f"Row keys don't match. Expected {expected_keys}, got {set(row.keys())}"
    )

    print("  ✓ Test 6 passed: HuggingFace row keys")


# ============================================================
# TEST 7: Build Dataset Order
# ============================================================

def test_7_build_dataset():
    """build_dataset should preserve the chronological order of messages."""
    messages = [
        RosSensorMessage(
            stamp={"secs": 100, "nsecs": 0}, lidar_scan=[1.0], linear_vel=0.5,
        ),
        RosSensorMessage(
            stamp={"secs": 200, "nsecs": 0}, lidar_scan=[2.0], linear_vel=0.3,
        ),
        RosSensorMessage(
            stamp={"secs": 300, "nsecs": 0}, lidar_scan=[3.0], linear_vel=0.0,
            angular_vel=0.5,
        ),
    ]
    dataset = build_dataset(messages)

    assert len(dataset) == 3, f"Expected 3 rows, got {len(dataset)}"
    assert isinstance(dataset[0], dict), (
        f"Each dataset row should be a dict, got {type(dataset[0]).__name__}"
    )

    # Dataset should preserve chronological order (same as input)
    timestamps = [row["timestamp"] for row in dataset]
    assert timestamps == [100.0, 200.0, 300.0], (
        f"Dataset should be in chronological order [100.0, 200.0, 300.0], "
        f"got {timestamps}.\n"
        f"  Hint: Check how rows are being added to the dataset list.\n"
        f"        Does the method preserve insertion order?"
    )

    print("  ✓ Test 7 passed: Build dataset preserves order")


# ============================================================
# TEST 8: Dataset Stats
# ============================================================

def test_8_dataset_stats():
    """compute_dataset_stats should give independent results each call."""
    # --- First call ---
    dataset_a = [
        {"action_label": "forward"},
        {"action_label": "forward"},
        {"action_label": "turn"},
        {"action_label": "stop"},
    ]
    stats_a = compute_dataset_stats(dataset_a)

    assert stats_a["total"] == 4
    assert stats_a["label_counts"]["forward"] == 2
    assert stats_a["label_counts"]["turn"] == 1
    assert stats_a["label_counts"]["stop"] == 1
    assert stats_a["label_percentages"]["forward"] == 50.0

    # --- Second call with DIFFERENT data ---
    # Results should be completely independent of the first call
    dataset_b = [
        {"action_label": "turn"},
        {"action_label": "turn"},
        {"action_label": "turn"},
        {"action_label": "stop"},
        {"action_label": "stop"},
    ]
    stats_b = compute_dataset_stats(dataset_b)

    assert stats_b["total"] == 5

    assert stats_b["label_counts"]["turn"] == 3, (
        f"Second call: expected turn count = 3, got {stats_b['label_counts']['turn']}.\n"
        f"  Hint: Are counts from the first call leaking into the second?\n"
        f"        Check where the counting variable is defined."
    )
    assert stats_b["label_percentages"]["turn"] == 60.0, (
        f"Second call: expected turn = 60.0%, got {stats_b['label_percentages']['turn']}.\n"
        f"  Hint: The stats function is called twice — are the results independent?"
    )

    # dataset_b has no "forward" — it shouldn't appear in the results
    assert "forward" not in stats_b["label_counts"], (
        f"Second call has no 'forward' data, but found it in counts: "
        f"{stats_b['label_counts']}.\n"
        f"  Hint: Leftover data from a previous call?"
    )

    print("  ✓ Test 8 passed: Dataset stats are independent")


# ============================================================
# TEST 9: Validate Dataset
# ============================================================

def test_9_validate_dataset():
    """A valid dataset should produce zero validation errors."""
    valid_dataset = [
        {"timestamp": 1.0, "lidar_scan": [0.5], "action_label": "forward"},
        {"timestamp": 2.0, "lidar_scan": [0.3], "action_label": "turn"},
        {"timestamp": 3.0, "lidar_scan": [0.1], "action_label": "stop"},
    ]
    errors = validate_dataset(valid_dataset)
    assert len(errors) == 0, (
        f"Valid dataset should have 0 errors, got {len(errors)}:\n"
        + "\n".join(f"  - {e}" for e in errors)
        + "\n  Hint: Are you checking the VALUE of 'action_label' or the KEY itself?"
    )

    # A dataset with missing keys should produce errors
    bad_dataset = [
        {"timestamp": 1.0},  # missing lidar_scan and action_label
    ]
    errors2 = validate_dataset(bad_dataset)
    assert len(errors2) >= 2, (
        f"Invalid dataset should have at least 2 errors, got {len(errors2)}"
    )

    print("  ✓ Test 9 passed: Dataset validation")


# ============================================================
# TEST 10: Train/Test Split
# ============================================================

def test_10_train_test_split():
    """Train/test split should preserve data order and not modify the input."""
    # Create a dataset with mixed labels in chronological order
    dataset = [
        {"action_label": "forward", "timestamp": 1.0},
        {"action_label": "turn",    "timestamp": 2.0},
        {"action_label": "forward", "timestamp": 3.0},
        {"action_label": "stop",    "timestamp": 4.0},
        {"action_label": "forward", "timestamp": 5.0},
        {"action_label": "turn",    "timestamp": 6.0},
        {"action_label": "forward", "timestamp": 7.0},
        {"action_label": "stop",    "timestamp": 8.0},
        {"action_label": "turn",    "timestamp": 9.0},
        {"action_label": "forward", "timestamp": 10.0},
    ]

    # Save original order to check for mutation
    original_timestamps = [row["timestamp"] for row in dataset]

    train, test = split_train_test(dataset, train_ratio=0.8)

    assert len(train) == 8, (
        f"With 10 items and 0.8 ratio, train should have 8 items, got {len(train)}."
    )
    assert len(test) == 2, (
        f"With 10 items and 0.8 ratio, test should have 2 items, got {len(test)}."
    )

    # The split should preserve the original chronological order
    train_timestamps = [row["timestamp"] for row in train]
    test_timestamps = [row["timestamp"] for row in test]

    assert train_timestamps == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0], (
        f"Train should be the first 8 items in original order.\n"
        f"  Got timestamps: {train_timestamps}\n"
        f"  Hint: Is something changing the order of the data before splitting?"
    )
    assert test_timestamps == [9.0, 10.0], (
        f"Test should be the last 2 items in original order.\n"
        f"  Got timestamps: {test_timestamps}\n"
        f"  Hint: The split should not rearrange the dataset."
    )

    # The original dataset should not have been modified
    current_timestamps = [row["timestamp"] for row in dataset]
    assert current_timestamps == original_timestamps, (
        f"split_train_test should not modify the original dataset.\n"
        f"  Before: {original_timestamps}\n"
        f"  After:  {current_timestamps}\n"
        f"  Hint: Is something sorting or rearranging the input data?"
    )

    print("  ✓ Test 10 passed: Train/test split preserves order")


# ============================================================
# TEST RUNNER
# ============================================================

def run_tests():
    tests = [
        test_1_timestamp_parsing,
        test_2_lidar_normalization,
        test_3_mutable_default,
        test_4_action_classification,
        test_5_filter_by_time_range,
        test_6_hf_row_keys,
        test_7_build_dataset,
        test_8_dataset_stats,
        test_9_validate_dataset,
        test_10_train_test_split,
    ]

    print("=" * 60)
    print("  🧪 Running Pipeline Debug Tests")
    print("=" * 60)
    print()

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__}: FAILED")
            # Show first 3 lines of error message
            msg = str(e)
            lines = msg.split("\n")
            for line in lines[:4]:
                print(f"    {line}")
            if len(lines) > 4:
                print(f"    ...")
            print()
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__}: CRASHED — {type(e).__name__}: {e}")
            print()
            failed += 1

    print()
    print("=" * 60)
    if failed == 0:
        print("  🎉 ALL TESTS PASSED! Great debugging work!")
    else:
        print(f"  Results: {passed} passed, {failed} failed out of {len(tests)}")
        print(f"  Keep debugging — you've got {failed} more bug(s) to find!")
    print("=" * 60)


if __name__ == "__main__":
    run_tests()
