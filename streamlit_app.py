import streamlit as st

st.title("VGTI 2nd 診断")

if "page" not in st.session_state:
    st.session_state.page = 0

# 頭文字の意味
letter_meaning = {
    "R": "生活リズム",
    "I": "不規則性",
    "H": "食事スタイル（家食）",
    "E": "食事スタイル（外食）",
    "F": "野菜摂取障壁が低い",
    "B": "野菜摂取障壁が高い",
    "L": "野菜への意識が高い",
    "D": "野菜への意識が低い"
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

# 日本語5段階ラベル
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
        st.markdown("### 🍅 1. 生活リズムについて")
        for i, q in enumerate([
            "小さい頃からの習慣で三食食べている",
            "自分で意識して三食食べている",
            "健康のために三食食べている",
            "なんとなく三食食べている"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"r{i}")
            st.session_state.answers[f"r{i}"] = labels[selected]

        st.markdown("### 🍅 2. 食事スタイルについて")
        for i, q in enumerate([
            "家で食べることが多い",
            "家族が作ってくれるから家で食べる",
            "健康に良いから家で食べる",
            "落ち着けるから家で食べる"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"h{i}")
            st.session_state.answers[f"h{i}"] = labels[selected]

        st.markdown("### 🍅 3. 野菜摂取障壁について")
        for i, q in enumerate([
            "野菜は手軽に買える",
            "野菜を調理しやすい",
            "野菜が好き",
            "野菜を食べるのが習慣になっている"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"f{i}")
            st.session_state.answers[f"f{i}"] = labels[selected]

        st.markdown("### 🍅 4. 野菜への意識について")
        for i, q in enumerate([
            "野菜をおいしいと思う",
            "育てた経験があるので親しみがある",
            "健康のために野菜を意識している",
            "なんとなく野菜を食べている"
        ]):
            selected = st.radio(q, list(labels.keys()), key=f"l{i}")
            st.session_state.answers[f"l{i}"] = labels[selected]

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

    # 5段階×4問 → 最小4, 最大20
    axis_scores = {
        "生活リズム": (r_score - 4) / 16 * 100,
        "食事スタイル": (h_score - 4) / 16 * 100,
        "野菜摂取障壁": (f_score - 4) / 16 * 100,
        "野菜への意識": (l_score - 4) / 16 * 100
    }

    # 逆文字判定
    final_code = []
    revised = []
    for idx, letter in enumerate(char4):
        # char4はR/H/F/Lなので日本語に合わせてスコア取る
        if letter == "R":
            score = axis_scores["生活リズム"]
        elif letter == "H":
            score = axis_scores["食事スタイル"]
        elif letter == "F":
            score = axis_scores["野菜摂取障壁"]
        elif letter == "L":
            score = axis_scores["野菜への意識"]
        else:
            score = 50  # 万一の場合

        if score < 60:
            final_code.append(opposite_letter[letter])
            revised.append((letter_meaning[letter], letter_meaning[opposite_letter[letter]]))
        else:
            final_code.append(letter)

    final_type = "".join(final_code)

    st.subheader("🍅 診断結果まとめ")
    for key, val in axis_scores.items():
        st.write(f"{key}: {val:.1f}%")
        st.progress(val/100)

    st.markdown("---")
    st.write(f"**前回のキャラクター:** {code}")  
    st.write(f"**今回の再確認後の提案キャラクター:** {final_type}")

    if revised:
        st.warning("以下の項目について逆の頭文字がより合う可能性があります。")
        for before, after in revised:
            st.write(f"- {before} → {after}")

    if st.button("もう一度診断する"):
        st.session_state.page = 0
        st.session_state.answers = {}
