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

def validate_card_library():
    """Validates all cards have required fields."""
    try:
        from card_library import CARD_LIBRARY
        
        required_fields = ['archetype', 'gnostic', 'advice']
        total_cards = len(CARD_LIBRARY)
        valid_cards = 0
        
        for card_name, card_data in CARD_LIBRARY.items():
            if all(field in card_data for field in required_fields):
                valid_cards += 1
        
        return valid_cards, total_cards, valid_cards == total_cards
    except Exception as e:
        return 0, 0, False

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
        
        time.sleep(random.uniform(0.2, 0.7))
    
    # Card Validation Step
    accumulated_html += '<div class="boot-text-green">> VALIDATING CARD_DATABASE...</div>'
    console_container.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    time.sleep(0.3)
    
    valid_cards, total_cards, validation_success = validate_card_library()
    
    if validation_success:
        accumulated_html += f'<div class="boot-text-green">> [{valid_cards}/{total_cards} CARDS OK]</div>'
    else:
        accumulated_html += f'<div class="boot-text-red">[ERROR]: CARD_DATABASE_CORRUPTED [{valid_cards}/{total_cards}]</div>'
    
    console_container.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    time.sleep(0.5)
    
    # Asset Preloading Step with Progress
    accumulated_html += '<div class="boot-text-green">> PRELOADING CARD_ASSETS...</div>'
    console_container.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    time.sleep(0.3)
    
    st.session_state.preloaded_images = preload_card_images()
    loaded_count = len(st.session_state.preloaded_images)
    
    if loaded_count > 0:
        accumulated_html += f'<div class="boot-text-green">> [{loaded_count} ASSETS LOADED]</div>'
    else:
        accumulated_html += '<div class="boot-text-red">[WARNING]: NO_ASSETS_FOUND</div>'
    
    console_container.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    time.sleep(0.5)
    
    # Final Step: Success
    success_msg = random.choice(SUCCESS_MESSAGES)
    accumulated_html += f'<div class="boot-text-white">> {success_msg}</div>'
    accumulated_html += '<div class="boot-text-white">> SYSTEM READY.</div>'
    
    console_container.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    time.sleep(0.5)
    
    # Clear console after displaying all messages
    console_container.empty()
    
    # Display final console with ENTER button (only if validation passed)
    st.markdown(
        f'<div style="font-family: monospace; line-height: 1.8;">{accumulated_html}</div>',
        unsafe_allow_html=True
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show button only if validation succeeded
    if validation_success:
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("[ ENTER ORACLE ]", key="boot_enter"):
                st.session_state.boot_complete = True
                st.rerun()
    else:
        # Show error message instead of button
        st.markdown(
            '<div class="boot-text-red" style="text-align: center; margin-top: 20px;">'
            'FATAL: SYSTEM INTEGRITY COMPROMISED. CONTACT ADMINISTRATOR.'
            '</div>',
            unsafe_allow_html=True
        )
