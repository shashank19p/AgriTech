import joblib
import numpy as np
import streamlit as st

from utils import (
    explain_crop_choice,
    fetch_weather_data,
    get_crop_display_name,
    get_crop_market_price,
    get_disease_advisory,
    get_fertilizer_recommendation,
    get_organic_farming_plan,
    get_state_specific_advice,
    get_suitability_feedback,
    get_weather_alerts,
    translate_text,
)


try:
    import pyttsx3
except Exception:
    pyttsx3 = None


STATES = ["Andhra Pradesh", "Punjab", "Tamil Nadu"]
SEASONS = ["Kharif", "Rabi", "Summer"]
SOIL_TYPES = ["Black", "Red", "Alluvial"]
LANGUAGES = ["English", "Telugu", "Hindi", "Tamil", "Kannada"]
QUICK_MODE_DEFAULTS = {
    "Black": {"n": 70, "p": 45, "k": 55},
    "Red": {"n": 50, "p": 40, "k": 45},
    "Alluvial": {"n": 65, "p": 50, "k": 60},
}

# Simple visual mapping keeps the result card crop-specific without adding heavy assets.
CROP_EMOJIS = {
    "Rice": "🌾",
    "Maize": "🌽",
    "Banana": "🍌",
    "Cotton": "🌿",
    "Mango": "🥭",
    "Apple": "🍎",
    "Orange": "🍊",
    "Papaya": "🍈",
    "Coconut": "🥥",
    "Grapes": "🍇",
    "Watermelon": "🍉",
    "Muskmelon": "🍈",
    "Pomegranate": "🍎",
    "Coffee": "☕",
    "Chickpea": "🫘",
    "Kidneybeans": "🫘",
    "Pigeonpeas": "🌱",
    "Mothbeans": "🌱",
    "Mungbean": "🌱",
    "Blackgram": "🌱",
    "Lentil": "🌱",
    "Jute": "🌿",
}

# Optional image placeholders; add local paths or URLs later if you want richer visuals.
CROP_IMAGES = {
    "Rice": None,
    "Maize": None,
    "Banana": None,
}


st.set_page_config(page_title="AgriSmart | Crop Advisor", page_icon="🌱", layout="wide")
initial_language = st.session_state.get("selected_language", "English")

