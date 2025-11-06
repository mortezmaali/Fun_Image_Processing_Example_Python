import cv2
import numpy as np

# ---------------------- USER SETTINGS ----------------------
image_path = 'pexels-souvenirpixels-417074.jpg'  # Replace with your image path
output_video = 'color_flow.mp4'
video_fps = 30
video_duration = 10  # seconds
hue_shift_speed = 2  # hue change per frame (1-5 is smooth)
# -----------------------------------------------------------

# Load image
img = cv2.imread(image_path)
if img is None:
    raise ValueError("Image not found at the specified path!")

# Convert to float32 for HSV manipulation
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
h, s, v = cv2.split(img_hsv)

# Video writer
height, width = img.shape[:2]
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, video_fps, (width, height))

# Total frames
total_frames = video_fps * video_duration

# Create a resizable window for full-resolution display
cv2.namedWindow('Color Flow', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Color Flow', width, height)

# Animate hue shift and display
for i in range(total_frames):
    # Shift hue
    h_shifted = (h + i * hue_shift_speed) % 180
    hsv_shifted = cv2.merge([h_shifted, s, v])
    bgr_shifted = cv2.cvtColor(hsv_shifted.astype(np.uint8), cv2.COLOR_HSV2BGR)
    
    # Show in full-res window
    cv2.imshow('Color Flow', bgr_shifted)
    if cv2.waitKey(int(1000 / video_fps)) & 0xFF == 27:  # ESC to exit early
        break
    
    # Write to video
    out.write(bgr_shifted)

out.release()
cv2.destroyAllWindows()
print(f"Video saved as {output_video}")
