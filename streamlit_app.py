import streamlit as st

st.title("VGTI 2nd 診断 - 7段階Likertスケール版")

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

elif st.session_state.page == 1:
    code = st.session_state.vgti_code
    st.subheader(f"あなたのVGTIタイプ: {code}")
    st.markdown("---")

    # スコア辞書
    score_map = {
        -3: "まったくそう思わない",
        -2: "そう思わない",
        -1: "ややそう思わない",
         0: "どちらでもない",
         1: "ややそう思う",
         2: "そう思う",
         3: "とてもそう思う"
    }

    # 項目ごとの質問
    st.markdown("### 🍅 1. 食事の規則性について")

    r_items = [
        "小さい頃からの習慣だから三食食べている",
        "自分で意識して三食食べている",
        "健康のために三食食べている",
        "なんとなく三食食べている"
    ]
    r_scores = []
    for item in r_items:
        val = st.slider(item, -3, 3, 0, 1, format="%d")
        r_scores.append(val)

    st.markdown("### 🍅 2. 食べる場所について")

    h_items = [
        "家で食べることが多い",
        "家族が作ってくれるから家で食べる",
        "健康に良いから家で食べる",
        "落ち着けるから家で食べる"
    ]
    h_scores = []
    for item in h_items:
        val = st.slider(item, -3, 3, 0, 1, format="%d")
        h_scores.append(val)

    st.markdown("### 🍅 3. 野菜の障壁について")

    f_items = [
        "野菜は手軽に買える",
        "野菜を調理しやすい",
        "野菜が好き",
        "野菜を食べるのが習慣になっている"
    ]
    f_scores = []
    for item in f_items:
        val = st.slider(item, -3, 3, 0, 1, format="%d")
        f_scores.append(val)

    st.markdown("### 🍅 4. 野菜の嗜好について")

    l_items = [
        "野菜をおいしいと思う",
        "育てた経験があるので親しみがある",
        "健康のために野菜を意識している",
        "なんとなく野菜を食べている"
    ]
    l_scores = []
    for item in l_items:
        val = st.slider(item, -3, 3, 0, 1, format="%d")
        l_scores.append(val)

    st.markdown("---")

    if st.button("診断結果を見る"):
        st.subheader("🍅 診断結果")

        # 軸ごとスコア
        axis_scores = {
            "規則性": sum(r_scores),
            "家食傾向": sum(h_scores),
            "野菜への障壁のなさ": sum(f_scores),
            "野菜の嗜好": sum(l_scores)
        }

        # パーセンテージ変換
        for k, v in axis_scores.items():
            norm = (v + 12) / 24 * 100  # -12~+12 → 0~100%
            st.write(f"**{k}**: {norm:.1f}%")

        # コメント例
        st.markdown("#### 📝 コメントまとめ")
        if axis_scores["規則性"] > 6:
            st.success("あなたは規則的に三食をとる習慣が根付いています。")
        elif axis_scores["規則性"] < -6:
            st.warning("三食のリズムが乱れがちかもしれません。")
        else:
            st.info("三食に関してはほどほどの意識です。")

        if axis_scores["家食傾向"] > 6:
            st.success("家での食事に安心感を持っています。")
        elif axis_scores["家食傾向"] < -6:
            st.warning("外食や中食を利用する傾向があります。")
        else:
            st.info("家食と外食のバランスをとっています。")

        if axis_scores["野菜への障壁のなさ"] > 6:
            st.success("野菜を自然に取り入れることができています。")
        elif axis_scores["野菜への障壁のなさ"] < -6:
            st.warning("野菜の摂取にハードルを感じているかもしれません。")
        else:
            st.info("野菜に対して特に強いこだわりはないようです。")

        if axis_scores["野菜の嗜好"] > 6:
            st.success("野菜を好んで食べる傾向があります。")
        elif axis_scores["野菜の嗜好"] < -6:
            st.warning("野菜の味やにおいに抵抗があるかもしれません。")
        else:
            st.info("野菜について特に強い好き嫌いはないようです。")

        # もう一度ボタン
        if st.button("もう一度診断する"):
            st.session_state.page = 0
            st.experimental_rerun()
