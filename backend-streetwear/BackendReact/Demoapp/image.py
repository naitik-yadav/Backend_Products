from PIL import Image
import base64

image_path = "/home/naitik/Downloads/Nike.jpeg"
image = Image.open(image_path)

image_byte_array = image.tobytes()
base64_image = base64.b64encode(image_byte_array).decode()
print(base64_image)