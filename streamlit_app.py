import streamlit as st

st.set_page_config(page_title="ベジタイプ16診断", page_icon="🥦")

st.title("ベジタイプ16診断（12問版）")

# =========================
# 12問の質問
# =========================
questions = [
    {"q": "1日3食食べていますか？", "options": ["Regular", "Irregular"]},
    {"q": "食事の時間は一定ですか？", "options": ["Yes", "No"]},
    {"q": "朝食を週にどのくらい食べますか？", "options": ["毎日", "週数回", "ほとんど食べない"]},
    {"q": "家で食べることが多いですか？", "options": ["Home", "Eat out"]},
    {"q": "外食のとき野菜を選びますか？", "options": ["Yes", "No"]},
    {"q": "外食の頻度は？", "options": ["週0回", "週1〜2回", "週3回以上"]},
    {"q": "野菜を食べるのに障壁を感じますか？", "options": ["Free", "Barrier"]},
    {"q": "野菜の価格が高いと感じますか？", "options": ["No", "Yes"]},
    {"q": "野菜の調理は面倒だと感じますか？", "options": ["No", "Yes"]},
    {"q": "野菜を意識して食べていますか？", "options": ["Yes", "No"]},
    {"q": "野菜は健康に必要だと思いますか？", "options": ["Yes", "No"]},
    {"q": "野菜は好きですか？", "options": ["Like", "Dislike"]},
]

# =========================
# 回答受付
# =========================
user_answers = []

for i, q in enumerate(questions):
    answer = st.radio(q["q"], q["options"], key=i)
    user_answers.append(answer)

# =========================
# 診断ボタン
# =========================
if st.button("診断する！"):
    # 回答を数値に変換
    answer_map = {
        "Regular": 1, "Irregular": 0,
        "Yes": 1, "No": 0,
        "毎日": 1, "週数回": 0.5, "ほとんど食べない": 0,
        "Home": 1, "Eat out": 0,
        "週0回": 1, "週1〜2回": 0.5, "週3回以上": 0,
        "Free": 1, "Barrier": 0,
        "Like": 1, "Dislike": 0,
    }
    user_vector = [answer_map[a] for a in user_answers]

    # =========================
    # 16タイプの理想ベクトル
    # =========================
    types = [
        "RHFL", "RHFD", "RHBL", "RHBD",
        "REFL", "REFD", "REBL", "REBD",
        "IHFL", "IHFD", "IHBL", "IHBD",
        "IEFL", "IEFD", "IEBL", "IEBD"
    ]

    ideal_vectors = [
        [1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,0,0,0],
        [1,1,1,1,1,1,0,0,0,1,1,1],
        [1,1,1,1,1,1,0,0,0,0,0,0],
        [1,1,1,0,0,0,1,1,1,1,1,1],
        [1,1,1,0,0,0,1,1,1,0,0,0],
        [1,1,1,0,0,0,0,0,0,1,1,1],
        [1,1,1,0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1],
        [0,0,0,1,1,1,1,1,1,0,0,0],
        [0,0,0,1,1,1,0,0,0,1,1,1],
        [0,0,0,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,1,1,1],
        [0,0,0,0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0],
    ]

    # =========================
    # 一致率計算
    # =========================
    scores = []
    for ideal in ideal_vectors:
        # 12問中一致している項目の割合
        match = 0
        for i in range(12):
            # 週数回や週1〜2回は0.5なので近い方に0.5点
            if abs(user_vector[i] - ideal[i]) == 0:
                match += 1
            elif user_vector[i] == 0.5 and ideal[i] == 1:
                match += 0.5
            elif user_vector[i] == 0.5 and ideal[i] == 0:
                match += 0.5
        percent = (match/12)*100
        scores.append(percent)

    # =========================
    # 表示
    # =========================
    st.subheader("診断結果")
    for t, s in zip(types, scores):
        st.write(f"**{t}度：{s:.1f}%**")

    # 代表タイプ
    max_idx = scores.index(max(scores))
    st.success(f"あなたの代表タイプは **{types[max_idx]}** です！")

