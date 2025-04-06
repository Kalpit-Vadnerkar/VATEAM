"""
Configuration settings for the TransFuser agent and leaderboard evaluation.
"""

import os

# Get environment variables
CARLA_ROOT = os.getenv('CARLA_ROOT')
SCENARIO_RUNNER_ROOT = os.getenv('SCENARIO_RUNNER_ROOT')
LEADERBOARD_ROOT = os.getenv('LEADERBOARD_ROOT')

# Agent configuration
AGENT_MODULE_PATH = os.path.join(os.path.dirname(__file__), 'compatibility', 'leaderboard_eval.py')

# Default evaluation settings - read from environment variables if available
DEFAULT_TRACK = os.getenv('CHALLENGE_TRACK_CODENAME', 'SENSORS')
DEFAULT_PORT = int(os.getenv('PORT', '2000'))
DEFAULT_TIMEOUT = int(os.getenv('TIMEOUT', '60'))
DEFAULT_OUTPUT_DIR = os.getenv('OUTPUT_DIR', 'results')
DEFAULT_TRAFFIC_MANAGER_PORT = int(os.getenv('TRAFFIC_MANAGER_PORT', '8000'))
DEFAULT_TRAFFIC_MANAGER_SEED = int(os.getenv('TRAFFIC_MANAGER_SEED', '0'))
DEFAULT_HOST = os.getenv('HOST', 'localhost')
DEFAULT_DEBUG = os.getenv('DEBUG_CHALLENGE', '0') == '1'
DEFAULT_RECORD = os.getenv('RECORD', '0') == '1'
DEFAULT_RESUME = os.getenv('RESUME', '0') == '1'
DEFAULT_REPETITIONS = int(os.getenv('REPETITIONS', '1'))

# Default paths - read from environment variables if available
DEFAULT_ROUTES = os.getenv('ROUTES', os.path.join(LEADERBOARD_ROOT, 'data/longest6/longest6.xml') if LEADERBOARD_ROOT else 'data/longest6/longest6.xml')
DEFAULT_SCENARIOS = os.getenv('SCENARIOS', os.path.join(LEADERBOARD_ROOT, 'data/longest6/eval_scenarios.json') if LEADERBOARD_ROOT else 'data/longest6/eval_scenarios.json') 