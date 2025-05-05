
# This MicroPython script reads EEG data from the Upside Down Labs
# Brain BioAmp EXG Pill via I2C on a Raspberry Pi Zero 2 W.
#
# Important:
#    * Ensure your Raspberry Pi Zero 2 W has I2C enabled.
#    * Connect the Brain BioAmp EXG Pill to the Pi's I2C pins (SDA, SCL, 3.3V, GND).
#    * Double-check all wiring before powering on to avoid damage.
#    * This code assumes the default I2C address of the Brain BioAmp EXG Pill (0x68).
#    * You may need to adjust the I2C address if you've changed it on the device.
#    * The Brain BioAmp EXG Pill provides 3 channels of data.
#
# Wiring (Example - verify with your specific setup):
#    Raspberry Pi Zero 2 W  <-----> Brain BioAmp EXG Pill
#    ----------------------      |
#    Pin 3 (GPIO 2, SDA)       -----> SDA
#    Pin 5 (GPIO 3, SCL)       -----> SCL
#    Pin 1 (3.3V)              -----> VCC (3.3V)
#    Pin 9 (GND)               -----> GND
#
# Dependencies:
#    * No external libraries are needed beyond the standard MicroPython 'machine' and 'time' libraries.

from machine import Pin, I2C
import time

# I2C configuration
I2C_SDA_PIN = 2  # GPIO 2 (Pin 3)
I2C_SCL_PIN = 3  # GPIO 3 (Pin 5)
I2C_ADDR = 0x68  # Default I2C address of the Brain BioAmp EXG Pill

# Initialize I2C
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=100000)  # 100kHz


def twos_complement(value, num_bits):
    """
    Convert a signed integer from two's complement representation.

    Args:
        value (int): The integer value to convert.
        num_bits (int): The number of bits used to represent the integer.

    Returns:
        int: The signed integer.
    """
    if (value & (1 << (num_bits - 1))) != 0:
        value = value - (1 << num_bits)
    return value

def read_exg_data():
    """
    Reads EXG data from the Brain BioAmp EXG Pill.

    Returns:
        tuple: A tuple containing three signed integer values representing the
               EXG data from the three channels.  Returns None on error.
    """
    try:
        # Read 9 bytes of data (3 channels, 3 bytes per channel)
        data = i2c.readfrom(I2C_ADDR, 9)

        # Combine the bytes for each channel and convert from two's complement
        # Each channel is represented by 3 bytes (24 bits).
        exg1 = twos_complement((data[0] << 16) | (data[1] << 8) | data[2], 24)
        exg2 = twos_complement((data[3] << 16) | (data[4] << 8) | data[5], 24)
        exg3 = twos_complement((data[6] << 16) | (data[7] << 8) | data[8], 24)

        return exg1, exg2, exg3

    except OSError as e:
        print(f"Error reading from I2C device: {e}")
        return None  # Return None to indicate an error


def main():
    """
    Main function to read and print EXG data.
    """
    print("Reading EXG data from Brain BioAmp EXG Pill...")
    print("Make sure the device is connected and powered on.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            exg_data = read_exg_data()
            if exg_data:
                exg1, exg2, exg3 = exg_data
                print(f"EXG1: {exg1}, EXG2: {exg2}, EXG3: {exg3}")
            else:
                print("Failed to read data. Check connection and I2C address.")
            time.sleep(0.1)  # Adjust the sampling rate as needed

    except KeyboardInterrupt:
        print("\nProgram stopped.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
