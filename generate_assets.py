import os
import requests
import time
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageChops
from glitch_this import ImageGlitcher

# --- CONFIGURATION ---
OUTPUT_DIR = "./assets/cards/"
FRAMES = 15             # Frames for the GIF
DURATION = 80           # Faster speed for smooth scanning
GLITCH_LEVEL = 2.0      # Static noise level

# --- RELIABLE SOURCE (Sacred Texts Archive) ---
# This is the gold standard for RWS images. They use 'ar00.jpg' format.
BASE_URL = "https://www.sacred-texts.com/tarot/pkt/img/"

# --- MAPPING (Updated for Sacred Texts) ---
# ar00 = Fool, ar01 = Magician, etc.
RWS_MAP = {
    "THE FOOL": "ar00.jpg", "THE MAGICIAN": "ar01.jpg", "THE HIGH PRIESTESS": "ar02.jpg",
    "THE EMPRESS": "ar03.jpg", "THE EMPEROR": "ar04.jpg", "THE HIEROPHANT": "ar05.jpg",
    "THE LOVERS": "ar06.jpg", "THE CHARIOT": "ar07.jpg", "STRENGTH": "ar08.jpg",
    "THE HERMIT": "ar09.jpg", "WHEEL OF FORTUNE": "ar10.jpg", "JUSTICE": "ar11.jpg",
    "THE HANGED MAN": "ar12.jpg", "DEATH": "ar13.jpg", "TEMPERANCE": "ar14.jpg",
    "THE DEVIL": "ar15.jpg", "THE TOWER": "ar16.jpg", "THE STAR": "ar17.jpg",
    "THE MOON": "ar18.jpg", "THE SUN": "ar19.jpg", "JUDGEMENT": "ar20.jpg",
    "THE WORLD": "ar21.jpg"
}

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_vintage_plate(filename):
    """Fetches the 1909 RWS card image from Sacred Texts."""
    url = BASE_URL + filename
    print(f"   >>> Downloading Archive: {filename}...")
    try:
        # User-Agent helps avoid being blocked by some servers
        headers = {'User-Agent': 'Mozilla/5.0'} 
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"   !!! DOWNLOAD ERROR: {e}")
        # Return a black fallback card so script doesn't crash
        return Image.new('RGB', (300, 500), color='black')

def generate_wireframe_overlay(w, h):
    """Creates the 'PIL Generated' techno-geometry layer."""
    img = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw random green grid lines
    for _ in range(10):
        x = random.randint(0, w)
        draw.line((x, 0, x, h), fill="#003300", width=1)
    
    # Draw random "Targeting" boxes
    for _ in range(5):
        x1 = random.randint(0, w-50)
        y1 = random.randint(0, h-50)
        draw.rectangle((x1, y1, x1+50, y1+50), outline="#39ff14", width=1)
    
    return img

def apply_scanner_effect(image, frame_index, total_frames):
    """Draws a horizontal bright green scanline."""
    w, h = image.size
    draw = ImageDraw.Draw(image)
    
    scan_y = int((h / total_frames) * frame_index)
    
    # Laser line
    draw.line((0, scan_y, w, scan_y), fill="#39ff14", width=3)
    # Trail
    if scan_y > 5:
        draw.line((0, scan_y-5, w, scan_y-5), fill="#005500", width=2)
    
    return image

def process_card_frame(base_img, wireframe_img, frame_idx, card_name):
    """Combines Vintage Card + Wireframe + Scanner + Text"""
    # 1. Resize/Grayscale
    img = ImageOps.grayscale(base_img).convert("RGB")
    img = img.resize((600, 900))
    
    # 2. Blend with Wireframe
    img = ImageChops.add(img, wireframe_img)
    
    # 3. Add Scanner Bar
    img = apply_scanner_effect(img, frame_idx, FRAMES)
    
    # 4. Add Text Label
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 55)
    except:
        font = ImageFont.load_default()
        
    w_text = draw.textlength(card_name, font=font)
    position = ((600 - w_text) / 2, 780)
    
    left, top, right, bottom = draw.textbbox(position, card_name, font=font)
    draw.rectangle((left-15, top-15, right+15, bottom+15), fill="black", outline="#39ff14")
    draw.text(position, card_name, fill="#39ff14", font=font)
    
    return img

def main():
    ensure_dir(OUTPUT_DIR)
    glitcher = ImageGlitcher()
    
    print(f"BOOTING SCANNER PROTOCOL... TARGET: {len(RWS_MAP)} ASSETS.")
    
    for name, filename in RWS_MAP.items():
        save_filename = name.lower().replace(" ", "_") + ".gif"
        save_path = os.path.join(OUTPUT_DIR, save_filename)
        
        if os.path.exists(save_path):
             print(f"[SKIP] {save_filename} exists.")
             continue
             
        print(f"PROCESSING: {name}")
        
        # 1. Fetch Source
        base_img = fetch_vintage_plate(filename)
        
        # 2. Generate Wireframe
        wireframe = generate_wireframe_overlay(600, 900)
        
        # 3. Build & Glitch Frames Individually (Fixes AttributeError)
        final_frames = []
        
        for i in range(FRAMES):
            # Create the raw frame (Scanner + Text + Vintage)
            raw_frame = process_card_frame(base_img, wireframe, i, name)
            
            # Glitch THIS specific frame
            # Note: glitch_image returns an Image object when gif=False
            glitched_frame = glitcher.glitch_image(raw_frame, GLITCH_LEVEL, color_offset=True, gif=False)
            
            final_frames.append(glitched_frame)
        
        # 4. Save the sequence as a GIF
        final_frames[0].save(
            save_path,
            format='GIF',
            append_images=final_frames[1:],
            save_all=True,
            duration=DURATION,
            loop=0
        )
        print(f"   -> COMPILED: {save_filename}")
        
        # Be polite to the server
        time.sleep(0.5)

    print("ALL ASSETS SECURED.")

if __name__ == "__main__":
    main()