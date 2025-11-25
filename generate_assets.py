import os
import requests
import time
import random
from io import BytesIO
from urllib.parse import quote  # <--- The fix for URL errors
from PIL import Image, ImageDraw, ImageFont
from glitch_this import ImageGlitcher

# CONFIGURATION
OUTPUT_DIR = "./assets/cards/"
GLITCH_LEVEL = 3.5
FRAMES = 15
DURATION = 100

# CARD MAPPING
CARD_DATA = {
    "THE FOOL": "cyberpunk silhouette stepping off a digital cliff into the void, neon green wireframe, glitch art",
    "THE MAGICIAN": "hacker wizard controlling floating data streams, holographic sigils, dark room, neon green",
    "THE HIGH PRIESTESS": "digital goddess behind a veil of binary code, mystical, dark, glowing eyes",
    "THE EMPRESS": "mother board circuit tree of life, nature merging with machine, lush digital green",
    "THE EMPEROR": "rigid geometric obsidian throne, authoritarian cyber structure, red and black",
    "THE HIEROPHANT": "robotic priest downloading dogma, connecting cables to followers, ancient cybernetic temple",
    "THE LOVERS": "two digital souls merging code, dna helix made of light, connection, harmony",
    "THE CHARIOT": "futuristic sleek tank vehicle speeding through a data tunnel, aggressive, motion blur",
    "STRENGTH": "woman taming a robotic cyber lion, glowing circuits, calm control",
    "THE HERMIT": "lone hooded figure holding a glowing lantern in a dark server room, isolation",
    "WHEEL OF FORTUNE": "giant mechanical gear wheel spinning destiny, tarot iconography, matrix code",
    "JUSTICE": "blindfolded android holding scales made of laser light, perfect balance, symmetry",
    "THE HANGED MAN": "figure suspended upside down in a web of wires, enlightenment, perspective shift",
    "DEATH": "grim reaper made of black smoke and skulls, end of simulation, reboot",
    "TEMPERANCE": "alchemist mixing two glowing fluids, balance, flow, water and fire",
    "THE DEVIL": "terrifying horned demon made of cables and chains, entrapment, addiction",
    "THE TOWER": "massive skyscraper struck by green lightning, crumbling, digital debris falling",
    "THE STAR": "naked figure pouring starlight into a pool, hope, distant glowing constellation",
    "THE MOON": "giant pale moon with glitch artifacts, wolf howling, illusion, subconscious",
    "THE SUN": "blindingly bright digital sun, joy, clarity, explosive energy, lens flare",
    "JUDGEMENT": "angels blowing trumpets awakening the dead from graves, ascension, final call",
    "THE WORLD": "perfect circle Ouroboros snake eating tail, completion, the universe inside a microchip"
}

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetch_fallback_image(card_name):
    """Fallback: Gets a moody random photo if AI fails"""
    print(f"   [!] ACTIVATING FALLBACK PROTOCOL FOR {card_name}...")
    # Seeded random so it's consistent for that card name
    seed = sum(bytearray(card_name.encode('utf-8')))
    url = f"https://picsum.photos/seed/{seed}/600/900?grayscale"
    try:
        response = requests.get(url, timeout=10)
        return Image.open(BytesIO(response.content))
    except:
        return Image.new('RGB', (600, 900), color='black')

def fetch_ai_image(prompt, card_name):
    """Tries to get AI image, handles 500 errors with retries"""
    # ENCODING FIX: Safely encode the URL string
    base_style = "dark noir cyberpunk style, stark black background, green neon accents, detailed, 8k"
    full_prompt = f"{prompt}, {base_style}"
    safe_prompt = quote(full_prompt) 
    
    url = f"https://image.pollinations.ai/prompt/{safe_prompt}?width=600&height=900&nologo=true"
    
    # RETRY LOOP
    for attempt in range(1, 4):
        try:
            print(f"   >>> Requesting Neural Pattern (Attempt {attempt}/3)...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            elif response.status_code >= 500:
                print(f"   [!] Server Error {response.status_code}. Retrying in 2s...")
                time.sleep(2)
            else:
                print(f"   [!] Client Error {response.status_code}.")
                break # Don't retry 404s
                
        except Exception as e:
            print(f"   [!] Connection Error: {e}")
            time.sleep(1)

    # If we get here, all retries failed. Use Fallback.
    return fetch_fallback_image(card_name)

def add_techno_text(image, text):
    draw = ImageDraw.Draw(image)
    W, H = image.size
    try:
        font = ImageFont.truetype("arial.ttf", 50)
    except:
        font = ImageFont.load_default()

    # Draw Text
    w_text = draw.textlength(text, font=font)
    position = ((W - w_text) / 2, H - 100)
    
    left, top, right, bottom = draw.textbbox(position, text, font=font)
    draw.rectangle((left-10, top-10, right+10, bottom+10), fill="black", outline="#39ff14")
    draw.text(position, text, fill="#39ff14", font=font)
    return image

def main():
    ensure_dir(OUTPUT_DIR)
    glitcher = ImageGlitcher()
    
    print(f"BOOTING ANIMATION PROTOCOL... {len(CARD_DATA)} ASSETS QUEUED.")
    
    for name, prompt in CARD_DATA.items():
        filename = name.lower().replace(" ", "_") + ".gif"
        save_path = os.path.join(OUTPUT_DIR, filename)
        
        if os.path.exists(save_path):
             print(f"[SKIP] {filename} exists.")
             continue

        print(f"PROCESSING: {name}")
        
        # 1. Get Image (With Fallback Protection)
        img = fetch_ai_image(prompt, name)
        
        # 2. Add Label
        img = add_techno_text(img, name)
        
        # 3. Glitch & Animate
        glitched_frames = glitcher.glitch_image(img, GLITCH_LEVEL, color_offset=True, gif=True, frames=FRAMES)
        
        # 4. Save
        glitched_frames[0].save(
            save_path,
            format='GIF',
            append_images=glitched_frames[1:],
            save_all=True,
            duration=DURATION,
            loop=0
        )
        print(f"   -> ANIMATION COMPILED: {filename}")
        
        # Pause to prevent rate limiting
        time.sleep(1.5)

    print("ALL GIFS GENERATED.")

if __name__ == "__main__":
    main()