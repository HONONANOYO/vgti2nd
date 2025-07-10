import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VGTI診断　２nd", page_icon="🍅🍅")
st.write("これは最新版です！！")

# 初期状態の設定
if "page" not in st.session_state:
    st.session_state.page = "question"

st.title("ベジタイプ16診断")

# 質問と選択肢の定義（最新版 12問）
questions = [
    # R/I
    {"q": "1日3食食べていますか？", "options": ["はい", "いいえ"]},
    {"q": "食事の時間は一定ですか？", "options": ["はい", "いいえ"]},
    {"q": "朝食を週にどのくらい食べますか？", "options": ["毎日", "週数回", "ほとんど食べない"]},
    {"q": "1日1回以上野菜を食べていますか？", "options": ["はい", "いいえ"]},

    # H/E（1問のみ）
    {"q": "週3回以上外食していますか？", "options": ["はい", "いいえ"]},

    # F/B
    {"q": "野菜の価格が高いと感じますか？", "options": ["はい", "いいえ"]},
    {"q": "毎日野菜を食べていますか？", "options": ["はい", "いいえ"]},
    {"q": "野菜を食べても満足感が得られないと感じますか？（※野菜よりおなかにたまりやすい食事を選んでしまう）", "options": ["はい", "いいえ"]},

    # L/D
    {"q": "意識的に野菜を摂取していますか？", "options": ["はい", "いいえ"]},
    {"q": "健康のために野菜を食べることはありますか？", "options": ["はい", "いいえ"]},
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
            if i == 2:  # 朝食頻度（R/I）
                score_vector.append({"毎日": 1, "週数回": 0.5, "ほとんど食べない": 0}[ans])
            elif i == 4:  # H/E（外食頻度のみ）
                score_vector.append(0 if ans == "はい" else 1)
            else:
                score_vector.append(1 if ans == "はい" else 0)

        # 全16タイプの理想ベクトルを作成
        ideal_vectors, types = [], []
        for r in "RI":
            for h in "HE":
                for f in "FB":
                    for l in "LD":
                        types.append(r + h + f + l)
                        vec = []
                        vec += [1,1,1,1] if r=="R" else [0,0,0,0]       # R/I（4問）
                        vec += [1] if h=="H" else [0]                   # H/E（1問）
                        vec += [1,1,1] if f=="F" else [0,0,0]           # F/B（3問）
                        vec += [1,1,1,1] if l=="L" else [0,0,0,0]       # L/D（4問）
                        ideal_vectors.append(vec)

        # スコア計算（パーセンテージに変換）
        scores = []
        for ideal in ideal_vectors:
            match = sum([1 if a == b else 0 for a, b in zip(score_vector, ideal)])
            mismatch_count = sum([1 for a, b in zip(score_vector, ideal) if a != b])
            similarity = match - (mismatch_count * 0.01)
            scores.append(similarity)

        percentage_scores = [(t, round((s / 12) * 100, 1)) for t, s in zip(types, scores)]
        st.session_state.result_type = types[np.argmax(scores)]
        st.session_state.result_scores = percentage_scores
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
        st.subheader("全タイプとの一致スコア（%）")
        df = pd.DataFrame(st.session_state.result_scores, columns=["タイプ", "一致度（%）"])
        st.dataframe(df.sort_values(by="一致度（%）", ascending=False).reset_index(drop=True))


    st.subheader("全体像はこちらです。")
    try:
        st.image("vgti_map.png", caption="ベジタイプ16 全体マップ", use_container_width=True)
    except:
        st.warning("全体マップ画像が見つかりませんでした")

    st.markdown("---")
    if st.button("もう一度診断する"):
        st.session_state.page = "question"
        st.rerun()

    st.markdown("---")
    if st.button("もう一度診断する"):
        st.session_state.page = "question"
        st.rerun()
