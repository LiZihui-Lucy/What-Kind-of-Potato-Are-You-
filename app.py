"""A one-question-at-a-time potato personality quiz."""

import streamlit as st


st.set_page_config(page_title="Potato Interrogation", page_icon="🥔", layout="centered")

QUESTIONS = [
    {
        "prompt": "Your plans get canceled. The universe has entered its apology era. You…",
        "answers": [
            ("Put on pajamas so powerful they cancel my other plans.", "cozy"),
            ("Schedule a replacement activity. The calendar fears me.", "bold"),
            ("Whisper 'so this is how it ends' to a houseplant.", "dramatic"),
        ],
    },
    {
        "prompt": "The potato fashion police are here. What illegal accessory are you hiding?",
        "answers": [
            ("A blanket cape. I am both cozy and legally a burrito.", "cozy"),
            ("Sunglasses indoors. These fluorescent lights know what they did.", "bold"),
            ("A tiny crown. The peasants (other vegetables) understand.", "dramatic"),
        ],
    },
    {
        "prompt": "One slice of cake remains. It has seen things. What do you do?",
        "answers": [
            ("Get a knife. We will divide this kingdom fairly.", "steady"),
            ("Make direct eye contact and eat it like a champion.", "bold"),
            ("Hold a tiny farewell ceremony. The fork gives a speech.", "dramatic"),
        ],
    },
    {
        "prompt": "The group chat has been silent for three hours. The vibes are buffering.",
        "answers": [
            ("Send a blurry photo of a frog with no explanation.", "chaotic"),
            ("Ask if everyone is okay. Then remind them to hydrate.", "steady"),
            ("Text 'the prophecy was true' and go offline.", "dramatic"),
        ],
    },
    {
        "prompt": "You have a free weekend and the approximate energy of a spoon. Plans?",
        "answers": [
            ("Build a blanket nest. Declare it an independent nation.", "cozy"),
            ("Get on a bus because its number feels lucky.", "chaotic"),
            ("Make a plan, pack snacks, become the group's expedition manager.", "steady"),
        ],
    },
]

RESULTS = {
    "cozy": ("Couch Potato Supreme", "Your natural habitat is a blanket pile. Scientists have classified you as 80% snack crumbs."),
    "bold": ("The Audacious Hash Brown", "You have the confidence of a potato that just got promoted to CEO of Breakfast."),
    "dramatic": ("Duchess Dramash", "Every minor inconvenience gets a three-act musical. The curtains are a dish towel."),
    "steady": ("Sir Spudsworth the Prepared", "You brought a snack, a backup snack, and a tiny clipboard. Society survives because of you."),
    "chaotic": ("Tater Tornado", "You are one suspicious noise away from starting a side quest in another postcode."),
}

st.markdown(
    """
    <style>
    .stApp { background: #fff8e8; }
    h1, h2, h3, p { color: #392b21; font-family: 'Trebuchet MS', sans-serif; }
    .eyebrow { color: #8b5e34; text-transform: uppercase; letter-spacing: .16em; font-size: .8rem; }
    .question-card { border: 3px solid #392b21; border-radius: 24px; padding: 1.4rem 1.5rem;
        background: #fffdf6; box-shadow: 5px 5px 0 #392b21; margin: 1rem 0 1.2rem; }
    .stButton button { width: 100%; min-height: 3.5rem; text-align: left; white-space: normal;
        background: #fffdf6; border: 2px solid #392b21; border-radius: 15px;
        color: #392b21; font-size: 1rem; font-weight: 650; transition: transform .12s ease, background .12s ease; }
    .stButton button:hover { background: #f4bd45; border-color: #392b21; color: #392b21; transform: translateY(-2px) rotate(-.3deg); }
    [data-testid="stProgressBar"] > div > div { background: #df774d; }
    </style>
    """,
    unsafe_allow_html=True,
)

if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {dimension: 0 for dimension in RESULTS}

st.title("🥔 What Kind of Potato Are You?")
st.caption("Answer quickly. A potato in a tiny hat is timing you.")

step = st.session_state.step
if step < len(QUESTIONS):
    st.progress(step / len(QUESTIONS))
    st.markdown(f'<div class="eyebrow">Interrogation {step + 1} of {len(QUESTIONS)}</div>', unsafe_allow_html=True)
    question = QUESTIONS[step]
    st.markdown(f'<div class="question-card"><h2>{question["prompt"]}</h2></div>', unsafe_allow_html=True)

    for option_number, (answer_text, dimension) in enumerate(question["answers"]):
        if st.button(answer_text, key=f"q{step}_option{option_number}"):
            st.session_state.scores[dimension] += 1
            st.session_state.step += 1
            st.rerun()
else:
    st.progress(1.0)
    st.markdown('<div class="eyebrow">The potato council has consulted the vibes</div>', unsafe_allow_html=True)
    winning_dimension = max(RESULTS, key=lambda dimension: st.session_state.scores[dimension])
    name, description = RESULTS[winning_dimension]
    st.markdown(f'<div class="question-card"><h2>✨ {name}</h2><p>{description}</p></div>', unsafe_allow_html=True)
    st.balloons()
    st.caption("Please allow 3–5 business potatoes for your crown to arrive.")
    if st.button("Get re-interrogated ↻"):
        st.session_state.step = 0
        st.session_state.scores = {dimension: 0 for dimension in RESULTS}
        st.rerun()

st.caption("This quiz is not peer reviewed. It was reviewed by a potato.")
