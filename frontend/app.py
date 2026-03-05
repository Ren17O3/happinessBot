import streamlit as st
import requests
import plotly.graph_objects as go

# ------------------------------------------------
# Page config
# ------------------------------------------------
API_URL = "https://happinessbot.onrender.com"
st.set_page_config(
    page_title="Couple Compatibility Analyzer",
    page_icon="💑",
    layout="wide"
)

# ------------------------------------------------
# Custom CSS
# ------------------------------------------------

st.markdown("""
<style>

.main-title {
    font-size:40px;
    font-weight:700;
    text-align:center;
}

.subtitle {
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# Header
# ------------------------------------------------

st.markdown(
    """
    <h1 style='text-align:center; font-size:60px; margin-bottom:10px;'>
    Couple Compatibility Analyzer
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown('<p class="subtitle">Analyze relationship alignment using AI insights</p>', unsafe_allow_html=True)

# ------------------------------------------------
# Session State
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = "A"

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = False

if "partner_a" not in st.session_state:
    st.session_state.partner_a = None

if "partner_b" not in st.session_state:
    st.session_state.partner_b = None

if "results" not in st.session_state:
    st.session_state.results = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------
# Questions
# ------------------------------------------------

questions = [
"I feel emotionally connected to my partner.",
"Thinking about my partner usually makes me happy.",
"I feel comfortable sharing my emotions with my partner.",
"I feel secure in this relationship.",

"My partner listens carefully when I speak.",
"We communicate openly about our feelings.",
"I feel understood after talking to my partner.",
"We can discuss difficult topics respectfully.",

"I trust my partner with my personal thoughts.",
"My partner supports me during difficult times.",
"I feel safe being my true self with my partner.",
"My partner respects my opinions.",

"We resolve disagreements calmly.",
"We try to understand each other during conflicts.",
"Small issues rarely turn into big fights.",
"We forgive each other after arguments.",

"I am satisfied with my relationship.",
"I feel valued by my partner.",
"My relationship improves my overall happiness.",
"I believe our relationship has a healthy future."
]

# ------------------------------------------------
# Questionnaire
# ------------------------------------------------

if st.session_state.step in ["A","B"] and not st.session_state.chat_mode:

    st.subheader("Relationship Questionnaire")

    if st.session_state.step == "A":
        st.info("Partner A should answer the questions independently.")

    if st.session_state.step == "B":
        st.info("Partner B should now answer the same questions.")

    answers = []
    total_questions = len(questions)


    for i,q in enumerate(questions):

        st.caption(f"Question {i+1} of {total_questions}")

        score = st.slider(
            q,
            1,
            5,
            3,
            key=f"{st.session_state.step}_{i}"
        )
        answers.append(score)

    if st.session_state.step == "A":

        if st.button("Submit Partner A"):
            st.session_state.partner_a = answers
            st.session_state.step = "B"
            st.rerun()

    elif st.session_state.step == "B":

        if st.button("Submit Partner B"):
            st.session_state.partner_b = answers
            st.session_state.step = "RESULT"
            st.rerun()

# ------------------------------------------------
# Compatibility Calculation
# ------------------------------------------------

if st.session_state.step == "RESULT" and not st.session_state.results:

    A = st.session_state.partner_a
    B = st.session_state.partner_b

    compatibility_scores = []

    for i in range(len(A)):
        diff = abs(A[i] - B[i])
        compatibility = 5 - diff
        compatibility_scores.append(compatibility)

    overall = sum(compatibility_scores)/(len(compatibility_scores)*5)*100

    response = requests.post(
        f"{API_URL}/submit",
        json={"answers":compatibility_scores}
    )

    st.session_state.results = response.json()
    st.session_state.overall = overall

# ------------------------------------------------
# RESULTS DASHBOARD
# ------------------------------------------------

if st.session_state.results and not st.session_state.chat_mode:

    result = st.session_state.results
    scores = result["scores"]
    insights = result["insights"]
    overall = st.session_state.overall

    st.divider()

    col1,col2 = st.columns([1,2])

    with col1:

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=overall,
            gauge={
                'axis': {'range': [0,100]},
                'steps': [
                    {'range':[0,50],'color':"#ff6b6b"},
                    {'range':[50,75],'color':"#ffd166"},
                    {'range':[75,100],'color':"#06d6a0"}
                ],
                'bar':{'color':"#ffffff"}
            }
        ))

        fig.update_layout(height=300)
        st.plotly_chart(fig,use_container_width=True)

    with col2:

        st.subheader("Compatibility Insights")

        c1,c2,c3 = st.columns(3)

        with c1:
            with st.container(border=True):
                st.markdown("### 💡 Strength")
                st.write(insights["strength"])

        with c2:
            with st.container(border=True):
                st.markdown("### ⚠ Focus Area")
                st.write(insights["focus_area"])

        with c3:
            with st.container(border=True):
                st.markdown("### 🚀 Suggestion")
                st.write(insights["suggestion"])

    st.divider()

    left,right = st.columns([1.3,1])

    with left:

        categories = [
            "Emotional",
            "Communication",
            "Trust",
            "Conflict",
            "Satisfaction"
        ]

        values = [
            scores["emotional"],
            scores["communication"],
            scores["trust"],
            scores["conflict"],
            scores["satisfaction"]
        ]

        values += values[:1]
        categories += categories[:1]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(range=[0,100])),
            showlegend=False
        )

        st.subheader("Compatibility Radar")
        st.plotly_chart(fig,use_container_width=True)

    with right:

        st.subheader("Relationship Dimensions")

        st.progress(scores["emotional"]/100)
        st.caption(f"Emotional Connection: {scores['emotional']}%")

        st.progress(scores["communication"]/100)
        st.caption(f"Communication: {scores['communication']}%")

        st.progress(scores["trust"]/100)
        st.caption(f"Trust: {scores['trust']}%")

        st.progress(scores["conflict"]/100)
        st.caption(f"Conflict Resolution: {scores['conflict']}%")

        st.progress(scores["satisfaction"]/100)
        st.caption(f"Satisfaction: {scores['satisfaction']}%")

