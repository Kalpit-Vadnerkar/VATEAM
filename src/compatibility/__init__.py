"""
Compatibility module for the TransFuser agent.

This module provides a compatibility layer between the TransFuser model
and the CARLA leaderboard evaluation framework.
"""

from .leaderboard_eval import TransFuserAgent, get_entry_point

__all__ = ['TransFuserAgent', 'get_entry_point'] 