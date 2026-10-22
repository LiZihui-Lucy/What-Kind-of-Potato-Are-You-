"""A silly, one-question-at-a-time potato personality adventure."""

from pathlib import Path

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
    "cozy": (
        "Couch Potato Supreme",
        "Your natural habitat is a blanket pile. Scientists have classified you as 80% snack crumbs.",
        "couch-potato.svg",
    ),
    "bold": (
        "The Audacious Hash Brown",
        "You have the confidence of a potato that just got promoted to CEO of Breakfast.",
        "hash-brown.svg",
    ),
    "dramatic": (
        "Duchess Dramash",
        "Every minor inconvenience gets a three-act musical. The curtains are a dish towel.",
        "duchess-dramash.svg",
    ),
    "steady": (
        "Sir Spudsworth the Prepared",
        "You brought a snack, a backup snack, and a tiny clipboard. Society survives because of you.",
        "sir-spudsworth.svg",
    ),
    "chaotic": (
        "Tater Tornado",
        "You are one suspicious noise away from starting a side quest in another postcode.",
        "tater-tornado.svg",
    ),
}

ANSWER_HTML = """
<div id="potato-quiz-root"></div>
"""

ANSWER_CSS = """
:host { display:block; font-family:var(--st-font, 'Trebuchet MS', sans-serif); color:#392b21; }
.quiz { position:relative; padding: .4rem 0 1rem; overflow:hidden; }
.hud { display:flex; justify-content:space-between; align-items:center; gap:1rem; margin:.7rem 0; }
.eyebrow { color:#8b5e34; font-size:.78rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; }
.wallet { color:#6e4a2d; font-size:.88rem; font-weight:700; white-space:nowrap; }
.track { height:9px; background:#f0dfbd; border:1px solid #392b21; border-radius:99px; overflow:hidden; margin: .6rem 0 1rem; }
.track-fill { height:100%; background:#df774d; border-radius:99px; transition:width .35s ease; }
.card { position:relative; border:3px solid #392b21; border-radius:24px; padding:1.3rem 1.4rem; background:#fffdf6; box-shadow:5px 5px 0 #392b21; margin:1rem 0 1.15rem; animation:card-in .42s cubic-bezier(.2,.8,.25,1.2) both; }
.card:before { content:'✳'; position:absolute; right:1rem; top:.65rem; color:#df774d; font-size:1.2rem; transform:rotate(12deg); }
.card h2 { font-family:'Trebuchet MS',sans-serif; color:#392b21; font-size:clamp(1.35rem,3.5vw,1.85rem); line-height:1.25; margin:.2rem 1.5rem .2rem 0; }
.answers { display:grid; gap:.72rem; }
.answer { width:100%; min-height:3.3rem; border:2px solid #392b21; border-radius:15px; padding:.8rem 1rem; background:#fffdf6; color:#392b21; font:650 1rem/1.35 'Trebuchet MS',sans-serif; text-align:left; cursor:pointer; box-shadow:2px 2px 0 #392b21; transition:transform .15s ease,background .15s ease,box-shadow .15s ease; }
.answer:hover:not(:disabled) { background:#f4bd45; transform:translateY(-2px) rotate(-.35deg); box-shadow:3px 4px 0 #392b21; }
.answer:focus-visible,.stamp:focus-visible { outline:3px solid #df774d; outline-offset:3px; }
.answer:disabled { cursor:default; }
.answer.drop { animation:answer-drop .68s cubic-bezier(.55,.04,.8,.25) forwards; }
.answer.fade { animation:answer-away .32s ease-in forwards; }
.stamp { position:absolute; z-index:2; right:1rem; top:3.2rem; width:4.6rem; height:4.6rem; border:2px dashed #392b21; border-radius:50%; background:#f4bd45; color:#392b21; cursor:pointer; display:grid; place-items:center; font-size:1.9rem; box-shadow:3px 3px 0 #392b21; animation:stamp-drop 1.25s ease-in-out infinite alternate; }
.stamp span { position:absolute; top:4.45rem; right:-.55rem; width:max-content; max-width:11rem; padding:.28rem .45rem; border-radius:8px; background:#fffdf6; border:1px solid #392b21; font:700 .68rem 'Trebuchet MS',sans-serif; font-size:.68rem; }
.stamp.picked { animation:stamp-pop .38s ease-out forwards; pointer-events:none; }
.hint { color:#8b5e34; font-size:.82rem; margin:.8rem 0 0; }
@keyframes card-in { from { opacity:0; transform:translateY(16px) rotate(-1.2deg) scale(.98); } to { opacity:1; transform:translateY(0) rotate(0) scale(1); } }
@keyframes answer-drop { 12% { transform:rotate(-3deg) translateY(-5px); } 100% { opacity:0; transform:translate(12px,115vh) rotate(18deg); } }
@keyframes answer-away { to { opacity:0; transform:scale(.78) rotate(-4deg); } }
@keyframes stamp-drop { from { transform:translateY(-8px) rotate(-9deg); } to { transform:translateY(8px) rotate(9deg); } }
@keyframes stamp-pop { to { opacity:0; transform:scale(1.8) rotate(28deg); } }
@media (prefers-reduced-motion: reduce) { *, *:before, *:after { animation-duration:.01ms !important; animation-iteration-count:1 !important; scroll-behavior:auto !important; transition-duration:.01ms !important; } }
"""

