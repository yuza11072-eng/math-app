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

st.title("📘 数学トレーニング")

# 🔁 1秒ごと自動更新（ここが超重要）
st.autorefresh(interval=1000, key="timer")

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
        # 25%で ax^2 型
        if random.random() < 0.25:
            x = random.choice([1, 2, 3, -1, -2])
            a = random.randint(1, 3)
            return f"{a}x² = {a*x*x} のとき x = ?（小さい方
