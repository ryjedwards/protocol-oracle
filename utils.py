import streamlit as st
import time
import random
import re

# --- BOOT SEQUENCE (Restored) ---
def run_boot_sequence():
    """Runs the BIOS start up lines."""
    placeholder = st.empty()
    
    sequence = [
        ("INITIALIZING MEDIUM...", "boot-line", 0.3),
        ("SENSING PRESENCE...", "boot-ghost", 0.3),
        ("ERROR: SOUL DATA CORRUPTED.", "boot-error", 0.5),
        ("ATTEMPTING TO BIND SPIRIT...", "boot-line", 0.4),
        ("THE VEIL IS THINNING...", "boot-ghost", 0.6),
        ("SIGNAL ACQUIRED.", "boot-line", 0.3),
        ("ORACLE IS AWAKE.", "boot-line", 0.6)
    ]
    
    current_html = '<div class="boot-container">'
    
    for text, style, delay in sequence:
        new_line = f'<div class="{style}">> {text}</div>'
        current_html += new_line
        placeholder.markdown(current_html + "</div>", unsafe_allow_html=True)
        time.sleep(delay)
        
    time.sleep(0.5)
    
    # Add fade-out class
    placeholder.markdown(f'<div class="boot-container fade-out">{current_html}</div>', unsafe_allow_html=True)
    time.sleep(1.0) 
    placeholder.empty()

# --- THINKING LOGS ---
def simulate_thinking_process(container):
    """
    Simulates the AI struggling.
    """
    logs = [
        ("LISTENING TO THE ECHO...", "boot-ghost"),
        ("ERROR: TRANSLATION FAILED.", "think-error"),
        ("THE STATIC IS TOO LOUD...", "think-error"),
        ("CALIBRATING FREQUENCY...", "boot-line"),
        ("I SEE IT NOW...", "boot-ghost")
    ]
    
    current_log_html = '<div class="thinking-log">'
    
    for text, style in logs:
        color_class = style if style else "boot-line"
        line = f'<div class="{color_class}">> {text}</div>'
        current_log_html += line
        container.markdown(current_log_html + "</div>", unsafe_allow_html=True)
        time.sleep(random.uniform(0.3, 0.5))
        
    time.sleep(0.5)
    container.empty()

# --- GLITCH TEXT ---
GLITCH_VOCAB = [
    "fate", "soul", "signal", "void", "path", "cycle", "pattern", "omen",
    "truth", "illusion", "echo", "shadow", "light", "spark", "destiny", 
    "blood", "mirror", "ghost", "broken"
]

def format_glitch_html(text):
    if not text: return ""
    words = text.split(" ")
    formatted = []
    for word in words:
        clean = re.sub(r'[^\w\s]', '', word).lower()
        if clean in GLITCH_VOCAB:
            formatted.append(f'<span class="highlight-word">{word}</span>')
        else:
            formatted.append(word)
    return " ".join(formatted).replace("\n", "<br>")

# --- TYPEWRITER ---
def stream_console_text(container, full_text):
    display_text = ""
    chars = list(full_text)
    junk_chars = "†‡§?¿!~-"
    
    for i, char in enumerate(chars):
        if random.random() < 0.02 and char.isalnum():
            typo = random.choice(junk_chars)
            container.markdown(f'''
                <div class="console-container">
                    {format_glitch_html(display_text + typo)}<span class="console-cursor"></span>
                </div>
            ''', unsafe_allow_html=True)
            time.sleep(0.05)
            time.sleep(0.1) 
            
            display_text += char
            container.markdown(f'''
                <div class="console-container">
                    {format_glitch_html(display_text)}<span class="console-cursor"></span>
                </div>
            ''', unsafe_allow_html=True)
        else:
            display_text += char
            if i % 2 == 0:
                container.markdown(f'''
                    <div class="console-container">
                        {format_glitch_html(display_text)}<span class="console-cursor"></span>
                    </div>
                ''', unsafe_allow_html=True)
            time.sleep(0.015)

    container.markdown(f'''
        <div class="console-container">
            {format_glitch_html(display_text)}<span class="console-cursor"></span>
        </div>
    ''', unsafe_allow_html=True)