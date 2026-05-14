import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정
st.set_page_config(page_title="에브리타임 밸런스 실시간 대시보드", layout="wide")

# 2. 구글 시트 URL
SHEET_ID = "1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/1Q1egbrduWjUgHm_DZii1jtNuNtG_cQekcD4tiPbwCZo/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def load_data(url):
    try:
        # 데이터 로드 시 헤더가 없는 행도 포함하기 위해 스킵 없이 읽음
        df = pd.read_csv(url, header=None) 
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return None

df_raw = load_data(SHEET_URL)

if df_raw is not None:
    st.title("🚀 실시간 마케팅 데이터 대시보드")
    
    # --- [추가] A7 셀 데이터 추출 (요약 문구) ---
    # 이미지 image_b1111d.png 기준 7행 1열(A7) 데이터를 가져옵니다.
    # pandas 인덱스는 0부터 시작하므로 A7은 [6, 0] 위치입니다.
    try:
        summary_text = df_raw.iloc[6, 0] 
        if pd.notnull(summary_text):
            st.info(f"📝 **실시간 데이터 요약:** {summary_text}")
    except:
        st.write("요약 데이터를 불러오는 중입니다...")

    st.divider()

    # --- 기존 KPI 로직 (헤더 재설정 후 처리) ---
    df = df_raw.copy()
    df.columns = df.iloc[0] # 첫 행을 컬럼명으로
    df = df[1:].reset_index(drop=True)
    df.columns = df.columns.str.strip()

    def get_metric(label_name):
        row = df[df['label'].str.contains(label_name, na=False)]
        if not row.empty:
            val = row.iloc[0]['value']
            delta_val = row.iloc[0]['delta']
            return val, delta_val
        return "N/A", None

    m1_val, m1_delta = get_metric("수도권 판매량")
    m2_val, m2_delta = get_metric("핵심 타겟층")
    m3_val, m3_delta = get_metric("스포츠 키워드")
    m4_val, m4_delta = get_metric("긍정 리뷰")

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("수도권 판매량", m1_val, m1_delta)
    with col2: st.metric("2030 타겟 비중", m2_val, m2_delta)
    with col3: st.metric("스포츠 키워드", m3_val, m3_delta)
    with col4: st.metric("긍정 리뷰 비율", m4_val, m4_delta)

    # 4. 시각화 (기존 동일)
    st.divider()
    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.subheader("📊 지역별 성장률 추이")
        mock_data = pd.DataFrame({"지역": ["수도권", "강원", "충청", "호남", "영남"], "성장률": [15, 5, 8, -2, 4]})
        st.plotly_chart(px.bar(mock_data, x="지역", y="성장률", color="성장률", color_continuous_scale="Blues"), use_container_width=True)
    with chart_col2:
        st.subheader("🎯 타겟 유입 분석")
        st.plotly_chart(px.pie(values=[45, 25, 20, 10], names=["2030", "4050", "60대", "기타"], hole=0.5), use_container_width=True)

else:
    st.error("데이터를 불러올 수 없습니다.")
