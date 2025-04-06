"""
Sensor Interface Module

This module provides interfaces for different types of CARLA sensors.
"""

import carla
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from queue import Queue
import threading

@dataclass
class SensorConfig:
    """Configuration for a sensor."""
    location: Tuple[float, float, float]
    rotation: Tuple[float, float, float]
    attachment: Optional[carla.Actor] = None

class BaseSensor:
    """Base class for all sensors."""
    def __init__(self, world: carla.World, config: SensorConfig):
        """Initialize the sensor.
        
        Args:
            world: CARLA world instance
            config: Sensor configuration
        """
        self.world = world
        self.config = config
        self.sensor = None
        self.queue = Queue()
        self.thread = None
        self.running = False
        
    def spawn(self) -> None:
        """Spawn the sensor in the world."""
        raise NotImplementedError
        
    def destroy(self) -> None:
        """Destroy the sensor and cleanup resources."""
        self.running = False
        if self.thread is not None:
            self.thread.join()
        if self.sensor is not None:
            self.sensor.destroy()
            
    def get_data(self) -> Optional[np.ndarray]:
        """Get the latest sensor data.
        
        Returns:
            Latest sensor data as numpy array, or None if no data available
        """
        try:
            return self.queue.get_nowait()
        except:
            return None
            
    def _sensor_callback(self, data) -> None:
        """Callback function for sensor data.
        
        Args:
            data: Raw sensor data
        """
        raise NotImplementedError

class RGBCamera(BaseSensor):
    """RGB camera sensor."""
    def __init__(self, world: carla.World, config: SensorConfig, fov: float = 90.0):
        """Initialize the RGB camera.
        
        Args:
            world: CARLA world instance
            config: Sensor configuration
            fov: Field of view in degrees
        """
        super().__init__(world, config)
        self.fov = fov
        
    def spawn(self) -> None:
        """Spawn the RGB camera."""
        blueprint = self.world.get_blueprint_library().find('sensor.camera.rgb')
        blueprint.set_attribute('fov', str(self.fov))
        
        transform = carla.Transform(
            carla.Location(*self.config.location),
            carla.Rotation(*self.config.rotation)
        )
        
        self.sensor = self.world.spawn_actor(
            blueprint,
            transform,
            attach_to=self.config.attachment
        )
        
        self.sensor.listen(self._sensor_callback)
        self.running = True
        self.thread = threading.Thread(target=self._process_data)
        self.thread.start()
        
    def _sensor_callback(self, data) -> None:
        """Process RGB camera data.
        
        Args:
            data: Raw camera data
        """
        array = np.frombuffer(data.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (data.height, data.width, 4))
        array = array[:, :, :3]  # Remove alpha channel
        self.queue.put(array)
        
    def _process_data(self) -> None:
        """Process sensor data in a separate thread."""
        while self.running:
            try:
                self.queue.get(timeout=0.1)
            except:
                continue

class LidarSensor(BaseSensor):
    """LIDAR sensor."""
    def __init__(self, world: carla.World, config: SensorConfig,
                 channels: int = 32, range: float = 50.0):
        """Initialize the LIDAR sensor.
        
        Args:
            world: CARLA world instance
            config: Sensor configuration
            channels: Number of LIDAR channels
            range: Maximum range in meters
        """
        super().__init__(world, config)
        self.channels = channels
        self.range = range
        
    def spawn(self) -> None:
        """Spawn the LIDAR sensor."""
        blueprint = self.world.get_blueprint_library().find('sensor.lidar.ray_cast')
        blueprint.set_attribute('channels', str(self.channels))
        blueprint.set_attribute('range', str(self.range))
        
        transform = carla.Transform(
            carla.Location(*self.config.location),
            carla.Rotation(*self.config.rotation)
        )
        
        self.sensor = self.world.spawn_actor(
            blueprint,
            transform,
            attach_to=self.config.attachment
        )
        
        self.sensor.listen(self._sensor_callback)
        self.running = True
        self.thread = threading.Thread(target=self._process_data)
        self.thread.start()
        
    def _sensor_callback(self, data) -> None:
        """Process LIDAR data.
        
        Args:
            data: Raw LIDAR data
        """
        array = np.frombuffer(data.raw_data, dtype=np.dtype('f4'))
        array = np.reshape(array, (int(array.shape[0] / 4), 4))
        self.queue.put(array)
        
    def _process_data(self) -> None:
        """Process sensor data in a separate thread."""
        while self.running:
            try:
                self.queue.get(timeout=0.1)
            except:
                continue

class SemanticCamera(BaseSensor):
    """Semantic segmentation camera."""
    def __init__(self, world: carla.World, config: SensorConfig, fov: float = 90.0):
        """Initialize the semantic camera.
        
        Args:
            world: CARLA world instance
            config: Sensor configuration
            fov: Field of view in degrees
        """
        super().__init__(world, config)
        self.fov = fov
        
    def spawn(self) -> None:
        """Spawn the semantic camera."""
        blueprint = self.world.get_blueprint_library().find('sensor.camera.semantic_segmentation')
        blueprint.set_attribute('fov', str(self.fov))
        
        transform = carla.Transform(
            carla.Location(*self.config.location),
            carla.Rotation(*self.config.rotation)
        )
        
        self.sensor = self.world.spawn_actor(
            blueprint,
            transform,
            attach_to=self.config.attachment
        )
        
        self.sensor.listen(self._sensor_callback)
        self.running = True
        self.thread = threading.Thread(target=self._process_data)
        self.thread.start()
        
    def _sensor_callback(self, data) -> None:
        """Process semantic camera data.
        
        Args:
            data: Raw semantic camera data
        """
        array = np.frombuffer(data.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (data.height, data.width, 4))
        array = array[:, :, 0]  # Only need the semantic segmentation channel
        self.queue.put(array)
        
    def _process_data(self) -> None:
        """Process sensor data in a separate thread."""
        while self.running:
            try:
                self.queue.get(timeout=0.1)
            except:
                continue

class DepthCamera(BaseSensor):
    """Depth camera."""
    def __init__(self, world: carla.World, config: SensorConfig, fov: float = 90.0):
        """Initialize the depth camera.
        
        Args:
            world: CARLA world instance
            config: Sensor configuration
            fov: Field of view in degrees
        """
        super().__init__(world, config)
        self.fov = fov
        
    def spawn(self) -> None:
        """Spawn the depth camera."""
        blueprint = self.world.get_blueprint_library().find('sensor.camera.depth')
        blueprint.set_attribute('fov', str(self.fov))
        
        transform = carla.Transform(
            carla.Location(*self.config.location),
            carla.Rotation(*self.config.rotation)
        )
        
        self.sensor = self.world.spawn_actor(
            blueprint,
            transform,
            attach_to=self.config.attachment
        )
        
        self.sensor.listen(self._sensor_callback)
        self.running = True
        self.thread = threading.Thread(target=self._process_data)
        self.thread.start()
        
    def _sensor_callback(self, data) -> None:
        """Process depth camera data.
        
        Args:
            data: Raw depth camera data
        """
        array = np.frombuffer(data.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (data.height, data.width, 4))
        array = array[:, :, 0]  # Only need the depth channel
        self.queue.put(array)
        
    def _process_data(self) -> None:
        """Process sensor data in a separate thread."""
        while self.running:
            try:
                self.queue.get(timeout=0.1)
            except:
                continue 