import cv2
import mediapipe as mp
import math

from gesture_mapping import calculate_servo_targets


# ============================================================
# MEDIAPIPE SETUP
# ============================================================

MODEL_PATH = "../models/hand_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=1,
    min_hand_detection_confidence=0.5,
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


# ============================================================
# JOINT ANGLE
# ============================================================

def calculate_joint_angle(point1, point2, point3):

    v1 = (
        point1.x - point2.x,
        point1.y - point2.y
    )

    v2 = (
        point3.x - point2.x,
        point3.y - point2.y
    )

    dot_product = (
        v1[0] * v2[0] +
        v1[1] * v2[1]
    )

    magnitude1 = math.sqrt(
        v1[0] ** 2 +
        v1[1] ** 2
    )

    magnitude2 = math.sqrt(
        v2[0] ** 2 +
        v2[1] ** 2
    )

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    cosine_angle = (
        dot_product /
        (magnitude1 * magnitude2)
    )

    cosine_angle = max(
        -1,
        min(1, cosine_angle)
    )

    return math.degrees(
        math.acos(cosine_angle)
    )


# ============================================================
# WHOLE HAND ANGLE
# ============================================================

def calculate_hand_angle(wrist, index_mcp):

    dx = index_mcp.x - wrist.x
    dy = index_mcp.y - wrist.y

    return math.degrees(
        math.atan2(dy, dx)
    )


# ============================================================
# MAIN
# ============================================================

