import streamlit as st

st.title("VGTI 2nd 診断 - Likert 7段階スケール版")

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

# ページ0: VGTIタイプ選択
if st.session_state.page == 0:
    vgti_code = st.selectbox(
        "あなたのVGTIタイプを選んでください",
        options=vgti_options
    )
    if st.button("次へ"):
        st.session_state.vgti_code = vgti_code
        st.session_state.page = 1

# ページ1: Likert 質問
elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    if "answers" not in st.session_state:
        st.session_state.answers = {}

    # Likert質問
    st.markdown("### 🍅 1. 食事の規則性について")
    r_items = [
        "小さい頃からの習慣だから三食食べている",
        "自分で意識して三食食べている",
        "健康のために三食食べている",
        "なんとなく三食食べている"
    ]
    for i, item in enumerate(r_items):
        val = st.slider(item, -3, 3, 0, 1, format="%d", key=f"r{i}")
        st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
        st.session_state.answers[f"r{i}"] = val

    st.markdown("### 🍅 2. 食べる場所について")
    h_items = [
        "家で食べることが多い",
        "家族が作ってくれるから家で食べる",
        "健康に良いから家で食べる",
        "落ち着けるから家で食べる"
    ]
    for i, item in enumerate(h_items):
        val = st.slider(item, -3, 3, 0, 1, format="%d", key=f"h{i}")
        st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
        st.session_state.answers[f"h{i}"] = val

    st.markdown("### 🍅 3. 野菜の障壁について")
    f_items = [
        "野菜は手軽に買える",
        "野菜を調理しやすい",
        "野菜が好き",
        "野菜を食べるのが習慣になっている"
    ]
    for i, item in enumerate(f_items):
        val = st.slider(item, -3, 3, 0, 1, format="%d", key=f"f{i}")
        st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
        st.session_state.answers[f"f{i}"] = val

    st.markdown("### 🍅 4. 野菜の嗜好について")
    l_items = [
        "野菜をおいしいと思う",
        "育てた経験があるので親しみがある",
        "健康のために野菜を意識している",
        "なんとなく野菜を食べている"
    ]
    for i, item in enumerate(l_items):
        val = st.slider(item, -3, 3, 0, 1, format="%d", key=f"l{i}")
        st.caption("まったくそう思わない (-3) ←→ とてもそう思う (+3)")
        st.session_state.answers[f"l{i}"] = val

    if st.button("診断結果を見る"):
        st.session_state.page = 2

# ページ2: 診断結果
elif st.session_state.page == 2:
    st.subheader("🍅 診断結果")

    answers = st.session_state.answers

    # 軸ごとに合計
    r_score = sum(answers[f"r{i}"] for i in range(4))
    h_score = sum(answers[f"h{i}"] for i in range(4))
    f_score = sum(answers[f"f{i}"] for i in range(4))
    l_score = sum(answers[f"l{i}"] for i in range(4))

    # パーセンテージ変換
    axis_scores = {
        "規則性": (r_score + 12) / 24 * 100,
        "家食傾向": (h_score + 12) / 24 * 100,
        "野菜への障壁のなさ": (f_score + 12) / 24 * 100,
        "野菜の嗜好": (l_score + 12) / 24 * 100
    }

    # 結果表示
    for k, v in axis_scores.items():
        st.write(f"**{k}**: {v:.1f}%")
        st.progress(v / 100)

    # コメント
    st.markdown("#### 📝 コメントまとめ")
    if r_score > 6:
        st.success("あなたは規則的に三食をとる習慣が根付いています。")
    elif r_score < -6:
        st.warning("三食のリズムが乱れがちかもしれません。")
    else:
        st.info("三食に関してはほどほどの意識です。")

    if h_score > 6:
        st.success("家での食事に安心感を持っています。")
    elif h_score < -6:
        st.warning("外食や中食を利用する傾向があります。")
    else:
        st.info("家食と外食のバランスをとっています。")

    if f_score > 6:
        st.success("野菜を自然に取り入れることができています。")
    elif f_score < -6:
        st.warning("野菜の摂取にハードルを感じているかもしれません。")
    else:
        st.info("野菜に対して特に強いこだわりはないようです。")

    if l_score > 6:
        st.success("野菜を好んで食べる傾向があります。")
    elif l_score < -6:
        st.warning("野菜の味やにおいに抵抗があるかもしれません。")
    else:
        st.info("野菜について特に強い好き嫌いはないようです。")

    if st.button("もう一度診断する"):
        st.session_state.page = 0
        st.session_state.answers = {}
