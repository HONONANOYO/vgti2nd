import streamlit as st

st.title("VGTI 2nd 診断")

if "page" not in st.session_state:
    st.session_state.page = 0

# 5段階ラベル
labels = {
    "まったくそう思わない": 1,
    "あまりそう思わない": 2,
    "どちらでもない": 3,
    "そう思う": 4,
    "とてもそう思う": 5
}

# 頭文字の説明
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

# 質問セット
questions = {
    "R": [
        "小さい頃からの習慣だから三食食べている",
        "自分で意識して三食食べている",
        "健康のために三食食べている",
        "なんとなく三食食べている"
    ],
    "I": [
        "好きな食べ物がないから三食食べていない",
        "食べる必要性を感じない",
        "食べる時間がない",
        "金銭的に余裕がない"
    ],
    "H": [
        "家で食べるのは安いから",
        "家族が作ってくれるから家で食べる",
        "健康に良いから家で食べる",
        "落ち着けるから家で食べる"
    ],
    "E": [
        "料理をするのが面倒だから外で食べる",
        "外食の方がおいしいから外で食べる",
        "買って食べる方が楽だから外で食べる",
        "気分を変えたいから外で食べる"
    ],
    "F": [
        "もともと野菜が好きだから野菜を食べる",
        "家族が作ってくれるから野菜を食べる",
        "野菜を手軽に買えるから食べる",
        "野菜を食べるのが習慣になっている"
    ],
    "B": [
        "野菜を買うのにお金がかかるからあまり食べない",
        "野菜を調理する時間がないからあまり食べない",
        "野菜の味が苦手であまり食べない",
        "野菜の必要性を感じない"
    ],
    "L": [
        "野菜をおいしいと思う",
        "育てた経験があるので親しみがある",
        "健康に良いから積極的に食べている",
        "なんとなく野菜を食べる"
    ],
    "D": [
        "野菜の味が苦手で意識して食べない",
        "食感が苦手で意識して食べない",
        "においが苦手で意識して食べない",
        "なんとなく気が向かない"
    ]
}

# ページ0: タイプ選択
if st.session_state.page == 0:
    st.subheader("VGTIタイプ選択")
    with st.form("vgti_form"):
        vgti_code = st.selectbox(
            "前回診断で出たあなたのVGTIタイプを選んでください",
            [
                "RHFL", "RHFD", "RHBL", "RHBD",
                "REFL", "REFD", "REBL", "REBD",
                "IHFL", "IHFD", "IHBL", "IHBD",
                "IEFL", "IEFD", "IEBL", "IEBD"
            ]
        )
        submitted = st.form_submit_button("次へ")
        if submitted:
            st.session_state.vgti_code = vgti_code
            st.session_state.page = 1

# ページ1: Likert質問
elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    char4 = list(code)

    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    with st.form("likert_form"):
        for idx, letter in enumerate(char4):
            st.markdown(f"### 🍅 {letter_meaning[letter]}について")
            for q_idx, q in enumerate(questions[letter]):
                ans = st.radio(q, list(labels.keys()), key=f"{letter}_{q_idx}")
                st.session_state.answers[f"{letter}{q_idx}"] = labels[ans]
        submitted = st.form_submit_button("診断結果を見る")
        if submitted:
            st.session_state.page = 2

# ページ2: 診断結果
elif st.session_state.page == 2:
    code = st.session_state.vgti_code
    char4 = list(code)
    answers = st.session_state.answers

    # 各軸の合計スコア
    scores = {}
    for letter in char4:
        score = sum(answers[f"{letter}{i}"] for i in range(4))
        # 4問×5点 → max20
        percent = (score - 4) / 16 * 100
        scores[letter] = percent

    # 逆タイプ判定
    opposite_letter = {
        "R": "I", "I": "R",
        "H": "E", "E": "H",
        "F": "B", "B": "F",
        "L": "D", "D": "L"
    }
    revised = []
    final_code = []
    for letter in char4:
        if scores[letter] < 60:
            new_letter = opposite_letter[letter]
            final_code.append(new_letter)
            revised.append((letter_meaning[letter], letter_meaning[new_letter]))
        else:
            final_code.append(letter)

    final_type = "".join(final_code)

    st.subheader("🍅 診断結果まとめ")
    for letter in char4:
        st.write(f"{letter_meaning[letter]}: {scores[letter]:.1f}%")
        st.progress(scores[letter]/100)

    st.markdown("---")
    st.write(f"**前回のキャラクター:** {code}")
    st.write(f"**今回の再確認後の提案キャラクター:** {final_type}")

    if revised:
        st.warning("以下の項目は逆タイプのほうが合う可能性があります👇")
        for before, after in revised:
            st.write(f"- {before} → {after}")

    if st.button("もう一度診断する"):
        st.session_state.page = 0
        st.session_state.answers = {}
