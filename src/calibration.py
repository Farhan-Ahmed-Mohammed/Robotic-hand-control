# ==========================================
# Robotic Hand Servo Calibration
# ==========================================

# Reference position for each servo
# These values were obtained during your
# individual servo testing/calibration.

SERVO_CALIBRATION = {

    1: {
        "name": "Pinky sideward",
        "center": 1220
    },

    2: {
        "name": "Pinky middle upper",
        "center": 3661
    },

    3: {
        "name": "Pinky bottom",
        "center": 4027
    },

    4: {
        "name": "Ring middle upper",
        "center": 3403
    },

    5: {
        "name": "Ring sideward",
        "left": 2454,
        "right": 2115
    },

    6: {
        "name": "Ring bottom",
        "center": 3370
    },

    7: {
        "name": "Index bottom",
        "center": 922
    },

    8: {
        "name": "Index sideward",
        "right": 2400
    },

    9: {
        "name": "Index middle upper",
        "center": 3471
    },

    10: {
        "name": "Middle middle upper",
        "center": 597
    },

    11: {
        "name": "Middle bottom",
        "center": 1302
    },

    12: {
        "name": "Thumb sideward middle",
        "center": 3851
    },

    13: {
        "name": "Thumb bottom",
        "center": 3756
    },

    14: {
        "name": "Thumb middle upper",
        "center": 922
    },

    15: {
        "name": "Whole hand sideward",
        "left": 2617,
        "right": 1098
    },

    16: {
        "name": "Whole hand front/back",
        "center": 1424
    }
}


# ==========================================
# Print calibration values
# ==========================================

def print_calibration():

    print("\n===== SERVO CALIBRATION =====")

    for servo_id, data in SERVO_CALIBRATION.items():

        print(
            f"ID {servo_id}: "
            f"{data['name']} -> {data}"
        )


# ==========================================
# Get calibration data for one servo
# ==========================================

def get_calibration(servo_id):

    return SERVO_CALIBRATION.get(servo_id)


# ==========================================
# Test this file directly
# ==========================================

if __name__ == "__main__":

    print_calibration()