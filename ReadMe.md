# Object Detection with Voice Command Control

This project integrates speech recognition with object detection using the YOLOv8 model. It allows a user to control the object detection process through voice commands and provides feedback via text-to-speech. The system continuously listens for specific commands to start, stop, or terminate the program.

## Features
- **Voice Command Control**: The system listens for and responds to specific voice commands such as `assist`, `stop`, and `sleep`.
- **Real-Time Object Detection**: Uses the YOLOv8 model to detect objects in real-time via a webcam.
- **Text-to-Speech Feedback**: Provides feedback about detected objects and movements via text-to-speech.
- **Navigation Based on Object Detection**: The system can make decisions on movements based on detected objects, such as moving left or right.

## Prerequisites

Before running the project, make sure you have the following installed:

- **Python 3.x**
- **PyTorch** (with CUDA support for GPU acceleration, if available)
- **Ultralytics YOLOv8** for object detection
- **OpenCV** for video capture and display
- **SpeechRecognition** for recognizing voice commands
- **pyttsx3** for text-to-speech functionality

You can install the required dependencies using the following command:

```bash
pip install torch opencv-python ultralytics SpeechRecognition pyttsx3
```

### Additional Requirements

- **YOLOv8 model file**: You need to download the YOLOv8 model weights (`yolov8n.pt`). You can download it from [Ultralytics GitHub](https://github.com/ultralytics/yolov8).

## How to Use

1. **Start the Program**: 
   - Run the Python script: 
   ```bash
   python object_detection_voice_control.py
   ```
2. **Voice Commands**:
   - Say **"assist"** to start the object detection and navigation process.
   - Say **"stop"** to stop object detection and navigation.
   - Say **"sleep"** to terminate the program completely.

3. **Object Detection**:
   - The system will display a live camera feed showing detected objects and their locations.
   - The program will respond with voice feedback, e.g., "Detected: person, dog" based on the objects detected.

4. **Exit the Program**: 
   - The program will terminate when you say **"sleep"** or press 'q' to quit the display window.

## Code Structure

- **listen_for_command()**: This function listens for voice commands in a separate thread. It processes specific commands such as "assist", "stop", and "sleep".
  
- **play_audio()**: This function uses `pyttsx3` to convert text into speech for feedback.

- **move_left()** and **move_right()**: These functions simulate robot movement based on the detected objects' positions.

- **run_object_detection()**: This function initializes the YOLOv8 model and performs object detection on the webcam feed.

- **main()**: This is the main entry point. It starts the voice command listener thread and waits for commands to start or stop object detection.

## Example Output

```bash
Listening for command...
Command detected: assist
Activation command received!
Starting object detection...
Detected: person, dog
Moving Left: move left
...
Listening for command...
Command detected: sleep
terminate command received..
Terminating program...
```

The camera feed will display with bounding boxes for detected objects. The system will speak out the detected objects and navigate based on the position of the objects.

## Troubleshooting

1. **Microphone not working**:
   - Ensure your microphone is correctly set up and detected by your system.
   - You can test microphone input by running a basic speech recognition script before using it in this program.

2. **Object Detection Errors**:
   - Ensure you have the correct YOLOv8 model file (`yolov8n.pt`) placed in the correct directory.
   - Make sure your camera is functioning correctly. You can test it with OpenCV using a simple script to capture video.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
