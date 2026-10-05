from calibration import SERVO_CALIBRATION


# ============================================================
# BASIC SETTINGS
# ============================================================

INITIAL_POSITION = 2047
OPEN_ANGLE = 175


# ============================================================
# SEPARATE CLOSED ANGLES
# ============================================================

# ------------------------------------------------------------
# PINKY
# ------------------------------------------------------------

# ID2 = Pinky middle upper
PINKY_ID2_CLOSED = 42

# ID3 = Pinky bottom
PINKY_ID3_CLOSED = 86


# ------------------------------------------------------------
# INDEX
# ------------------------------------------------------------

# ID7 and ID9
INDEX_CLOSED = 52


# ------------------------------------------------------------
# MIDDLE
# ------------------------------------------------------------

# ID10 = Middle middle upper
MIDDLE_ID10_CLOSED = 40

# ID11 = Middle bottom
MIDDLE_ID11_CLOSED = 36


# ------------------------------------------------------------
# RING
# ------------------------------------------------------------

RING_CLOSED = 35


# ------------------------------------------------------------
# THUMB
# ------------------------------------------------------------

# ID13 = Thumb bottom
THUMB_ID13_CLOSED = 100

# ID14 = Thumb middle upper
THUMB_ID14_CLOSED = 37.6


# ============================================================
# CLAMP
# ============================================================

def clamp(value, minimum, maximum):

    return max(
        minimum,
        min(value, maximum)
    )


# ============================================================
# FINGER ANGLE → SERVO POSITION
# ============================================================

def map_finger_angle(
    angle,
    closed_angle,
    goal_position
):

    angle = clamp(
        angle,
        closed_angle,
        OPEN_ANGLE
    )

    if OPEN_ANGLE == closed_angle:

        closing_ratio = 0.0

    else:

        closing_ratio = (
            OPEN_ANGLE - angle
        ) / (
            OPEN_ANGLE - closed_angle
        )

    closing_ratio = clamp(
        closing_ratio,
        0.0,
        1.0
    )

    position = (
        INITIAL_POSITION
        +
        closing_ratio
        * (
            goal_position
            - INITIAL_POSITION
        )
    )

    return int(round(position))


# ============================================================
# ID1 — PINKY SIDEWARD
# ============================================================

def map_pinky_sideward(pinky_x):

    # --------------------------------------------------------
    # ACTUAL LIVE MEASUREMENTS
    # --------------------------------------------------------
    #
    # Open hand:
    # X = 0.683
    # Servo = 2047
    #
    # Pinky moved sideways:
    # X = 0.536
    # Servo = 1220
    #
    # --------------------------------------------------------

    open_x = 0.683

    sideward_x = 0.536

    open_position = INITIAL_POSITION

    sideward_position = (
        SERVO_CALIBRATION[1]["center"]
    )

    # Calculate movement ratio
    ratio = (
        pinky_x - open_x
    ) / (
        sideward_x - open_x
    )

    # Keep inside valid range
    ratio = clamp(
        ratio,
        0.0,
        1.0
    )

    # Convert X movement to servo position
    position = (
        open_position
        +
        ratio
        * (
            sideward_position
            - open_position
        )
    )

    return int(round(position))


# ============================================================
# WHOLE HAND SIDEWARD — ID15
# ============================================================

def map_whole_hand_sideward(hand_angle):

    hand_angle = clamp(
        hand_angle,
        -90,
        90
    )

    right_position = (
        SERVO_CALIBRATION[15]["right"]
    )

    left_position = (
        SERVO_CALIBRATION[15]["left"]
    )

    ratio = (
        hand_angle + 90
    ) / 180

    position = (
        right_position
        +
        ratio
        * (
            left_position
            - right_position
        )
    )

    return int(round(position))


# ============================================================
# MAIN SERVO MAPPING
# ============================================================

