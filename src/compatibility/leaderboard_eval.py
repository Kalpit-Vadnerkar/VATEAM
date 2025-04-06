"""
TransFuser Agent for Leaderboard Evaluation

This module provides a compatibility layer between the TransFuser model
and the CARLA leaderboard evaluation framework.
"""

import os
import sys
import time
import json
import numpy as np
import carla
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import deque
import copy
from srunner.scenariomanager.carla_data_provider import CarlaDataProvider

from leaderboard.autoagents.autonomous_agent import AutonomousAgent
from leaderboard.utils.checkpoint_tools import fetch_dict, create_default_json_msg, save_dict
from leaderboard.envs.sensor_interface import SensorConfigurationInvalid
from leaderboard.autoagents.agent_wrapper_local import AgentWrapper, AgentError
from leaderboard.utils.route_parser import RouteParser
from leaderboard.utils.statistics_manager_local import StatisticsManager

# Import the working implementation
team_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../team_code_transfuser'))
if team_code_path not in sys.path:
    sys.path.append(team_code_path)

from submission_agent import HybridAgent
from team_code_transfuser.config import GlobalConfig  # Use the full path to avoid conflicts

def get_entry_point():
    """
    Returns the name of the agent class to be used by the leaderboard evaluator.
    """
    return 'TransFuserAgent'

class TransFuserAgent(HybridAgent):
    """
    TransFuser agent that implements the leaderboard's AutonomousAgent interface.
    This class inherits from the working HybridAgent implementation.
    """
    
    def __init__(self, path_to_conf_file):
        """
        Initialize the TransFuser agent.
        
        Args:
            path_to_conf_file (str): Path to model weights or configuration file
        """
        print("[TransFuserAgent] Starting initialization...")
        super().__init__(path_to_conf_file)
        print("[TransFuserAgent] Initialization completed")
    
    def setup(self, path_to_conf_file):
        """
        Setup the agent with the given configuration file.
        
        Args:
            path_to_conf_file (str): Path to configuration file
        """
        print("[TransFuserAgent] Setting up agent...")
        super().setup(path_to_conf_file)
        print("[TransFuserAgent] Setup completed")
    
    def set_global_plan(self, global_plan_gps, global_plan_world_coord):
        """
        Set the plan (route) for the agent.
        
        Args:
            global_plan_gps (list): List of GPS coordinates for the route
            global_plan_world_coord (list): List of world coordinates for the route
        """
        print("[TransFuserAgent] Setting global plan...")
        self._global_plan = global_plan_gps
        self._global_plan_world_coord = global_plan_world_coord
        self._init()  # This will set up the route planner
        print(f"[TransFuserAgent] Global plan set with {len(global_plan_gps)} waypoints")
    
    def run_step(self, input_data, timestamp):
        """
        Execute one step of navigation.
        
        Args:
            input_data (dict): Dictionary containing sensor data
            timestamp (float): Current timestamp
            
        Returns:
            carla.VehicleControl: Control command for the vehicle
        """
        return super().run_step(input_data, timestamp)
    
    def destroy(self):
        """
        Clean up resources.
        """
        super().destroy() 