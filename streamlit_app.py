import streamlit as st

st.title("VGTI 2nd 診断")

# ページ管理
if "page" not in st.session_state:
    st.session_state.page = 0

# コメント辞書
comment_dict = {
    "Q2": {
        "小さい頃からの習慣": "子どもの頃から続けている規則的な食習慣を大切にされています。",
        "意識している": "食事をきちんと管理しようという意識がとても高いです。",
        "健康のため": "健康維持を意識して三食きちんと摂る、バランスの良い習慣があります。",
        "なんとなく": "無意識でも三食とれている、安定した生活リズムが身についています。"
    },
    "Q1": {
        "好きな食べ物がない": "食への楽しみを感じにくく、食事回数が減る傾向があります。",
        "食べる必要性を感じない": "食への関心が薄く、生活リズムに課題があるかもしれません。",
        "食べる時間がない": "忙しさから食事の優先度が下がりがちな傾向です。",
        "金銭的な余裕がない": "食事にお金をかけづらく、回数が減ることがあります。"
    },
    "Q5": {
        "安いから": "経済的に家での食事をうまく活用しています。",
        "家族が作ってくれるから": "家族とのつながりを感じながら食事を大切にしています。",
        "健康に良いから": "自宅で健康的な食事を心がける傾向があります。",
        "落ち着けるから": "リラックスできる食空間を重視しています。"
    },
    "Q4": {
        "面倒だから": "調理の負担を減らし、外食に頼りがちです。",
        "外食がおいしいから": "バラエティ豊かな外食の味を楽しむ傾向があります。",
        "買った方が楽だから": "利便性を優先し、中食や外食を活用するタイプです。",
        "気分を変えたいから": "食を通して気分転換をする柔軟さがあります。"
    },
    "Q7": {
        "もともと好き": "野菜に親しみがあり、積極的に取り入れる傾向があります。",
        "家族が作ってくれる": "家族の影響で野菜を無理なく食べられています。",
        "手軽に買える": "アクセスしやすい環境で、野菜摂取に困らない生活です。",
        "習慣になっている": "習慣化されており、抵抗なく野菜をとれます。",
        "料理に取り入れやすい": "調理の工夫で野菜を取り入れる柔軟さがあります。"
    },
    "Q6": {
        "お金がかかる": "野菜を買う負担感があり、摂取頻度が減りやすいです。",
        "調理の時間がない": "忙しさから野菜の準備が後回しになりがちです。",
        "味が苦手": "味覚の好みで野菜から遠ざかる傾向があります。",
        "必要性を感じない": "野菜の重要性をあまり意識していない傾向があります。"
    },
    "Q8": {
        "おいしい": "野菜の味そのものを楽しめる感性があります。",
        "育てた経験がある": "野菜への愛着があり、積極的に食べる意識があります。",
        "健康に良い": "健康意識から野菜をしっかり摂ろうとしています。",
        "なんとなく": "無意識に野菜をとる習慣が根づいています。"
    },
    "Q9": {
        "味が苦手": "野菜の風味が合わず、苦手意識があります。",
        "食感が苦手": "食感への好みで野菜を避ける傾向があります。",
        "においが苦手": "においに敏感で野菜を遠ざけやすいです。",
        "なんとなく気が向かない": "特に理由はないものの、積極的に野菜をとらない傾向があります。"
    }
}

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

    st.subheader(f"あなたのタイプ: {code}")
    st.markdown("---")

    answers = {}

    # 軸1
    if a1 == "R":
        q = st.radio("Q2. 一日三食食べられている理由は？", list(comment_dict["Q2"].keys()))
        answers["Q2"] = q
    else:
        q = st.radio("Q1. 一日三食食べられない理由は？", list(comment_dict["Q1"].keys()))
        answers["Q1"] = q

    # 軸2
    if a2 == "H":
        q = st.radio("Q5. 家で食べる理由は？", list(comment_dict["Q5"].keys()))
        answers["Q5"] = q
    else:
        q = st.radio("Q4. 家で食べない理由は？", list(comment_dict["Q4"].keys()))
        answers["Q4"] = q

    # 軸3
    if a3 == "F":
        q = st.radio("Q7. 野菜に障壁がない理由は？", list(comment_dict["Q7"].keys()))
        answers["Q7"] = q
    else:
        q = st.radio("Q6. 野菜を食べるうえでの障壁は？", list(comment_dict["Q6"].keys()))
        answers["Q6"] = q

    # 軸4
    if a4 == "L":
        q = st.radio("Q8. 野菜を意識して食べる理由は？", list(comment_dict["Q8"].keys()))
        answers["Q8"] = q
    else:
        q = st.radio("Q9. 野菜をあまり食べない理由は？", list(comment_dict["Q9"].keys()))
        answers["Q9"] = q

    if st.button("診断結果を見る"):
        st.subheader("🍅 診断結果")
        for key, choice in answers.items():
            comment = comment_dict[key][choice]
            st.write(f"**{choice}** → {comment}")
        st.success("診断ありがとうございました！")

