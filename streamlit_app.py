import streamlit as st
import matplotlib.pyplot as plt

st.title("VGTI 2nd 診断")

# VGTIコード入力
vgti_code = st.text_input("あなたのVGTIタイプ4文字を入力してください（例: RHFL）")

# スコア初期化
score_irregular = 0
score_regular = 0
score_home = 0
score_eatout = 0
score_free = 0
score_barrier = 0
score_like = 0
score_dislike = 0

if vgti_code and len(vgti_code) == 4:
    axis1 = vgti_code[0].upper()  # R/I
    axis2 = vgti_code[1].upper()  # H/E
    axis3 = vgti_code[2].upper()  # F/B
    axis4 = vgti_code[3].upper()  # L/D

    st.subheader("🍅 あなたのタイプに基づくコメント")

    # 軸1
    if axis1 == "R":
        st.write("✅ 規則的な食事習慣があるのでその維持を深掘りします。")
    else:
        st.write("✅ 食事が不規則なので改善ヒントを深掘りします。")

    # 軸2
    if axis2 == "H":
        st.write("✅ 家食派としてのポイントを深掘りします。")
    else:
        st.write("✅ 外食派としての工夫を深掘りします。")

    # 軸3
    if axis3 == "F":
        st.write("✅ 野菜に障壁がない強みをさらに伸ばしましょう。")
    else:
        st.write("✅ 野菜の障壁の原因を一緒に探します。")

    # 軸4
    if axis4 == "L":
        st.write("✅ 野菜好きの強みを活かします。")
    else:
        st.write("✅ 野菜が苦手な部分をカバーしましょう。")

    st.markdown("---")
    st.subheader("🍅 あなたに合わせた質問")

    # =========================
    # 軸1 (食事の規則性)
    if axis1 == "R":
        q2 = st.multiselect(
            "Q2. 一日三食食べられている理由は？",
            ["小さい頃からの習慣", "意識している", "健康のため", "なんとなく"]
        )
        score_regular += 25 * len(q2)
    else:
        q1 = st.multiselect(
            "Q1. 一日三食きちんと食べられない理由は？",
            ["好きな食べ物がない", "食べる必要性を感じない", "食べる時間がない", "金銭的な余裕がない"]
        )
        score_irregular += 25 * len(q1)

    # =========================
    # 軸2 (食事の場所)
    if axis2 == "H":
        q5 = st.multiselect(
            "Q5. 家で食べる理由は？",
            ["安いから", "家族が作ってくれるから", "健康に良いから", "落ち着けるから"]
        )
        score_home += 25 * len(q5)
    else:
        q4 = st.multiselect(
            "Q4. 家で食べない理由は？",
            ["面倒だから", "外食がおいしいから", "買った方が楽だから", "気分を変えたいから"]
        )
        score_eatout += 25 * len(q4)

    # =========================
    # 軸3 (野菜の障壁)
    if axis3 == "F":
        q7 = st.multiselect(
            "Q7. 野菜に障壁がない理由は？",
            ["もともと好き", "家族が作ってくれる", "手軽に買える", "習慣になっている", "料理に取り入れやすい"]
        )
        score_free += 20 * len(q7)
    else:
        q6 = st.multiselect(
            "Q6. 野菜を食べるうえでの障壁は？",
            ["お金がかかる", "調理の時間がない", "味が苦手", "必要性を感じない"]
        )
        score_barrier += 25 * len(q6)

    # =========================
    # 軸4 (野菜の嗜好)
    if axis4 == "L":
        q8 = st.multiselect(
            "Q8. 野菜を意識して食べる理由は？",
            ["おいしい", "育てた経験がある", "健康に良い", "なんとなく"]
        )
        score_like += 25 * len(q8)
    else:
        q9 = st.multiselect(
            "Q9. 野菜をあまり食べない理由は？",
            ["味が苦手", "食感が苦手", "においが苦手", "なんとなく気が向かない"]
        )
        score_dislike += 25 * len(q9)

    # =========================
    # パーセンテージ計算
    total_reg = score_regular + score_irregular
    p_regular = score_regular / total_reg * 100 if total_reg else 0
    p_irregular = score_irregular / total_reg * 100 if total_reg else 0

    total_home = score_home + score_eatout
    p_home = score_home / total_home * 100 if total_home else 0
    p_eatout = score_eatout / total_home * 100 if total_home else 0

    total_barrier = score_barrier + score_free
    p_barrier = score_barrier / total_barrier * 100 if total_barrier else 0
    p_free = score_free / total_barrier * 100 if total_barrier else 0

    total_like = score_like + score_dislike
    p_like = score_like / total_like * 100 if total_like else 0
    p_dislike = score_dislike / total_like * 100 if total_like else 0

    # =========================
    # 結果表示
    st.subheader("🍅 診断結果")

    st.write("**食事の規則性**")
    st.progress(p_regular / 100, text=f"Regular {p_regular:.1f}%")
    st.progress(p_irregular / 100, text=f"Irregular {p_irregular:.1f}%")

    st.write("**食事の場所**")
    st.progress(p_home / 100, text=f"Home {p_home:.1f}%")
    st.progress(p_eatout / 100, text=f"Eat out {p_eatout:.1f}%")

    st.write("**野菜摂取の障壁**")
    st.progress(p_free / 100, text=f"Free {p_free:.1f}%")
    st.progress(p_barrier / 100, text=f"Barrier {p_barrier:.1f}%")

    st.write("**野菜の嗜好**")
    st.progress(p_like / 100, text=f"Like {p_like:.1f}%")
    st.progress(p_dislike / 100, text=f"Dislike {p_dislike:.1f}%")

else:
    st.info("まずは4文字のVGTIコードを入力してください。")

