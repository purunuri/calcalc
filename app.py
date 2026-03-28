%%writefile app.py
import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# --- 앱 설정 ---
st.set_page_config(page_title="공무원 경력 계산기", page_icon="📜")

st.title("📜 역(曆)에 의한 경력 계산기")
st.markdown("---")
st.write("공무원 인사처 기준에 맞춘 역에 의한 경력 산출 도구입니다.")

# --- 입력 부 ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("임용일 (시작일)", date.today())
with col2:
    end_date = st.date_input("퇴직일 (종료일)", date.today())

# --- 계산 로직 ---
if start_date and end_date:
    if start_date > end_date:
        st.error("⚠️ 시작일이 종료일보다 늦을 수 없습니다.")
    else:
        # 1. 전체 일수 계산 (당일 포함이므로 +1)
        total_days = (end_date - start_date).days + 1

        # 2. 역에 의한 연/월/일 계산
        # 공무원 경력 계산은 종료일 '다음날'까지를 기준으로 상대적 차이를 구함
        diff = relativedelta(end_date + relativedelta(days=1), start_date)
        
        years = diff.years
        months = diff.months
        days = diff.days

        # --- 결과 출력 ---
        st.markdown("### 📊 계산 결과")
        
        # 메인 결과 카드
        st.success(f"### **{years}년 {months}월 {days}일**")
        
        # 상세 정보
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric(label="총 일수", value=f"{total_days}일")
        with col_res2:
            st.info(f"💡 기간: {start_date} ~ {end_date}")

st.markdown("---")
st.caption("※ 본 계산은 민법 제160조(역에 의한 계산) 원칙을 따르며, 종료일 다음날을 기준으로 기간을 산출합니다.")