def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        print("ERROR: Could not open camera.")
        return


    with HandLandmarker.create_from_options(options) as detector:

        while cap.isOpened():

            ret, frame = cap.read()

            if not ret:

                print("ERROR: Could not read camera frame.")
                break


            frame = cv2.flip(
                frame,
                1
            )


            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )


            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )


            result = detector.detect(
                mp_image
            )


            if result.hand_landmarks:

                hand = result.hand_landmarks[0]


                # ====================================================
                # LANDMARKS
                # ====================================================

                wrist = hand[0]

                # Thumb
                thumb_mcp = hand[2]
                thumb_ip = hand[3]
                thumb_tip = hand[4]

                # Index
                index_mcp = hand[5]
                index_pip = hand[6]
                index_dip = hand[7]
                index_tip = hand[8]

                # Middle
                middle_mcp = hand[9]
                middle_pip = hand[10]
                middle_dip = hand[11]
                middle_tip = hand[12]

                # Ring
                ring_mcp = hand[13]
                ring_pip = hand[14]
                ring_dip = hand[15]
                ring_tip = hand[16]

                # Pinky
                pinky_mcp = hand[17]
                pinky_pip = hand[18]
                pinky_dip = hand[19]
                pinky_tip = hand[20]


                # ====================================================
                # JOINT ANGLES
                # ====================================================

                angles = {

                    "thumb_mcp":
                        calculate_joint_angle(
                            hand[1],
                            thumb_mcp,
                            thumb_ip
                        ),

                    "thumb_ip":
                        calculate_joint_angle(
                            thumb_mcp,
                            thumb_ip,
                            thumb_tip
                        ),


                    "index_mcp":
                        calculate_joint_angle(
                            index_mcp,
                            index_pip,
                            index_dip
                        ),

                    "index_pip":
                        calculate_joint_angle(
                            index_pip,
                            index_dip,
                            index_tip
                        ),

                    "index_dip":
                        calculate_joint_angle(
                            index_pip,
                            index_dip,
                            index_tip
                        ),


                    "middle_mcp":
                        calculate_joint_angle(
                            middle_mcp,
                            middle_pip,
                            middle_dip
                        ),

                    "middle_pip":
                        calculate_joint_angle(
                            middle_pip,
                            middle_dip,
                            middle_tip
                        ),

                    "middle_dip":
                        calculate_joint_angle(
                            middle_pip,
                            middle_dip,
                            middle_tip
                        ),


                    "ring_mcp":
                        calculate_joint_angle(
                            ring_mcp,
                            ring_pip,
                            ring_dip
                        ),

                    "ring_pip":
                        calculate_joint_angle(
                            ring_pip,
                            ring_dip,
                            ring_tip
                        ),

                    "ring_dip":
                        calculate_joint_angle(
                            ring_pip,
                            ring_dip,
                            ring_tip
                        ),


                    "pinky_mcp":
                        calculate_joint_angle(
                            pinky_mcp,
                            pinky_pip,
                            pinky_dip
                        ),

                    "pinky_pip":
                        calculate_joint_angle(
                            pinky_pip,
                            pinky_dip,
                            pinky_tip
                        ),

                    "pinky_dip":
                        calculate_joint_angle(
                            pinky_pip,
                            pinky_dip,
                            pinky_tip
                        )
                }


                # ====================================================
                # HAND ANGLE
                # ====================================================

                hand_angle = calculate_hand_angle(
                    wrist,
                    index_mcp
                )


                # ====================================================
                # PALM SIZE
                # ====================================================

                dx = index_mcp.x - wrist.x
                dy = index_mcp.y - wrist.y

                palm_size = math.sqrt(
                    dx * dx +
                    dy * dy
                )


                # ====================================================
                # DEBUG
                # ====================================================

                print(
                    "DEBUG INDEX:",
                    round(angles["index_mcp"], 1),
                    round(angles["index_pip"], 1),
                    round(angles["index_dip"], 1)
                )

                print(
                    "DEBUG PINKY:",
                    round(angles["pinky_mcp"], 1),
                    round(angles["pinky_pip"], 1),
                    round(angles["pinky_dip"], 1)
                )

                print(
                    "PINKY POSITION:",
                    round(pinky_mcp.x, 3),
                    round(pinky_mcp.y, 3)
                )

                print(
                    "DEBUG MIDDLE:",
                    round(angles["middle_mcp"], 1),
                    round(angles["middle_pip"], 1),
                    round(angles["middle_dip"], 1)
                )

                print(
                    "DEBUG RING:",
                    round(angles["ring_mcp"], 1),
                    round(angles["ring_pip"], 1),
                    round(angles["ring_dip"], 1)
                )

                print(
                    "DEBUG THUMB:",
                    round(angles["thumb_mcp"], 1),
                    round(angles["thumb_ip"], 1)
                )

                print(
                    "HAND ANGLE:",
                    round(hand_angle, 1)
                )

                print("-" * 50)


                # ====================================================
                # SERVO TARGETS
                # ====================================================

                servo_targets = calculate_servo_targets(
                    angles,
                    hand_angle,
                    pinky_mcp.x
                )


                # ====================================================
                # DISPLAY
                # ====================================================

                cv2.putText(
                    frame,
                    f"Palm Size: {palm_size:.3f}",
                    (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Hand Angle: {hand_angle:.1f}",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Pinky X: {pinky_mcp.x:.3f}",
                    (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID1: {servo_targets.get(1, 0)}",
                    (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID3: {servo_targets.get(3, 0)}",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID7: {servo_targets.get(7, 0)}",
                    (20, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID11: {servo_targets.get(11, 0)}",
                    (20, 210),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID14: {servo_targets.get(14, 0)}",
                    (20, 240),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"ID15: {servo_targets.get(15, 0)}",
                    (20, 270),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 255),
                    2
                )


                # ====================================================
                # ALL SERVO TARGETS
                # ====================================================

                y_position = 310

                for servo_id in sorted(servo_targets):

                    cv2.putText(
                        frame,
                        f"ID {servo_id}: "
                        f"{servo_targets[servo_id]}",
                        (20, y_position),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.45,
                        (255, 255, 255),
                        1
                    )

                    y_position += 22

                    if y_position > 700:
                        break


                # ====================================================
                # DRAW LANDMARKS
                # ====================================================

                for landmark in hand:

                    x = int(
                        landmark.x *
                        frame.shape[1]
                    )

                    y = int(
                        landmark.y *
                        frame.shape[0]
                    )

                    cv2.circle(
                        frame,
                        (x, y),
                        4,
                        (0, 255, 0),
                        -1
                    )


            # ========================================================
            # SHOW CAMERA
            # ========================================================

            cv2.imshow(
                "Robotic Hand Gesture Control",
                frame
            )


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    cap.release()
    cv2.destroyAllWindows()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()