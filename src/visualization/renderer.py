"""
Visualization Renderer Module

This module handles visualization of simulation results and model outputs.
"""

import cv2
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class Renderer:
    def __init__(self, 
                 output_dir: str = 'results',
                 save_video: bool = False,
                 fps: int = 30):
        """Initialize the renderer.
        
        Args:
            output_dir: Directory to save visualization outputs
            save_video: Whether to save video output
            fps: Frames per second for video output
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.save_video = save_video
        self.fps = fps
        self.video_writer = None
        self.frame_count = 0
        
    def setup_video_writer(self, 
                          width: int,
                          height: int,
                          filename: str = 'output.mp4') -> None:
        """Set up video writer for saving frames.
        
        Args:
            width: Video width in pixels
            height: Video height in pixels
            filename: Output video filename
        """
        if not self.save_video:
            return
            
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = self.output_dir / filename
        self.video_writer = cv2.VideoWriter(
            str(output_path),
            fourcc,
            self.fps,
            (width, height)
        )
        
    def render_frame(self,
                    camera_image: np.ndarray,
                    model_output: Optional[Tuple[float, float]] = None,
                    debug_info: Optional[Dict] = None) -> np.ndarray:
        """Render a single frame with visualization overlays.
        
        Args:
            camera_image: RGB camera image
            model_output: Tuple of (steering, throttle) values
            debug_info: Additional debug information to display
            
        Returns:
            Rendered frame as numpy array
        """
        # Convert to BGR for OpenCV
        frame = cv2.cvtColor(camera_image, cv2.COLOR_RGB2BGR)
        
        # Add model output visualization
        if model_output is not None:
            steering, throttle = model_output
            self._draw_control_info(frame, steering, throttle)
            
        # Add debug information
        if debug_info:
            self._draw_debug_info(frame, debug_info)
            
        # Save frame if video recording is enabled
        if self.save_video and self.video_writer is not None:
            self.video_writer.write(frame)
            self.frame_count += 1
            
        return frame
        
    def _draw_control_info(self,
                          frame: np.ndarray,
                          steering: float,
                          throttle: float) -> None:
        """Draw control information on the frame.
        
        Args:
            frame: Frame to draw on
            steering: Steering value
            throttle: Throttle value
        """
        height, width = frame.shape[:2]
        
        # Draw steering bar
        bar_width = 200
        bar_height = 20
        x = width - bar_width - 20
        y = height - 60
        
        # Background
        cv2.rectangle(frame,
                     (x, y),
                     (x + bar_width, y + bar_height),
                     (0, 0, 0),
                     -1)
                     
        # Steering indicator
        steering_pos = int(x + (bar_width / 2) * (1 + steering))
        cv2.line(frame,
                (steering_pos, y),
                (steering_pos, y + bar_height),
                (0, 255, 0),
                2)
                
        # Draw throttle bar
        y += 30
        cv2.rectangle(frame,
                     (x, y),
                     (x + bar_width, y + bar_height),
                     (0, 0, 0),
                     -1)
                     
        # Throttle indicator
        throttle_width = int(bar_width * (throttle + 1) / 2)
        cv2.rectangle(frame,
                     (x, y),
                     (x + throttle_width, y + bar_height),
                     (0, 255, 0),
                     -1)
                     
    def _draw_debug_info(self,
                        frame: np.ndarray,
                        debug_info: Dict) -> None:
        """Draw debug information on the frame.
        
        Args:
            frame: Frame to draw on
            debug_info: Dictionary of debug information
        """
        y = 30
        for key, value in debug_info.items():
            text = f"{key}: {value}"
            cv2.putText(frame,
                       text,
                       (10, y),
                       cv2.FONT_HERSHEY_SIMPLEX,
                       0.5,
                       (255, 255, 255),
                       1)
            y += 20
            
    def save_frame(self,
                  frame: np.ndarray,
                  filename: Optional[str] = None) -> None:
        """Save a single frame to disk.
        
        Args:
            frame: Frame to save
            filename: Output filename (if None, auto-generated)
        """
        if filename is None:
            filename = f"frame_{self.frame_count:06d}.jpg"
            
        output_path = self.output_dir / filename
        cv2.imwrite(str(output_path), frame)
        
    def cleanup(self) -> None:
        """Clean up resources."""
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None 