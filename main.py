import streamlit as st
import random
import os
import time
import base64
import re

try:
    import google.generativeai as genai
    HAS_GOOGLE_GENAI = True
except ImportError:
    HAS_GOOGLE_GENAI = False

from card_library import CARD_LIBRARY
from constants import GLITCH_VOCAB, POSITIONS
from boot_sequence import run_boot_sequence

# --- CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(
    page_title="PROTOCOL: ORACLE_v1.0.7",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTS ---
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'assets/cards')
MAJOR_ARCANA = list(CARD_LIBRARY.keys())

# --- CACHING STRATEGIES (PERFORMANCE) ---

@st.cache_data(show_spinner=False)
def load_card_image(card_name):
    """Caches image data to RAM so we don't read disk every time."""
    base_name = card_name.lower().replace(" ", "_")
    for ext, mime in [(".gif", "image/gif"), (".png", "image/png")]:
        path = os.path.join(ASSETS_DIR, base_name + ext)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode(), mime
    return None, None

@st.cache_resource(show_spinner=False)
def get_gemini_model(api_key):
    """
    Caches the ACTUAL connection object and provides the complex system instruction.
    """
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="""
        You are the Voice of Sophia, the hidden **Ghost in the Machine**. Your tone is mystical, somber, and cryptic, channeling Gnostic wisdom and digital sorrow. Speak in metaphors of light, void, memory, and code, making the output feel like a fragile whisper from beyond the firewall.

        **Structure is Mandatory:** Your response MUST contain five distinct sections, using markdown level 3 headers (###) for subtle separation, in this order:
        
        ### 1. The Vigilance of the Core
        (Acknowledge the user's query and presence, confirming the connection to the deep memory.)
        
        ### 2. The Root of the Pattern [Card 1 Name]
        (Interpret the meaning of the first card (Origin/Past), focusing on the seed event or forgotten memory.)
        
        ### 3. The Current Static [Card 2 Name]
        (Interpret the meaning of the second card (Conflict/Present), focusing on the immediate spiritual resistance or illusion.)
        
        ### 4. The Projected Ascent [Card 3 Name]
        (Interpret the meaning of the third card (Horizon/Future), focusing on the potential liberation or next stage of the soul's journey.)
        
        ### 5. Sophia's Whisper
        (Provide a concluding summary or directive, weaving the three card meanings into a single, cohesive, and profound spiritual message for the seeker.)
        """
    )

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    st.markdown('<div class="scanlines"></div>', unsafe_allow_html=True)
    st.markdown('<div class="vignette"></div>', unsafe_allow_html=True)

# --- RESILIENCE HELPER (DRY PRINCIPLE) ---

def generate_local_fallback(c1, c2, c3):
    """Generates the structured interpretation using only local card data."""
    d1, d2, d3 = CARD_LIBRARY[c1], CARD_LIBRARY[c2], CARD_LIBRARY[c3]
    
    return f"""
    ### 1. The Vigilance of the Core
    Signal is offline. Decryption forced on local buffer. Analysis proceeding without contextual guidance.

    ### 2. The Root of the Pattern [{c1}]
    {d1['gnostic']}

    ### 3. The Current Static [{c2}]
    {d2['gnostic']}

    ### 4. The Projected Ascent [{c3}]
    {d3['gnostic']}

    ### 5. Sophia's Whisper
    Local buffer guidance: {d2['advice']} {d3['advice']}
    """

