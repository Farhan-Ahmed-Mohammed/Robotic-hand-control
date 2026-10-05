import cv2
import mediapipe as mp
import math


# ==========================================
# MediaPipe configuration
# ==========================================

MODEL_PATH = "../models/hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


# ==========================================
# Calculate angle between 3 landmarks
#
# point1 -> point2 -> point3
# ==========================================

def calculate_joint_angle(point1, point2, point3):

    angle1 = math.atan2(
        point1.y - point2.y,
        point1.x - point2.x
    )

    angle2 = math.atan2(
        point3.y - point2.y,
        point3.x - point2.x
    )

    angle = math.degrees(angle2 - angle1)

    angle = abs(angle)

    if angle > 180:
        angle = 360 - angle

    return angle


# ==========================================
# Distance between two landmarks
# ==========================================

def calculate_distance(point1, point2):

    dx = point1.x - point2.x
    dy = point1.y - point2.y

    return math.sqrt(dx * dx + dy * dy)


# ==========================================
# Whole hand angle
# Wrist -> Index MCP
# ==========================================

def calculate_hand_angle(wrist, index_mcp):

    dx = index_mcp.x - wrist.x
    dy = index_mcp.y - wrist.y

    return math.degrees(
        math.atan2(dy, dx)
    )


# ==========================================
# Calculate individual finger joint angles
# ==========================================

def calculate_finger_angles(hand):

    # --------------------------------------
    # THUMB
    #
    # 1 = thumb CMC
    # 2 = thumb MCP
    # 3 = thumb IP
    # 4 = thumb TIP
    # --------------------------------------

    thumb_mcp = calculate_joint_angle(
        hand[1],
        hand[2],
        hand[3]
    )

    thumb_ip = calculate_joint_angle(
        hand[2],
        hand[3],
        hand[4]
    )

    # --------------------------------------
    # INDEX
    #
    # 5 = MCP
    # 6 = PIP
    # 7 = DIP
    # 8 = TIP
    # --------------------------------------

    index_mcp = calculate_joint_angle(
        hand[0],
        hand[5],
        hand[6]
    )

    index_pip = calculate_joint_angle(
        hand[5],
        hand[6],
        hand[7]
    )

    index_dip = calculate_joint_angle(
        hand[6],
        hand[7],
        hand[8]
    )

    # --------------------------------------
    # MIDDLE
    #
    # 9 = MCP
    # 10 = PIP
    # 11 = DIP
    # 12 = TIP
    # --------------------------------------

    middle_mcp = calculate_joint_angle(
        hand[0],
        hand[9],
        hand[10]
    )

    middle_pip = calculate_joint_angle(
        hand[9],
        hand[10],
        hand[11]
    )

    middle_dip = calculate_joint_angle(
        hand[10],
        hand[11],
        hand[12]
    )

    # --------------------------------------
    # RING
    #
    # 13 = MCP
    # 14 = PIP
    # 15 = DIP
    # 16 = TIP
    # --------------------------------------

    ring_mcp = calculate_joint_angle(
        hand[0],
        hand[13],
        hand[14]
    )

    ring_pip = calculate_joint_angle(
        hand[13],
        hand[14],
        hand[15]
    )

    ring_dip = calculate_joint_angle(
        hand[14],
        hand[15],
        hand[16]
    )

    # --------------------------------------
    # PINKY
    #
    # 17 = MCP
    # 18 = PIP
    # 19 = DIP
    # 20 = TIP
    # --------------------------------------

    pinky_mcp = calculate_joint_angle(
        hand[0],
        hand[17],
        hand[18]
    )

    pinky_pip = calculate_joint_angle(
        hand[17],
        hand[18],
        hand[19]
    )

    pinky_dip = calculate_joint_angle(
        hand[18],
        hand[19],
        hand[20]
    )

    return {
        "thumb_mcp": thumb_mcp,
        "thumb_ip": thumb_ip,

        "index_mcp": index_mcp,
        "index_pip": index_pip,
        "index_dip": index_dip,

        "middle_mcp": middle_mcp,
        "middle_pip": middle_pip,
        "middle_dip": middle_dip,

        "ring_mcp": ring_mcp,
        "ring_pip": ring_pip,
        "ring_dip": ring_dip,

        "pinky_mcp": pinky_mcp,
        "pinky_pip": pinky_pip,
        "pinky_dip": pinky_dip
    }


