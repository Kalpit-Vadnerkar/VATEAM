#!/bin/bash

# Source configuration
source "$(dirname "$0")/config.sh"

# Default values
MODEL_PATH="${WORK_DIR}/model_ckpt/models_2022/transfuser"
PORT=2000
TIMEOUT=60
OUTPUT_DIR="results"
AGENT_PATH="src/compatibility/leaderboard_eval.py"
WEATHER_PRESET="HardRainNoon"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --model-path)
            MODEL_PATH="$2"
            shift 2
            ;;
        --routes)
            ROUTES="$2"
            shift 2
            ;;
        --scenarios)
            SCENARIOS="$2"
            shift 2
            ;;
        --checkpoint)
            CHECKPOINT_ENDPOINT="$2"
            shift 2
            ;;
        --track)
            CHALLENGE_TRACK_CODENAME="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --work-dir)
            WORK_DIR="$2"
            export WORK_DIR
            shift 2
            ;;
        --carla-root)
            CARLA_ROOT="$2"
            export CARLA_ROOT
            shift 2
            ;;
        --agent)
            AGENT_PATH="$2"
            shift 2
            ;;
        --weather-preset)
            WEATHER_PRESET="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Check if CARLA server is running
if ! pgrep -x "CarlaUE4" > /dev/null; then
    echo "Starting CARLA server..."
    if [ -f "$CARLA_SERVER" ]; then
        "$CARLA_SERVER" --world-port=${PORT} -opengl &
    else
        echo "Error: CarlaUE4.sh not found at $CARLA_SERVER"
        echo "Please set the correct CARLA_ROOT path using --carla-root"
        exit 1
    fi
    sleep 10
fi

# Build the weather preset parameter if provided
WEATHER_PARAM=""
if [ -n "$WEATHER_PRESET" ]; then
    WEATHER_PARAM="--weather-preset=${WEATHER_PRESET}"
fi

# Run the leaderboard evaluation directly
python3 "${LEADERBOARD_ROOT}/leaderboard/leaderboard_evaluator_local.py" \
    --scenarios="${SCENARIOS}" \
    --routes="${ROUTES}" \
    --repetitions=1 \
    --track="${CHALLENGE_TRACK_CODENAME}" \
    --checkpoint="${CHECKPOINT_ENDPOINT}" \
    --agent="${AGENT_PATH}" \
    --agent-config="${MODEL_PATH}" \
    --debug=0 \
    --resume=0 \
    --port="${PORT}" \
    --timeout="${TIMEOUT}" \
    ${WEATHER_PARAM}

# Kill CARLA server if we started it
if [ "$KILL_CARLA_ON_EXIT" = true ] && pgrep -x "CarlaUE4" > /dev/null; then
    echo "Stopping CARLA server..."
    pkill -f "CarlaUE4"
fi 