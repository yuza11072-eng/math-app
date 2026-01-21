import streamlit as st
import random
import time

st.set_page_config(page_title="数学トレーニング", layout="centered")
st.title("📘 数学トレーニング")

# =====================
# 表示補助
# =====================
def term(coef, var):
    if coef == 0:
        return ""
    if coef == 1:
        return var
    if coef == -1:
        return f"-{var}"
    return f"{coef}{var}"

def make_eq(a, b, c):
    parts = [term(a, "x²"), term(b, "x"), str(c) if c != 0 else ""]
    eq = " ".join([p for p in parts if p != ""])
    eq = eq.replace("+ -", "- ")
    return eq

# =====================
# 問題生成
# =====================
def make_question(grade):
    if grade == "中学1年":
        x = random.randint(1, 10)
        a = random.randint(2, 5)
        b = random.randint(1, 10)
        return f"{term(a,'x')} + {b} = {a*x+b} のとき x = ?", x

    if grade == "中学2年":
        x = random.randint(1, 10)
        a = random.randint(2, 9)
        return f"{term(a,'x')} = {a*x} のとき x = ?", x

    if grade == "中学3年":
        # ax² = k
        if random.random() < 0.3:
            x = random.choice([1, 2, 3])
            a = random.randint(1, 3)
            return f"{term(a,'x²')} = {a*x*x} のとき x = ?（小さい方）", -x

        # ax² + bx + c = 0
        r1 = random.choice([-3, -2, -1])
        r2 = random.choice([1, 2, 3])
        a = random.randint(1, 3)
        b = -a * (r1 + r2)
        c = a * r1 * r2
        eq = make_eq(a, b, c)
        return f"{eq} = 0 のとき x = ?（小さい方）", r1

# =====================
# 初期化
# =====================
if "page" not in st.session_state:
    st.session_state.page = "select"

# =====================
# 学年選択
# =====================
if st.session_state.page == "select":
    st.subheader("学年を選んでね")
    grade = st.radio("", ["中学1年", "中学2年", "中学3年"])

    if st.button("▶ スタート"):
        st.session_state.grade = grade
        st.session_state.q = 1
        st.session_state.score = 0
        st.session_state.question, st.session_state.answer = make_question(grade)
        st.session_state.start = time.time()
        st.session_state.page = "quiz"
        st.rerun()

# =====================
# クイズ画面
# =====================
if st.session_state.page == "quiz":
    TOTAL = 15
    LIMIT = 300

    elapsed = int(time.time() - st.session_state.start)
    remain = max(0, LIMIT - elapsed)

    st.markdown(f"### 第 {st.session_state.q} 問 / {TOTAL}")
    st.markdown(f"⏱ 残り時間：{remain//60}分 {remain%60}秒")
    st.markdown(f"🏆 正解数：{st.session_state.score}")
    st.divider()

    if st.session_state.q > TOTAL or remain == 0:
        st.success("🎉 終了！")
        st.markdown(f"## 正解：{st.session_state.score} / {TOTAL}")
        if st.button("🔁 最初に戻る"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    st.markdown(st.session_state.question)
    user = st.number_input("答え", step=1)

    if st.button("答え合わせ"):
        if user == st.session_state.answer:
            st.success("⭕ 正解！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 正解は {st.session_state.answer}")

        st.session_state.q += 1
        st.session_state.question, st.session_state.answer = make_question(
            st.session_state.grade
        )
        st.session_state.start = time.time()
        st.rerun()