# ==========================================
# MediaPipe options
# ==========================================

options = HandLandmarkerOptions(

    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),

    running_mode=RunningMode.VIDEO,

    num_hands=1,

    min_hand_detection_confidence=0.5,

    min_hand_presence_confidence=0.5,

    min_tracking_confidence=0.5
)


# ==========================================
# Camera
# ==========================================

cap = cv2.VideoCapture(0)


# ==========================================
# Start MediaPipe
# ==========================================

with HandLandmarker.create_from_options(options) as landmarker:

    frame_timestamp = 0

    while cap.isOpened():

        success, frame = cap.read()

        if not success:
            print("Camera frame could not be read.")
            break

        # BGR -> RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        # Detect hand
        result = landmarker.detect_for_video(
            mp_image,
            frame_timestamp
        )

        frame_timestamp += 1

        # ==================================
        # If hand detected
        # ==================================

        if result.hand_landmarks:

            hand = result.hand_landmarks[0]

            # ==================================
            # Basic hand measurements
            # ==================================

            wrist = hand[0]
            index_mcp_point = hand[5]

            palm_size = calculate_distance(
                wrist,
                index_mcp_point
            )

            hand_angle = calculate_hand_angle(
                wrist,
                index_mcp_point
            )

            # ==================================
            # Finger joint measurements
            # ==================================

            angles = calculate_finger_angles(hand)

            # ==================================
            # Display basic values
            # ==================================

            cv2.putText(
                frame,
                f"Palm: {palm_size:.3f}",
                (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"Hand: {hand_angle:.1f}",
                (20, 55),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

            # ==================================
            # Display THUMB
            # ==================================

            cv2.putText(
                frame,
                f"Thumb MCP: {angles['thumb_mcp']:.1f}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            cv2.putText(
                frame,
                f"Thumb IP: {angles['thumb_ip']:.1f}",
                (20, 115),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            # ==================================
            # Display INDEX
            # ==================================

            cv2.putText(
                frame,
                f"Index: {angles['index_mcp']:.1f} "
                f"{angles['index_pip']:.1f} "
                f"{angles['index_dip']:.1f}",
                (20, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            # ==================================
            # Display MIDDLE
            # ==================================

            cv2.putText(
                frame,
                f"Middle: {angles['middle_mcp']:.1f} "
                f"{angles['middle_pip']:.1f} "
                f"{angles['middle_dip']:.1f}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            # ==================================
            # Display RING
            # ==================================

            cv2.putText(
                frame,
                f"Ring: {angles['ring_mcp']:.1f} "
                f"{angles['ring_pip']:.1f} "
                f"{angles['ring_dip']:.1f}",
                (20, 210),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            # ==================================
            # Display PINKY
            # ==================================

            cv2.putText(
                frame,
                f"Pinky: {angles['pinky_mcp']:.1f} "
                f"{angles['pinky_pip']:.1f} "
                f"{angles['pinky_dip']:.1f}",
                (20, 240),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.50,
                (255, 255, 255),
                2
            )

            # ==================================
            # Draw landmarks
            # ==================================

            h, w, _ = frame.shape

            for landmark in hand:

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    4,
                    (0, 255, 0),
                    -1
                )

        # ==================================
        # Display camera
        # ==================================

        cv2.imshow(
            "Robotic Hand Tracking",
            frame
        )

        # Press Q to exit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


# ==========================================
# Cleanup
# ==========================================

cap.release()
cv2.destroyAllWindows()