# Brewtracker JSON Structure Documentation

This document describes the JSON structure returned by the Brewfather brewtracker API for use in automation and scripting.

## High-Level Structure

The brewtracker API returns a JSON object with the following structure:

```json
{
  "_id": "batch_id_string",
  "name": "Batch #45",
  "active": true,
  "completed": false,
  "stage": 0,                    // Current stage index (0-based)
  "startTime": 1760396686456,     // Overall start timestamp (ms since epoch)
  "stages": [
    {
      "name": "Mash",           // Stage name
      "type": "tracker",        // Stage type
      "duration": 3600,         // Stage duration in seconds
      "step": 4,                // Current step index within this stage
      "position": 3598,         // Current position in seconds within stage
      "paused": false,          // Whether stage is paused
      "start": 1760398179706,   // Stage start timestamp (ms)
      "steps": [
        {
          "type": "mash",       // Step type: "mash", "ramp", "event", "boil", "hopstand"
          "name": "Temperature", // Step name (may be null for unnamed steps)
          "time": 3600,         // Step timing reference (seconds from stage start)
          "duration": 1800,     // Step duration in seconds (null for instant steps)
          "value": 63.0,        // Target value (temperature for mash/ramp steps)
          "priority": 10,       // Step priority (higher = more important)
          "description": "Temperature - 30 min @ 63 °C",
          "tooltip": "30 min @ 63 °C",
          "pauseBefore": false, // Whether this step pauses before starting
          "startTime": 1760398179662,  // Step start timestamp (ms, may be null)
          "endTime": null,               // Step end timestamp (ms, may be null)
          "final": false         // Whether this is the final step of stage
        }
        // ... more steps
      ]
    }
    // ... more stages (Boil, Hop Stand, etc.)
  ]
}
```

## Key Fields for Automation

### Overall Status
- `tracker.stage`: Current active stage index (0-based)
- `tracker.active`: Whether the brewtracker is currently active
- `tracker.completed`: Whether the brewing process is completed

### Stage Information
- `tracker.stages[stage].step`: Current active step index within stage
- `tracker.stages[stage].position`: Current position in seconds within stage
- `tracker.stages[stage].paused`: Whether the current stage is paused
- `tracker.stages[stage].duration`: Total stage duration in seconds

### Step Information
- `tracker.stages[stage].steps[step].startTime`: When current step started (ms since epoch)
- `tracker.stages[stage].steps[step].duration`: How long step should last (seconds)
- `tracker.stages[stage].steps[step].type`: What kind of step it is
- `tracker.stages[stage].steps[step].value`: Target temperature (for mash/ramp steps)
- `tracker.stages[stage].steps[step].name`: Step name (may be null)
- `tracker.stages[stage].steps[step].description`: Step description
- `tracker.stages[stage].steps[step].tooltip`: Short tooltip/description

## Timing Calculation

To calculate elapsed and remaining time for the current step:

```javascript
// Get current timestamp in milliseconds
const currentTimeMs = Date.now();

// Calculate elapsed time in seconds
const elapsedSeconds = (currentTimeMs - stepStartTimeMs) / 1000;

// Calculate remaining time in seconds
const remainingSeconds = stepDurationSeconds - elapsedSeconds;

// Convert to minutes and seconds
const elapsedMinutes = Math.floor(elapsedSeconds / 60);
const elapsedSecondsRemainder = Math.floor(elapsedSeconds % 60);
const remainingMinutes = Math.floor(remainingSeconds / 60);
const remainingSecondsRemainder = Math.floor(remainingSeconds % 60);
```

## Step Types

| Type | Description | Has Duration | Has Target | Purpose |
|------|-------------|--------------|------------|---------|
| `"mash"` | Temperature hold step | Yes | Yes | Hold mash temperature for specified time |
| `"ramp"` | Heat/cool to target | No | Yes | Change temperature (no duration) |
| `"event"` | Additions or actions | No | No | Add ingredients or take actions |
| `"boil"` | Boiling step | Variable | No | Boiling wort |
| `"hopstand"` | Hop stand step | Yes | Yes | Steep hops at specific temp |

## Python Example

```python
import time
from datetime import datetime

def get_step_timing(step):
    """Calculate timing for a brewtracker step"""
    if not step.get('startTime') or not step.get('duration'):
        return None

    current_time_ms = int(time.time() * 1000)
    start_time_ms = step['startTime']
    duration_seconds = step['duration']

    elapsed_seconds = (current_time_ms - start_time_ms) / 1000
    remaining_seconds = duration_seconds - elapsed_seconds

    return {
        'elapsed_seconds': elapsed_seconds,
        'remaining_seconds': remaining_seconds,
        'elapsed_minutes': int(elapsed_seconds // 60),
        'elapsed_seconds_rem': int(elapsed_seconds % 60),
        'remaining_minutes': int(remaining_seconds // 60),
        'remaining_seconds_rem': int(remaining_seconds % 60),
        'step_type': step['type'],
        'target_temp': step.get('value'),
        'step_name': step.get('name')
    }

# Example usage with the current step
def get_current_step_info(tracker_data):
    current_stage_idx = tracker_data['stage']
    current_stage = tracker_data['stages'][current_stage_idx]
    current_step_idx = current_stage['step']
    current_step = current_stage['steps'][current_step_idx]

    return get_step_timing(current_step)
```

## Access via MCP Tool

Use the `get_batch_brewtracker` tool with a batch ID to retrieve this data:

```
get_batch_brewtracker(batch_id="xcDltKGoKBZyHvmp7RM71AL4O44e5v")
```

The tool will return human-readable timing information for the current step, including elapsed and remaining time.