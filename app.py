import streamlit as st
from datetime import date
from dateutil.relativedelta import relativedelta

# --- 앱 설정 ---
st.set_page_config(page_title="공무원 경력 합산기", page_icon="🗂️", layout="wide")

st.title("🗂️ 공무원 경력 합산 계산기 (v2.0)")
st.markdown("여러 개의 경력을 입력하면 역에 의해 합산하여 최종 결과를 보여줍니다.")

# --- 세션 상태 초기화 (경력 리스트 저장용) ---
if 'career_list' not in st.session_state:
    st.session_state.career_list = [{'content': '', 'start': date.today(), 'end': date.today()}]

# --- 기능 함수: 경력 추가/삭제 ---
def add_career():
    st.session_state.career_list.append({'content': '', 'start': date.today(), 'end': date.today()})

def remove_career(index):
    if len(st.session_state.career_list) > 1:
        st.session_state.career_list.pop(index)

# --- 입력 UI ---
st.subheader("1. 경력 사항 입력")
for i, career in enumerate(st.session_state.career_list):
    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
    
    with col1:
        career['content'] = st.text_input(f"내용 (선택)", value=career['content'], key=f"content_{i}", placeholder="예: OO초등학교 근무")
    with col2:
        career['start'] = st.date_input(f"시작일", value=career['start'], key=f"start_{i}")
    with col3:
        career['end'] = st.date_input(f"종료일", value=career['end'], key=f"end_{i}")
    with col4:
        st.write(" ") # 간격 맞추기용
        if st.button("삭제", key=f"del_{i}"):
            remove_career(i)
            st.rerun()

st.button("➕ 경력 추가", on_click=add_career)

# --- 계산 로직 ---
st.markdown("---")
st.subheader("2. 최종 합산 결과")

total_years = 0
total_months = 0
total_days = 0
grand_total_days = 0

for career in st.session_state.career_list:
    s = career['start']
    e = career['end']
    
    if s <= e:
        # 각 항목별 일수 (당일 포함 +1)
        item_total_days = (e - s).days + 1
        grand_total_days += item_total_days
        
        # 역에 의한 차이 계산 (종료일 다음날 기준)
        diff = relativedelta(e + relativedelta(days=1), s)
        total_years += diff.years
        total_months += diff.months
        total_days += diff.days

# 월과 일 올림 처리 (30일 -> 1월, 12월 -> 1년)
# ※ 참고: 공무원 획일적 계산 방식에 따라 단순 합산 후 조정
total_months += total_days // 30
total_days = total_days % 30
total_years += total_months // 12
total_months = total_months % 12

# --- 결과 출력 ---
res_col1, res_col2 = st.columns(2)

with res_col1:
    st.success(f"### 합산 경력: **{total_years}년 {total_months}월 {total_days}일**")
    st.info(f"💡 모든 기간을 역에 의해 합산한 결과입니다.")

with res_col2:
    st.metric(label="총 일수 합계", value=f"{grand_total_days}일")

st.markdown("---")
st.caption("※ 본 계산기는 입력된 각 기간의 연/월/일을 먼저 구한 뒤 합산하며, 남은 일수가 30일 이상일 경우 1개월로 환산합니다.")
