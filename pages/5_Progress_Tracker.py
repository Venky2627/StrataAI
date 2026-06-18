import streamlit as st
import pandas as pd
from src.db.database import get_quiz_history, get_study_history

st.set_page_config(page_title="Progress Tracker | StrataAI", layout="wide")

# --- CUSTOM CSS FOR FLASHY ANALYTICS ---
st.markdown("""
<style>
    /* Flashy Gradient Header */
    .progress-header {
        background: linear-gradient(135deg, #00C9FF 0%, #92FE9D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.2rem;
    }
    .progress-sub {
        color: #A0A0A0;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Sleek Metric Cards */
    .metric-card {
        background: rgba(30, 30, 36, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #f0f0f0;
        margin-bottom: 0.2rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #00C9FF;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="progress-header">Progress Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="progress-sub">Track your mastery, review historical scores, and measure your study commitments.</div>', unsafe_allow_html=True)

# Fetch data
quiz_data = get_quiz_history()
study_data = get_study_history()

# --- HIGH LEVEL METRICS ---
col1, col2, col3 = st.columns(3)

total_quizzes = len(quiz_data)
total_hours_planned = sum([row[2] * row[3] for row in study_data]) if study_data else 0

average_score = 0
if total_quizzes > 0:
    # Score percentage: (score / max_score) * 100
    percentages = [(row[3] / row[4]) * 100 for row in quiz_data if row[4] > 0]
    if percentages:
        average_score = sum(percentages) / len(percentages)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_quizzes}</div>
        <div class="metric-label">Quizzes Completed</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{average_score:.1f}%</div>
        <div class="metric-label">Average Accuracy</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_hours_planned}h</div>
        <div class="metric-label">Total Hours Planned</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><hr style='border-color: #333;'><br>", unsafe_allow_html=True)

# --- CHARTS AND TABLES ---
col_chart, col_history = st.columns([2, 1])

with col_chart:
    st.markdown("### Performance Trajectory")
    if quiz_data:
        # Convert to pandas dataframe for charting
        df = pd.DataFrame(quiz_data, columns=['Timestamp', 'Document', 'Type', 'Score', 'Max Score'])
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        # Calculate percentage
        df['Accuracy (%)'] = (df['Score'] / df['Max Score']) * 100
        
        # Sort by chronological order for the line chart
        df = df.sort_values(by='Timestamp')
        
        st.line_chart(df, x='Timestamp', y='Accuracy (%)', color='#00C9FF')
    else:
        st.info("Take a quiz in the Arena or Study Space to see your performance graph here!")

with col_history:
    st.markdown("### Recent Activity")
    
    tab1, tab2 = st.tabs(["Quizzes", "Study Plans"])
    
    with tab1:
        if quiz_data:
            df_q = pd.DataFrame(quiz_data, columns=['Date', 'Doc', 'Type', 'Score', 'Max'])
            df_q['Date'] = pd.to_datetime(df_q['Date']).dt.strftime('%b %d, %H:%M')
            df_q['Score'] = df_q['Score'].astype(str) + "/" + df_q['Max'].astype(str)
            st.dataframe(df_q[['Date', 'Type', 'Score']], hide_index=True, use_container_width=True)
        else:
            st.write("No quiz data yet.")
            
    with tab2:
        if study_data:
            df_s = pd.DataFrame(study_data, columns=['Date', 'Docs', 'Days', 'Hrs/Day', 'Goal'])
            df_s['Date'] = pd.to_datetime(df_s['Date']).dt.strftime('%b %d, %H:%M')
            df_s['Total Hrs'] = df_s['Days'] * df_s['Hrs/Day']
            st.dataframe(df_s[['Date', 'Total Hrs', 'Goal']], hide_index=True, use_container_width=True)
        else:
            st.write("No study plans generated yet.")