def calculate_servo_targets(
    angles,
    hand_angle,
    pinky_x=None
):

    targets = {}


    # ========================================================
    # PINKY
    # ========================================================

    # --------------------------------------------------------
    # ID1 = Pinky sideward
    # --------------------------------------------------------

    if pinky_x is not None:

        targets[1] = map_pinky_sideward(
            pinky_x
        )


    # --------------------------------------------------------
    # ID2 = Pinky middle upper
    # --------------------------------------------------------

    targets[2] = map_finger_angle(
        angles["pinky_pip"],
        PINKY_ID2_CLOSED,
        SERVO_CALIBRATION[2]["center"]
    )


    # --------------------------------------------------------
    # ID3 = Pinky bottom
    # --------------------------------------------------------

    targets[3] = map_finger_angle(
        angles["pinky_pip"],
        PINKY_ID3_CLOSED,
        SERVO_CALIBRATION[3]["center"]
    )


    # ========================================================
    # RING
    # ========================================================

    # --------------------------------------------------------
    # ID4 = Ring middle upper
    # --------------------------------------------------------

    targets[4] = map_finger_angle(
        angles["ring_pip"],
        RING_CLOSED,
        SERVO_CALIBRATION[4]["center"]
    )


    # --------------------------------------------------------
    # ID6 = Ring bottom
    # --------------------------------------------------------

    targets[6] = map_finger_angle(
        angles["ring_dip"],
        RING_CLOSED,
        SERVO_CALIBRATION[6]["center"]
    )


    # ========================================================
    # INDEX
    # ========================================================

    # --------------------------------------------------------
    # ID9 = Index middle upper
    # --------------------------------------------------------

    targets[9] = map_finger_angle(
        angles["index_pip"],
        INDEX_CLOSED,
        SERVO_CALIBRATION[9]["center"]
    )


    # --------------------------------------------------------
    # ID7 = Index bottom
    # --------------------------------------------------------

    targets[7] = map_finger_angle(
        angles["index_pip"],
        INDEX_CLOSED,
        SERVO_CALIBRATION[7]["center"]
    )


    # ========================================================
    # MIDDLE
    # ========================================================

    # --------------------------------------------------------
    # ID10 = Middle middle upper
    # --------------------------------------------------------

    targets[10] = map_finger_angle(
        angles["middle_pip"],
        MIDDLE_ID10_CLOSED,
        SERVO_CALIBRATION[10]["center"]
    )


    # --------------------------------------------------------
    # ID11 = Middle bottom
    # --------------------------------------------------------

    targets[11] = map_finger_angle(
        angles["middle_pip"],
        MIDDLE_ID11_CLOSED,
        SERVO_CALIBRATION[11]["center"]
    )


    # ========================================================
    # THUMB
    # ========================================================

    # --------------------------------------------------------
    # ID13 = Thumb bottom
    # --------------------------------------------------------

    targets[13] = map_finger_angle(
        angles["thumb_ip"],
        THUMB_ID13_CLOSED,
        SERVO_CALIBRATION[13]["center"]
    )


    # --------------------------------------------------------
    # ID14 = Thumb middle upper
    # --------------------------------------------------------

    targets[14] = map_finger_angle(
        angles["thumb_ip"],
        THUMB_ID14_CLOSED,
        SERVO_CALIBRATION[14]["center"]
    )


    # ========================================================
    # WHOLE HAND
    # ========================================================

    # --------------------------------------------------------
    # ID15 = Whole hand sideward
    # --------------------------------------------------------

    targets[15] = map_whole_hand_sideward(
        hand_angle
    )


    # ========================================================
    # NOT MAPPED YET
    # ========================================================

    # ID5  = Ring sideward
    # ID8  = Index sideward
    # ID12 = Thumb sideward middle
    # ID16 = Whole hand front/back


    return targets


# ============================================================
# PRINT RESULTS
# ============================================================

def print_servo_targets(
    title,
    targets
):

    print("\n==========================================")
    print(title)
    print("==========================================")

    for servo_id in sorted(targets):

        print(
            f"ID {servo_id:2d} -> "
            f"Position {targets[servo_id]}"
        )


# ============================================================
# OPEN HAND TEST
# ============================================================

OPEN_HAND = {

    "thumb_mcp": 168,
    "thumb_ip": 175,

    "index_mcp": 170,
    "index_pip": 177,
    "index_dip": 178,

    "middle_mcp": 179,
    "middle_pip": 179,
    "middle_dip": 179,

    "ring_mcp": 173,
    "ring_pip": 174,
    "ring_dip": 176,

    "pinky_mcp": 178,
    "pinky_pip": 176,
    "pinky_dip": 175
}


# ============================================================
# CLOSED / BOTTOM HAND TEST
# ============================================================

CLOSED_HAND = {

    "thumb_mcp": 162,
    "thumb_ip": 37.6,

    "index_mcp": 175,
    "index_pip": 52,
    "index_dip": 163,

    "middle_mcp": 163,
    "middle_pip": 36,
    "middle_dip": 175,

    "ring_mcp": 139,
    "ring_pip": 96,
    "ring_dip": 35,

    "pinky_mcp": 97,
    "pinky_pip": 86,
    "pinky_dip": 157.3
}


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    # Open hand
    open_targets = calculate_servo_targets(
        OPEN_HAND,
        hand_angle=0,
        pinky_x=0.683
    )

    print_servo_targets(
        "OPEN HAND TARGETS",
        open_targets
    )


    # Pinky sideward
    sideward_targets = calculate_servo_targets(
        CLOSED_HAND,
        hand_angle=0,
        pinky_x=0.536
    )

    print_servo_targets(
        "PINKY SIDEWARD TARGETS",
        sideward_targets
    )


    # ========================================================
    # POSITION CHANGES
    # ========================================================

    print("\n==========================================")
    print("POSITION CHANGES")
    print("==========================================")

    all_ids = sorted(
        set(open_targets.keys())
        |
        set(sideward_targets.keys())
    )

    for servo_id in all_ids:

        open_position = open_targets.get(
            servo_id,
            "Not mapped"
        )

        sideward_position = sideward_targets.get(
            servo_id,
            "Not mapped"
        )

        if (
            isinstance(open_position, int)
            and isinstance(sideward_position, int)
        ):

            difference = (
                sideward_position -
                open_position
            )

            print(
                f"ID {servo_id:2d}: "
                f"{open_position} -> "
                f"{sideward_position} "
                f"(change: {difference:+d})"
            )

        else:

            print(
                f"ID {servo_id:2d}: "
                f"{open_position} -> "
                f"{sideward_position}"
            )