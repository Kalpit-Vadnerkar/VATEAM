#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default values
export WORK_DIR=${WORK_DIR:-$SCRIPT_DIR}
export CARLA_ROOT=${CARLA_ROOT:-"${WORK_DIR}/carla"}
export SCENARIO_RUNNER_ROOT=${SCENARIO_RUNNER_ROOT:-"${WORK_DIR}/scenario_runner"}
export LEADERBOARD_ROOT=${LEADERBOARD_ROOT:-"${WORK_DIR}/leaderboard"}

# CARLA paths
export CARLA_SERVER=${CARLA_ROOT}/CarlaUE4.sh
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI
export PYTHONPATH=$PYTHONPATH:${CARLA_ROOT}/PythonAPI/carla
export PYTHONPATH=$PYTHONPATH:$CARLA_ROOT/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg

# Scenario Runner and Leaderboard paths
export PYTHONPATH="${CARLA_ROOT}/PythonAPI/carla/":"${SCENARIO_RUNNER_ROOT}":"${LEADERBOARD_ROOT}":${PYTHONPATH}

# Leaderboard environment variables
export DEBUG_CHALLENGE=${DEBUG_CHALLENGE:-0}  # 0 for normal operation, 1 for debug mode
export RECORD=${RECORD:-0}  # 0 for no recording, 1 for recording
export RESUME=${RESUME:-0}  # 0 for new run, 1 for resuming from checkpoint

# Default evaluation settings
export SCENARIOS=${SCENARIOS:-"${LEADERBOARD_ROOT}/data/longest6/eval_scenarios.json"}
export ROUTES=${ROUTES:-"${LEADERBOARD_ROOT}/data/longest6/longest6.xml"}
export REPETITIONS=${REPETITIONS:-1}
export CHALLENGE_TRACK_CODENAME=${CHALLENGE_TRACK_CODENAME:-"SENSORS"}
export CHECKPOINT_ENDPOINT=${CHECKPOINT_ENDPOINT:-"${WORK_DIR}/results/evaluation.json"}

# Verify paths exist
for path in "$CARLA_ROOT" "$SCENARIO_RUNNER_ROOT" "$LEADERBOARD_ROOT"; do
    if [ ! -d "$path" ]; then
        echo "Error: Directory not found: $path"
        exit 1
    fi
done

# Verify CARLA Python API
if [ ! -d "${CARLA_ROOT}/PythonAPI/carla" ]; then
    echo "Error: CARLA Python API not found at ${CARLA_ROOT}/PythonAPI/carla"
    exit 1
fi

# Verify Scenario Runner
if [ ! -d "${SCENARIO_RUNNER_ROOT}/srunner" ]; then
    echo "Error: Scenario Runner not found at ${SCENARIO_RUNNER_ROOT}/srunner"
    exit 1
fi

# Verify Leaderboard
if [ ! -d "${LEADERBOARD_ROOT}/leaderboard" ]; then
    echo "Error: Leaderboard not found at ${LEADERBOARD_ROOT}/leaderboard"
    exit 1
fi

echo "Environment configured:"
echo "WORK_DIR: $WORK_DIR"
echo "CARLA_ROOT: $CARLA_ROOT"
echo "SCENARIO_RUNNER_ROOT: $SCENARIO_RUNNER_ROOT"
echo "LEADERBOARD_ROOT: $LEADERBOARD_ROOT"
echo "PYTHONPATH: $PYTHONPATH"
echo "DEBUG_CHALLENGE: $DEBUG_CHALLENGE"
echo "RECORD: $RECORD"
echo "RESUME: $RESUME" 