# ------------------------------------------------
# CHAT MODE
# ------------------------------------------------

# ------------------------------------------------
# CHAT MODE
# ------------------------------------------------

if st.session_state.results:

    scores = st.session_state.results["scores"]

    st.divider()
    st.subheader("💬 Relationship Chat Assistant")

    if st.button("Switch to Chat Mode"):
        st.session_state.chat_mode = True
        st.rerun()

    if st.session_state.chat_mode:

        if st.button("⬅ Back to Analysis"):
            st.session_state.chat_mode = False
            st.rerun()

        # Initialize suggested question holder
        if "suggested_question" not in st.session_state:
            st.session_state.suggested_question = None

        # Suggested questions (only show if no conversation yet)
        if len(st.session_state.messages) == 0:

            st.subheader("Suggested Questions")

            col1, col2, col3 = st.columns(3)

            if col1.button("How can we improve communication?"):
                st.session_state.suggested_question = "How can we improve communication?"

            if col2.button("Why do we argue about small things?"):
                st.session_state.suggested_question = "Why do we argue about small things?"

            if col3.button("How can we strengthen our relationship?"):
                st.session_state.suggested_question = "How can we strengthen our relationship?"

        # Chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Normal chat input always visible
        chat_input = st.chat_input("Ask about your relationship...")

        # Determine user message
        user_input = None

        if st.session_state.suggested_question:
            user_input = st.session_state.suggested_question
            st.session_state.suggested_question = None

        elif chat_input:
            user_input = chat_input

        # Process message
        if user_input:

            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })

            with st.chat_message("user"):
                st.markdown(user_input)

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "message": user_input,
                    "scores": scores,
                    "mode": "chat"
                }
            )

            bot_reply = response.json()["reply"]

            st.session_state.messages.append({
                "role": "assistant",
                "content": bot_reply
            })

            with st.chat_message("assistant"):
                st.markdown(bot_reply)