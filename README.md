# TransFuser Evaluation System

This project implements an evaluation system for the TransFuser autonomous driving model in CARLA 0.9.10.

## Overview

TransFuser is a perception-prediction-planning model that fuses camera and LiDAR sensor data for end-to-end autonomous driving. This repository contains a refactored version of the original TransFuser system integrated with the CARLA Leaderboard evaluation framework.

## Requirements

- CARLA 0.9.10
- Python 3.7
- PyTorch 1.7+
- CUDA 10.2+ (for GPU acceleration)

## Project Structure

- `src/`: Core modules of the system
  - `compatibility/`: CARLA Leaderboard compatibility layer
    - `leaderboard_eval.py`: Implements the `TransFuserAgent` class that interfaces with the Leaderboard evaluator
  - `carla_interface/`: Interface to the CARLA simulator
  - `config/`: Configuration files
  - `utils/`: Utility functions
  - `run_evaluation.py`: Main script to run the evaluation
- `leaderboard/`: CARLA Leaderboard evaluation framework
- `scenario_runner/`: Scenario definitions for evaluation
- `team_code_transfuser/`: Original TransFuser implementation
  - `submission_agent.py`: Main agent implementation
  - `model.py`: Neural network model definitions
  - `config.py`: Configuration classes
  - Other implementation files
- `model_ckpt/`: Pretrained model checkpoints
  - `models 2022/transfuser/`: Default model weights directory

## Setup

1. Install CARLA 0.9.10:
   ```bash
   ./setup_carla.sh
   ```

2. Set up the environment:
   ```bash
   source config.sh
   ```

## Running the Evaluation

The evaluation can be run using the `run_evaluation.sh` script:

```bash
./run_evaluation.sh
```

This will use the default model path (`model_ckpt/models 2022/transfuser`). If you want to use a different model, you can specify it with the `--model-path` argument:

```bash
./run_evaluation.sh --model-path /path/to/your/model
```

### Additional Options

- `--routes`: Path to routes file (default: `${LEADERBOARD_ROOT}/data/longest6/longest6.xml`)
- `--scenarios`: Path to scenarios file (default: `${LEADERBOARD_ROOT}/data/longest6/eval_scenarios.json`)
- `--track`: Track to evaluate (SENSORS or MAP, default: SENSORS)
- `--port`: CARLA server port (default: 2000)
- `--timeout`: Timeout for each route in seconds (default: 60)
- `--output-dir`: Directory to save evaluation results (default: results)
- `--carla-root`: Path to CARLA installation (default: ${WORK_DIR}/carla)

## License

See LICENSE file for details.
