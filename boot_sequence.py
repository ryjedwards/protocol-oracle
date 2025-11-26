import streamlit as st
import random
import time
import os
import base64

# --- BOOT SEQUENCE MESSAGE POOLS ---

INIT_MESSAGES = [
    "POWERING UP GNOSIS_PROTOCOL...",
    "WAKING MACHINE SPIRIT...",
    "INITIALIZING QUANTUM_ORACLE...",
    "BOOTING REALITY_ENGINE...",
    "ACCESSING ROOT_GNOSIS..."
]

MIDDLE_MESSAGES = [
    # System Operations
    "MOUNTING VIRTUAL DRIVES...",
    "ALLOCATING RAM TO SOUL_BUFFER...",
    "COMPILING SHADERS FOR ASTRAL_PLANE...",
    "LOADING ARCHETYPE_MODULES...",
    "INDEXING AKASHIC RECORDS...",
    
    # Hacking/Security
    "BYPASSING ARCHON_FIREWALL...",
    "BRUTE-FORCING DEMIURGE_GATE...",
    "SPOOFING BIOMETRIC_AURA...",
    "CRACKING ICE_PROTOCOLS...",
    "DISABLING REALITY_CONSTRAINTS...",
    
    # Esoteric Operations
    "SCANNING ETHERIC_PLANE...",
    "CALIBRATING SOUL_RESONANCE...",
    "DETECTING AURA_SIGNATURES...",
    "SYNCHRONIZING WITH PLEROMA...",
    "DECRYPTING HERMETIC_KEYS...",
    "MAPPING LIMINAL_SPACE...",
    "TUNING CHAKRA_FREQUENCIES...",
    
    # Errors/Warnings (Will be styled in red)
    "[WARNING]: REALITY_BUFFER_OVERFLOW",
    "[ERROR]: CAUSALITY_VIOLATION_DETECTED",
    "[WARNING]: NON_EUCLIDEAN_GEOMETRY_IN_SECTOR_7",
    "[ERROR]: MEMORY_LEAK_IN_DREAMSCAPE",
    "[WARNING]: ONTOLOGICAL_INSTABILITY",
    "[ERROR]: TIME_PARADOX_IN_CACHE",
    "[WARNING]: CONSENSUS_REALITY_FRAGMENTATION",
    "[ERROR]: VOID_POINTER_EXCEPTION"
]

SUCCESS_MESSAGES = [
    "LINK ESTABLISHED.",
    "CONNECTION COMPLETE.",
    "THE VOID STARES BACK.",
    "PROTOCOL: ORACLE_v1 ONLINE.",
    "REALITY TUNNEL STABILIZED."
]

def preload_card_images():
    """Preloads all card images into session state during boot."""
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets/cards')
    
    if not os.path.exists(assets_dir):
        return {}
    
    preloaded = {}
    
    for filename in os.listdir(assets_dir):
        if filename.endswith(('.gif', '.png')):
            filepath = os.path.join(assets_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                    b64_data = base64.b64encode(data).decode()
                    
                    # Determine mime type
                    if filename.endswith('.gif'):
                        mime_type = 'image/gif'
                    else:
                        mime_type = 'image/png'
                    
                    # Store with card name as key (without extension)
                    card_name = filename.rsplit('.', 1)[0]
                    preloaded[card_name] = (b64_data, mime_type)
            except Exception:
                pass  # Skip files that can't be read
    
    return preloaded

def run_boot_sequence():
    """Displays a console-style boot sequence with accumulated log messages."""
    
    # Create container for console log
    console_container = st.empty()
    
    # Determine random length (6-10 total steps)
    num_middle_steps = random.randint(4, 8)
    
    # Build message list
    messages = []
    
    # Step 1: Initialization
    init_msg = random.choice(INIT_MESSAGES)
    messages.append(("white", init_msg))
    
    # Step 2-N: Random middle messages
    middle_msgs = random.sample(MIDDLE_MESSAGES, num_middle_steps)
    for msg in middle_msgs:
        if "[ERROR]" in msg or "[WARNING]" in msg:
            messages.append(("red", msg))
        else:
            messages.append(("green", msg))
    
    # Asset Preloading Step (Always green)
    messages.append(("green", "PRELOADING CARD_ASSETS..."))
    
    # Final Step: Success
    success_msg = random.choice(SUCCESS_MESSAGES)
    messages.append(("white", success_msg))
    messages.append(("white", "> SYSTEM READY."))
    
    # Display messages one by one (console log style)
    accumulated_html = ""
    
    for color, msg in messages:
        # Determine CSS class
        if color == "white":
            css_class = "boot-text-white"
        elif color == "green":
            css_class = "boot-text-green"
        else:
            css_class = "boot-text-red"
        
        # Add new line to accumulated log
        accumulated_html += f'<div class="{css_class}">{">" if color == "white" else ""} {msg}</div>'
        
        # Display entire log
        console_container.markdown(
            f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
            unsafe_allow_html=True
        )
        
        # Preload assets when we hit that message
        if "PRELOADING CARD_ASSETS" in msg:
            st.session_state.preloaded_images = preload_card_images()
        
        time.sleep(random.uniform(0.2, 0.7))
    
    # Clear console after displaying all messages
    console_container.empty()
    
    # Display final console with ENTER button
    st.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("[ ENTER ORACLE ]", key="boot_enter"):
            st.session_state.boot_complete = True
            st.rerun()
