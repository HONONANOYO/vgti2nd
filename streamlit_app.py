import streamlit as st

st.title("VGTI 2nd 診断")

if "page" not in st.session_state:
    st.session_state.page = 0

# 頭文字の意味
letter_meaning = {
    "R": "規則性",
    "I": "不規則性",
    "H": "家食",
    "E": "外食",
    "F": "障壁少",
    "B": "障壁多",
    "L": "意識高",
    "D": "意識低"
}

# 逆文字
opposite_letter = {
    "R": "I",
    "I": "R",
    "H": "E",
    "E": "H",
    "F": "B",
    "B": "F",
    "L": "D",
    "D": "L"
}

vgti_options = [
    "RHFL", "RHFD", "RHBL", "RHBD",
    "REFL", "REFD", "REBL", "REBD",
    "IHFL", "IHFD", "IHBL", "IHBD",
    "IEFL", "IEFD", "IEBL", "IEBD"
]

# 日本語ラベル5段階
labels = {
    "まったくそう思わない": 1,
    "あまりそう思わない": 2,
    "どちらでもない": 3,
    "ややそう思う": 4,
    "とてもそう思う": 5
}

# -------------------
# ページ0: キャラクター選択
# -------------------
if st.session_state.page == 0:
    st.subheader("VGTIタイプ選択")
    with st.form("vgti_form"):
        vgti_code = st.selectbox(
            "前回の診断で出たあなたのVGTIタイプを選んでください",
            options=vgti_options
        )
        submitted = st.form_submit_button("次へ")
        if submitted:
            st.session_state.vgti_code = vgti_code
            st.session_state.page = 1

# -------------------
# ページ1: 詳細質問
# -------------------
elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    with st.form("likert_form"):
        st.markdown("### 🍅 1. 食事の規則性について")
        for i, q in enumerate([
            "小さい頃からの習慣で三食食べている",
            "自分で意識して三食食べている",
            "健康のために三食食べている",
            "なんとなく三食食べている"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"r{i}")
            st.session_state.answers[f"r{i}"] = labels[selected]

        st.markdown("### 🍅 2. 食べる場所について")
        for i, q in enumerate([
            "家で食べることが多い",
            "家族が作ってくれるから家で食べる",
            "健康に良いから家で食べる",
            "落ち着けるから家で食べる"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"h{i}")
            st.session_state.answers[f"h{i}"] = labels[selected]

        st.markdown("### 🍅 3. 野菜の障壁について")
        for i, q in enumerate([
            "野菜は手軽に買える",
            "野菜を調理しやすい",
