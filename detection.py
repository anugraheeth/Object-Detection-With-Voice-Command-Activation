import cv2
from ultralytics import YOLO
import pyttsx3
import torch
import time
import speech_recognition as sr
import threading
import queue

# Initialize speech recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Configuration
confidence_threshold = 0.8
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Global variables
last_speech_time = 0
speech_interval = 5
is_running = False
terminate = False
command_queue = queue.Queue()

def listen_for_command():
    """
    Continuously listen for voice commands in a separate thread
    """
    global is_running
    while not terminate:
        try:
            print("Listening for command...")
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
                
                try:
                    # Recognize speech
                    command = recognizer.recognize_google(audio).lower()
                    print(f"Command detected: {command}")
                    
                    # Process specific commands
                    if "assist" in command:
                        print("Activation command received!")
                        command_queue.put("start")
                    elif "stop" in command:
                        print("Stop command received!")
                        command_queue.put("stop")
                    elif "sleep" in command:
                        print("terminate command received..")
                        command_queue.put("sleep")
                    
                except sr.UnknownValueError:
                    print("Could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results: {e}")
        
        except Exception as e:
            print(f"Error in command listening: {e}")

def play_audio(label):
    """
    Text-to-speech function with print for debugging
    """
    print(f"Speaking: {label}")
    engine.say(label)
    engine.runAndWait()

def move_left(text="move left"):
    """Left movement voice command"""
    print(f"Moving Left: {text}")
    engine.say(text)
    engine.runAndWait()

def move_right(text="move right"):
    """Right movement voice command"""
    print(f"Moving Right: {text}")
    engine.say(text)
    engine.runAndWait()

def run_object_detection():
    """
    Main object detection function
    """
    global last_speech_time, is_running
    
    # Load YOLO model
    model = YOLO('yolov8n.pt').to(device)  
    
    # Open camera
    cap = cv2.VideoCapture(0) 
    
    object_labels = set()

    while is_running:
        # Check for stop command
        if not command_queue.empty():
            cmd = command_queue.get()
            if cmd == "stop":
                print("Stopping object detection...")
                break
            elif cmd=="sleep":
                print("terminating the program....")
                break        
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect objects
        results = model(frame_rgb)

        obstacle_in_center = False
        obstacle_in_left = False
        obstacle_in_right = False

        detected_objects = []
        
        for result in results:
            annotated_frame = result.plot() 
            annotated_frame_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            
            if result.boxes:
                for box in result.boxes:
                    b = box.xyxy[0]  
                    x,y,h,w = b
                    
                    # Determine object position
                    if x < 640//3:
                        obstacle_in_left = True
                    elif x+w > 2 * 640//3:
                        obstacle_in_right = True
                    else:
                        obstacle_in_center = True
                    
                    class_id = int(box.cls.item())  
                    confidence = box.conf.item()    
                    
                    if confidence >= confidence_threshold:
                        label = result.names[class_id]
                        if label:
                            detected_objects.append(label)
                            
                            current_time = time.time()
                            if detected_objects and (current_time - last_speech_time > speech_interval):
                                object_text = "Detected: " + ", ".join(detected_objects)
                                play_audio(object_text) 
                                last_speech_time = current_time
                                
                                # Navigation logic
                                if obstacle_in_center:
                                    if not obstacle_in_left:
                                        move_left()
                                    elif not obstacle_in_right:
                                        move_right()
                                    else:
                                        play_audio("Obstacle ahead, can't move")
                                elif obstacle_in_left:
                                    move_right()
                                elif obstacle_in_right:
                                    move_left()

            cv2.imshow('YOLOv8 Object Detection', annotated_frame_bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Clean up
    cap.release()
    cv2.destroyAllWindows()
    is_running = False

def main():
    """
    Main function to start voice command and object detection
    """
    global is_running
    
    # Start voice command listener thread
    voice_thread = threading.Thread(target=listen_for_command, daemon=True)
    voice_thread.start()
    
    print("Voice Assistant Ready. Say 'assist' to start object detection.")
    
    while True:
        if not command_queue.empty():
            cmd = command_queue.get()
            if cmd == "start":
                is_running = True
                play_audio("Starting object detection")
                run_object_detection()
            elif cmd =="sleep":
                terminate = True
                break
        
        # Prevent tight loop
        time.sleep(0.1)

if __name__ == "__main__":
    main()
