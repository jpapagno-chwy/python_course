# 🛠 Debug the Data Pipeline — ROS to HuggingFace Dataset Converter

## Scenario

A teammate wrote a Python script to convert our robot's ROS sensor data into a HuggingFace-compatible dataset for training a navigation model. The script runs... but produces wrong and corrupt data.

There are **10 bugs** hidden in the code. Your job is to find and fix every one.

## Files

| File | Description |
|------|-------------|
| `project.py` | The buggy pipeline script — **edit this file** |
| `tests.py` | One test per bug — run this to check your fixes |
| `sensor_data.json` | Sample ROS sensor messages (input data) |

## How To Work

1. Run the tests to see which ones fail:
   ```
   python tests.py
   ```

2. Pick a failing test and read the error message carefully

3. Find the bug in `project.py` and fix it

4. Re-run the tests — repeat until all 10 pass!

You can also run the full pipeline to see its output:
```
python project.py
```

## The Pipeline

The script converts ROS robot data → ML training data:

```
sensor_data.json (ROS format)
        │
        ▼
   Parse timestamps (secs + nanoseconds → float)
        │
        ▼
   Normalize LIDAR scans (raw meters → 0.0 to 1.0)
        │
        ▼
   Classify actions (velocity → "forward" / "turn" / "stop")
        │
        ▼
   Filter by time range
        │
        ▼
   Convert to HuggingFace row format
        │
        ▼
   Build dataset → Validate → Compute stats → Train/test split
        │
        ▼
   output_dataset.json (HuggingFace format)
```

## Bug Types to Look For

- Wrong operators or values
- Logic errors in conditions
- Python-specific gotchas
- Data structure misuse
- Key/variable name errors
- Scope and state management issues

**Note:** 7 of the bugs are marked with `# BUG` comments in the code.
The remaining 3 are **unmarked** — you'll need to find those through
the test output alone. Welcome to real debugging.

## Debugging Tips

- Add `print()` statements to see variable values
- Read the **docstrings** — they describe the CORRECT behavior
- Check expected vs actual output in the test error messages
- Work through bugs one at a time (they're numbered in the tests)
- Use the Python debugger: `breakpoint()` or `python -m pdb project.py`

## Stretch Goal

After fixing all bugs, write a short "post-mortem" for each bug:
1. What was the bug?
2. What was the symptom?
3. How did you find it?

Good luck!
