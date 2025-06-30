import streamlit as st
import matplotlib.pyplot as plt

st.title("VGTI 2nd 診断")

# スコアを初期化
score_irregular = 0
score_regular = 0

score_home = 0
score_eatout = 0

score_free = 0
score_barrier = 0

score_like = 0
score_dislike = 0

# =========================
# 1. 食事の規則性
st.header("🍅 食事の規則性")

q1 = st.multiselect(
    "Q1. 一日三食きちんと食べられない理由はありますか？",
    ["好きな食べ物がない", "食べる必要性を感じない", "食べる時間がない", "金銭的な余裕がない"]
)
score_irregular += 25 * len(q1)

q2 = st.multiselect(
    "Q2. 一日三食食べられている理由はありますか？",
    ["小さい頃からの習慣", "自分で意識している", "健康のために気をつけている", "なんとなく"]
)
score_regular += 25 * len(q2)

# =========================
# 2. 食べる場所
st.header("🍅 食べる場所")

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
    "Q4. 家で食べない理由は何ですか？",
    ["料理をするのが面倒だから", "外食の方がおいしいから", "買って食べる方が楽だから", "気分を変えたいから"]
)
score_eatout += 25 * len(q4)

q5 = st.multiselect(
    "Q5. 家で食べる理由は何ですか？",
    ["安いから", "家族が作ってくれるから", "健康に良いと思うから", "落ち着けるから"]
)
score_home += 25 * len(q5)

# =========================
# 3. 野菜の障壁
st.header("🍅 野菜の障壁")

q6 = st.multiselect(
    "Q6. 野菜を食べるうえでの障壁はありますか？",
    ["野菜を買うのにお金がかかる", "野菜を調理する時間がない", "野菜の味が苦手", "野菜の必要性を感じない"]
)
score_barrier += 25 * len(q6)

q7 = st.multiselect(
    "Q7. 野菜に障壁がない理由はありますか？",
    ["もともと野菜が好き", "家族が作ってくれる", "野菜を手軽に買える", "習慣になっている", "料理に取り入れやすい"]
)
score_free += 20 * len(q7)

# =========================
# 4. 野菜の嗜好
st.header("🍅 野菜の嗜好")

q8 = st.multiselect(
    "Q8. 野菜を意識して食べる理由は？",
    ["おいしいと思うから", "育てた経験があるから", "健康に良いから", "なんとなく好き"]
)
score_like += 25 * len(q8)

q9 = st.multiselect(
    "Q9. 野菜をあまり意識して食べない理由は？",
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
st.subheader("🍅 診断結果")

labels = ["Regular", "Irregular"]
values = [p_regular, p_irregular]
st.bar_chart(values, use_container_width=True)

labels = ["Home", "Eat out"]
values = [p_home, p_eatout]
st.bar_chart(values, use_container_width=True)

labels = ["Free", "Barrier"]
values = [p_free, p_barrier]
st.bar_chart(values, use_container_width=True)

labels = ["Like", "Dislike"]
values = [p_like, p_dislike]
st.bar_chart(values, use_container_width=True)
