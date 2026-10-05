import cv2
import mediapipe as mp
import math

# Path to MediaPipe model
MODEL_PATH = "../models/hand_landmarker.task"

# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=RunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)


# Calculate distance between two landmarks
def calculate_distance(point1, point2):

    dx = point1.x - point2.x
    dy = point1.y - point2.y

    distance = math.sqrt(dx * dx + dy * dy)

    return distance


# Calculate angle of wrist → index MCP
def calculate_hand_angle(wrist, index_mcp):

    dx = index_mcp.x - wrist.x
    dy = index_mcp.y - wrist.y

    angle = math.degrees(math.atan2(dy, dx))

    return angle


with HandLandmarker.create_from_options(options) as landmarker:

    frame_timestamp = 0

    while True:

        success, frame = cap.read()

        if not success:
            print("Could not access camera")
            break

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe image
        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hand
        result = landmarker.detect_for_video(
            mp_image,
            frame_timestamp
        )

        # If hand detected
        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # Important landmarks
            wrist = hand[0]
            index_mcp = hand[5]

            # Calculate palm size
            palm_size = calculate_distance(
                wrist,
                index_mcp
            )

            # Calculate hand angle
            hand_angle = calculate_hand_angle(
                wrist,
                index_mcp
            )

            # Print values
            print(
                f"Palm Size: {palm_size:.3f} | "
                f"Hand Angle: {hand_angle:.2f}°"
            )

            # Draw landmarks

            h, w, _ = frame.shape

            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    5,
                    (0, 255, 0),
                    -1
                )

            # Connections
            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (5, 9), (9, 10), (10, 11), (11, 12),
                (9, 13), (13, 14), (14, 15), (15, 16),
                (13, 17), (17, 18), (18, 19), (19, 20),
                (0, 17)
            ]

            for start, end in connections:

                x1 = int(hand[start].x * w)
                y1 = int(hand[start].y * h)

                x2 = int(hand[end].x * w)
                y2 = int(hand[end].y * h)

                cv2.line(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

            # Display measurements on camera

            cv2.putText(
                frame,
                f"Palm Size: {palm_size:.3f}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Angle: {hand_angle:.1f} deg",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        # Show camera
        cv2.imshow(
            "Robotic Hand - Hand Measurements",
            frame
        )

        # Increase timestamp
        frame_timestamp += 1

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


cap.release()
cv2.destroyAllWindows()