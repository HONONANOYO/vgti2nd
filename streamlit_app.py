import streamlit as st

st.title("VGTI 2nd 診断")

# ページ管理
if "page" not in st.session_state:
    st.session_state.page = 0

# 16タイプの選択肢
vgti_options = [
    "RHFL", "RHFD", "RHBL", "RHBD",
    "REFL", "REFD", "REBL", "REBD",
    "IHFL", "IHFD", "IHBL", "IHBD",
    "IEFL", "IEFD", "IEBL", "IEBD"
]

# ページ0: VGTIタイプ選択
if st.session_state.page == 0:
    vgti_code = st.selectbox(
        "あなたのVGTIタイプを選んでください",
        options=vgti_options
    )
    if st.button("次へ"):
        st.session_state.vgti_code = vgti_code
        st.session_state.page = 1
        st.experimental_rerun()

# ページ1: 質問
elif st.session_state.page == 1:
    vgti_code = st.session_state.vgti_code
    axis1 = vgti_code[0]
    axis2 = vgti_code[1]
    axis3 = vgti_code[2]
    axis4 = vgti_code[3]

    st.subheader(f"あなたのVGTIタイプ: {vgti_code}")

    st.markdown("---")
    st.subheader("🍅 あなたに合わせた質問")

    results = {}

    # 軸1
    if axis1 == "R":
        q2 = st.multiselect(
            "Q2. 一日三食食べられている理由は？",
            ["小さい頃からの習慣", "意識している", "健康のため", "なんとなく"]
        )
        results['規則性'] = len(q2)
    else:
        q1 = st.multiselect(
            "Q1. 一日三食きちんと食べられない理由は？",
            ["好きな食べ物がない", "食べる必要性を感じない", "食べる時間がない", "金銭的な余裕がない"]
        )
        results['不規則性'] = len(q1)

    # 軸2
    if axis2 == "H":
        q5 = st.multiselect(
            "Q5. 家で食べる理由は？",
            ["安いから", "家族が作ってくれるから", "健康に良いから", "落ち着けるから"]
        )
        results['家食傾向'] = len(q5)
    else:
        q4 = st.multiselect(
            "Q4. 家で食べない理由は？",
            ["面倒だから", "外食がおいしいから", "買った方が楽だから", "気分を変えたいから"]
        )
        results['外食傾向'] = len(q4)

    # 軸3
    if axis3 == "F":
        q7 = st.multiselect(
            "Q7. 野菜に障壁がない理由は？",
            ["もともと好き", "家族が作ってくれる", "手軽に買える", "習慣になっている", "料理に取り入れやすい"]
        )
        results['野菜に障壁がない'] = len(q7)
    else:
        q6 = st.multiselect(
            "Q6. 野菜を食べるうえでの障壁は？",
            ["お金がかかる", "調理の時間がない", "味が苦手", "必要性を感じない"]
        )
        results['野菜に障壁がある'] = len(q6)

    # 軸4
    if axis4 == "L":
        q8 = st.multiselect(
            "Q8. 野菜を意識して食べる理由は？",
            ["おいしい", "育てた経験がある", "健康に良い", "なんとなく"]
        )
        results['野菜好き'] = len(q8)
    else:
        q9 = st.multiselect(
            "Q9. 野菜をあまり食べない理由は？",
            ["味が苦手", "食感が苦手", "においが苦手", "なんとなく気が向かない"]
        )
        results['野菜が苦手'] = len(q9)

    st.markdown("---")

    # 診断ボタン
    if st.button("診断結果を見る"):
        st.subheader("🍅 診断結果")
        for key, value in results.items():
            if value == 0:
                st.write(f"👉 **{key}**: 特に当てはまる理由は選ばれていませんでした。")
            else:
                st.write(f"👉 **{key}**: {value}件当てはまりました。")

        st.success("診断ありがとうございました！")

