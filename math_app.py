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

# =====================
# 1秒ごと自動更新
# =====================
st.autorefresh(interval=1000, key="timer")

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
        # 25%で ax^2 = k 型
        if random.random() < 0.25:
            x = random.choice([1, 2, 3, -1, -2])
            a = random.randint(1, 3)
            return f"{a}x² = {a*x*x} のとき x = ?（小さい方）", -abs(x)

        # ax^2 + bx + c = 0 型
        r1 = random.choice([-3, -2, -1])
        r2 = random.choice([1, 2, 3])
        a = random.randint(1, 3)
        b = -a * (r1 + r2)
        c = a * r1 * r2
        return f"{a}x² {b:+}x {c:+} = 0 のとき x = ?（小さい方）", r1

# =====================
# セッション初期化
# =====================
if "page" not in st.session_state:
    st.session_state.page = "select"  # select / quiz

# =====================
# 学年選択画面
# =====================
if st.session_state.page == "select":
    st.subheader("学年を選んでね")

    grade = st.radio(
        "",
        ["中学1年", "中学2年", "中学3年"]
    )

    if st.button("▶ スタート"):
        st.session_state.grade = grade
        st.session_state.q_no = 1
        st.session_state.score = 0
        st.session_state.question, st.session_state.answer = make_question(grade)
        st.session_state.start_time = time.time()
        st.session_state.answered = False
        st.session_state.page = "quiz"
        st.rerun()

# =====================
# 問題画面
# =====================
if st.session_state.page == "quiz":
    TOTAL = 15
    LIMIT = 300  # 5分

    elapsed = int(time.time() - st.session_state.start_time)
    remain = LIMIT - elapsed

    st.markdown(f"### ❓ 第 {st.session_state.q_no} 問 / {TOTAL}")
    st.markdown(f"🎓 学年：{st.session_state.grade}")
    st.markdown(f"⏱ 残り時間：**{remain//60}分 {remain%60}秒**")
    st.markdown(f"🏆 正解数：**{st.session_state.score}**")
    st.markdown("---")

    # 終了
    if st.session_state.q_no > TOTAL:
        st.success("🎉 終了！")
        st.markdown(f"## 🏆 正解数：{st.session_state.score} / {TOTAL}")
        if st.button("🔁 最初に戻る"):
            st.session_state.clear()
            st.rerun()
        st.stop()

    # 時間切れ
    if remain <= 0:
        st.error("⏰ 時間切れ！")
        if st.button("➡ 次の問題へ"):
            st.session_state.q_no += 1
            st.session_state.question, st.session_state.answer = make_question(
                st.session_state.grade
            )
            st.session_state.start_time = time.time()
            st.session_state.answered = False
            st.rerun()

    # 問題表示
    st.markdown(st.session_state.question)
    user_answer = st.number_input("答えを入力", step=1)

    # 判定
    if st.button("答え合わせ"):
        if user_answer == st.session_state.answer:
            st.success("⭕ 正解！")
            st.session_state.score += 1
        else:
            st.error(f"❌ 不正解… 正解は {st.session_state.answer}")
        st.session_state.answered = True

    # 次へ
    if st.session_state.answered:
        if st.button("➡ 次の問題"):
            st.session_state.q_no += 1
            st.session_state.question, st.session_state.answer = make_question(
                st.session_state.grade
            )
            st.session_state.start_time = time.time()
            st.session_state.answered = False
            st.rerun()