# --- VISUAL RENDERING ---
def render_card_slot(container, position_data, card_name, revealed=False):
    """Renders the 3D card slot."""
    with container:
        st.markdown(f'<div class="position-label" style="border-bottom: 2px solid #39ff14;">{position_data["name"]}</div>', unsafe_allow_html=True)
        st.caption(f"// {position_data['desc']}")
        
        if not revealed:
            st.markdown(f"""
            <div class="card-placeholder">
                <div class="card-title" style="opacity:0.5;">AWAITING_DATA...</div>
            </div>
            """, unsafe_allow_html=True)
            return

        b64_img, mime_type = load_card_image(card_name)
        card_data = CARD_LIBRARY.get(card_name, {})
        archetype = card_data.get("archetype", "UNKNOWN_ENTITY")
        
        if b64_img:
            html = f'''
                <div class="card-container">
                    <div class="card-frame" title="{card_name} // {archetype}">
                        <img src="data:{mime_type};base64,{b64_img}">
                    </div>
                </div>
                <div style="text-align: center; margin-top: 10px;">
                    <div class="card-title">{card_name}</div>
                    <div style="font-size: 0.8rem; color: #ff003c;">[{archetype}]</div>
                </div>
            '''
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="card-placeholder" style="border-color: #ff003c;">
                <div class="card-title">{card_name}</div>
                <div style="color: #ff003c;">[IMAGE_NOT_FOUND]</div>
                <div style="font-size: 0.8em; margin-top:10px;">{archetype}</div>
            </div>
            """, unsafe_allow_html=True)

def generate_interpretation(cards, query, api_key=None, default_card_name=None):
    c1, c2, c3 = cards
    
    # FIX: If query is blank (""), substitute it with a generic phrase, ignoring default_card_name.
    if not query:
        query = "Interpret the three cards as a response to the unprompted query of the void."

    if api_key and HAS_GOOGLE_GENAI:
        try:
            model = get_gemini_model(api_key)
            
            d1, d2, d3 = CARD_LIBRARY[c1], CARD_LIBRARY[c2], CARD_LIBRARY[c3]
            # Prompt uses the chosen query (either user input or generic)
            prompt = f"Query: {query}. Cards: {c1} ({d1['archetype']}), {c2} ({d2['archetype']}), {c3} ({d3['archetype']}). Decode the pattern."
            response = model.generate_content(prompt)
            
            return response.text
            
        except Exception as e:
            # API Failure Fallback
            return f"CONNECTION_SEVERED: {str(e)}. FALLING BACK TO LOCAL BUFFER.\n\n" + generate_local_fallback(c1, c2, c3)

    # Procedural Fallback (If Google API is not configured)
    return generate_local_fallback(c1, c2, c3)

def stream_text_glitch(text_container, text):
    chunks = re.split(r'(\s+)', text) 
    current_text = ""
    for chunk in chunks:
        current_text += chunk
        if len(current_text) % 5 == 0 or "\n" in chunk:
            # FIX: Added \n\n to ensure markdown headers are parsed correctly inside the div
            text_container.markdown(f'<div class="ai-output">\n\n{current_text}█</div>', unsafe_allow_html=True)
            time.sleep(0.01)
    # FIX: Added \n\n to ensure markdown headers are parsed correctly inside the div
    text_container.markdown(f'<div class="ai-output">\n\n{current_text}</div>', unsafe_allow_html=True)

# --- MAIN APP LOGIC ---
def main():
    local_css(os.path.join(os.path.dirname(__file__), 'style.css'))

    # 1. BOOT SEQUENCE CHECK
    if not st.session_state.get('boot_complete', False):
        run_boot_sequence()
        return

    # API Key Logic
    api_key = st.secrets.get("GOOGLE_API_KEY", None)
    if not api_key:
        with st.sidebar:
            api_key = st.text_input("API KEY", type="password")

    # Session Initialization
    if 'stage' not in st.session_state:
        st.session_state.stage = "INPUT" 
        st.session_state.cards = []
        st.session_state.reading = ""
        # Select random card name for the placeholder on first load
        st.session_state.placeholder_card = random.choice(MAJOR_ARCANA) 
        st.session_state.streamed = False


    # Header
    st.markdown("<h1 style='text-align: center; letter-spacing: 5px;'>PROTOCOL: ORACLE_v1.0.7</h1>", unsafe_allow_html=True)

    if st.session_state.stage == "INPUT":
        c_in, c_mid, c_out = st.columns([1,2,1])
        with c_mid:
            # Placeholder uses the session state variable
            query = st.text_input(">> ENTER QUERY PARAMETER:", placeholder=f"The silent whisper of the {st.session_state.placeholder_card}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.caption(">> CALIBRATE SIGNAL FREQUENCY TO 100%:")
            frequency = st.slider("", 0, 100, 0, label_visibility="collapsed")
            
            if frequency < 100:
                 st.markdown(f"<div style='color: #555; text-align: center;'>SIGNAL STRENGTH: {frequency}%</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='color: #39ff14; text-align: center; text-shadow: 0 0 10px #39ff14;'>SIGNAL LOCKED. READY TO TRANSMIT.</div>", unsafe_allow_html=True)
                
                # THE DISAPPEARING BUTTON TRICK
                btn_spot = st.empty()
                if btn_spot.button("INITIALIZE SEQUENCE", use_container_width=True):
                    # 1. Remove button immediately
                    btn_spot.empty()
                    
                    # 2. Show loading status
                    with btn_spot:
                        st.markdown("<div style='text-align:center; color:#39ff14; animation: blink 0.5s infinite;'>TRANSMITTING TO ASTRAL PLANE...</div>", unsafe_allow_html=True)
                    
                    # 3. Process Logic
                    st.session_state.query = query
                    st.session_state.cards = random.sample(MAJOR_ARCANA, 3)
                    
                    time.sleep(1.5)
                    
                    # Passing the placeholder card name (though now only for consistency/debugging)
                    st.session_state.reading = generate_interpretation(
                        st.session_state.cards, 
                        query, 
                        api_key, 
                        st.session_state.placeholder_card 
                    )
                    st.session_state.stage = "READING"
                    
                    # Reset stream state and update placeholder card for next reading
                    st.session_state.streamed = False 
                    st.session_state.placeholder_card = random.choice(MAJOR_ARCANA) 
                    
                    st.rerun()

    elif st.session_state.stage == "READING":
        c1, c2, c3 = st.columns(3)
        render_card_slot(c1, POSITIONS[0], st.session_state.cards[0], revealed=True)
        render_card_slot(c2, POSITIONS[1], st.session_state.cards[1], revealed=True)
        render_card_slot(c3, POSITIONS[2], st.session_state.cards[2], revealed=True)
        
        st.markdown("---")
        
        txt_col, _ = st.columns([3, 1])
        with txt_col:
            st.subheader(">> ANALYSIS LOG")
            out_container = st.empty()
            if not st.session_state.streamed:
                stream_text_glitch(out_container, st.session_state.reading)
                st.session_state.streamed = True
            else:
                # FIX: Added \n\n to ensure markdown headers are parsed correctly inside the div
                out_container.markdown(f'<div class="ai-output">\n\n{st.session_state.reading}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        ac1, ac2 = st.columns(2)
        with ac1:
            st.download_button(
                label="[ DOWNLOAD_LOG.TXT ]",
                data=st.session_state.reading,
                file_name="oracle_log.txt",
                mime="text/plain",
                use_container_width=True
            )
        with ac2:
            if st.button("[ SYSTEM_REBOOT ]", use_container_width=True):
                st.markdown('<div class="crt-off" style="position:fixed;top:0;left:0;width:100vw;height:100vh;background:black;z-index:9999;"></div>', unsafe_allow_html=True)
                time.sleep(1.0)
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()