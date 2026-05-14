import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 페이지 설정 및 디자인 (Tailwind-like CSS 주입)
st.set_page_config(page_title="Everytime Balance Marketing Dashboard", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .kpi-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #1d4ed8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .strategy-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        height: 100%;
    }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Pretendard', sans-serif; }
    </style>
""", unsafe_allow_html=True)

# 2. 데이터 준비
sales_data = pd.DataFrame({
    '채널': ['수도권 편의점', '지방 대형마트'],
    '성장률(%)': [15, -2],
    '색상': ['#1d4ed8', '#f97316']
})

age_data = pd.DataFrame({
    '연령층': ['2030 사회초년생', '3040 부모세대', '5060 시니어', '기타'],
    '비중': [45, 25, 20, 10]
})

keyword_data = pd.DataFrame({
    '키워드': ['등산', '테니스', '자기관리', '선물하기', '오운완'],
    '언급량': [35, 28, 18, 22, 25],
    '성장성': [70, 85, 40, 50, 90]
})

# 3. 헤더 섹션
st.title("🚀 에브리타임 밸런스 마케팅 통찰 보고서")
st.caption("2026년 3월 4주차 | KGC 브랜드 전략실 팀장 보고용")

# 4. KPI 지표 섹션
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("수도권 매출 성장", "+15%", delta="전주 대비")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("2030 구매 비중", "45%", delta="전략 타겟 유입")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-card">', unsafe_allow_html=True)
    st.metric("아웃도어 키워드", "+30%", delta="트렌드 확산")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 5. 판매 및 연령 분석 (차트 섹션)
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 채널별 판매 실적")
    fig_sales = px.bar(sales_data, x='채널', y='성장률(%)', color='채널',
                       color_discrete_sequence=['#1d4ed8', '#f97316'],
                       text_auto=True)
    fig_sales.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_sales, use_container_width=True)
    st.info("수도권 편의점 채널이 리뉴얼 효과를 견인하고 있습니다.")

with chart_col2:
    st.subheader("🎯 핵심 타겟 분포")
    fig_age = px.pie(age_data, values='비중', names='연령층', 
                     hole=0.6, color_discrete_sequence=['#1e3a8a', '#3b82f6', '#93c5fd', '#e2e8f0'])
    st.plotly_chart(fig_age, use_container_width=True)
    st.success("2030 사회초년생이 전체의 45%를 차지하며 주력 고객으로 안착했습니다.")

# 6. 라이프스타일 트렌드 (버블 차트)
st.subheader("🏃 라이프스타일 키워드 분석")
fig_trend = px.scatter(keyword_data, x='언급량', y='성장성', size='언급량', color='키워드',
                       hover_name='키워드', size_max=60,
                       color_discrete_sequence=px.colors.qualitative.Safe)
fig_trend.update_layout(plot_bgcolor='white')
st.plotly_chart(fig_trend, use_container_width=True)
st.markdown("**Insight:** '등산'과 '테니스' 키워드가 성장을 주도하며 제품의 아웃도어 확장성을 증명함.")

# 7. VOC 및 전략 제언 섹션
st.divider()
voc_col1, voc_col2 = st.columns(2)

with voc_col1:
    st.markdown("### 💬 소비자 반응 (VOC)")
    st.write("✅ **긍정:** 쓴맛 개선에 대한 높은 만족도, 선물용 디자인 선호")
    st.write("⚠️ **부정:** 작년 대비 인상된 가격 저항, 박스 개봉 사용성 불만")

with voc_col2:
    st.markdown("### 💡 전략적 핵심 제언")
    with st.expander("1. '갓생 아웃도어' 캠페인 가동"):
        st.write("- 테니스장/등산로 거점 팝업 스토어 및 편의점 연계 프로모션")
    with st.expander("2. 지역/채널별 차별화 프로모션"):
        st.write("- 지방 대형마트 대상 '가족 대용량팩' 또는 보상 판매 이벤트")
    with st.expander("3. 패키지 UX 즉각 개선"):
        st.write("- 이지 오픈 기능 강화 및 생산 공정 정밀 점검")

# 8. 푸터
st.markdown("---")
st.caption("© 2026 KGC Brand Strategy Dept. | 본 보고서는 내부 의사결정용으로 외부 유출을 금합니다.")
