
from machine import Pin
import time

# Configure the GPIO pin.  For example, GPIO pin 2.
# Change this number to the actual pin you want to use.
data_pin = Pin(2, Pin.IN)  # Set pin 2 as an input

# Optional:  Set up a pull-up or pull-down resistor if needed.
# This helps to ensure a stable reading if your input signal is not actively driven.
#
# To enable pull-up resistor:
# data_pin = Pin(2, Pin.IN, Pin.PULL_UP)
#
# To enable pull-down resistor:
# data_pin = Pin(2, Pin.IN, Pin.PULL_DOWN)
#
# If your sensor/device actively drives the pin HIGH or LOW, you don't need a pull resistor.

def main():
    """
    Reads and prints the digital value of the GPIO pin in a loop.
    """
    print("Starting digital read loop. Press Ctrl+C to stop.")
    try:
        while True:
            # Read the digital value from the pin (0 or 1).
            digital_value = data_pin.value()

            # Print the value.
            print("Digital value:", digital_value)

            # Wait a short time before reading again.  Adjust as needed.
            time.sleep(0.5)  # Wait 0.5 seconds (500 milliseconds)

    except KeyboardInterrupt:
        # This block will be executed when Ctrl+C is pressed.
        print("Program stopped by User.")
    finally:
        #This block is optional.  You might use it to turn off a device,
        #or reset a pin, if needed.  For simple digital reading, it's
        #often not necessary.
        print("Finished.")

if __name__ == "__main__":
    main()
