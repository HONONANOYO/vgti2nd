import streamlit as st

st.title("VGTI 横並びサンプル")

if "r_answers" not in st.session_state:
    st.session_state.r_answers = [3, 3, 3, 3]  # デフォルト: 中央

# 5段階のラベル
labels = ["まったくそう思わない", "あまりそう思わない", "どちらでもない", "そう思う", "とてもそう思う"]

# 円の絵文字
icons = ["⚪️", "🟢", "🟡", "🟠", "🔴"]

# 質問
r_questions = [
    "小さい頃からの習慣だから三食食べている",
    "自分で意識して三食食べている",
    "健康のために三食食べている",
    "なんとなく三食食べている"
]

for q_idx, question in enumerate(r_questions):
    st.markdown(f"#### 🍅 {question}")
    cols = st.columns(5)
    for i, col in enumerate(cols):
        if col.button(f"{icons[i]}"):
            st.session_state.r_answers[q_idx] = i + 1
    
    # 選択中のラベルを表示
    current = st.session_state.r_answers[q_idx]
    st.write(f"→ 今の選択: {labels[current - 1]}")

st.markdown("---")
if st.button("次へ"):
    st.write("次の処理に進みます（テスト用）")
