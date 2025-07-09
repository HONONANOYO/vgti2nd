import streamlit as st

st.set_page_config(page_title="ベジタイプ16診断　2nd", page_icon="🥦")

# 初回アクセス時にページ状態を初期化
if "page" not in st.session_state:
    st.session_state.page = "question"

st.title("ベジタイプ16診断 2nd（12問版）")

# =========================
# ページ1：質問ページ
# =========================
if st.session_state.page == "question":

    # 質問内容
    questions = [
        {"q": "1日3食食べていますか？", "options": ["毎日３食", "２食以下になることが多い"]},
        {"q": "食事の時間は一定ですか？", "options": ["Yes", "No"]},
        {"q": "朝食を週にどのくらい食べますか？", "options": ["毎日", "週数回", "ほとんど食べない"]},
        {"q": "どこで食べることが多いですか？", "options": ["家", "外食"]},
        {"q": "外食のとき野菜を選びますか？", "options": ["Yes", "No"]},
        {"q": "外食の頻度は？", "options": ["週0回", "週1〜2回", "週3回以上"]},
        {"q": "野菜を食べるのに障壁を感じますか？", "options": ["Yes", "No"]},
        {"q": "野菜の価格が高いと感じますか？", "options": ["Yes", "No"]},
        {"q": "野菜の調理は面倒だと感じますか？", "options": ["Yes", "No"]},
        {"q": "野菜を意識して食べていますか？", "options": ["Yes", "No"]},
        {"q": "野菜は健康に必要だと思いますか？", "options": ["Yes", "No"]},
        {"q": "野菜は好きですか？", "options": ["Like", "Dislike"]},
    ]

    # 回答
    user_answers = []
    for i, q in enumerate(questions):
        answer = st.radio(q["q"], q["options"], key=f"q{i}")
        user_answers.append(answer)

    # ボタン押したら診断
    if st.button("診断する！"):
        answer_map = {
            "毎日３食": 1, "２食以下になることが多い": 0,
            "Yes": 1, "No": 0,
            "毎日": 1, "週数回": 0.5, "ほとんど食べない": 0,
            "家": 1, "外食": 0,
            "週0回": 1, "週1〜2回": 0.5, "週3回以上": 0,
            "Like": 1, "Dislike": 0,
        }

        user_vector = []
        for i, a in enumerate(user_answers):
            if i == 6 or i == 7:  # 障壁・価格
                user_vector.append(0 if a == "Yes" else 1)
            else:
                user_vector.append(answer_map[a])

        # タイプと理想ベクトル
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

        scores = []
        for ideal in ideal_vectors:
            match = 0
            for i in range(12):
                if abs(user_vector[i] - ideal[i]) == 0:
                    match += 1
                elif user_vector[i] == 0.5:
                    match += 0.5
            scores.append((match / 12) * 100)

        max_idx = scores.index(max(scores))
        st.session_state.result_type = types[max_idx]
        st.session_state.page = "result"
        st.rerun()

# =========================
# ページ2：診断結果ページ
# =========================
elif st.session_state.page == "result":
    result_type = st.session_state.result_type
    st.header("あなたの代表タイプは？")
    st.subheader(f"**{result_type} タイプ**")

    # 画像表示（ルート直下にファイルがある前提）
    image_file = f"{result_type.lower()}.png"
    try:
        st.image(image_file, caption=f"{result_type} タイプ", use_column_width=True)
    except:
        st.warning("画像が見つかりませんでした。")

    st.subheader("診断結果スコアは非表示にしました")
    st.markdown(
        "アンケートご協力お願いします！： [アンケートフォーム](https://docs.google.com/forms/d/e/1FAIpQLSfMbMGtTDsTk-f8VTxYseqijcZDyrIfZKyf9e-ryCThoHxVag/viewform)",
        unsafe_allow_html=True
    )
