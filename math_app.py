import streamlit as st
import random
import time

# =====================
# ページ設定
# =====================
st.set_page_config(
    page_title="数学トレーニング",
    page_icon="📘",
    layout="centered"
)

st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 3em;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 📘 数学トレーニング")
st.markdown("---")

# =====================
# 学年選択
# =====================
grade = st.selectbox(
    "学年を選んでね",
    ["中学1年", "中学2年", "中学3年"]
)

# =====================
# 問題生成
# =====================
def make_question(grade):
    if grade == "中学1年":
        a = random.randint(-10, 10)
        b = random.randint(1, 10)
        return f"{a} + {b} = ?", a + b

    if grade == "中学2年":
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        return f"x + y = {x+y}, x = {x} のとき y = ?", y

    if grade == "中学3年":
        a = random.randint(1, 9)
        return f"x² = {a*a} のとき x = ?", a

# =====================
# セッション初期化
# =====================
if "question_no" not in st.session_state:
    st.session_state.question_no = 1
    st.session_state.score = 0
    st.session_state.q, st.session_state.ans = make_question(grade)
    st.session_state.start_time = time.time()
    st.session_state.answered = False

# =====================
# 終了判定（15問）
# =====================
TOTAL = 15
LIMIT = 300  # 5分

if st.session_state.question_no > TOTAL:
    st.success("🎉 終了！")
    st.markdown(f"## 🏆 正解数：{st.session_state.score} / {TOTAL}")
    st.stop()

# =====================
# タイマー（1問ごと）
# =====================
elapsed = int(time.time() - st.session_state.start_time)
remain = LIMIT - elapsed

st.markdown(f"### ❓ 第 {st.session_state.question_no} 問 / {TOTAL}")
st.markdown(f"⏱ 残り時間：**{remain//60}分 {remain%60}秒**")
st.markdown(f"🏆 正解数：**{st.session_state.score}**")
st.markdown("---")

# =====================
# 時間切れ
# =====================
if remain <= 0:
    st.error("⏰ 時間切れ！")
    if st.button("➡ 次の問題へ"):
        st.session_state.question_no += 1
        st.session_state.q, st.session_state.ans = make_question(grade)
        st.session_state.start_time = time.time()
        st.experimental_rerun()

# =====================
# 問題表示
# =====================
st.markdown(f"### {st.session_state.q}")
user = st.number_input("答えを入力", step=1)

# =====================
# 判定
# =====================
if st.button("答え合わせ"):
    if user == st.session_state.ans:
        st.success("⭕ 正解！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解… 正解は {st.session_state.ans}")
    st.session_state.answered = True

# =====================
# 次の問題
# =====================
if st.session_state.answered:
    if st.button("➡ 次の問題"):
        st.session_state.question_no += 1
        st.session_state.q, st.session_state.ans = make_question(grade)
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.experimental_rerun()
