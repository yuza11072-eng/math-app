import streamlit as st
import random
import time

st.set_page_config(page_title="数学トレーニング", layout="centered")
st.title("📘 数学トレーニング")

# =====================
# 表示用関数
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
    parts = [term(a, "x²"), term(b, "x")]
    if c != 0:
        parts.append(str(c))
    eq = " ".join([p for p in parts if p])
    return eq.replace("+ -", "- ")

# =====================
# 問題生成
# =====================
def make_question(grade):
    # 中1：一次方程式
    if grade == "中学1年":
        x = random.randint(1, 10)
        a = random.randint(2, 6)
        b = random.randint(1, 10)
        q = f"{term(a,'x')} + {b} = {a*x + b} のとき x = ?"
        return q, [x]

    # 中2：ax = b
    if grade == "中学2年":
        x = random.randint(1, 10)
        a = random.randint(2, 9)
        q = f"{term(a,'x')} = {a*x} のとき x = ?"
        return q, [x]

    # 中3：二次方程式
    # ax² = k
    if random.random() < 0.3:
        x = random.randint(1, 5)
        a = random.randint(1, 3)
        q = f"{term(a,'x²')} = {a*x*x} のとき x = ?"
        return q, [-x, x]

    # ax² + bx + c = 0
    r1 = random.choice([-3, -2, -1])
    r2 = random.choice([1, 2, 3])
    a = random.randint(1, 3)
    b = -a * (r1 + r2)
    c = a * r1 * r2
    eq = make_eq(a, b, c)
    q = f"{eq} = 0 のとき x = ?"
    return q, [r1, r2]

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
        st.session_state.no = 1
        st.session_state.score = 0
        st.session_state.q, st.session_state.ans = make_question(grade)
        st.session_state.start = time.time()
        st.session_state.page = "quiz"
        st.rerun()

# =====================
# 問題画面
# =====================
if st.session_state.page == "quiz":
    TOTAL = 15
    LIMIT = 300  # 5分

    elapsed = int(time.time() - st.session_state.start)
    remain = max(0, LIMIT - elapsed)

    st.markdown(f"### 第 {st.session_state.no} 問 / {TOTAL}")
    st.markdown(f"⏱ 残り時間：{remain//60}分 {remain%60}秒")
    st.markdown(f"🏆 正解数：{st.session_state.score}")
    st.divider()

    # 終了判定
    if st.session_state.no > TOTAL or remain == 0:
        st.success("🎉 終了！")
        st.markdown(f"## 正解：{st.session_state.score} / {TOTAL}")
        if st.button("🔁 最初に戻る"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    st.markdown(st.session_state.q)

    # 解が1つか2つかで入力欄を変える
    if len(st.session_state.ans) == 1:
        user1 = st.number_input("x =", step=1)
        user_answers = [user1]
    else:
        st.caption("※順番はどちらでもOK")
        u1 = st.number_input("x =", key="x1", step=1)
        u2 = st.number_input("x =", key="x2", step=1)
        user_answers = [u1, u2]

    if st.button("答え合わせ"):
        if sorted(user_answers) == sorted(st.session_state.ans):
            st.success("⭕ 正解！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 正解は {st.session_state.ans}")

        st.session_state.no += 1
        st.session_state.q, st.session_state.ans = make_question(
            st.session_state.grade
        )
        st.session_state.start = time.time()
        st.rerun()
