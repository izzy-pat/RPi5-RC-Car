# TUNES TURN WHILST GOING FORWARDS FUNCTIONALITY. 
# MULTIPLE KEYS ARE PRESSED SIMULTANEOUSLY TO ACHIEVE FORWARDS + TURN

from gpiozero import DigitalOutputDevice, PWMOutputDevice
import signal
import sys
import keyboard  # For detecting key presses

# GPIO Pins for Motor A (left motor)
IN1 = 24
IN2 = 23
ENA = 25

# GPIO Pins for Motor B (right motor)
IN3 = 5
IN4 = 6
ENB = 13

# Set up GPIO devices for Motor A
motor_a_in1 = DigitalOutputDevice(IN2)
motor_a_in2 = DigitalOutputDevice(IN1)
motor_a_en = PWMOutputDevice(ENA)

# Set up GPIO devices for Motor B
motor_b_in1 = DigitalOutputDevice(IN3)
motor_b_in2 = DigitalOutputDevice(IN4)
motor_b_en = PWMOutputDevice(ENB)

# Base speed for both motors
BASE_SPEED = 0.8
TURN_SPEED = 0.2  # Speed reduction for turning

def set_motors(speed_left, speed_right, direction='forward'):
    """
    Set motor speeds and direction for each motor.
    
    Args:
        speed_left (float): Speed for the left motor (0 to 1).
        speed_right (float): Speed for the right motor (0 to 1).
        direction (str): 'forward' or 'backward'.
    """
    if direction == 'forward':
        motor_a_in1.on()
        motor_a_in2.off()
        motor_b_in1.on()
        motor_b_in2.off()
    elif direction == 'backward':
        motor_a_in1.off()
        motor_a_in2.on()
        motor_b_in1.off()
        motor_b_in2.on()
    else:
        stop_motors()
        return

    motor_a_en.value = speed_left
    motor_b_en.value = speed_right

def stop_motors():
    """Stop both motors."""
    motor_a_in1.off()
    motor_a_in2.off()
    motor_b_in1.off()
    motor_b_in2.off()
    motor_a_en.off()
    motor_b_en.off()

def cleanup():
    """Turn off motors and clean up GPIO."""
    stop_motors()
    print("GPIO cleaned up")

def signal_handler(sig, frame):
    cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print("\n")
print("2WD Robot Control with Simultaneous Movement and Turning")
print("Keys:")
print("  W - forward")
print("  S - backward")
print("  A - turn left")
print("  D - turn right")
print("  Space - stop")
print("  Ctrl+C - exit")
print("\n")

try:
    while True:
        forward = keyboard.is_pressed('w')
        backward = keyboard.is_pressed('s')
        left = keyboard.is_pressed('a')
        right = keyboard.is_pressed('d')

        if forward and right:
            set_motors(TURN_SPEED, BASE_SPEED, 'forward')  # Turn right while moving forward
        elif forward and left:
            set_motors(BASE_SPEED, TURN_SPEED, 'forward')  # Turn left while moving forward
        elif backward and right:
            set_motors(TURN_SPEED, BASE_SPEED, 'backward')  # Turn right while moving backward
        elif backward and left:
            set_motors(BASE_SPEED, TURN_SPEED, 'backward')  # Turn left while moving backward
        elif forward:
            set_motors(BASE_SPEED, BASE_SPEED, 'forward')
        elif backward:
            set_motors(BASE_SPEED, BASE_SPEED, 'backward')
        elif left:
            set_motors(BASE_SPEED, TURN_SPEED, 'forward')  # Default left turn
        elif right:
            set_motors(TURN_SPEED, BASE_SPEED, 'forward')  # Default right turn
        else:
            stop_motors()  # Stop if no keys are pressed

except KeyboardInterrupt:
    print("Exiting...")
    cleanup()
except Exception as e:
    print(f"Error: {e}")
    cleanup()
