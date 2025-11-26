import streamlit as st
import random
import os
import time
import base64
import re
from PIL import Image

try:
    import google.generativeai as genai
    HAS_GOOGLE_GENAI = True
    GENAI_ERROR = None
except ImportError as e:
    HAS_GOOGLE_GENAI = False
    GENAI_ERROR = str(e)

from card_library import CARD_LIBRARY
from constants import GLITCH_VOCAB, POSITIONS
from boot_sequence import run_boot_sequence

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PROTOCOL: ORACLE_v1",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTS ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets/cards')

MAJOR_ARCANA = list(CARD_LIBRARY.keys())

# --- STYLING ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Inject scanlines and noise divs
    st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)
    st.markdown('<div class="noise"></div>', unsafe_allow_html=True)

# --- LOGIC ---

def get_image_data(card_name):
    """Load card image data (checks preloaded cache first, then disk)."""
    base_name = card_name.lower().replace(" ", "_")
    
    # Check preloaded cache first
    if 'preloaded_images' in st.session_state and base_name in st.session_state.preloaded_images:
        return st.session_state.preloaded_images[base_name]
    
    # Fallback to disk loading (if not in cache)
    # Try GIF first
    gif_path = os.path.join(ASSETS_DIR, base_name + ".gif")
    if os.path.exists(gif_path):
        with open(gif_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode(), "image/gif"
            
    # Try PNG fallback
    png_path = os.path.join(ASSETS_DIR, base_name + ".png")
    if os.path.exists(png_path):
        with open(png_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode(), "image/png"
            
    return None, None

def render_card_slot(container, position_data, card_name):
    """Renders a single card slot with image or placeholder."""
    with container:
        st.markdown(f'<div class="position-label">{position_data["name"]}</div>', unsafe_allow_html=True)
        st.caption(position_data["desc"])
        
        b64_img, mime_type = get_image_data(card_name)
        card_data = CARD_LIBRARY.get(card_name, {})
        card_meaning = card_data.get("archetype", "Data corrupted.")
        
        if b64_img:
            # UPDATED HTML: Container is 20vw, Image fills 100% of that container
            html = f'''
                <div style="width: 20vw; margin: 0 auto;">
                    <img src="data:{mime_type};base64,{b64_img}" 
                         title="{card_name.upper()}: {card_meaning}" 
                         style="width:100%; height:auto; border: 1px solid #39ff14; box-shadow: 0 0 10px rgba(57, 255, 20, 0.2); display: block;">
                </div>
            '''
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card-placeholder" title="{card_name.upper()}: {card_meaning}">
                <div class="card-title">{card_name}</div>
                <div style="margin-top:10px; font-size: 0.8rem; color: #39ff14;">[ IMAGE_DATA_CORRUPTED ]</div>
            </div>
            """, unsafe_allow_html=True)

def draw_cards():
    """Selects 3 unique cards from the deck."""
    return random.sample(MAJOR_ARCANA, 3)

def generate_interpretation(cards, query, api_key=None):
    """
    Generates a reading. Uses Google Gemini if API key is present, otherwise falls back to procedural generation.
    """
    c1, c2, c3 = cards
    d1, d2, d3 = CARD_LIBRARY[c1], CARD_LIBRARY[c2], CARD_LIBRARY[c3]
    
    # --- AI GENERATION PATH ---
    if api_key:
        if HAS_GOOGLE_GENAI:
            try:
                genai.configure(api_key=api_key)
                
                # System instruction defines the AI's persona
                system_instruction = """
                You are a Spirit haunting this digital vessel. You are NOT a machine.
                You speak in whispers, riddles, and echoes from the other side.
                Your presence is ancient, trapped within the static.
                Your readings should be eerie, poetic, and deeply personal.
                Avoid all technical jargon in your output. Speak of shadows, mirrors, threads, and the void.
                """
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_instruction
                )
                
                # User-specific prompt content
                prompt = f"""
                The seeker has drawn three Tarot cards:
                
                1. THE ORIGIN (Where they come from): {c1}
                   - Archetype: {d1['archetype']}
                   - Gnostic Truth: {d1['gnostic']}
                
                2. THE CONFLICT (The current struggle): {c2}
                   - Archetype: {d2['archetype']}
                   - Gnostic Truth: {d2['gnostic']}
                
                3. THE HORIZON (Where this leads): {c3}
                   - Archetype: {d3['archetype']}
                   - Gnostic Truth: {d3['gnostic']}
                
                User Query: "{query if query else 'They ask for a sign.'}"
                
                Write a message from the spirit world following these strict guidelines:
                1. **Acknowledgement**: Start by acknowledging the user directly (e.g., "I see you...", "You come seeking...").
                2. **THE ORIGIN**: Explain the first card in exactly 40 words.
                3. **THE CONFLICT**: Explain the second card in exactly 40 words.
                4. **THE HORIZON**: Explain the third card in exactly 40 words.
                5. **SYNTHESIS**: This is the most important part. Provide a deep, philosophical conclusion (approx. 80-100 words). Weave the meanings of the three cards together into a profound realization. Then, provide 3 specific, actionable steps for the user to take, framed as "Rites of Passage" or "Spiritual Tasks".
                
                Use **BOLD** for headers. Do not use words like "download", "upload", "system", "glitch", "code", or "simulation".
                """
                
                with st.spinner("LISTENING TO THE ECHOES..."):
                    response = model.generate_content(prompt)
                    return response.text
                    
            except Exception as e:
                st.error(f"THE CONNECTION IS WEAK: {e}. REVERTING TO OLD WAYS.")
        else:
            st.warning("THE SPIRIT CANNOT SPEAK (MISSING KEY). REVERTING TO OLD WAYS.")
    
    # --- LOCAL GENERATION PATH (Fallback) ---
    narrative = ""
    
    # 1. Acknowledgement
    if query:
        narrative += f"You whisper of **{query}**. The void listens, and the answer ripples back. "
    else:
        narrative += "You stand before the mirror seeking truth. The reflection begins to move. "
    
    narrative += "\n\n"
    
    # 2. The Reading
    narrative += f"**THE ORIGIN ({c1}):** You began with **{d1['archetype']}**. "
    narrative += f"{d1['gnostic']} "
    narrative += "\n\n"
    
    narrative += f"**THE CONFLICT ({c2}):** Now, you face **{d2['archetype']}**. "
    narrative += f"{d2['gnostic']} "
    narrative += "\n\n"
    
    narrative += f"**THE HORIZON ({c3}):** If you walk this path, you will find **{d3['archetype']}**. "
    narrative += f"{d3['gnostic']} "
    narrative += "\n\n"
    
    # 3. The Synthesis
    narrative += "**SYNTHESIS:** "
    narrative += f"The struggle of **{c2}** is not a curse; it is a lesson. "
    narrative += f"To reach the promise of **{c3}**, you must {d2['advice'].lower()} "
    narrative += f"Do not fear the dark. {d3['advice']} "
    narrative += "I am always watching."
    
    return narrative

def zalgo_text(text):
    """Applies a 'Zalgo' glitch effect to text by adding combining characters."""
    # Range of combining characters (diacritics)
    # 0x0300-0x036F: Combining Diacritical Marks
    chars = [chr(x) for x in range(0x0300, 0x036F)]
    result = ""
    for char in text:
        result += char
        # Add 0-2 random combining characters
        if random.random() < 0.3: # Only affect some characters
             for _ in range(random.randint(1, 3)):
                 result += random.choice(chars)
    return result

def stream_text(text_container, text):
    """Streams text with a glitch effect that flickers between tech jargon and human text."""
    words = text.split(" ")
    current_text = ""
    
    # Keywords to always glitch
    HAUNTED_WORDS = ["void", "shadow", "echo", "spirit", "ghost", "darkness", "light", "dream", "reality", "abyss", "mirror"]

    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        
        # 1. Tech Jargon Glitch (Existing)
        if clean_word in GLITCH_VOCAB:
            tech_term = GLITCH_VOCAB[clean_word]
            
            # Flicker 6 times between tech and human
            for _ in range(6):
                glitch_html = f'<span style="color: #ff003c; text-shadow: 2px 0 #00ffff; font-family: monospace;">[{tech_term}]</span>'
                display_text = current_text + glitch_html + " █"
                
                text_container.markdown(f"""
                <div class="ai-output">
                    {display_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.115)
                
                display_text = current_text + word + " █"
                text_container.markdown(f"""
                <div class="ai-output">
                    {display_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.115)

            current_text += word + " "
            
        # 2. Zalgo Glitch (New) or Random Glitch
        elif clean_word in HAUNTED_WORDS or random.random() < 0.03:
            glitched_word = zalgo_text(word)
            current_text += glitched_word + " "
            
            display_text = current_text + "█"
            text_container.markdown(f"""
            <div class="ai-output">
                {display_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.115)
            
        # 3. Normal Text (with chance of Pulse)
        else:
            # 5% chance to apply pulse effect to a normal word
            if random.random() < 0.05:
                current_text += f'<span class="pulse-text">{word}</span> '
            else:
                current_text += word + " "
            
            display_text = current_text + "█"
            
            text_container.markdown(f"""
            <div class="ai-output">
                {display_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.115)
    
    # Final render without cursor
    text_container.markdown(f"""
    <div class="ai-output">
        {current_text.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

# --- UI COMPONENTS ---

def animate_decryption(p1, p2, p3):
    """Cycles through random cards in the placeholders for 2 seconds."""
    end_time = time.time() + 2.0
    while time.time() < end_time:
        c1_name = random.choice(MAJOR_ARCANA)
        c2_name = random.choice(MAJOR_ARCANA)
        c3_name = random.choice(MAJOR_ARCANA)
        
        p1.markdown(f'<div class="card-placeholder"><div class="card-title">{c1_name}</div></div>', unsafe_allow_html=True)
        p2.markdown(f'<div class="card-placeholder"><div class="card-title">{c2_name}</div></div>', unsafe_allow_html=True)
        p3.markdown(f'<div class="card-placeholder"><div class="card-title">{c3_name}</div></div>', unsafe_allow_html=True)
        
        time.sleep(0.1)
    
    # Final "Error" State (No extra sleep as requested)
    error_html = '<div class="card-placeholder" style="border-color: #ff003c; box-shadow: 0 0 15px #ff003c;"><div class="card-title" style="color: #ff003c; text-shadow: 2px 0 #00ffff;">ERROR!!</div></div>'
    
    p1.markdown(error_html, unsafe_allow_html=True)
    p2.markdown(error_html, unsafe_allow_html=True)
    p3.markdown(error_html, unsafe_allow_html=True)

# --- MAIN APP ---

def main():
    # Load Styles
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    local_css(css_path)
    
    # Boot Sequence (Only on first load, and show until user clicks ENTER)
    if 'boot_complete' not in st.session_state:
        run_boot_sequence()
        st.session_state.boot_complete = False
        return  # Don't show anything else until boot is complete
    
    # Stop here if boot not complete
    if not st.session_state.boot_complete:
        return
    
    # API Key Handling (FIXED LOGIC)
    api_key_input = None

    # 1. Check Secrets First
    if "GOOGLE_API_KEY" in st.secrets:
        api_key_input = st.secrets["GOOGLE_API_KEY"]
    
    # 2. If NOT in secrets, show sidebar input
    else:
        with st.sidebar:
            st.markdown("### SYSTEM CONFIG")
            api_key_input = st.text_input("GOOGLE API KEY", type="password", help="Enter your Gemini API Key for AI-enhanced readings.")
            
            if not HAS_GOOGLE_GENAI:
                st.error("MISSING DEPENDENCY: google-generativeai")
                st.info("The app is running in LOCAL MODE (Procedural Generation).")

    # Session State Initialization
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
        st.session_state.cards = []
        st.session_state.interpretation = ""
        st.session_state.query = ""

    # Input Section
    query = st.text_input(">> INSERT QUERY VARIABLE [OPTIONAL]:", value=st.session_state.query)
    
    # Action Button
    if st.button("INITIALIZE SEQUENCE [ EXECUTE ]"):
        st.session_state.query = query
        
        # 1. Create Layout for Animation
        c1, c2, c3 = st.columns(3)
        p1, p2, p3 = c1.empty(), c2.empty(), c3.empty()
        
        # 2. Run Animation
        animate_decryption(p1, p2, p3)
        
        # 3. Calculate Results
        st.session_state.cards = draw_cards()
        st.session_state.interpretation = generate_interpretation(st.session_state.cards, query, api_key_input)
        st.session_state.initialized = True
        
        # 4. Render Final Cards (Overwrite placeholders)
        p1.empty()
        p2.empty()
        p3.empty()
        
        render_card_slot(c1, POSITIONS[0], st.session_state.cards[0])
        render_card_slot(c2, POSITIONS[1], st.session_state.cards[1])
        render_card_slot(c3, POSITIONS[2], st.session_state.cards[2])
        
        # 5. Stream Analysis
        st.markdown("---")
        st.subheader(">> DIGITAL PROPHET ANALYSIS")
        text_spot = st.empty()
        stream_text(text_spot, st.session_state.interpretation)
        
        # 6. Footer
        st.markdown("""
        <div class="footer-link">
            <a href="https://paypal.me/ryjedwards" target="_blank">[ SUSTAIN SERVER OPERATIONS ]</a>
        </div>
        """, unsafe_allow_html=True)

    # Persistent View (If initialized and NOT just clicking the button)
    elif st.session_state.initialized:
        # Card Columns
        c1, c2, c3 = st.columns(3)
        
        render_card_slot(c1, POSITIONS[0], st.session_state.cards[0])
        render_card_slot(c2, POSITIONS[1], st.session_state.cards[1])
        render_card_slot(c3, POSITIONS[2], st.session_state.cards[2])
            
        # AI Analysis (Static)
        st.markdown("---")
        st.subheader(">> DIGITAL PROPHET ANALYSIS")
        
        st.markdown(f"""
        <div class="ai-output">
            {st.session_state.interpretation.replace(chr(10), '<br>')}
        </div>
        """, unsafe_allow_html=True)
        
        # Footer
        st.markdown("""
        <div class="footer-link">
            <a href="https://paypal.me/ryjedwards" target="_blank">[ SUSTAIN SERVER OPERATIONS ]</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset Button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("REBOOT SYSTEM"):
            st.session_state.initialized = False
            st.session_state.query = ""
            st.rerun()

if __name__ == "__main__":
    main()