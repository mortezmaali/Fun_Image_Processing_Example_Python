import cv2
import numpy as np

# ---------------------- USER SETTINGS ----------------------
image_path = 'Einstein.png'  # Replace with your image path
output_video = 'pixel_explosion.mp4'
video_fps = 30
video_duration = 10  # seconds total (including original & final hold)
hold_time = 1  # seconds to show original and final images
explosion_strength = 5  # pixels per frame for outward movement
# -----------------------------------------------------------

# Load image
img = cv2.imread(image_path)
if img is None:
    raise ValueError("Image not found at the specified path!")

height, width = img.shape[:2]

# Prepare video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, video_fps, (width, height))

# Create pixel coordinates grid
ys, xs = np.indices((height, width))
coords = np.stack([xs.flatten(), ys.flatten()], axis=-1)
colors = img.reshape(-1, 3)

# Random directions for explosion
np.random.seed(42)
directions = np.random.randn(*coords.shape).astype(np.float32)
directions /= np.linalg.norm(directions, axis=1, keepdims=True)  # normalize

# Total frames for explosion & reassembly
explosion_frames = video_fps * (video_duration - 2*hold_time) // 2
total_frames = explosion_frames * 2 + 2*video_fps*hold_time

# Create a full-screen window
cv2.namedWindow('Pixel Explosion', cv2.WINDOW_NORMAL)
cv2.setWindowProperty('Pixel Explosion', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# ----------------- Show original image -----------------
for _ in range(video_fps * hold_time):
    cv2.imshow('Pixel Explosion', img)
    if cv2.waitKey(int(1000/video_fps)) & 0xFF == 27:
        break
    out.write(img)

# ----------------- Explosion and Reassembly -----------------
for i in range(explosion_frames*2):
    frame = np.zeros_like(img)

    if i < explosion_frames:
        # Explosion phase
        offset = directions * (i * explosion_strength)
    else:
        # Reassembly phase
        offset = directions * ((2*explosion_frames - i) * explosion_strength)

    new_coords = coords + offset
    new_coords = np.round(new_coords).astype(int)

    # Keep within image bounds
    valid_mask = (new_coords[:,0] >=0) & (new_coords[:,0] < width) & \
                 (new_coords[:,1] >=0) & (new_coords[:,1] < height)
    valid_coords = new_coords[valid_mask]
    valid_colors = colors[valid_mask]

    frame[valid_coords[:,1], valid_coords[:,0]] = valid_colors

    cv2.imshow('Pixel Explosion', frame)
    if cv2.waitKey(int(1000/video_fps)) & 0xFF == 27:
        break
    out.write(frame)

# ----------------- Show reconstructed image -----------------
for _ in range(video_fps * hold_time):
    cv2.imshow('Pixel Explosion', img)
    if cv2.waitKey(int(1000/video_fps)) & 0xFF == 27:
        break
    out.write(img)

out.release()
cv2.destroyAllWindows()
print(f"Video saved as {output_video}")
