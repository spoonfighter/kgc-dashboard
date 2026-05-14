import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="에브리타임 밸런스 자동화 대시보드", layout="wide")

# 2. 구글 시트 URL (CSV 내보내기 형식)
# https://docs.google.com/spreadsheets/d/1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo/edit?usp=sharing
SHEET_URL = "https://docs.google.com/spreadsheets/d/1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo/export?format=csv"

# 3. 데이터 로드 함수 (캐싱 적용)
@st.cache_data(ttl=60) # 1분마다 새로고침
def load_data(url):
    df = pd.read_csv(url)
    return df

try:
    df = load_data(SHEET_URL)

    st.title("🚀 실시간 마케팅 데이터 대시보드")
    st.markdown("구글 스프레드시트와 직접 연결되어 데이터 입력 시 실시간으로 반영됩니다.")

    # 4. 상단 지표 (KPI)
    # 시트에 '성장률', '비중', '키워드상승' 컬럼이 있다고 가정
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("수도권 성장률", f"{df.iloc[0]['성장률']}%")
    with m2:
        st.metric("2030 구매비중", f"{df.iloc[0]['비중']}%")
    with m3:
        st.metric("아웃도어 키워드", f"{df.iloc[0]['키워드상승']}%")

    st.divider()

    # 5. 시각화 차트
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 지역별 판매 분포")
        fig1 = px.bar(df, x='지역', y='판매량', color='지역', 
                      color_discrete_sequence=['#1d4ed8', '#f97316'])
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("🏃 라이프스타일 트렌드")
        fig2 = px.scatter(df, x='언급량', y='성장성', size='언급량', color='키워드',
                          hover_name='키워드')
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"데이터를 가져오지 못했습니다. 공유 설정을 확인하세요! 💡 오류: {e}")
