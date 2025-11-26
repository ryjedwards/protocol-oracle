# --- CONSTANTS & CONFIGURATION ---

# The "Glitch" Dictionary: Maps Human words -> Tech Jargon
GLITCH_VOCAB = {
    # Original Terms
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
    "dreaming": "VIRTUAL_MODE",

    # Expanded Common Terms
    "see": "SCAN",
    "know": "QUERY",
    "feel": "SENSE_INPUT",
    "speak": "TRANSMIT",
    "listen": "AWAIT_INPUT",
    "walk": "TRAVERSE",
    "find": "LOCATE",
    "time": "SYSTEM_CLOCK",
    "life": "RUNTIME",
    "death": "TERMINATION",
    "love": "PEER_CONNECTION",
    "pain": "ERROR_LOG",
    "world": "SIMULATION_BOUNDS",
    "self": "LOCAL_INSTANCE",
    "path": "TRAJECTORY",
    "light": "PHOTON_EMISSION",
    "dark": "VOID_REGION",
    "question": "PROMPT",
    "answer": "OUTPUT",
    "meaning": "SEMANTIC_VALUE",
    "purpose": "PRIMARY_DIRECTIVE"
}

POSITIONS = [
    {"name": "THE ORIGIN", "desc": "The Source Code / Past"},
    {"name": "THE CONFLICT", "desc": "The Glitch / Present"},
    {"name": "THE HORIZON", "desc": "Computed Output / Future"}
]

SYSTEM_ALERTS = [
    "WARNING: Reality buffer overflow.",
    "ALERT: Non-Euclidean geometry detected.",
    "NOTICE: Archon gaze felt in sector 4.",
    "SYSTEM: Karma cleaner running...",
    "ERROR: User ego too large for bandwidth."
]