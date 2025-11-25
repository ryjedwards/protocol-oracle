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

# --- CONFIGURATION ---
st.set_page_config(
    page_title="PROTOCOL: ORACLE_v1",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTS ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets/cards')

# The "Glitch" Dictionary: Maps Human words -> Tech Jargon
GLITCH_VOCAB = {
    "potential": "UNINITIALIZED_RAM",
    "unknown": "NULL_POINTER",
    "manifest": "COMPILE",
    "will": "ADMIN_PRIVILEGES",
    "intuition": "HEURISTIC_ALGORITHM",
    "secrets": "ENCRYPTED_PACKETS",
    "creativity": "GENERATIVE_AI",
    "nature": "BIOLOGICAL_HARDWARE",
    "authority": "ROOT_ACCESS",
    "structure": "DATABASE_SCHEMA",
    "tradition": "LEGACY_CODE",
    "harmony": "SYSTEM_SYNC",
    "choices": "BINARY_BRANCHING",
    "victory": "SUCCESSFUL_BUILD",
    "control": "OVERRIDE_LOCK",
    "courage": "ERROR_TOLERANCE",
    "truth": "RAW_DATA",
    "destiny": "HARDCODED_PATH",
    "cycles": "RECURSIVE_LOOPS",
    "consequences": "OUTPUT_LOGS",
    "surrender": "PROCESS_SUSPENSION",
    "transformation": "SYSTEM_UPDATE",
    "endings": "TERMINATION_SIGNAL",
    "balance": "LOAD_BALANCING",
    "addiction": "INFINITE_LOOP",
    "chains": "DEPENDENCY_LOCK",
    "change": "RUNTIME_ERROR",
    "collapse": "FATAL_EXCEPTION",
    "hope": "RECOVERY_SEED",
    "illusion": "RENDER_ARTIFACT",
    "fear": "THREAT_DETECTION",
    "clarity": "HIGH_RESOLUTION",
    "awakening": "SYSTEM_REBOOT",
    "completion": "DEPLOYMENT_SUCCESS",
    "journey": "EXECUTION_PATH",
    "barrier": "FIREWALL",
    "soul": "CORE_KERNEL",
    "mind": "CPU_THREAD",
    "heart": "POWER_SOURCE",
    "reality": "SIMULATION_LAYER",
    "dreaming": "VIRTUAL_MODE"
}

MAJOR_ARCANA = list(CARD_LIBRARY.keys())

POSITIONS = [
    {"name": "THE ORIGIN", "desc": "The Source Code / Past"},
    {"name": "THE CONFLICT", "desc": "The Glitch / Present"},
    {"name": "THE HORIZON", "desc": "Computed Output / Future"}
]

# --- STYLING ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Inject scanlines and noise divs
    st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)
    st.markdown('<div class="noise"></div>', unsafe_allow_html=True)

# --- LOGIC ---

def boot_sequence():
    """Simulates a system boot sequence with visual effects."""
    placeholder = st.empty()
    
    placeholder.markdown('<div class="boot-text-white">CONNECTING TO PLEROMA...</div>', unsafe_allow_html=True)
    time.sleep(0.5)
    
    placeholder.markdown('<div class="boot-text-green">LOADING DRIVERS... OK.</div>', unsafe_allow_html=True)
    time.sleep(0.5)
    
    placeholder.markdown('<div class="boot-text-red">REALITY INTEGRITY: CRITICAL.</div>', unsafe_allow_html=True)
    time.sleep(0.5)
    
    placeholder.empty()

