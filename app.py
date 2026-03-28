import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# --- 앱 설정 ---
st.set_page_config(page_title="공무원 경력 합산기", page_icon="🗂️", layout="wide")

st.title("🗂️ 공무원 경력 합산 계산기 (v2.2)")

# --- 세션 상태 초기화 ---
if 'career_list' not in st.session_state:
    st.session_state.career_list = [{'content': '', 'start': date.today(), 'end': date.today()}]

def add_career():
    st.session_state.career_list.append({'content': '', 'start': date.today(), 'end': date.today()})

def remove_career(index):
    if len(st.session_state.career_list) > 1:
        st.session_state.career_list.pop(index)

# --- 상단 헤더 (한 번만 표시) ---
st.subheader("1. 경력 사항 입력")
header_cols = st.columns([2.5, 2, 2, 2.5, 0.5])
header_cols[0].write("**내용**")
header_cols[1].write("**시작일**")
header_cols[2].write("**종료일**")
header_cols[3].write("**항목 결과 (역에 의한 계산)**")
header_cols[4].write("")

# --- 입력 및 계산 로직 ---
total_years, total_months, total_days = 0, 0, 0
grand_total_days = 0

for i, career in enumerate(st.session_state.career_list):
    # label_visibility="collapsed"를 써서 라벨을 숨기고 높이를 맞춤
    col1, col2, col3, col4, col5 = st.columns([2.5, 2, 2, 2.5, 0.5])
    
    with col1:
        career['content'] = st.text_input(f"content_{i}", value=career['content'], key=f"c_{i}", label_visibility="collapsed", placeholder="기관명 등")
    with col2:
        career['start'] = st.date_input(f"start_{i}", value=career['start'], key=f"s_{i}", label_visibility="collapsed")
    with col3:
        career['end'] = st.date_input(f"end_{i}", value=career['end'], key=f"e_{i}", label_visibility="collapsed")
    
    # --- 계산 및 정렬 ---
    s, e = career['start'], career['end']
    
    # 3. 날짜 오류 표시 방지: 종료일이 시작일보다 빠를 때만 경고, 입력 중엔 조용히 처리
    if s <= e:
        item_days = (e - s).days + 1
        diff = relativedelta(e + relativedelta(days=1), s)
        res_text = f"{diff.years}년 {diff.months}월 {diff.days}일 ({item_days}일)"
        
        grand_total_days += item_days
        total_years += diff.years
        total_months += diff.months
        total_days += diff.days
        
        # 2. 결과 텍스트를 입력창과 같은 라인에 배치 (vertical_alignment 대신 st.info 스타일 활용)
        with col4:
            st.info(res_text)
    else:
        with col4:
            st.write("---") # 입력 대기 중이거나 오류 시 조용히 대시 표시

    with col5:
        if st.button("❌", key=f"del_{i}"):
            remove_career(i)
            st.rerun()

st.button("➕ 경력 추가", on_click=add_career)

# --- 최종 합산 로직 ---
total_months += total_days // 30
total_days = total_days % 30
total_years += total_months // 12
total_months = total_months % 12

st.markdown("---")
st.subheader("2. 최종 합산 결과")

res_col1, res_col2 = st.columns(2)
with res_col1:
    st.success(f"### 최종 합산: **{total_years}년 {total_months}월 {total_days}일**")
with res_col2:
    st.metric(label="총 일수 합계", value=f"{grand_total_days}일")

st.markdown("---")
st.caption("※ 본 계산기는 입력된 각 기간의 연/월/일을 구한 뒤 합산하며, 남은 일수가 30일 이상이면 1개월로 환산합니다.")
