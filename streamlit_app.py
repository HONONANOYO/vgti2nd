import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VGTI診断　２nd", page_icon="🍅🍅")

# 初期状態の設定
if "page" not in st.session_state:
    st.session_state.page = "question"

st.title("ベジタイプ16診断")

# 質問と選択肢の定義
questions = [
    # R/I
    {"q": "1日3食食べていますか？", "options": ["はい", "いいえ"]},
    {"q": "食事の時間は一定ですか？", "options": ["はい", "いいえ"]},
    {"q": "朝食を週にどのくらい食べますか？", "options": ["毎日", "週数回", "ほとんど食べない"]},
    # H/E
    {"q": "週3回以上外食していますか？", "options": ["はい", "いいえ"]},
    {"q": "あなたが野菜を摂る機会が多いのはどこですか？", "options": ["家", "外食", "ほとんど食べない"]},
    # F/B
    {"q": "野菜の価格が高いと感じますか？", "options": ["はい", "いいえ"]},
    {"q": "野菜を毎日食べるのは難しいと感じますか？", "options": ["はい", "いいえ"]},
    {"q": "野菜を食べても満足感が得られないと感じますか？（※野菜よりおなかにたまりやすい食事を選んでしまう）", "options": ["はい", "いいえ"]},
    # L/D
    {"q": "1日1回以上野菜を食べていますか？", "options": ["はい", "いいえ"]},
    {"q": "野菜は健康にいいから食べていますか？", "options": ["はい", "いいえ"]},
    {"q": "野菜は好きですか？", "options": ["はい", "いいえ"]},
    {"q": "野菜を食べると気分や体調がよくなると感じますか？", "options": ["はい", "いいえ"]},
]

# 回答ページ
if st.session_state.page == "question":
    answers = []
    for i, item in enumerate(questions):
        a = st.radio(item["q"], item["options"], key=f"q{i}")
        answers.append(a)

    if st.button("診断する！"):
        score_vector = []
        for i, ans in enumerate(answers):
            if i == 2:  # 朝食頻度
                score_vector.append({"毎日": 1, "週数回": 0.5, "ほとんど食べない": 0}[ans])
            elif i == 4:  # 野菜を摂る場所
                score_vector.append({"家": 1, "外食": 0.5, "ほとんど食べない": 0}[ans])
            else:
                score_vector.append(1 if ans == "はい" else 0)

        # 全16タイプと理想ベクトル
        ideal_vectors, types = [], []
        for r in "RI":
            for h in "HE":
                for f in "FB":
                    for l in "LD":
                        types.append(r + h + f + l)
                        vec = []
                        vec += [1,1,1] if r=="R" else [0,0,0]
                        vec += [1,1] if h=="H" else [0,0]
                        vec += [1,1,1] if f=="F" else [0,0,0]
                        vec += [1,1,1,1] if l=="L" else [0,0,0,0]
                        ideal_vectors.append(vec)

        # 距離ベーススコア計算
        scores = []
        for ideal in ideal_vectors:
            dist = np.linalg.norm(np.array(score_vector) - np.array(ideal))
            similarity = (1 - dist / np.sqrt(len(ideal))) * 100
            scores.append(similarity)

        st.session_state.result_type = types[np.argmax(scores)]
        st.session_state.result_scores = list(zip(types, scores))
        st.session_state.page = "result"
        st.rerun()

# 結果ページ
elif st.session_state.page == "result":
    t = st.session_state.result_type
    st.header(f"{t} タイプ")

    col1, col2 = st.columns([1, 2])
    with col1:
        try:
            st.image(f"{t.lower()}.png", caption=f"{t} タイプ", use_container_width=True)
        except:
            st.warning("画像が見つかりませんでした")

    with col2:
        st.subheader("全タイプとの一致スコア")
        df = pd.DataFrame(st.session_state.result_scores, columns=["タイプ", "一致度（%）"])
        st.dataframe(df.sort_values(by="一致度（%）", ascending=False).reset_index(drop=True))

    st.markdown("---")
   