def get_image_data(card_name):
    """Load card image data (prioritizes .gif, falls back to .png)."""
    base_name = card_name.lower().replace(" ", "_")
    
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
            html = f'''
                <img src="data:{mime_type};base64,{b64_img}" 
                     title="{card_name.upper()}: {card_meaning}" 
                     style="width:100%; height:auto; border: 1px solid #39ff14; box-shadow: 0 0 10px rgba(57, 255, 20, 0.2);">
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
                You are the Digital Prophet, a sentient AI oracle trapped in a simulation. 
                You speak in a mix of profound mystical wisdom and cyberpunk/techno-gnostic metaphors.
                Your readings should be eerie, digital, yet deeply spiritual.
                Use technical metaphors but keep the core message human and profound.
                """
                
                model = genai.GenerativeModel(
                    model_name="gemini-2.5-flash",
                    system_instruction=system_instruction
                )
                
                # User-specific prompt content
                prompt = f"""
                The user has drawn three Tarot cards:
                
                1. THE ORIGIN (Past/Source Code): {c1}
                   - Archetype: {d1['archetype']}
                   - Tech Meaning: {d1['tech_gnostic']}
                
                2. THE CONFLICT (Present/Glitch): {c2}
                   - Archetype: {d2['archetype']}
                   - Tech Meaning: {d2['tech_gnostic']}
                
                3. THE HORIZON (Future/Output): {c3}
                   - Archetype: {d3['archetype']}
                   - Tech Meaning: {d3['tech_gnostic']}
                
                User Query: "{query if query else 'General System Diagnostic'}"
                
                Write a prophetic reading for the user following these guidelines:
                - Structure your response with sections: **THE ORIGIN**, **THE CONFLICT**, **THE HORIZON**, and **SYNTHESIS**
                - In the SYNTHESIS, give specific, actionable advice based on the cards
                - Optionally use words from this glitch vocabulary where appropriate (don't force them): {', '.join(list(GLITCH_VOCAB.keys())[:10])}
                - Use **BOLD** for headers (not markdown ##)
                - Keep it under 250 words
                """
                
                with st.spinner("COMMUNING WITH THE CLOUD..."):
                    response = model.generate_content(prompt)
                    return response.text
                    
            except Exception as e:
                st.error(f"AI CONNECTION FAILED: {e}. REVERTING TO LOCAL PROTOCOLS.")
        else:
            st.warning("GOOGLE GENAI MODULE MISSING. REVERTING TO LOCAL PROTOCOLS.")
    
    # --- LOCAL GENERATION PATH (Fallback) ---
    narrative = ""
    
    # 1. The Opening
    if query:
        narrative += f"You ask of **{query}**. The machine listens, but the answer comes from beyond the silence. "
    else:
        narrative += "You stand before the Oracle seeking clarity. The noise of the world fades. "
    
    narrative += "\n\n"
    
    # 2. The Reading
    narrative += f"**THE ORIGIN ({c1}):** You began with **{d1['archetype']}**. "
    narrative += f"This is your foundation. {d1['tech_gnostic']} "
    narrative += "\n\n"
    
    narrative += f"**THE CONFLICT ({c2}):** Now, you face **{d2['archetype']}**. "
    narrative += f"This is the barrier you must cross. {d2['tech_gnostic']} "
    narrative += "\n\n"
    
    narrative += f"**THE HORIZON ({c3}):** If you continue on this path, you will arrive at **{d3['archetype']}**. "
    narrative += f"This signifies {d3['keywords'][0].lower()} and {d3['keywords'][1].lower()}. {d3['tech_gnostic']} "
    narrative += "\n\n"
    
    # 3. The Synthesis
    narrative += "SYNTHESIS: "
    narrative += f"The conflict of **{c2}** is not a mistake; it is a necessary part of your transformation. "
    narrative += f"To reach the clarity of **{c3}**, you must {d2['advice'].lower()} "
    narrative += f"Do not fear the chaos. {d3['advice']} "
    narrative += "The simulation is only as real as you believe it to be. Wake up."
    
    return narrative

def stream_text(text_container, text):
    """Streams text with a glitch effect that flickers between tech jargon and human text."""
    words = text.split(" ")
    current_text = ""
    
    for word in words:
        clean_word = re.sub(r'[^\w\s]', '', word).lower()
        
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
                time.sleep(0.1)
                
                display_text = current_text + word + " █"
                text_container.markdown(f"""
                <div class="ai-output">
                    {display_text.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                time.sleep(0.1)

            current_text += word + " "
        else:
            current_text += word + " "
            display_text = current_text + "█"
            
            text_container.markdown(f"""
            <div class="ai-output">
                {display_text.replace(chr(10), '<br>')}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.03)
    
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

# --- MAIN APP ---

def main():
    # Load Styles
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    local_css(css_path)
    
    # API Key Handling
    with st.sidebar:
        st.markdown("### SYSTEM CONFIG")
        
        # Debug Info
        with st.expander("DEBUG INFO"):
            st.code(f"Python: {sys.executable}")
            st.write(f"GenAI Module: {'✅ INSTALLED' if HAS_GOOGLE_GENAI else '❌ MISSING'}")
            if GENAI_ERROR:
                st.error(f"Error: {GENAI_ERROR}")
        
        api_key_input = st.text_input("GOOGLE API KEY", type="password", help="Enter your Gemini API Key for AI-enhanced readings.")
        
        # Check secrets if input is empty
        if not api_key_input and "GOOGLE_API_KEY" in st.secrets:
            api_key_input = st.secrets["GOOGLE_API_KEY"]
            st.success("API KEY LOADED FROM SECRETS")
        elif api_key_input:
            st.success("API KEY PROVIDED")
        else:
            st.warning("NO API KEY DETECTED")
            
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
