"""
CARLA Simulator Interface

This module provides a simplified interface to the CARLA simulator.
"""

import carla
import numpy as np
from typing import Union

class CarlaSimulator:
    """
    Simplified interface to the CARLA simulator.
    """
    
    def __init__(self):
        """Initialize the simulator interface."""
        self.client = None
        self.world = None
        self.vehicle = None
        self.sensors = {}
        self.sensor_data = {}
    
    def connect(self, host='localhost', port=2000):
        """
        Connect to the CARLA server.
        
        Args:
            host (str): CARLA server host
            port (int): CARLA server port
        """
        try:
            self.client = carla.Client(host, port)
            self.client.set_timeout(10.0)
            self.world = self.client.get_world()
            print(f"Connected to CARLA server at {host}:{port}")
        except Exception as e:
            print(f"Failed to connect to CARLA server: {e}")
            raise
    
    def spawn_vehicle(self, model, transform, rolename='scenario'):
        """
        Spawn a vehicle in the simulation.
        
        Args:
            model (str): The model name of the vehicle to spawn
            transform (Union[dict, carla.Transform]): The transform for the vehicle
            rolename (str): The role name for the vehicle
            
        Returns:
            carla.Actor: The spawned vehicle actor
        """
        if not self.world:
            raise RuntimeError("Cannot spawn vehicle: World is not connected")
            
        # Get the blueprint
        blueprint = self.world.get_blueprint_library().find(model)
        if not blueprint:
            raise ValueError(f"Vehicle model '{model}' not found")
            
        # Set the role name
        blueprint.set_attribute('role_name', rolename)
        
        # Handle transform
        if isinstance(transform, dict):
            # Convert dictionary to carla.Transform
            location = carla.Location(
                x=float(transform.get('x', 0)),
                y=float(transform.get('y', 0)),
                z=float(transform.get('z', 0))
            )
            rotation = carla.Rotation(
                pitch=float(transform.get('pitch', 0)),
                yaw=float(transform.get('yaw', 0)),
                roll=float(transform.get('roll', 0))
            )
            transform = carla.Transform(location, rotation)
        elif not isinstance(transform, carla.Transform):
            raise ValueError("Transform must be either a dictionary or carla.Transform object")
            
        # Lift the vehicle slightly to avoid collisions
        spawn_point = carla.Transform(carla.Location(), transform.rotation)
        spawn_point.location.x = transform.location.x
        spawn_point.location.y = transform.location.y
        spawn_point.location.z = transform.location.z + 0.2  # Lift by 0.2 units
            
        # Try to spawn the vehicle
        try:
            vehicle = self.world.try_spawn_actor(blueprint, spawn_point)
            if vehicle is None:
                raise RuntimeError(f"Failed to spawn vehicle: Spawn failed because of collision at spawn position")
            
            # Store the vehicle reference
            self.vehicle = vehicle
            return vehicle
        except Exception as e:
            raise RuntimeError(f"Failed to spawn vehicle: {str(e)}")
    
    def add_rgb_camera(self, name, position, rotation, fov=90):
        """
        Add an RGB camera to the vehicle.
        
        Args:
            name (str): Camera name
            position (tuple): Camera position (x, y, z)
            rotation (tuple): Camera rotation (pitch, yaw, roll)
            fov (float): Field of view in degrees
        """
        if not self.vehicle:
            raise RuntimeError("No vehicle spawned")
        
        # Get camera blueprint
        blueprint = self.world.get_blueprint_library().find('sensor.camera.rgb')
        blueprint.set_attribute('image_size_x', '960')
        blueprint.set_attribute('image_size_y', '480')
        blueprint.set_attribute('fov', str(fov))
        
        # Create transform
        location = carla.Location(x=position[0], y=position[1], z=position[2])
        rotation = carla.Rotation(pitch=rotation[0], yaw=rotation[1], roll=rotation[2])
        transform = carla.Transform(location, rotation)
        
        # Attach camera to vehicle
        camera = self.world.spawn_actor(blueprint, transform, attach_to=self.vehicle)
        self.sensors[name] = camera
        
        # Set up callback
        camera.listen(lambda data: self._on_camera_data(name, data))
    
    def add_lidar(self, name, position, rotation, channels=64, range=100.0):
        """
        Add a LIDAR sensor to the vehicle.
        
        Args:
            name (str): LIDAR name
            position (tuple): LIDAR position (x, y, z)
            rotation (tuple): LIDAR rotation (pitch, yaw, roll)
            channels (int): Number of channels
            range (float): Range in meters
        """
        if not self.vehicle:
            raise RuntimeError("No vehicle spawned")
        
        # Get LIDAR blueprint
        blueprint = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')
        blueprint.set_attribute('channels', str(channels))
        blueprint.set_attribute('range', str(range))
        
        # Create transform
        location = carla.Location(x=position[0], y=position[1], z=position[2])
        rotation = carla.Rotation(pitch=rotation[0], yaw=rotation[1], roll=rotation[2])
        transform = carla.Transform(location, rotation)
        
        # Attach LIDAR to vehicle
        lidar = self.world.spawn_actor(blueprint, transform, attach_to=self.vehicle)
        self.sensors[name] = lidar
        
        # Set up callback
        lidar.listen(lambda data: self._on_lidar_data(name, data))
    
    def _on_camera_data(self, name, data):
        """
        Callback for camera data.
        
        Args:
            name (str): Camera name
            data (carla.Image): Camera data
        """
        # Convert to numpy array
        array = np.frombuffer(data.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (data.height, data.width, 4))
        array = array[:, :, :3]  # Remove alpha channel
        
        # Store data
        self.sensor_data[name] = array
    
    def _on_lidar_data(self, name, data):
        """
        Callback for LIDAR data.
        
        Args:
            name (str): LIDAR name
            data (carla.LidarMeasurement): LIDAR data
        """
        # Convert to numpy array
        array = np.frombuffer(data.raw_data, dtype=np.dtype('f4'))
        array = np.reshape(array, (int(array.shape[0] / 4), 4))
        
        # Store data
        self.sensor_data[name] = array
    
    def get_sensor_data(self):
        """
        Get sensor data.
        
        Returns:
            dict: Sensor data
        """
        return self.sensor_data
    
    def get_actors(self):
        """
        Get all actors in the world.
        
        Returns:
            carla.ActorList: List of actors
        """
        if not self.world:
            raise RuntimeError("Not connected to CARLA server")
        
        return self.world.get_actors()
    
    def disconnect(self):
        """Disconnect from the CARLA server."""
        # Destroy sensors
        for sensor in self.sensors.values():
            sensor.destroy()
        
        # Destroy vehicle
        if self.vehicle:
            self.vehicle.destroy()
        
        # Reset client
        self.client = None
        self.world = None
        self.vehicle = None
        self.sensors = {}
        self.sensor_data = {} 