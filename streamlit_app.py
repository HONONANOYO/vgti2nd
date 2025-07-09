import streamlit as st
import pandas as pd
import math

st.set_page_config(page_title="ベジタイプ16診断　2nd", page_icon="🥦")

if "page" not in st.session_state:
    st.session_state.page = "question"

st.title("ベジタイプ16診断 2nd（12問版）")

# =========================
# 質問ページ
# =========================
if st.session_state.page == "question":

    questions = [
        {"q": "1日3食食べていますか？", "options": ["毎日３食", "２食以下になることが多い"]},
        {"q": "食事の時間は一定ですか？", "options": ["Yes", "No"]},
        {"q": "朝食を週にどのくらい食べますか？", "options": ["毎日", "週数回", "ほとんど食べない"]},
        {"q": "どこで食べることが多いですか？", "options": ["家", "外食"]},
        {"q": "外食のとき野菜を選びますか？", "options": ["Yes", "No"]},
        {"q": "外食の頻度は？", "options": ["週0回", "週1〜2回", "週3回以上"]},
        {"q": "野菜を毎日食べるのは難しいと感じますか？", "options": ["Yes", "No"]},
        {"q": "野菜の価格が高いと感じますか？", "options": ["Yes", "No"]},
        {"q": "野菜よりも満足感のある食べ物を優先してしまいがちですか？", "options": ["Yes", "No"]},
        {"q": "野菜を意識して食べていますか？", "options": ["Yes", "No"]},
        {"q": "野菜は健康に必要だと思いますか？", "options": ["Yes", "No"]},
        {"q": "野菜は好きですか？", "options": ["Like", "Dislike"]},
    ]

    user_answers = []
    for i, q in enumerate(questions):
        answer = st.radio(q["q"], q["options"], key=f"q{i}")
        user_answers.append(answer)

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
            if i in [6, 7, 8]:  # Q7〜Q9（障壁系）：Yes→0, No→1
                user_vector.append(0 if a == "Yes" else 1)
            else:
                user_vector.append(answer_map[a])

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

        max_distance = math.sqrt(12)
        scores = []
        for ideal in ideal_vectors:
            dist = sum((user_vector[i] - ideal[i]) ** 2 for i in range(12))
            dist = math.sqrt(dist)
            score = 100 - (dist / max_distance) * 100
            scores.append(round(score, 2))

        max_idx = scores.index(max(scores))
        st.session_state.result_type = types[max_idx]
        st.session_state.scores = scores
        st.session_state.types = types
        st.session_state.page = "result"
        st.rerun()

# =========================
# 結果ページ
# =========================
elif st.session_state.page == "result":
    result_type = st.session_state.result_type
    scores = st.session_state.scores
    types = st.session_state.types

    st.header("あなたの代表タイプは？")
    st.subheader(f"**{result_type} タイプ**")

    col1, col2 = st.columns([1, 2])

    with col1:
        image_file = f"{result_type.lower()}.png"
        try:
            st.image(image_file, caption=f"{result_type} タイプ", use_container_width=True)
        except:
            st.warning("画像が見つかりませんでした。")

    with col2:
        st.subheader("全タイプとの一致スコア")
        df = pd.DataFrame({
            "タイプ": types,
            "一致度（%）": scores
        }).sort_values(by="一致度（%）", ascending=False)
        st.dataframe(df.reset_index(drop=True), use_container_width=True)

    st.markdown(
        "アンケートご協力お願いします！： [アンケートフォーム](https://docs.google.com/forms/d/e/1FAIpQLSfMbMGtTDsTk-f8VTxYseqijcZDyrIfZKyf9e-ryCThoHxVag/viewform)",
        unsafe_allow_html=True
    )
