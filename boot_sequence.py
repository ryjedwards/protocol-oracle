import streamlit as st
import random
import time
import os
import base64

# --- CONFIGURATION & CONSTANTS ---
# Ensure your boot_logo.gif is in the assets folder
BOOT_LOGO_PATH = os.path.join(os.path.dirname(__file__), 'assets/boot_logo.gif') 

BOOT_LOGS = [
    "MOUNTING ASTRAL DRIVES...",
    "ALLOCATING QUANTUM RAM...",
    "BYPASSING ARCHON FIREWALL...",
    "CALIBRATING SPIRIT BOX...",
    "PINGING THE VOID... [RESPONSE RECEIVED]",
    "DECRYPTING ARCANA...",
    "LOADING DAEMON THREADS...",
    "SYNCHRONIZING WITH LOCAL TIME...",
]

# --- UTILITY FUNCTIONS ---

@st.cache_data(show_spinner=False)
def load_boot_logo():
    """Caches the generated boot logo GIF for quick access."""
    try:
        with open(BOOT_LOGO_PATH, "rb") as f:
            data = f.read()
            b64_data = base64.b64encode(data).decode()
            return f"data:image/gif;base64,{b64_data}"
    except FileNotFoundError:
        return None

def render_ascii_art(container):
    """Renders the cached animated logo, wrapped in a dynamic container."""
    b64_img_src = load_boot_logo()
    
    if b64_img_src:
        # Applies .boot-logo-container for the channel shift effect
        container.markdown(f"""
        <div class="boot-logo-container" style="display: flex; justify-content: center;">
            <img src="{b64_img_src}" alt="PROTOCOL ORACLE Logo" style="width: 80%; height: auto; image-rendering: pixelated;"/>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Fallback if image generation failed
        container.text("PROTOCOL: ORACLE_v1 [IMAGE ERROR]") 

def render_hex_dump(container, lines=8):
    """Simulates a memory dump waterfall."""
    hex_chars = "0123456789ABCDEF"
    font_style = "font-family: 'Courier New', monospace; font-size: 12px; line-height: 14px;"
    
    for _ in range(lines):
        row = " ".join("".join(random.choices(hex_chars, k=2)) for _ in range(8))
        address = "0x" + "".join(random.choices(hex_chars, k=8))
        color = "#39ff14" if random.random() > 0.1 else "#ff003c"
        
        container.markdown(
            f"<div style='{font_style} color: {color}; opacity: 0.8;'>{address}  {row}  ...</div>", 
            unsafe_allow_html=True
        )
        time.sleep(0.03)
    container.empty()

def render_final_state(container):
    """Draws the static 'System Ready' screen, applying neon and flicker effects."""
    # FIX: Use 'with container.container()' to ensure all elements are scoped to the passed container.
    # AND pass the container context (st) to render_ascii_art so it draws INSIDE this container.
    with container.container():
        render_ascii_art(st) # 'st' here refers to the container context because of the 'with' block
        
        # Apply flicker to horizontal rules
        st.markdown("<div class='flicker-text'>---</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        
        # Apply flicker to system stats
        c1.markdown("""
        <div class="flicker-text" style="font-family: monospace; font-size: 0.8rem; color: #555;">
        <b>CPU:</b> NEURAL_X9 [64 CORE]<br>
        <b>RAM:</b> AKASHIC_BUFFER
        </div>
        """, unsafe_allow_html=True)
        
        c2.markdown("""
        <div class="flicker-text" style="font-family: monospace; font-size: 0.8rem; color: #555;">
        <b>OS:</b> GNOSIS_LINUX<br>
        <b>STATUS:</b> <span style='color:#39ff14'>ONLINE</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div class='flicker-text'>---</div>", unsafe_allow_html=True)
        
        # Apply neon-glow to the final message
        st.markdown("<div class='neon-glow' style='text-align:center; color:#39ff14; margin-top: 20px; animation: blink 2s infinite;'>SYSTEM_READY. AWAITING UPLINK.</div>", unsafe_allow_html=True)

def complete_boot():
    """Callback to set state before rerun."""
    st.session_state.boot_complete = True

# --- MAIN SEQUENCE ---

def run_boot_sequence():
    if st.session_state.get('boot_complete', False):
        return

    st.markdown("<br>", unsafe_allow_html=True)
    console = st.empty()
    
    if 'boot_animation_done' not in st.session_state:
        # 1. ANIMATION PATH
        with console.container():
            st.markdown("<div style='font-family: monospace; color: #39ff14;'>INIT_MEM_DUMP...</div>", unsafe_allow_html=True)
            dump_area = st.empty()
            render_hex_dump(dump_area, lines=8)
            
            render_ascii_art(st) 
            time.sleep(0.3)
            
            log_container = st.empty()
            logs_html = ""
            for msg in BOOT_LOGS:
                # Apply flicker to individual log entries during the stream
                logs_html += f"<div class='flicker-text' style='color:#39ff14; font-family: monospace; font-size: 14px;'>[OK] {msg}</div>"
                log_container.markdown(logs_html, unsafe_allow_html=True)
                time.sleep(random.uniform(0.05, 0.15))
            
            time.sleep(0.5)
            log_container.empty()
        
        st.session_state.boot_animation_done = True
        
        # Clear animation container and render the final clean state
        console.empty()
        render_final_state(console)
        
    else:
        # 2. STATIC PATH
        render_final_state(console)

    # --- BUTTON LOGIC ---
    button_spot = st.empty()
    if not st.session_state.get('boot_complete', False):
        with button_spot:
             st.button(" >>  ESTABLISH UPLINK  << ", 
                     key="boot_btn", 
                     on_click=complete_boot,
                     use_container_width=True)

    st.markdown("""
    <style>
    @keyframes blink {
        0% { opacity: 0.3; }
        50% { opacity: 1; }
        100% { opacity: 0.3; }
    }
    </style>
    """, unsafe_allow_html=True)