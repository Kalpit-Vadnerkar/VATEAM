"""
Run Leaderboard Evaluation

This script runs the CARLA leaderboard evaluation using our TransFuser agent.
"""

import os
import sys
import argparse
from pathlib import Path

# Get environment variables
CARLA_ROOT = os.getenv('CARLA_ROOT')
SCENARIO_RUNNER_ROOT = os.getenv('SCENARIO_RUNNER_ROOT')
LEADERBOARD_ROOT = os.getenv('LEADERBOARD_ROOT')

if not all([CARLA_ROOT, SCENARIO_RUNNER_ROOT, LEADERBOARD_ROOT]):
    raise RuntimeError("Missing required environment variables. Please source config.sh first")

# Add paths to Python path
carla_path = os.path.join(CARLA_ROOT, 'PythonAPI', 'carla')
if carla_path not in sys.path:
    sys.path.append(carla_path)
if SCENARIO_RUNNER_ROOT not in sys.path:
    sys.path.append(SCENARIO_RUNNER_ROOT)
if LEADERBOARD_ROOT not in sys.path:
    sys.path.append(LEADERBOARD_ROOT)

try:
    from leaderboard.leaderboard_evaluator_local import LeaderboardEvaluator
except ImportError as e:
    print(f"Error importing leaderboard modules: {e}")
    print(f"CARLA_ROOT: {CARLA_ROOT}")
    print(f"SCENARIO_RUNNER_ROOT: {SCENARIO_RUNNER_ROOT}")
    print(f"LEADERBOARD_ROOT: {LEADERBOARD_ROOT}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

from leaderboard.utils.statistics_manager_local import StatisticsManager
from leaderboard_config import (
    AGENT_MODULE_PATH, DEFAULT_TRACK, DEFAULT_PORT, DEFAULT_TIMEOUT,
    DEFAULT_OUTPUT_DIR, DEFAULT_TRAFFIC_MANAGER_PORT, DEFAULT_TRAFFIC_MANAGER_SEED,
    DEFAULT_HOST, DEFAULT_DEBUG, DEFAULT_RECORD, DEFAULT_RESUME, DEFAULT_REPETITIONS,
    DEFAULT_ROUTES, DEFAULT_SCENARIOS
)

def parse_args():
    parser = argparse.ArgumentParser(description='Run TransFuser evaluation')
    parser.add_argument('--model-path', type=str, default=os.getenv('DEFAULT_MODEL_PATH'),
                      help='Path to TransFuser model weights')
    parser.add_argument('--routes', type=str, default=DEFAULT_ROUTES,
                      help='Path to routes file')
    parser.add_argument('--scenarios', type=str, default=DEFAULT_SCENARIOS,
                      help='Path to scenarios file')
    parser.add_argument('--checkpoint', type=str, default=None,
                      help='Path to checkpoint file')
    parser.add_argument('--track', type=str, default=DEFAULT_TRACK,
                      help='Track to evaluate (SENSORS or MAP)')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT,
                      help='CARLA server port')
    parser.add_argument('--timeout', type=int, default=DEFAULT_TIMEOUT,
                      help='Timeout for each route in seconds')
    parser.add_argument('--output-dir', type=str, default=DEFAULT_OUTPUT_DIR,
                      help='Directory to save evaluation results')
    parser.add_argument('--agent', type=str, default=AGENT_MODULE_PATH,
                      help='Path to agent module')
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create a namespace object to hold the arguments for the evaluator
    class Args:
        pass
    
    eval_args = Args()
    eval_args.routes = args.routes
    eval_args.scenarios = args.scenarios
    eval_args.repetitions = DEFAULT_REPETITIONS
    eval_args.agent = args.agent  # This should point to our compatibility module
    eval_args.agent_config = args.model_path  # Pass model path as agent config
    eval_args.checkpoint = args.checkpoint
    eval_args.track = args.track
    eval_args.port = args.port
    eval_args.timeout = args.timeout
    eval_args.host = DEFAULT_HOST
    eval_args.trafficManagerPort = DEFAULT_TRAFFIC_MANAGER_PORT
    eval_args.trafficManagerSeed = DEFAULT_TRAFFIC_MANAGER_SEED
    eval_args.debug = DEFAULT_DEBUG
    eval_args.record = DEFAULT_RECORD
    eval_args.resume = DEFAULT_RESUME
    
    # Create statistics manager
    statistics_manager = StatisticsManager()
    
    # Create evaluator
    evaluator = LeaderboardEvaluator(eval_args, statistics_manager)
    
    # Run evaluation
    evaluator.run(eval_args)
    
    # Print results
    print("\nEvaluation Results:")
    print("==================")
    try:
        for route_record in statistics_manager._records:
            print(f"Route: {route_record['route_id']}")
            print(f"Status: {route_record['status']}")
            print(f"Completion: {route_record['route_completion']*100:.2f}%")
            print(f"Infractions: {route_record['infractions']}")
            print("-" * 30)
    except Exception as e:
        print(f"Error getting statistics: {e}")
        print("Evaluation completed, but statistics could not be retrieved.")

if __name__ == '__main__':
    main() 