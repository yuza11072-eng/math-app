import streamlit as st
import random
import time
from datetime import datetime, timezone, timedelta

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

st.title("📘 数学トレーニング")

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
        x = random.randint(1, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        c = a * x + b
        return f"{a}x + {b} = {c} のとき x = ?", x

    if grade == "中学2年":
        x = random.randint(1, 10)
        a = random.randint(2, 8)
        return f"{a}x = {a*x} のとき x = ?", x

    if grade == "中学3年":
        x = random.choice([-3, -2, -1, 1, 2, 3])
        b = -2 * x
        c = x * x
        return f"x² {b:+}x + {c} = 0 のとき x = ?（小さい方）", x

# =====================
# セッション初期化
# =====================
if "q_no" not in st.session_state:
    st.session_state.q_no = 1
    st.session_state.score = 0
    st.session_state.question, st.session_state.answer = make_question(grade)
    st.session_state.start_time = time.time()
    st.session_state.answered = False

# =====================
# 定数
# =====================
TOTAL = 15
LIMIT = 300  # 5分

# =====================
# 終了
# =====================
if st.session_state.q_no > TOTAL:
    st.success("🎉 終了！")
    st.markdown(f"## 🏆 正解数：{st.session_state.score} / {TOTAL}")
    if st.button("🔁 もう一回"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    st.stop()

# =====================
# タイマー（自動更新）
# =====================
elapsed = int(time.time() - st.session_state.start_time)
remain = LIMIT - elapsed

timer_box = st.empty()
timer_box.markdown(
    f"### ⏱ 残り時間：{remain//60}分 {remain%60}秒"
)

if remain <= 0:
    st.error("⏰ 時間切れ！")
    if st.button("➡ 次の問題へ"):
        st.session_state.q_no += 1
        st.session_state.question, st.session_state.answer = make_question(grade)
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.rerun()

# =====================
# 問題表示
# =====================
st.markdown(f"### ❓ 第 {st.session_state.q_no} 問 / {TOTAL}")
st.markdown(st.session_state.question)

user = st.number_input("答えを入力", step=1)

# =====================
# 判定
# =====================
if st.button("答え合わせ"):
    if user == st.session_state.answer:
        st.success("⭕ 正解！")
        st.session_state.score += 1
    else:
        st.error(f"❌ 不正解… 正解は {st.session_state.answer}")
    st.session_state.answered = True

# =====================
# 次へ
# =====================
if st.session_state.answered:
    if st.button("➡ 次の問題"):
        st.session_state.q_no += 1
        st.session_state.question, st.session_state.answer = make_question(grade)
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.rerun()

# =====================
# 自動リフレッシュ（1秒）
# =====================
time.sleep(1)
st.rerun()