st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at top right, rgba(201, 151, 51, 0.16), transparent 28%),
            radial-gradient(circle at bottom left, rgba(43, 106, 63, 0.14), transparent 34%),
            linear-gradient(180deg, #f8f4ea 0%, #eef4ea 52%, #f5f1e6 100%);
    }

    .stApp {
        color: #1a1a1a;
        font-family: "Trebuchet MS", "Gill Sans", "Segoe UI", sans-serif;
    }

    .stApp, .stApp p, .stApp li, .stApp span, .stMarkdown, .stMarkdown p, .stCaption, .stAlert, .stText, div {
        color: #1a1a1a;
    }

    h1, h2, h3, h4, h5, h6, .stSubheader, .stHeader {
        color: #10281a !important;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 2rem;
    }

    .main-header {
        background:
            linear-gradient(135deg, rgba(20, 67, 40, 0.97), rgba(52, 125, 73, 0.93) 58%, rgba(201, 151, 51, 0.88)),
            linear-gradient(180deg, rgba(255, 255, 255, 0.08), transparent);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 28px;
        padding: 30px 34px;
        color: #fdfbf4;
        text-align: center;
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(2rem, 3vw, 3.15rem);
        font-weight: 700;
        letter-spacing: 0.05em;
        text-shadow: 0 2px 14px rgba(0, 0, 0, 0.18);
        box-shadow: 0 28px 70px rgba(24, 50, 33, 0.2);
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
    }

    .hero-heart-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1.5rem;
        flex-wrap: wrap;
    }

    .hero-copy {
        flex: 1 1 360px;
        min-width: 280px;
    }

    .hero-heart {
        width: min(260px, 72vw);
        aspect-ratio: 1 / 1;
        position: relative;
        flex: 0 0 auto;
        filter: drop-shadow(0 18px 28px rgba(0, 0, 0, 0.22));
    }

    .hero-heart-fill,
    .hero-heart-outline {
        position: absolute;
        inset: 0;
    }

    .hero-heart-fill {
        background:
            linear-gradient(180deg, rgba(255, 214, 140, 0.85) 0%, rgba(255, 214, 140, 0.15) 24%, transparent 32%),
            url("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=900&q=80");
        background-size: cover;
        background-position: center;
        -webkit-mask-repeat: no-repeat;
        -webkit-mask-position: center;
        -webkit-mask-size: contain;
        mask-repeat: no-repeat;
        mask-position: center;
        mask-size: contain;
        -webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 87 16 55C7 46 7 30 18 21c10-8 24-6 32 8 8-14 22-16 32-8 11 9 11 25 2 34Z' fill='black'/></svg>");
        mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 87 16 55C7 46 7 30 18 21c10-8 24-6 32 8 8-14 22-16 32-8 11 9 11 25 2 34Z' fill='black'/></svg>");
    }

    .hero-heart-fill::after {
        content: "";
        position: absolute;
        inset: 0;
        background:
            radial-gradient(circle at 50% 18%, rgba(255, 255, 255, 0.2), transparent 26%),
            linear-gradient(180deg, rgba(12, 44, 24, 0.02), rgba(12, 44, 24, 0.28));
        -webkit-mask-repeat: no-repeat;
        -webkit-mask-position: center;
        -webkit-mask-size: contain;
        mask-repeat: no-repeat;
        mask-position: center;
        mask-size: contain;
        -webkit-mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 87 16 55C7 46 7 30 18 21c10-8 24-6 32 8 8-14 22-16 32-8 11 9 11 25 2 34Z' fill='black'/></svg>");
        mask-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 87 16 55C7 46 7 30 18 21c10-8 24-6 32 8 8-14 22-16 32-8 11 9 11 25 2 34Z' fill='black'/></svg>");
    }

    .hero-heart-outline {
        background: center / contain no-repeat url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path d='M50 87 16 55C7 46 7 30 18 21c10-8 24-6 32 8 8-14 22-16 32-8 11 9 11 25 2 34Z' fill='none' stroke='black' stroke-width='4.5' stroke-linecap='round' stroke-linejoin='round'/></svg>");
    }

    .main-header::after {
        content: "";
        position: absolute;
        inset: auto -60px -70px auto;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.18), transparent 68%);
        pointer-events: none;
    }

    [data-testid="column"] {
        border-radius: 28px;
        border: 1px solid rgba(34, 76, 48, 0.14);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 251, 243, 0.96));
        box-shadow: 0 24px 60px rgba(31, 63, 41, 0.14);
        padding: 18px 26px 18px;
        overflow: hidden;
    }

    [data-testid="column"] h3 {
        color: #17492c;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.5rem;
        margin: 0 0 0.75rem 0;
        letter-spacing: 0.02em;
        display: block;
        padding: 0.65rem 0.9rem;
        background: linear-gradient(135deg, rgba(43, 106, 63, 0.10), rgba(201, 151, 51, 0.10));
        border: 1px solid rgba(34, 76, 48, 0.08);
        border-radius: 16px;
    }

    .prediction-box {
        margin-top: 1.25rem;
        padding: 34px 30px;
        text-align: center;
        border-radius: 28px;
        border: 1px solid rgba(34, 76, 48, 0.14);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(255, 251, 243, 0.96));
        box-shadow: 0 32px 72px rgba(24, 50, 33, 0.16);
    }

    .prediction-box p {
        color: #1a1a1a;
    }

    .crop-text {
        font-size: clamp(2.5rem, 4vw, 4.35rem);
        color: #17492c;
        font-family: Georgia, "Times New Roman", serif;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin: 0.35rem 0 0.7rem;
        text-shadow: 0 1px 0 rgba(255, 255, 255, 0.7);
    }

    .advisory-card {
        margin-top: 1.25rem;
        padding: 26px 24px;
        border-radius: 24px;
        border: 1px solid rgba(34, 76, 48, 0.14);
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.97), rgba(250, 247, 239, 0.96));
        box-shadow: 0 20px 48px rgba(31, 63, 41, 0.12);
        min-height: 100%;
    }

    .advisory-card h3 {
        margin: 0 0 0.85rem 0;
        color: #17492c;
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.45rem;
    }

    .advisory-card p,
    .advisory-card li {
        color: #1a1a1a !important;
        font-size: 1rem;
        line-height: 1.6;
    }

    .advisory-metric {
        margin: 0.8rem 0;
        padding: 0.85rem 1rem;
        border-radius: 16px;
        background: rgba(43, 106, 63, 0.08);
        border: 1px solid rgba(43, 106, 63, 0.12);
        color: #17492c;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        min-height: 3.45rem;
        border: none !important;
        border-radius: 999px !important;
        background: linear-gradient(135deg, #2b6a3f, #3d8450 62%, #c99733) !important;
        color: #fffdf8 !important;
        font-weight: 800 !important;
        font-size: 1rem !important;
        letter-spacing: 0.08em;
        box-shadow: 0 18px 34px rgba(31, 63, 41, 0.24);
        transition: transform 0.22s ease, box-shadow 0.22s ease, filter 0.22s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        filter: saturate(1.06);
        box-shadow: 0 22px 38px rgba(31, 63, 41, 0.3);
    }

    .stButton > button:focus:not(:active) {
        border: none !important;
        box-shadow: 0 0 0 4px rgba(201, 151, 51, 0.18), 0 18px 34px rgba(31, 63, 41, 0.24) !important;
    }

    label,
    .stMarkdown p,
    .stCaption {
        color: #1a1a1a;
    }

    .stSlider label,
    .stNumberInput label,
    .stTextInput label,
    .stSelectbox label,
    .stFileUploader label,
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #1a1a1a !important;
        font-family: "Times New Roman", Times, serif !important;
        font-weight: 700 !important;
        letter-spacing: 0 !important;
    }

    div[data-baseweb="input"] > div,
    div[data-baseweb="base-input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background: rgba(248, 244, 235, 0.96);
        border: 1px solid rgba(34, 76, 48, 0.16);
        border-radius: 16px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.7);
        transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="base-input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(201, 151, 51, 0.7);
        box-shadow: 0 0 0 4px rgba(201, 151, 51, 0.18);
        background: #fffdf8;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div {
        color: #183126;
        font-weight: 600;
    }

    div[data-baseweb="select"] * {
        color: #183126 !important;
    }

    div[data-testid="stNumberInput"] button {
        border-radius: 12px !important;
    }

    div[data-baseweb="slider"] [role="slider"] {
        background: #2b6a3f !important;
        border: 3px solid #fffdf8 !important;
        box-shadow: 0 8px 18px rgba(31, 63, 41, 0.24);
    }

    div[data-testid="stSlider"] {
        padding: 0.45rem 0.2rem 0.2rem;
        border-radius: 18px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
        background: rgba(43, 106, 63, 0.1);
        padding: 0.7rem 1.15rem;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #2b6a3f, #c99733) !important;
        color: #fffdf8 !important;
    }

    .stMarkdown hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(34, 76, 48, 0.22), transparent);
        margin: 2.2rem 0 1rem;
    }

    div[data-testid="stCaptionContainer"] {
        text-align: center;
        color: #687466;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        font-size: 0.82rem;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #153724 0%, #1f5132 46%, #2c6a3f 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    .sidebar-heart {
        width: min(170px, 100%);
        aspect-ratio: 1 / 1;
        position: relative;
        margin: 0 auto 1rem;
        filter: drop-shadow(0 14px 20px rgba(0, 0, 0, 0.22));
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #f7f3e7 !important;
    }

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] .stMarkdown p {
        color: #f7f3e7 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] > div,
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        box-shadow: none;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] input,
    section[data-testid="stSidebar"] div[data-baseweb="base-input"] input,
    section[data-testid="stSidebar"] div[data-baseweb="select"] *,
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #fffdf8;
    }

    section[data-testid="stSidebar"] [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.11);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 20px;
        padding: 14px 16px;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    }

    @media (max-width: 900px) {
        .block-container {
            padding-top: 1.4rem;
        }

        .main-header {
            padding: 24px 20px;
            border-radius: 22px;
            letter-spacing: 0.03em;
        }

        [data-testid="column"],
        .prediction-box,
        .advisory-card {
            border-radius: 22px;
        }

        .hero-heart {
            width: min(220px, 66vw);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="main-header">
        <div class="hero-heart-wrap">
            <div class="hero-copy">🌾 {translate_text("Smart Crop Advisory System", initial_language)} 🌱</div>
            <div class="hero-heart" aria-hidden="true">
                <div class="hero-heart-fill"></div>
                <div class="hero-heart-outline"></div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model():
    try:
        return joblib.load("model.pkl")
    except Exception:
        return None


def speak_recommendation(text, language):
    if pyttsx3 is None:
        return False, translate_text("pyttsx3 is not installed. Run `pip install pyttsx3` to enable voice output.", language)

    try:
        engine = pyttsx3.init()
        language_voice_hints = {
            "Telugu": ["telugu", "te-", "te_", "te "],
            "Hindi": ["hindi", "hi-", "hi_", "hi "],
            "Tamil": ["tamil", "ta-", "ta_", "ta "],
            "Kannada": ["kannada", "kn-", "kn_", "kn "],
        }
        voices = engine.getProperty("voices")
        for voice in voices:
            voice_blob = f"{getattr(voice, 'name', '')} {getattr(voice, 'id', '')}".lower()
            if any(hint in voice_blob for hint in language_voice_hints.get(language, [])):
                engine.setProperty("voice", voice.id)
                break
        engine.say(text)
        engine.runAndWait()
        return True, translate_text("Voice output played on the local machine.", language)
    except Exception as exc:
        return False, f"{translate_text('Voice output failed:', language)} {exc}"


def render_weather_panel():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-heart" aria-hidden="true">
                <div class="hero-heart-fill"></div>
                <div class="hero-heart-outline"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        sidebar_language = st.session_state.get("selected_language", "English")
        st.header(f"🌦️ {translate_text('Weather Panel', sidebar_language)}")
        location = st.text_input(translate_text("City Name:", sidebar_language), "Amaravati")
        api_key = st.text_input(translate_text("OpenWeather API Key:", sidebar_language), type="password")

        if "weather_data" not in st.session_state:
            st.session_state.weather_data = fetch_weather_data(location, api_key)

        if st.button(translate_text("Check Forecast", sidebar_language)):
            st.session_state.weather_data = fetch_weather_data(location, api_key)

        weather_data = st.session_state.weather_data
        if "error" in weather_data:
            st.error(translate_text(weather_data["error"], sidebar_language))
        else:
            st.metric(translate_text("Temperature", sidebar_language), f"{weather_data['temperature']} °C")
            st.metric(translate_text("Humidity", sidebar_language), f"{weather_data['humidity']}%")
            st.info(f"{translate_text('Condition:', sidebar_language)} {translate_text(weather_data['weather'], sidebar_language)}")
            if weather_data.get("mocked"):
                st.caption(translate_text("Showing default demo weather because no API key was provided.", sidebar_language))

        st.markdown("---")
        st.selectbox(translate_text("Language", sidebar_language), LANGUAGES, key="selected_language")
        return location, weather_data


def build_voice_text(result, language):
    return (
        f"{translate_text('Recommended Crop', language)}: {result['display_crop']}. "
        f"{translate_text('Fertilizer Advice', language)}: {result['fertilizer_display']}. "
        f"{translate_text('State Advice', language)}: {result['state_advice']} "
        f"{translate_text('Estimated Market Price', language)}: {result['price_text']}."
    )


def get_crop_visuals(crop_name):
    emoji = CROP_EMOJIS.get(crop_name, "🌱")
    image = CROP_IMAGES.get(crop_name)
    return emoji, image


def get_top_crop_suggestions(model, input_data, predicted_crop):
    if model is not None and hasattr(model, "predict_proba") and hasattr(model, "classes_"):
        probabilities = model.predict_proba(input_data)[0]
        ranked = np.argsort(probabilities)[::-1][:3]
        return [(model.classes_[idx], float(probabilities[idx])) for idx in ranked]

    fallback = [predicted_crop]
    for crop in CROP_EMOJIS:
        if crop != predicted_crop:
            fallback.append(crop)
        if len(fallback) == 3:
            break
    return [(crop, 0.0) for crop in fallback]


def format_price(price_value, language):
    if not price_value:
        return translate_text("Not available", language)
    return f"₹ {price_value} / quintal"


def get_mode_defaults(soil_type):
    return QUICK_MODE_DEFAULTS.get(soil_type, {"n": 60, "p": 45, "k": 50})


rf_model = load_model()
location, weather_data = render_weather_panel()
language = st.session_state.get("selected_language", "English")

if "recommendation_result" not in st.session_state:
    st.session_state.recommendation_result = None

st.info(translate_text("This system supports farmer decisions, not replaces them.", language))
if rf_model is None:
    st.error(translate_text("Model file `model.pkl` is not loaded. Please run the training script before generating prediction.", language))

step1_col, step2_col = st.columns(2, gap="large")
with step1_col:
    st.subheader(translate_text("Step 1: Location + Season", language))
    st.caption(translate_text("Use local climate or weather panel values for better guidance", language))
    state = st.selectbox(translate_text("State", language), STATES)
    season = st.selectbox(translate_text("Season", language), SEASONS)
    land_area = st.number_input(translate_text("Land Area (acres)", language), min_value=0.1, value=1.0, step=0.1)

with step2_col:
    st.subheader(translate_text("Step 2: Soil + NPK", language))
    st.caption(translate_text("Adjust values based on your soil test report", language))
    st.markdown(f"**{translate_text('🌱 Soil Details', language)}**")
    soil_type = st.selectbox(translate_text("Soil Type", language), SOIL_TYPES)
    input_mode = st.selectbox(
        translate_text("Input Mode", language),
        [translate_text("Quick Mode", language), translate_text("Advanced Mode", language)],
    )
    quick_defaults = get_mode_defaults(soil_type)
    is_quick_mode = input_mode == translate_text("Quick Mode", language)
    if is_quick_mode:
        st.caption(translate_text("Quick Mode uses suggested NPK values based on soil type.", language))
    n_val = st.slider(translate_text("Nitrogen (N)", language), 0, 150, quick_defaults["n"] if is_quick_mode else 50, disabled=is_quick_mode)
    p_val = st.slider(translate_text("Phosphorus (P)", language), 0, 150, quick_defaults["p"] if is_quick_mode else 50, disabled=is_quick_mode)
    k_val = st.slider(translate_text("Potassium (K)", language), 0, 150, quick_defaults["k"] if is_quick_mode else 50, disabled=is_quick_mode)

env_col1, env_col2, env_col3 = st.columns(3)
st.markdown(f"**{translate_text('🌤️ Weather Details', language)}**")
with env_col1:
    temp_val = st.number_input(translate_text("Temperature (°C)", language), 0.0, 50.0, 25.0)
with env_col2:
    hum_val = st.number_input(translate_text("Humidity (%)", language), 0.0, 100.0, 70.0)
with env_col3:
    ph_val = st.number_input(translate_text("Soil pH Level", language), 0.0, 14.0, 6.5)

st.subheader(translate_text("Step 3: Generate", language))
st.caption(translate_text("Tip: If unsure, follow the first recommendation.", language))

st.markdown("<br>", unsafe_allow_html=True)

if st.button(translate_text("Get Smart Recommendation", language)):
    if rf_model is None:
        st.error(translate_text("Model file `model.pkl` not found. Please run the training script.", language))
    else:
        with st.spinner(translate_text("Analyzing data...", language)):
            input_data = np.array([[n_val, p_val, k_val, temp_val, hum_val, ph_val]])
            prediction = rf_model.predict(input_data)[0]
            fert_rec = get_fertilizer_recommendation(n_val, p_val, k_val)
            organic_plan = get_organic_farming_plan(prediction, land_area)
            suitability = get_suitability_feedback(prediction, season, soil_type)
            state_advice = get_state_specific_advice(state)
            market_price = get_crop_market_price(prediction)
            disease_options = get_disease_advisory(prediction)
            weather_alerts = get_weather_alerts(weather_data)
            top_suggestions = get_top_crop_suggestions(rf_model, input_data, prediction)
            explain_points = explain_crop_choice(
                prediction, n_val, p_val, k_val, temp_val, hum_val, ph_val, season, soil_type, state
            )

            st.session_state.recommendation_result = {
                "crop": prediction,
                "display_crop": get_crop_display_name(prediction, language),
                "fertilizer": fert_rec,
                "fertilizer_display": translate_text(fert_rec, language),
                "organic_plan": organic_plan,
                "suitability": suitability,
                "state_advice": state_advice,
                "market_price": market_price,
                "price_text": format_price(market_price, language),
                "diseases": disease_options,
                "weather_alerts": weather_alerts,
                "top_suggestions": top_suggestions,
                "explain_points": explain_points,
                "state": state,
                "season": season,
                "soil_type": soil_type,
                "location": location,
            }
        st.success(translate_text("Recommendation generated successfully!", language))

result = st.session_state.recommendation_result

tab1, tab2, tab3 = st.tabs(
    [
        translate_text("Crop Recommendation", language),
        translate_text("Disease Detection", language),
        translate_text("Market Info", language),
    ]
)

with tab1:
    if not result:
        st.info(translate_text("No crop predicted yet.", language))
    else:
        display_crop = get_crop_display_name(result["crop"], language)
        fertilizer_display = translate_text(result["fertilizer"], language)
        price_text = format_price(result["market_price"], language)
        crop_emoji, crop_image = get_crop_visuals(result["crop"])

        summary_col1, summary_col2, summary_col3 = st.columns(3)
        with summary_col1:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Summary", language)}</h3>
                    <p><b>{crop_emoji} {translate_text("Recommended Crop", language)}</b></p>
                    <p>{display_crop}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with summary_col2:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Estimated Market Price", language)}</h3>
                    <p><b>💰 {price_text}</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with summary_col3:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Season Fit", language)}</h3>
                    <p><b>📍 {translate_text(result['suitability']['season_fit'], language)}</b></p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown(
            f"""
            <div class="prediction-box">
                <p style="font-size: 18px;">{translate_text("Recommended Crop", language)}</p>
                <div class="crop-text">{crop_emoji} {display_crop}</div>
                <p style="font-size: 20px;"><b>{translate_text("Fertilizer Advice", language)}:</b> {fertilizer_display}</p>
                <p style="color: #1a1a1a;"><i>{translate_text("This recommendation is based on the trained Random Forest model and simple SIH rule-based advisory layers.", language)}</i></p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if crop_image:
            st.image(crop_image, caption=f"{crop_emoji} {display_crop}", use_container_width=True)

        if st.button(f"🔊 {translate_text('Read Recommendation Aloud', language)}"):
            voice_result = dict(result)
            voice_result["display_crop"] = display_crop
            voice_result["fertilizer_display"] = fertilizer_display
            voice_result["price_text"] = price_text
            success, message = speak_recommendation(build_voice_text(voice_result, language), language)
            if success:
                st.success(message)
            else:
                st.warning(message)

        st.markdown(f"### {translate_text('Top 3 Crop Suggestions', language)}")
        suggestion_cols = st.columns(3)
        for idx, (crop_name, score) in enumerate(result["top_suggestions"]):
            suggestion_display = get_crop_display_name(crop_name, language)
            suggestion_emoji, _ = get_crop_visuals(crop_name)
            label = translate_text("Best Match", language) if idx == 0 else translate_text(f"Alternative {idx}", language)
            with suggestion_cols[idx]:
                confidence_text = (
                    f"{translate_text('Model confidence:', language)} {round(score * 100, 1)}%"
                    if score
                    else translate_text("Rule-based backup suggestion", language)
                )
                st.markdown(
                    f"""
                    <div class="advisory-card">
                        <h3>{label}</h3>
                        <p style="font-size: 1.2rem;"><b>{suggestion_emoji} {suggestion_display}</b></p>
                        <p>{confidence_text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        advice_col, organic_col = st.columns(2, gap="large")

        with advice_col:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("State Advice", language)}</h3>
                    <p><b>{translate_text("Season Fit", language)}:</b> {translate_text(result['suitability']['season_fit'], language)}</p>
                    <p><b>{translate_text("Soil Fit", language)}:</b> {translate_text(result['suitability']['soil_fit'], language)}</p>
                    <p><b>{translate_text("Region:", language)}</b> {result['state']}</p>
                    <p>{translate_text(result['state_advice'], language)}</p>
                    <p><b>{translate_text("Suitability Summary:", language)}</b> {translate_text(result['suitability']['summary'], language)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Crop Advice for", language)} {display_crop}</h3>
                    <p><b>{translate_text("Watering:", language)}</b> {translate_text(result['organic_plan']['watering'], language)}</p>
                    <p><b>{translate_text("Field Guidance:", language)}</b> {translate_text(result['organic_plan']['crop_advice'], language)}</p>
                    <p><b>{translate_text("Best Organic Components:", language)}</b> {", ".join(result['organic_plan']['booster_components'])}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with organic_col:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Organic Farming Plan", language)}</h3>
                    <p>{translate_text("Calculated for", language)} <b>{land_area} {translate_text("acre(s).", language)}</b></p>
                    <div class="advisory-metric">{translate_text("Panchagavya", language)}: {result['organic_plan']['panchagavya_total_litres']} {translate_text("litres", language)}</div>
                    <div class="advisory-metric">{translate_text("Vermicompost", language)}: {result['organic_plan']['vermicompost_total_kg']} {translate_text("kg", language)}</div>
                    <p><b>{translate_text("Panchagavya schedule:", language)}</b> {translate_text(result['organic_plan']['application_schedule']['panchagavya'], language)}</p>
                    <p><b>{translate_text("Vermicompost schedule:", language)}</b> {translate_text(result['organic_plan']['application_schedule']['vermicompost'], language)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{translate_text("Weather Alerts", language)}</h3>
                """,
                unsafe_allow_html=True,
            )
            if result["weather_alerts"]:
                for alert in result["weather_alerts"]:
                    st.warning(translate_text(alert, language))
            else:
                st.success(translate_text("No major weather warning based on the current weather panel values.", language))
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="advisory-card">
                <h3>{translate_text("Why this crop?", language)}</h3>
                <p>{translate_text("This section explains the recommendation using your NPK, temperature, humidity, pH, season, soil, and location inputs.", language)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for point in result["explain_points"]:
            st.write(f"- {translate_text(point, language)}")

with tab2:
    uploaded_file = st.file_uploader(translate_text("Upload a crop leaf image", language), type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        st.image(uploaded_file, caption=translate_text("Uploaded crop image", language), use_container_width=True)

    if not result:
        st.info(translate_text("Generate a crop recommendation first to unlock crop-based disease suggestions.", language))
    else:
        st.markdown(
            f"""
            <div class="advisory-card">
                <h3>{translate_text("Possible Diseases", language)} - {get_crop_display_name(result['crop'], language)}</h3>
                <p>{translate_text("Based on your crop, these diseases are most likely.", language)}</p>
                <p>{translate_text("Student-project note: this is rule-based advisory linked to the predicted crop. The image upload is included for the SIH-style workflow.", language)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        for disease in result["diseases"]:
            st.markdown(
                f"""
                <div class="advisory-card">
                    <h3>{disease['name']}</h3>
                    <p><b>{translate_text("Remedy", language)}:</b> {disease['remedy']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab3:
    if not result:
        st.info(translate_text("Generate a crop recommendation to view market information.", language))
    else:
        display_crop = get_crop_display_name(result["crop"], language)
        price_text = format_price(result["market_price"], language)
        compare_options = [result["crop"]] + [crop for crop, _ in result["top_suggestions"] if crop != result["crop"]]
        if len(compare_options) < 2:
            compare_options.append("Maize")
        st.markdown(
            f"""
            <div class="advisory-card">
                <h3>{translate_text("Market Info", language)}</h3>
                <p><b>{translate_text("Estimated Market Price", language)}:</b> {price_text}</p>
                <p><b>{translate_text("Recommended Crop", language)}:</b> {display_crop}</p>
                <p><b>{translate_text("Location:", language)}</b> {result['state']} | <b>{translate_text("Season", language)}:</b> {translate_text(result['season'], language)} | <b>{translate_text("Soil Type", language)}:</b> {translate_text(result['soil_type'], language)}</p>
                <p>{translate_text("Use this as an approximate demo value for presentation. Real mandi prices can change by district and date.", language)}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        compare_crop = st.selectbox(translate_text("Compare market price with another crop", language), compare_options[1:], key="market_compare_crop")
        compare_crop_price = get_crop_market_price(compare_crop)
        compare_crop_display = get_crop_display_name(compare_crop, language)

        compare_col1, compare_col2 = st.columns(2)
        with compare_col1:
            st.metric(display_crop, price_text)
        with compare_col2:
            st.metric(compare_crop_display, format_price(compare_crop_price, language))

        if result["market_price"] and compare_crop_price:
            higher_crop = display_crop if result["market_price"] >= compare_crop_price else compare_crop_display
            st.success(f"{translate_text('Higher market price:', language)} {higher_crop}")

st.markdown("---")
st.caption(translate_text("This system supports farmer decisions, not replaces them.", language))
