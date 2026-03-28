import streamlit as st
from datetime import date

# --- 앱 제목 및 설명 ---
st.title("📅 역에 의한 날짜 계산기")
st.markdown("---")
st.write("두 날짜 사이의 간격이 며칠인지 계산해 줍니다. (기준일 포함)")

# --- 입력 부 ---
st.subheader("1. 날짜를 선택해 주세요")

# 오늘 날짜를 기본값으로 설정
today = date.today()

# 두 개의 날짜 입력창
start_date = st.date_input("기준 날짜", today)
end_date = st.date_input("종료 날짜", today)

# --- 로직 부 ---
if start_date and end_date:
    # 두 날짜의 차이 계산
    delta = end_date - start_date
    diff_days = delta.days

    # 결과 출력 (보통 D-Day는 기준일을 1일로 포함하므로 +1)
    d_day_result = diff_days + 1

    # --- 출력 부 ---
    st.markdown("---")
    st.subheader("2. 계산 결과")

    if d_day_result > 0:
        st.success(f"**기준일로부터 {d_day_result}일째** 되는 날입니다.")
    elif d_day_result == 1:
        st.info("**오늘입니다.**")
    else:
        # 종료일이 과거일 경우
        st.warning(f"**기준일보다 {abs(d_day_result)+1}일 전입니다.**")

    # 가독성을 위한 부가 정보
    st.info(f"(순수 날짜 차이: {diff_days}일)")

# --- 푸터 ---
st.markdown("---")
st.caption("간단한 스트림릿 실습 앱입니다.")
