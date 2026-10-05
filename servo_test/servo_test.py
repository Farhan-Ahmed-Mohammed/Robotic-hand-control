import serial
import time

# -----------------------------
# Serial connection
# -----------------------------
PORT = "COM11"
BAUDRATE = 1000000

ser = serial.Serial(
    port=PORT,
    baudrate=BAUDRATE,
    bytesize=8,
    parity=serial.PARITY_NONE,
    stopbits=1,
    timeout=0.1
)

print("Connected to", PORT)
print("Baud rate:", BAUDRATE)


# -----------------------------
# STS3215 Read Position
# -----------------------------
def read_position(servo_id):

    # Present Position register
    ADDRESS = 56

    # Read instruction
    INSTRUCTION = 0x02

    # Read 2 bytes (position is 2 bytes)
    READ_LENGTH = 2

    # Packet:
    # FF FF | ID | Length | Instruction | Address | Read Length
    packet = bytearray([
        0xFF,
        0xFF,
        servo_id,
        0x04,
        INSTRUCTION,
        ADDRESS,
        READ_LENGTH,
    ])

    # Checksum
    checksum = (~sum(packet[2:])) & 0xFF
    packet.append(checksum)

    print("Sending:", packet.hex(" "))

    ser.reset_input_buffer()
    ser.write(packet)

    time.sleep(0.05)

    response = ser.read(20)

    print("Response:", response.hex(" "))

    if len(response) < 8:
        print("No valid response received.")
        return None

    # Position bytes in the response
    position_low = response[5]
    position_high = response[6]

    position = position_low | (position_high << 8)

    return position


# -----------------------------
# Test Servo ID 1
# -----------------------------
servo_id = 1

position = read_position(servo_id)

if position is not None:
    print("Servo ID:", servo_id)
    print("Current position:", position)

ser.close()
print("Serial connection closed.")