import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="에브리타임 밸런스 실시간 대시보드", layout="wide")

# 2. 구글 시트 URL (CSV 내보내기 형식)
SHEET_ID = "1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        # 데이터를 읽어오고 공백 제거
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

df = load_data(SHEET_URL)

if df is not None:
    st.title("🚀 실시간 마케팅 데이터 대시보드")
    st.markdown("구글 스프레드시트의 **KPI 탭** 데이터가 실시간으로 반영됩니다.")
    
    # 데이터 처리 함수: label 열에서 특정 이름을 찾아 value와 delta를 반환
    def get_metric(label_name):
        # 해당 라벨을 포함하는 행 찾기
        row = df[df['label'].str.contains(label_name, na=False)]
        if not row.empty:
            val = row.iloc[0]['value']
            # 숫자가 0.95와 같은 형태일 경우 %로 변환
            if isinstance(val, (float, int)) and val <= 1.0:
                display_val = f"{val*100:.1f}%"
            else:
                display_val = str(val)
            
            delta_val = row.iloc[0]['delta']
            return display_val, delta_val
        return "N/A", "데이터 없음"

    # 3. 상단 지표 (KPI)
    m1_val, m1_delta = get_metric("수도권 판매량")
    m2_val, m2_delta = get_metric("핵심 타겟층")
    m3_val, m3_delta = get_metric("스포츠 키워드")
    m4_val, m4_delta = get_metric("긍정 리뷰")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("수도권 판매량", m1_val, m1_delta)
    with col2:
        st.metric("2030 타겟 비중", m2_val, m2_delta)
    with col3:
        st.metric("스포츠 키워드", m3_val, m3_delta)
    with col4:
        st.metric("긍정 리뷰 비율", m4_val, m4_delta)

    st.divider()

    # 4. 시각화
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 지역별 성장률 추이")
        mock_data = pd.DataFrame({
            "지역": ["수도권", "강원", "충청", "호남", "영남"],
            "성장률": [15, 5, 8, -2, 4]
        })
        fig1 = px.bar(mock_data, x="지역", y="성장률", color="성장률", 
                      color_continuous_scale="Blues")
        st.plotly_chart(fig1, use_container_width=True)

    with chart_col2:
        st.subheader("🎯 타겟 유입 분석")
        fig2 = px.pie(values=[45, 25, 20, 10], names=["2030", "4050", "60대", "기타"], hole=0.5)
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.error("데이터를 불러올 수 없습니다. 구글 시트의 공유 설정을 다시 확인하세요.")
