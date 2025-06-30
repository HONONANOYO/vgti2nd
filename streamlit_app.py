import streamlit as st

st.title("VGTI 2nd 診断 - 7段階ラベル版")

# ページ管理
if "page" not in st.session_state:
    st.session_state.page = 0

# VGTIタイプ選択
vgti_options = [
    "RHFL", "RHFD", "RHBL", "RHBD",
    "REFL", "REFD", "REBL", "REBD",
    "IHFL", "IHFD", "IHBL", "IHBD",
    "IEFL", "IEFD", "IEBL", "IEBD"
]

if st.session_state.page == 0:
    vgti_code = st.selectbox(
        "あなたのVGTIタイプを選んでください",
        options=vgti_options
    )
    if st.button("次へ"):
        st.session_state.vgti_code = vgti_code
        st.session_state.page = 1
        st.experimental_rerun()

# 診断ページ
elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    # ラベル
    options = [
        "とてもそう思う", 
        "そう思う", 
        "ややそう思う", 
        "どちらでもない", 
        "ややそう思わない", 
        "そう思わない", 
        "まったくそう思わない"
    ]
    score_map = {
        "とてもそう思う": 3,
        "そう思う": 2,
        "ややそう思う": 1,
        "どちらでもない": 0,
        "ややそう思わない": -1,
        "そう思わない": -2,
        "まったくそう思わない": -3
    }

    # 質問
    q1 = st.radio("一日三食をきちんと食べている", options, index=3)
    q2 = st.radio("家で食事をとる機会が多い", options, index=3)
    q3 = st.radio("野菜は取り入れやすいと感じる", options, index=3)
    q4 = st.radio("野菜を好きだと感じる", options, index=3)

    # スコア計算
    scores = [score_map[q] for q in [q1, q2, q3, q4]]
    total = sum(scores)
    max_score = 3 * 4
    min_score = -3 * 4
    normalized = (total - min_score) / (max_score - min_score) * 100

    st.markdown("---")
    if st.button("診断結果を見る"):
        st.subheader("🍅 診断結果")

        st.write(f"あなたの健康食生活スコアは **{total}** です。")
        st.progress(normalized / 100)
        st.write(f"健康意識スコア: **{normalized:.1f}%**")

        # コメント
        if normalized >= 70:
            st.success("非常にバランスの良い健康志向タイプです。今後も維持していきましょう！")
        elif normalized >= 40:
            st.info("健康意識はまずまず。より意識的に野菜や食習慣を整えるとさらに良いです。")
        else:
            st.warning("生活改善の余地があります。三食・野菜の習慣を振り返ってみましょう。")

        # さらに戻るボタン
        if st.button("もう一度診断する"):
            st.session_state.page = 0
            st.experimental_rerun()

