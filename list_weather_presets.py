#!/usr/bin/env python3

"""
Script to list all available weather presets in CARLA.
"""

import sys

def main():
    """
    Main function to print all weather presets available in CARLA.
    """
    # These are the preset names available in CARLA (in different formats)
    # The format with spaces is what CARLA actually returns
    WEATHER_PRESETS = [
        {"internal": "ClearNoon", "display": "Clear Noon"},
        {"internal": "CloudyNoon", "display": "Cloudy Noon"},
        {"internal": "WetNoon", "display": "Wet Noon"},
        {"internal": "WetCloudyNoon", "display": "Wet Cloudy Noon"},
        {"internal": "MidRainyNoon", "display": "Mid Rainy Noon"},
        {"internal": "HardRainNoon", "display": "Hard Rain Noon"},
        {"internal": "SoftRainNoon", "display": "Soft Rain Noon"},
        {"internal": "ClearSunset", "display": "Clear Sunset"},
        {"internal": "CloudySunset", "display": "Cloudy Sunset"},
        {"internal": "WetSunset", "display": "Wet Sunset"},
        {"internal": "WetCloudySunset", "display": "Wet Cloudy Sunset"},
        {"internal": "MidRainSunset", "display": "Mid Rain Sunset"},
        {"internal": "HardRainSunset", "display": "Hard Rain Sunset"},
        {"internal": "SoftRainSunset", "display": "Soft Rain Sunset"},
    ]

    print("\nAvailable CARLA Weather Presets:")
    print("================================")
    print("Here are the available presets you can use:")
    
    for preset in WEATHER_PRESETS:
        print(f"--weather-preset={preset['display']:<20} # CARLA's internal name")
        print(f"--weather-preset={preset['internal']:<20} # No spaces version (also works)")
        print("")
        
    print("\nExample usage:")
    print("./run_evaluation.sh --weather-preset=\"Hard Rain Noon\"")
    print("./run_evaluation.sh --weather-preset=HardRainNoon")
    print("")
    print("NOTE: The default preset is HardRainNoon")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 