import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# --- 앱 설정 ---
st.set_page_config(page_title="공무원 경력 합산기", page_icon="🗂️", layout="wide")

st.title("🗂️ 공무원 경력 합산 계산기 (v2.1)")
st.markdown("각 경력별 계산 결과를 실시간으로 확인하고 합산할 수 있습니다.")

# --- 세션 상태 초기화 ---
if 'career_list' not in st.session_state:
    st.session_state.career_list = [{'content': '', 'start': date.today(), 'end': date.today()}]

def add_career():
    st.session_state.career_list.append({'content': '', 'start': date.today(), 'end': date.today()})

def remove_career(index):
    if len(st.session_state.career_list) > 1:
        st.session_state.career_list.pop(index)

# --- 입력 및 항목별 계산 UI ---
st.subheader("1. 경력 사항 입력 및 항목별 계산")

total_years, total_months, total_days = 0, 0, 0
grand_total_days = 0

for i, career in enumerate(st.session_state.career_list):
    # 칸을 5개로 나눠서 입력과 개별 결과를 한 줄에 배치
    col1, col2, col3, col4, col5 = st.columns([2.5, 2, 2, 2.5, 1])
    
    with col1:
        career['content'] = st.text_input(f"내용", value=career['content'], key=f"content_{i}", placeholder="기관명 등")
    with col2:
        career['start'] = st.date_input(f"시작일", value=career['start'], key=f"start_{i}")
    with col3:
        career['end'] = st.date_input(f"종료일", value=career['end'], key=f"end_{i}")
    
    # --- 개별 항목 계산 ---
    s, e = career['start'], career['end']
    if s <= e:
        item_days = (e - s).days + 1
        diff = relativedelta(e + relativedelta(days=1), s)
        
        # 개별 결과 표시 (4번째 칸)
        with col4:
            st.write("⏱️ 항목 결과")
            st.code(f"{diff.years}년 {diff.months}월 {diff.days}일 ({item_days}일)")
        
        # 전체 합산을 위한 누적
        grand_total_days += item_days
        total_years += diff.years
        total_months += diff.months
        total_days += diff.days
    else:
        with col4:
            st.write(" ")
            st.error("날짜 오류")

    with col5:
        st.write(" ")
        if st.button("❌", key=f"del_{i}"):
            remove_career(i)
            st.rerun()

st.button("➕ 경력 추가", on_click=add_career)

# --- 최종 합산 로직 (30일/12개월 단위 올림) ---
total_months += total_days // 30
total_days = total_days % 30
total_years += total_months // 12
total_months = total_months % 12

# --- 최종 결과 출력 ---
st.markdown("---")
st.subheader("2. 최종 합산 결과")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.success(f"### 최종 합산: **{total_years}년 {total_months}월 {total_days}일**")
with res_col2:
    st.metric(label="총 일수 합계", value=f"{grand_total_days}일")

st.markdown("---")
st.caption("※ 각 항목의 '년/월/일'을 먼저 계산한 후 합산하며, 남은 일수가 30일 이상일 경우 1개월로 환산합니다.")
