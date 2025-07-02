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

# 逆頭文字
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
# ページ1: Likert詳細質問
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
            "小さい頃からの習慣だから三食食べている",
            "自分で意識して三食食べている",
            "健康のために三食食べている",
            "なんとなく三食食べている"
        ]):
            val = st.slider(q, -3, 3, 0, 1, format="%d", key=f"r{i}")
            st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
            st.session_state.answers[f"r{i}"] = val

        st.markdown("### 🍅 2. 食べる場所について")
        for i, q in enumerate([
            "家で食べることが多い",
            "家族が作ってくれるから家で食べる",
            "健康に良いから家で食べる",
            "落ち着けるから家で食べる"
        ]):
            val = st.slider(q, -3, 3, 0, 1, format="%d", key=f"h{i}")
            st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
            st.session_state.answers[f"h{i}"] = val

        st.markdown("### 🍅 3. 野菜の障壁について")
        for i, q in enumerate([
            "野菜は手軽に買える",
            "野菜を調理しやすい",
            "野菜が好き",
            "野菜を食べるのが習慣になっている"
        ]):
            val = st.slider(q, -3, 3, 0, 1, format="%d", key=f"f{i}")
            st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
            st.session_state.answers[f"f{i}"] = val

        st.markdown("### 🍅 4. 野菜の嗜好について")
        for i, q in enumerate([
            "野菜をおいしいと思う",
            "育てた経験があるので親しみがある",
            "健康のために野菜を意識している",
            "なんとなく野菜を食べている"
        ]):
            val = st.slider(q, -3, 3, 0, 1, format="%d", key=f"l{i}")
            st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
            st.session_state.answers[f"l{i}"] = val

        submitted = st.form_submit_button("診断結果を見る")
        if submitted:
            st.session_state.page = 2

# -------------------
# ページ2: 診断結果
# -------------------
elif st.session_state.page == 2:
    code = st.session_state.vgti_code
    char4 = list(code)

    answers = st.session_state.answers

    r_score = sum(answers[f"r{i}"] for i in range(4))
    h_score = sum(answers[f"h{i}"] for i in range(4))
    f_score = sum(answers[f"f{i}"] for i in range(4))
    l_score = sum(answers[f"l{i}"] for i in range(4))

    axis_scores = {
        "R": (r_score + 12) / 24 * 100,
        "H": (h_score + 12) / 24 * 100,
        "F": (f_score + 12) / 24 * 100,
        "L": (l_score + 12) / 24 * 100
    }

    # 逆文字変換
    final_code = []
    revised = []
    for idx, letter in enumerate(char4):
        score = axis_scores[letter]
        if score < 60:
            final_code.append(opposite_letter[letter])
            revised.append((letter, opposite_letter[letter]))
        else:
            final_code.append(letter)

    final_type = "".join(final_code)

    st.subheader("🍅 診断結果まとめ")
    for key, val in axis_scores.items():
        st.write(f"{letter_meaning[key]}: {val:.1f}%")
        st.progress(val/100)

    st.markdown("---")
    st.write(f"**前回のキャラクター:** {code}")  
    st.write(f"**今回の再確認後の提案キャラクター:** {final_type}")

    if revised:
        st.warning("以下の項目について逆の頭文字がより合う可能性があります。")
        for before, after in revised:
            st.write(f"- {letter_meaning[before]} → {letter_meaning[after]}")

    if st.button("もう一度診断する"):
        st.session_state.page = 0
        st.session_state.answers = {}
