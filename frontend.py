import streamlit as st
import time
from datetime import datetime

from backend import (
    load_data, add_employee, login, get_performance_tier,
    get_filtered_data, get_top_performers, calculate_kpi,
    create_bar_chart, create_line_chart, create_pie_chart,
    create_tier_pie, create_radar_chart
)


def apply_glass_ui():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

        .stApp {
            background: linear-gradient(135deg, #0a0a1a 0%, #1a1a3e 25%, #0d0d2b 50%, #1a0a2e 75%, #0a0a1a 100%);
            font-family: 'Inter', sans-serif;
        }

        [data-testid="stSidebar"] {
            background: rgba(15, 15, 40, 0.95) !important;
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255,255,255,0.06);
        }

        [data-testid="stSidebar"] .stMarkdown h1,
        [data-testid="stSidebar"] .stMarkdown h2,
        [data-testid="stSidebar"] .stMarkdown h3 {
            color: #e0e0ff !important;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px 32px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                        inset 0 1px 0 rgba(255,255,255,0.05);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .glass-card:hover {
            background: rgba(255, 255, 255, 0.06);
            border-color: rgba(255,255,255,0.12);
            transform: translateY(-2px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4),
                        inset 0 1px 0 rgba(255,255,255,0.08);
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.03);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            transition: all 0.3s ease;
        }

        .metric-card:hover {
            background: rgba(255, 255, 255, 0.06);
            transform: translateY(-4px);
            box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
        }

        .metric-value {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #7c4dff, #448aff, #00e5ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 8px 0;
        }

        .metric-label {
            font-size: 0.85rem;
            color: rgba(255, 255, 255, 0.5);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
        }

        .hero-title {
            font-size: 2.8rem;
            font-weight: 900;
            background: linear-gradient(135deg, #b388ff 0%, #7c4dff 30%, #448aff 60%, #00e5ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
            letter-spacing: -1px;
            line-height: 1.1;
        }

        .hero-subtitle {
            font-size: 1.05rem;
            color: rgba(255, 255, 255, 0.45);
            font-weight: 400;
            letter-spacing: 0.3px;
        }

        .section-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #e0e0ff;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .top-performer-card {
            background: linear-gradient(135deg, rgba(124, 77, 255, 0.15), rgba(68, 138, 255, 0.1));
            border: 1px solid rgba(124, 77, 255, 0.25);
            border-radius: 16px;
            padding: 20px 24px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }

        .top-performer-card:hover {
            transform: translateX(8px);
            background: linear-gradient(135deg, rgba(124, 77, 255, 0.2), rgba(68, 138, 255, 0.15));
        }

        .rank-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 36px;
            height: 36px;
            border-radius: 10px;
            font-weight: 800;
            font-size: 0.95rem;
            margin-right: 16px;
        }

        .rank-1 { background: linear-gradient(135deg, #FFD700, #FFA000); color: #1a1a1a; }
        .rank-2 { background: linear-gradient(135deg, #B0BEC5, #78909C); color: #1a1a1a; }
        .rank-3 { background: linear-gradient(135deg, #A1887F, #795548); color: #fff; }
        .rank-other { background: rgba(255,255,255,0.08); color: rgba(255,255,255,0.7); }

        .emp-name {
            font-weight: 600;
            color: #e0e0ff;
            font-size: 1.05rem;
        }

        .kpi-badge {
            font-weight: 700;
            font-size: 1.1rem;
            padding: 6px 14px;
            border-radius: 10px;
            background: rgba(124, 77, 255, 0.15);
            color: #b388ff;
        }

        .login-container {
            max-width: 420px;
            margin: 80px auto;
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(30px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 48px 40px;
            box-shadow: 0 24px 80px rgba(0, 0, 0, 0.5);
        }

        .login-title {
            font-size: 2rem;
            font-weight: 800;
            text-align: center;
            background: linear-gradient(135deg, #b388ff, #7c4dff, #448aff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }

        .login-subtitle {
            text-align: center;
            color: rgba(255,255,255,0.4);
            font-size: 0.9rem;
            margin-bottom: 32px;
        }

        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #e0e0ff !important;
            padding: 12px 16px !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: rgba(124, 77, 255, 0.5) !important;
            box-shadow: 0 0 0 3px rgba(124, 77, 255, 0.1) !important;
        }

        .stNumberInput > div > div > input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #e0e0ff !important;
            font-family: 'Inter', sans-serif !important;
        }

        .stSelectbox > div > div {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }

        .stButton > button {
            background: linear-gradient(135deg, #7c4dff, #448aff) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 12px 32px !important;
            font-weight: 600 !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.5px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 16px rgba(124, 77, 255, 0.3) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 24px rgba(124, 77, 255, 0.4) !important;
        }

        .stSlider > div > div > div > div {
            background: linear-gradient(90deg, #7c4dff, #448aff) !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.06);
        }

        .stTabs [data-baseweb="tab-list"] {
            background: rgba(255, 255, 255, 0.03);
            border-radius: 12px;
            padding: 4px;
            border: 1px solid rgba(255,255,255,0.06);
            gap: 4px;
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 10px !important;
            color: rgba(255,255,255,0.5) !important;
            font-weight: 500 !important;
            padding: 10px 20px !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(124, 77, 255, 0.2) !important;
            color: #b388ff !important;
        }

        .divider {
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(124, 77, 255, 0.3), transparent);
            margin: 24px 0;
        }

        .stDownloadButton > button {
            background: linear-gradient(135deg, #00e676, #00c853) !important;
            color: #1a1a1a !important;
            font-weight: 700 !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 10px 24px !important;
        }

        [data-testid="stMetric"] {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 20px;
        }

        [data-testid="stMetric"] label {
            color: rgba(255,255,255,0.5) !important;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.75rem !important;
        }

        [data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #e0e0ff !important;
            font-weight: 800 !important;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .animate-in {
            animation: fadeInUp 0.6s ease forwards;
        }

        .watermark {
            position: fixed;
            bottom: 12px;
            right: 20px;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.15);
            font-weight: 500;
            letter-spacing: 1px;
            z-index: 9999;
        }
    </style>
    """, unsafe_allow_html=True)


def login_ui():
    st.markdown("""
        <div class="login-container animate-in">
            <div class="login-title">🔐 PerformX</div>
            <div class="login-subtitle">Employee Performance Analytics Platform</div>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter admin username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

            if submitted:
                if login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.login_time = datetime.now().strftime("%H:%M:%S")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

        st.markdown("""
            <div style="text-align:center; margin-top:16px; color:rgba(255,255,255,0.25); font-size:0.8rem;">
                Default: admin / 1234
            </div>
        """, unsafe_allow_html=True)


def sidebar_menu(df):
    with st.sidebar:
        st.markdown("""
            <div style="text-align:center; padding: 20px 0 8px 0;">
                <div style="font-size:2rem; font-weight:900;
                    background: linear-gradient(135deg, #b388ff, #7c4dff, #448aff);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                    background-clip: text;">PerformX</div>
                <div style="color:rgba(255,255,255,0.35); font-size:0.75rem;
                    letter-spacing:2px; text-transform:uppercase; margin-top:2px;">
                    Analytics Suite</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["📊 Dashboard", "➕ Add Employee", "📈 Visualizations", "🏆 Rankings"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        if not df.empty:
            st.markdown(f"""
                <div class="metric-card" style="margin-top:8px;">
                    <div class="metric-label">Total Employees</div>
                    <div class="metric-value">{len(df)}</div>
                </div>
            """, unsafe_allow_html=True)

            avg_kpi = df["KPI"].mean()
            st.markdown(f"""
                <div class="metric-card" style="margin-top:12px;">
                    <div class="metric-label">Average KPI</div>
                    <div class="metric-value">{avg_kpi:.1f}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.markdown(f"""
            <div style="color:rgba(255,255,255,0.2); font-size:0.7rem; padding:8px 0;">
                🕐 Session: {st.session_state.get('login_time', 'N/A')}
            </div>
        """, unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    return page


def dashboard_ui(df):
    st.markdown("""
        <div class="animate-in">
            <div class="hero-title">Dashboard Overview</div>
            <div class="hero-subtitle">Monitor employee performance metrics in real-time</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
            <div class="glass-card" style="text-align:center; padding:60px;">
                <div style="font-size:3rem; margin-bottom:16px;">📋</div>
                <div style="font-size:1.2rem; color:#e0e0ff; font-weight:600;">No Employee Data Yet</div>
                <div style="color:rgba(255,255,255,0.4); margin-top:8px;">
                    Navigate to "Add Employee" to start building your analytics.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Employees", len(df))
    with col2:
        st.metric("Avg KPI Score", f"{df['KPI'].mean():.1f}")
    with col3:
        st.metric("Top KPI", f"{df['KPI'].max():.1f}")
    with col4:
        elite_count = len(df[df["KPI"] >= 90])
        st.metric("Elite Performers", elite_count)

    st.markdown("<br>", unsafe_allow_html=True)

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search_term = st.text_input("🔍 Search Employees", placeholder="Type a name...")
    with col_filter:
        tier_filter = st.selectbox("Filter by Tier", [
            "All", "🏆 Elite (90+)", "⭐ Excellent (75-89)",
            "✅ Good (60-74)", "⚠️ Average (45-59)", "🔻 Below 45"
        ])

    filtered = get_filtered_data(df, search_term, tier_filter)

    st.markdown('<div class="section-title">📋 Employee Records</div>', unsafe_allow_html=True)

    display_df = filtered[["Rank", "Name", "Productivity", "Quality",
                           "Attendance", "Task", "Efficiency", "KPI", "Date Added"]]
    display_df = display_df.sort_values("Rank")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn("🏅 Rank", width="small"),
            "KPI": st.column_config.ProgressColumn(
                "KPI Score", min_value=0, max_value=100, format="%.1f"
            ),
            "Productivity": st.column_config.ProgressColumn(
                "Productivity", min_value=0, max_value=100, format="%.0f"
            ),
            "Quality": st.column_config.ProgressColumn(
                "Quality", min_value=0, max_value=100, format="%.0f"
            ),
            "Attendance": st.column_config.ProgressColumn(
                "Attendance", min_value=0, max_value=100, format="%.0f"
            ),
            "Task": st.column_config.ProgressColumn(
                "Tasks", min_value=0, max_value=100, format="%.0f"
            ),
            "Efficiency": st.column_config.ProgressColumn(
                "Efficiency", min_value=0, max_value=100, format="%.0f"
            ),
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col_dl1, col_dl2, _ = st.columns([1, 1, 2])
    with col_dl1:
        csv_data = filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Report (CSV)",
            data=csv_data,
            file_name=f"employee_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    with col_dl2:
        full_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📦 Download All Data",
            data=full_csv,
            file_name=f"all_employees_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">🌟 Top 5 Performers</div>', unsafe_allow_html=True)

    top5 = get_top_performers(df, 5)
    for _, row in top5.iterrows():
        rank = int(row["Rank"])
        tier, color = get_performance_tier(row["KPI"])
        rank_class = f"rank-{rank}" if rank <= 3 else "rank-other"
        st.markdown(f"""
            <div class="top-performer-card">
                <div style="display:flex; align-items:center;">
                    <div class="rank-badge {rank_class}">#{rank}</div>
                    <div>
                        <div class="emp-name">{row['Name']}</div>
                        <div style="color:{color}; background:rgba(255,255,255,0.05);
                            display:inline-block; margin-top:4px; padding:4px 12px;
                            border-radius:20px; font-size:0.8rem; font-weight:600;">{tier}</div>
                    </div>
                </div>
                <div class="kpi-badge">{row['KPI']:.1f}</div>
            </div>
        """, unsafe_allow_html=True)


def add_employee_ui():
    st.markdown("""
        <div class="animate-in">
            <div class="hero-title">Add Employee</div>
            <div class="hero-subtitle">Enter performance metrics for a new employee</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("employee_form", clear_on_submit=True):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        name = st.text_input("👤 Employee Name", placeholder="Enter full name")

        st.markdown('<div class="section-title" style="margin-top:16px;">📊 Performance Metrics</div>',
                    unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            productivity = st.slider("🚀 Productivity", 0, 100, 50, help="Work output and deliverables")
            quality = st.slider("💎 Quality of Work", 0, 100, 50, help="Accuracy and attention to detail")
            attendance = st.slider("📅 Attendance / Punctuality", 0, 100, 50, help="Presence and time management")

        with col2:
            task = st.slider("✅ Task Completion Rate", 0, 100, 50, help="Percentage of tasks completed on time")
            efficiency = st.slider("⚡ Efficiency", 0, 100, 50, help="Resource utilization and speed")

        kpi_preview = calculate_kpi(productivity, quality, attendance, task, efficiency)
        tier, color = get_performance_tier(kpi_preview)

        st.markdown(f"""
            <div style="background: rgba(124, 77, 255, 0.08); border: 1px solid rgba(124, 77, 255, 0.2);
                        border-radius: 16px; padding: 20px; margin: 16px 0; text-align: center;">
                <div style="color: rgba(255,255,255,0.5); font-size: 0.8rem; text-transform: uppercase;
                            letter-spacing: 1.5px; font-weight: 600;">KPI Preview</div>
                <div style="font-size: 2.5rem; font-weight: 800; color: #e0e0ff; margin: 4px 0;">{kpi_preview:.1f}</div>
                <div style="color: {color}; font-weight: 600;">{tier}</div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
        submitted = st.form_submit_button("💾 Save Employee Record", use_container_width=True)

        if submitted:
            if not name.strip():
                st.error("❌ Please enter an employee name.")
            else:
                kpi = add_employee(name.strip(), productivity, quality, attendance, task, efficiency)
                st.success(f"✅ {name} has been added successfully! KPI: {kpi}")
                st.balloons()
                time.sleep(1)
                st.rerun()


def visualizations_ui(df):
    st.markdown("""
        <div class="animate-in">
            <div class="hero-title">Visual Analytics</div>
            <div class="hero-subtitle">Comprehensive performance insights through interactive charts</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
            <div class="glass-card" style="text-align:center; padding:60px;">
                <div style="font-size:3rem; margin-bottom:16px;">📊</div>
                <div style="font-size:1.2rem; color:#e0e0ff; font-weight:600;">No Data to Visualize</div>
                <div style="color:rgba(255,255,255,0.4); margin-top:8px;">
                    Add employees first to see performance charts.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    import matplotlib.pyplot as plt

    tab1, tab2, tab3, tab4 = st.tabs(["📊 KPI Bar Chart", "📈 KPI Trends", "🥧 Metric Distribution", "🔬 Radar Analysis"])

    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = create_bar_chart(df)
        st.pyplot(fig)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        fig = create_line_chart(df)
        st.pyplot(fig)
        plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            fig = create_pie_chart(df)
            st.pyplot(fig)
            plt.close(fig)
        with col2:
            fig = create_tier_pie(df)
            st.pyplot(fig)
            plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        if len(df) > 0:
            selected = st.selectbox("Select Employee for Radar Analysis",
                                     df.sort_values("Rank")["Name"].tolist())
            fig = create_radar_chart(df, selected)
            st.pyplot(fig)
            plt.close(fig)
        st.markdown('</div>', unsafe_allow_html=True)


def rankings_ui(df):
    st.markdown("""
        <div class="animate-in">
            <div class="hero-title">Performance Rankings</div>
            <div class="hero-subtitle">Complete employee ranking based on KPI scores</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if df.empty:
        st.markdown("""
            <div class="glass-card" style="text-align:center; padding:60px;">
                <div style="font-size:3rem; margin-bottom:16px;">🏆</div>
                <div style="font-size:1.2rem; color:#e0e0ff; font-weight:600;">No Rankings Available</div>
                <div style="color:rgba(255,255,255,0.4); margin-top:8px;">
                    Add employees to see rankings.
                </div>
            </div>
        """, unsafe_allow_html=True)
        return

    col1, col2, col3 = st.columns(3)
    top3 = get_top_performers(df, 3)

    podium = [
        (col2, "🥇", "1st Place", "#FFD700", "linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,160,0,0.08))"),
        (col1, "🥈", "2nd Place", "#B0BEC5", "linear-gradient(135deg, rgba(176,190,197,0.15), rgba(120,144,156,0.08))"),
        (col3, "🥉", "3rd Place", "#A1887F", "linear-gradient(135deg, rgba(161,136,127,0.15), rgba(121,85,72,0.08))"),
    ]

    for i, (col, medal, place, color, bg) in enumerate(podium):
        with col:
            if i < len(top3):
                row = top3.iloc[i]
                tier, tier_color = get_performance_tier(row["KPI"])
                st.markdown(f"""
                    <div class="glass-card" style="text-align:center; background:{bg};
                         border-color:{color}33; padding:32px 20px;">
                        <div style="font-size:3rem;">{medal}</div>
                        <div style="font-size:0.75rem; color:{color}; text-transform:uppercase;
                             letter-spacing:2px; font-weight:700; margin:8px 0;">{place}</div>
                        <div style="font-size:1.3rem; font-weight:700; color:#e0e0ff;
                             margin:12px 0 4px 0;">{row['Name']}</div>
                        <div style="font-size:2.2rem; font-weight:900; color:{color};
                             margin:4px 0;">{row['KPI']:.1f}</div>
                        <div style="color:{tier_color}; font-size:0.85rem; font-weight:600;">{tier}</div>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">📋 Full Rankings</div>', unsafe_allow_html=True)

    ranked_df = df.sort_values("Rank")
    for _, row in ranked_df.iterrows():
        rank = int(row["Rank"])
        tier, color = get_performance_tier(row["KPI"])
        rank_class = f"rank-{rank}" if rank <= 3 else "rank-other"

        metrics_html = ""
        for label, key in [("PRD", "Productivity"), ("QUA", "Quality"),
                            ("ATT", "Attendance"), ("TSK", "Task"), ("EFF", "Efficiency")]:
            val = row[key]
            m_color = "#00E676" if val >= 75 else ("#FFA726" if val >= 50 else "#EF5350")
            metrics_html += f"""
                <span style="background:rgba(255,255,255,0.04); padding:3px 8px; border-radius:6px;
                      font-size:0.7rem; color:{m_color}; font-weight:500; margin-right:4px;">
                    {label} {val:.0f}
                </span>
            """

        st.markdown(f"""
            <div class="top-performer-card">
                <div style="display:flex; align-items:center; flex:1;">
                    <div class="rank-badge {rank_class}">#{rank}</div>
                    <div>
                        <div class="emp-name">{row['Name']}</div>
                        <div style="margin-top:6px;">{metrics_html}</div>
                    </div>
                </div>
                <div style="text-align:right;">
                    <div class="kpi-badge">{row['KPI']:.1f}</div>
                    <div style="color:{color}; font-size:0.75rem; font-weight:600; margin-top:4px;">{tier}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
