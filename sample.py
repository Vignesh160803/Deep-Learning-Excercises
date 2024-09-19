import socket
import time
import os
from subprocess import call

# Define the SSID and password of the ESP32-CAM access point
ssid = "ESP32_CAM_AP"
password = "12345678"

# Define the folder where images will be saved
save_folder = "/home/pi/captured_images"

# Ensure the folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Connect to the ESP32-CAM access point
def connect_to_wifi():
    print("Connecting to ESP32-CAM AP...")
    call(["sudo", "nmcli", "d", "wifi", "connect", ssid, "password", password])
    print("Connected to ESP32-CAM AP")

def receive_image():
    host = "192.168.4.1"  # ESP32-CAM's IP
    port = 80
    
    while True:
        try:
            # Create socket and connect to ESP32-CAM server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            print("Connected to ESP32-CAM")

            # Receive image data
            image_data = b""
            while True:
                chunk = s.recv(1024)
                if not chunk:
                    break
                image_data += chunk

            # Save the image
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            image_path = os.path.join(save_folder, f"image_{timestamp}.jpg")
            with open(image_path, "wb") as f:
                f.write(image_data)

            print(f"Image saved as {image_path}")
            s.close()

        except Exception as e:
            print(f"Error: {e}")
            s.close()

        # Wait for the next image (every 5 seconds)
        time.sleep(5)

if __name__ == "__main__":
    connect_to_wifi()
    receive_image()
