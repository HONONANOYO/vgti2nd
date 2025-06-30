import streamlit as st
import matplotlib.pyplot as plt

st.title("VGTI 2nd 診断")

# VGTIコード入力
vgti_code = st.text_input("あなたのVGTIタイプ4文字を入力してください（例: RHFL）")

# スコアを初期化
score_irregular = 0
score_regular = 0

score_home = 0
score_eatout = 0

score_free = 0
score_barrier = 0

score_like = 0
score_dislike = 0

if vgti_code and len(vgti_code) == 4:
    axis1 = vgti_code[0].upper()  # R or I
    axis2 = vgti_code[1].upper()  # H or E
    axis3 = vgti_code[2].upper()  # F or B
    axis4 = vgti_code[3].upper()  # L or D

    # 各軸ごとのコメント
    st.subheader("🍅 あなたのタイプに基づく追加コメント")

    if axis1 == "R":
        st.write("✅ 規則正しい食事習慣があるので、その継続ポイントを深掘りしてみましょう。")
    elif axis1 == "I":
        st.write("✅ 食事が不規則気味なので、改善のヒントを探してみましょう。")

    if axis2 == "H":
        st.write("✅ 家食派としてのこだわりについても掘り下げていきます。")
    elif axis2 == "E":
        st.write("✅ 外食派のあなたに合わせた改善策を考えていきます。")

    if axis3 == "F":
        st.write("✅ 野菜摂取に障壁がないのは素晴らしいですね、さらにプラスできる工夫を考えます。")
    elif axis3 == "B":
        st.write("✅ 野菜に障壁があるようなので、その要因を一緒に見直してみましょう。")

    if axis4 == "L":
        st.write("✅ 野菜が好きな強みを活かせる行動を考えます。")
    elif axis4 == "D":
        st.write("✅ 野菜が苦手な点をどうカバーするか考えましょう。")

    st.markdown("---")
    st.subheader("🍅 共通の深掘り質問")

    # =========================
    # 食事の規則性
    q1 = st.multiselect(
        "Q1. 一日三食きちんと食べられない理由はありますか？（複数選択可）",
        ["好きな食べ物がない", "食べる必要性を感じない", "食べる時間がない", "金銭的な余裕がない"]
    )
    score_irregular += 25 * len(q1)

    q2 = st.multiselect(
        "Q2. 一日三食食べられている理由はありますか？（複数選択可）",
        ["小さい頃からの習慣", "自分で意識している", "健康のために気をつけている", "なんとなく"]
    )
    score_regular += 25 * len(q2)

    # =========================
    # 食事場所
    q3 = st.radio(
        "Q3. 普段どこで食事をとることが多いですか？",
        ["家", "外食（レストラン・食堂など）", "中食（お弁当・総菜など）", "フードコート"]
    )
    if q3 == "家":
        score_home += 100
    elif q3 == "外食（レストラン・食堂など）":
        score_eatout += 100
    elif q3 == "中食（お弁当・総菜など）":
        score_home += 30
        score_eatout += 70
    elif q3 == "フードコート":
        score_eatout += 100

    q4 = st.multiselect(
        "Q4. 家で食べない理由は何ですか？（複数選択可）",
        ["料理をするのが面倒だから", "外食の方がおいしいから", "買って食べる方が楽だから", "気分を変えたいから"]
    )
    score_eatout += 25 * len(q4)

    q5 = st.multiselect(
        "Q5. 家で食べる理由は何ですか？（複数選択可）",
        ["安いから", "家族が作ってくれるから", "健康に良いと思うから", "落ち着けるから"]
    )
    score_home += 25 * len(q5)

    # =========================
    # 野菜の障壁
    q6 = st.multiselect(
        "Q6. 野菜を食べるうえでの障壁はありますか？（複数選択可）",
        ["野菜を買うのにお金がかかる", "野菜を調理する時間がない", "野菜の味が苦手", "野菜の必要性を感じない"]
    )
    score_barrier += 25 * len(q6)

    q7 = st.multiselect(
        "Q7. 野菜に障壁がない理由はありますか？（複数選択可）",
        ["もともと野菜が好き", "家族が作ってくれる", "野菜を手軽に買える", "習慣になっている", "料理に取り入れやすい"]
    )
    score_free += 20 * len(q7)

    # =========================
    # 野菜の嗜好
    q8 = st.multiselect(
        "Q8. 野菜を意識して食べる理由は？（複数選択可）",
        ["おいしいと思うから", "育てた経験があるから", "健康に良いから", "なんとなく好き"]
    )
    score_like += 25 * len(q8)

    q9 = st.multiselect(
        "Q9. 野菜をあまり意識して食べない理由は？（複数選択可）",
        ["味が苦手", "食感が苦手", "においが苦手", "なんとなく気が向かない"]
    )
    score_dislike += 25 * len(q9)

    # =========================
    # 正規化（パーセンテージ計算）
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
    st.subheader("🍅 あなたの診断結果")

    st.write("**食事の規則性**")
    st.progress(p_regular, text=f"Regular {p_regular:.1f}%")
    st.progress(p_irregular, text=f"Irregular {p_irregular:.1f}%")

    st.write("**食事の場所**")
    st.progress(p_home, text=f"Home {p_home:.1f}%")
    st.progress(p_eatout, text=f"Eat out {p_eatout:.1f}%")

    st.write("**野菜摂取の障壁**")
    st.progress(p_free, text=f"Free {p_free:.1f}%")
    st.progress(p_barrier, text=f"Barrier {p_barrier:.1f}%")

    st.write("**野菜の嗜好**")
    st.progress(p_like, text=f"Like {p_like:.1f}%")
    st.progress(p_dislike, text=f"Dislike {p_dislike:.1f}%")

else:
    st.info("まずは4文字のVGTIコードを入力してください。")

