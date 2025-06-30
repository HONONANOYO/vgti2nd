import streamlit as st

st.title("VGTI 2nd 診断 - Likert 7段階版")

# ページ管理
if "page" not in st.session_state:
    st.session_state.page = 0

# 16タイプ
vgti_options = [
    "RHFL", "RHFD", "RHBL", "RHBD",
    "REFL", "REFD", "REBL", "REBD",
    "IHFL", "IHFD", "IHBL", "IHBD",
    "IEFL", "IEFD", "IEBL", "IEBD"
]

if st.session_state.page == 0:
    vgti_code = st.selectbox("あなたのVGTIタイプを選んでください", options=vgti_options)
    if st.button("次へ"):
        st.session_state.vgti_code = vgti_code
        st.session_state.page = 1
        st.experimental_rerun()

elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    a1, a2, a3, a4 = code[0], code[1], code[2], code[3]

    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    # Likert質問
    st.write("以下の質問にお答えください。（-3: まったくそう思わない 〜 +3: とてもそう思う）")

    q1 = st.slider("一日三食をきちんと食べている", -3, 3, 0, 1)
    q2 = st.slider("家で食事をとる機会が多い", -3, 3, 0, 1)
    q3 = st.slider("野菜は取り入れやすいと感じる", -3, 3, 0, 1)
    q4 = st.slider("野菜を好きだと感じる", -3, 3, 0, 1)

    # スコア計算
    total_score = q1 + q2 + q3 + q4
    max_score = 3 * 4   # +3が4問
    min_score = -3 * 4  # -3が4問
    normalized = (total_score - min_score) / (max_score - min_score) * 100

    st.markdown("---")
    if st.button("診断結果を見る"):
        st.subheader("🍅 診断結果")
        st.write(f"あなたの総合スコアは **{total_score}** です。")
        st.write(f"VGTIパーセンテージ: **{normalized:.1f}%**")

        if normalized >= 70:
            st.success("健康意識が非常に高く、野菜・食事に対する自己管理力が高い傾向があります。")
        elif normalized >= 40:
            st.info("ある程度バランスは意識しているものの、波がある傾向があります。")
        else:
            st.warning("生活や食事習慣に改善の余地がありそうです。ぜひ振り返ってみましょう。")

