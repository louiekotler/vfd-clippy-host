import time
import atexit
import sys
import serial
import serial.tools.list_ports
from AppKit import NSPasteboard

USB_PRODUCT_NAME = "VFD Clippy"
BAUDRATE = 115200

ser = None


def find_arduino_port(product_name=USB_PRODUCT_NAME):
    """Search connected USB devices for the Arduino by product name."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.product and product_name in port.product:
            return port.device
    return None


def safe_serial_write(ser, message):
    """Write to serial safely."""
    try:
        # Append newline to string to indicate end of message to receiver
        ser.write(message.encode("utf-8") + b"\n")
    except serial.SerialException:
        return False
    return True


def send_to_arduino(message, max_retries=2):
    """Attempt to send a message, retrying if the serial port is disconnected."""
    global ser
    for attempt in range(max_retries):
        # If serial is not connected, try to reconnect
        if not ser or not ser.is_open:
            port_name = find_arduino_port()
            if port_name:
                try:
                    ser = serial.Serial(port_name, BAUDRATE, timeout=1)
                    print(f"Connected to Arduino at {port_name}")
                except serial.SerialException as e:
                    print("Failed to connect to Arduino:", e)
                    ser = None
            else:
                print("Arduino not found, retrying...")
                time.sleep(0.5)
                continue

        # Try sending
        if ser and ser.is_open:
            if safe_serial_write(ser, message):
                return True
            else:
                print("Serial write failed, closing port.")
                ser.close()
                ser = None
                time.sleep(0.2)
    return False


def cleanup():
    """Close serial port on exit."""
    global ser
    if ser and ser.is_open:
        ser.close()
        print("Serial port closed.")


def watch_clipboard():
    pb = NSPasteboard.generalPasteboard()
    last_change = pb.changeCount()

    atexit.register(cleanup)

    print("Watching clipboard…")
    while True:
        try:
            time.sleep(0.2)
            new_change = pb.changeCount()
            if new_change != last_change:
                last_change = new_change
                content = pb.stringForType_("public.utf8-plain-text")
                if content:
                    # Strip all newline characters from clipboard
                    content_sanitized = content.replace("\r", "").replace("\n", "")[
                        :245
                    ]
                    print("Clipboard changed:", content_sanitized)

                    if not send_to_arduino(content_sanitized):
                        print("Failed to send clipboard data after retries.")

        except KeyboardInterrupt:
            print("Exiting…")
            cleanup()
            sys.exit(0)
        except Exception as e:
            print("Error:", e)
            if ser and ser.is_open:
                ser.close()
                ser = None


if __name__ == "__main__":
    watch_clipboard()