ANSWER_JS = """
export default function(component) {
  const { data, parentElement, setTriggerValue } = component;
  const root = parentElement.querySelector("#potato-quiz-root");
  if (!root) return;

  const renderKey = `${data.step}:${data.stamps}:${data.showStamp}`;
  if (root.dataset.renderKey !== renderKey) {
    root.dataset.renderKey = renderKey;
    const escapeHtml = (value) => String(value).replace(/[&<>\"']/g, (char) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "\\\"": "&quot;", "'": "&#39;"
    }[char]));
    const percent = Math.round((data.step / data.total) * 100);
    const options = data.answers.map((answer, index) =>
      `<button type="button" class="answer" data-answer="${index}">${escapeHtml(answer)}</button>`
    ).join("");
    const stamp = data.showStamp
      ? `<button type="button" class="stamp" aria-label="Collect the falling potato stamp">🥔<span>bonus stamp! tap to grab</span></button>`
      : "";
    root.innerHTML = `
      <section class="quiz">
        <div class="hud"><span class="eyebrow">Interrogation ${data.step + 1} of ${data.total}</span><span class="wallet">Stamp wallet: ${data.stamps} 🥔</span></div>
        <div class="track" role="progressbar" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100"><div class="track-fill" style="width:${percent}%"></div></div>
        <div class="card"><h2>${escapeHtml(data.prompt)}</h2>${stamp}</div>
        <div class="answers">${options}</div>
        <p class="hint">Pick one. The potato tribunal is legally not a tribunal.</p>
      </section>`;
  }

  const answerButtons = root.querySelectorAll(".answer");
  answerButtons.forEach((button) => {
    button.onclick = () => {
      if (button.disabled) return;
      answerButtons.forEach((item) => { item.disabled = true; });
      button.classList.add("drop");
      answerButtons.forEach((item) => { if (item !== button) item.classList.add("fade"); });
      const delay = window.matchMedia("(prefers-reduced-motion: reduce)").matches ? 40 : 700;
      window.setTimeout(() => {
        window.scrollTo({ top: 0, behavior: "smooth" });
        setTriggerValue("answered", Number(button.dataset.answer));
      }, delay);
    };
  });

  const stampButton = root.querySelector(".stamp");
  if (stampButton) {
    stampButton.onclick = () => {
      if (stampButton.disabled) return;
      stampButton.disabled = true;
      stampButton.classList.add("picked");
      window.setTimeout(() => setTriggerValue("collected", data.step), 260);
    };
  }
}
"""

ANSWER_COMPONENT = st.components.v2.component(
    "potato_answer_flow",
    html=ANSWER_HTML,
    css=ANSWER_CSS,
    js=ANSWER_JS,
)


def reset_quiz() -> None:
    st.session_state.step = 0
    st.session_state.scores = {dimension: 0 for dimension in RESULTS}
    st.session_state.stamps = 0
    st.session_state.stamp_questions = []


if "step" not in st.session_state:
    reset_quiz()

st.title("🥔 What Kind of Potato Are You?")
st.caption("Answer quickly. A potato in a tiny hat is timing you.")

step = st.session_state.step
if step < len(QUESTIONS):
    question = QUESTIONS[step]
    show_stamp = step in (1, 3) and step not in st.session_state.stamp_questions
    answer_flow = ANSWER_COMPONENT(
        key="potato_answer_flow",
        data={
            "step": step,
            "total": len(QUESTIONS),
            "prompt": question["prompt"],
            "answers": [answer for answer, _dimension in question["answers"]],
            "stamps": st.session_state.stamps,
            "showStamp": show_stamp,
        },
        on_answered_change=lambda: None,
        on_collected_change=lambda: None,
    )

    if answer_flow.answered is not None:
        answer_index = int(answer_flow.answered)
        if 0 <= answer_index < len(question["answers"]):
            chosen_dimension = question["answers"][answer_index][1]
            st.session_state.scores[chosen_dimension] += 1
            st.session_state.step += 1
            st.rerun()

    if answer_flow.collected is not None:
        stamp_step = int(answer_flow.collected)
        if stamp_step in (1, 3) and stamp_step not in st.session_state.stamp_questions:
            st.session_state.stamp_questions.append(stamp_step)
            st.session_state.stamps += 1
            st.rerun()
else:
    winning_dimension = max(RESULTS, key=lambda dimension: st.session_state.scores[dimension])
    name, description, illustration = RESULTS[winning_dimension]
    st.progress(1.0)
    st.markdown("### The potato council has consulted the vibes")
    st.image(
        str(Path(__file__).parent / "assets" / "results" / illustration),
        width=380,
        alt=f"Hand-drawn potato illustration for {name}",
    )
    st.subheader(f"✨ {name}")
    st.write(description)
    if st.session_state.stamps == 2:
        st.success("Secret badge unlocked: **Certified Potato Evidence Collector** 🥔")
    else:
        st.caption(f"You rescued {st.session_state.stamps} of 2 falling potato stamps.")
    st.caption("Please allow 3–5 business potatoes for your crown to arrive.")
    if st.button("Get re-interrogated ↻", width="content"):
        reset_quiz()
        st.rerun()

st.caption("This quiz is not peer reviewed. It was reviewed by a potato.")
