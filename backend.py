import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import numpy as np
import os
import hashlib
from datetime import datetime

FILE = "employee_data.csv"
COLUMNS = [
    "Name", "Productivity", "Quality",
    "Attendance", "Task", "Efficiency",
    "KPI", "Rank", "Date Added"
]

ADMIN_CREDENTIALS = {
    "admin": hashlib.sha256("1234".encode()).hexdigest()
}


def init_file():
    if not os.path.exists(FILE):
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(FILE, index=False)


def load_data():
    init_file()
    df = pd.read_csv(FILE)
    if not df.empty:
        df = update_ranks(df)
    return df


def save_data(df):
    df.to_csv(FILE, index=False)


def calculate_kpi(p, q, a, t, e):
    return round((p + q + a + t + e) / 5, 2)


def update_ranks(df):
    if not df.empty:
        df["Rank"] = df["KPI"].rank(ascending=False, method="min").astype(int)
    return df


def add_employee(name, p, q, a, t, e):
    df = load_data()
    kpi = calculate_kpi(p, q, a, t, e)
    new_row = pd.DataFrame([{
        "Name": name,
        "Productivity": p,
        "Quality": q,
        "Attendance": a,
        "Task": t,
        "Efficiency": e,
        "KPI": kpi,
        "Rank": 0,
        "Date Added": datetime.now().strftime("%Y-%m-%d %H:%M")
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df = update_ranks(df)
    save_data(df)
    return kpi


def login(username, password):
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    return username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == pwd_hash


def get_performance_tier(kpi):
    if kpi >= 90:
        return "🏆 Elite", "#FFD700"
    elif kpi >= 75:
        return "⭐ Excellent", "#00E676"
    elif kpi >= 60:
        return "✅ Good", "#29B6F6"
    elif kpi >= 45:
        return "⚠️ Average", "#FFA726"
    else:
        return "🔻 Needs Improvement", "#EF5350"


def get_filtered_data(df, search_term="", tier_filter="All"):
    filtered = df.copy()
    if search_term:
        filtered = filtered[filtered["Name"].str.contains(search_term, case=False, na=False)]
    if tier_filter == "🏆 Elite (90+)":
        filtered = filtered[filtered["KPI"] >= 90]
    elif tier_filter == "⭐ Excellent (75-89)":
        filtered = filtered[(filtered["KPI"] >= 75) & (filtered["KPI"] < 90)]
    elif tier_filter == "✅ Good (60-74)":
        filtered = filtered[(filtered["KPI"] >= 60) & (filtered["KPI"] < 75)]
    elif tier_filter == "⚠️ Average (45-59)":
        filtered = filtered[(filtered["KPI"] >= 45) & (filtered["KPI"] < 60)]
    elif tier_filter == "🔻 Below 45":
        filtered = filtered[filtered["KPI"] < 45]
    return filtered


def get_top_performers(df, n=5):
    if df.empty:
        return df
    return df.nsmallest(n, "Rank")


def get_tier_distribution(df):
    return {
        "Elite (90+)": len(df[df["KPI"] >= 90]),
        "Excellent (75-89)": len(df[(df["KPI"] >= 75) & (df["KPI"] < 90)]),
        "Good (60-74)": len(df[(df["KPI"] >= 60) & (df["KPI"] < 75)]),
        "Average (45-59)": len(df[(df["KPI"] >= 45) & (df["KPI"] < 60)]),
        "Below 45": len(df[df["KPI"] < 45]),
    }


def setup_chart_style():
    plt.rcParams.update({
    
    'figure.facecolor': '#0a0a1a',
    'axes.edgecolor': (1, 1, 1, 0.1),  # ✅ FIXED
})
    


def create_bar_chart(df):
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    sorted_df = df.sort_values("KPI", ascending=True)

    colors = []
    for kpi in sorted_df["KPI"]:
        if kpi >= 90: colors.append("#FFD700")
        elif kpi >= 75: colors.append("#00E676")
        elif kpi >= 60: colors.append("#29B6F6")
        elif kpi >= 45: colors.append("#FFA726")
        else: colors.append("#EF5350")

    bars = ax.barh(sorted_df["Name"], sorted_df["KPI"],
                   color=colors, height=0.6, edgecolor='none', alpha=0.9)

    for bar, kpi in zip(bars, sorted_df["KPI"]):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f'{kpi:.1f}', va='center', ha='left', fontweight='bold',
                fontsize=9, color='#e0e0ff')

    ax.set_xlabel("KPI Score", fontsize=11, fontweight='600')
    ax.set_title("Employee KPI Scores", fontsize=14, fontweight='700', pad=20, color='#e0e0ff')
    ax.set_xlim(0, 110)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='x', alpha=0.1)
    plt.tight_layout()
    return fig


def create_line_chart(df):
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(12, 6))
    sorted_df = df.sort_values("KPI")
    x = range(len(sorted_df))

    ax.fill_between(x, sorted_df["KPI"], alpha=0.15, color='#7c4dff')
    ax.plot(x, sorted_df["KPI"], color='#7c4dff', linewidth=2.5,
            marker='o', markersize=8, markerfacecolor='#b388ff',
            markeredgecolor='#7c4dff', markeredgewidth=2, zorder=5)

    for i, (name, kpi) in enumerate(zip(sorted_df["Name"], sorted_df["KPI"])):
        ax.annotate(f'{kpi:.0f}', (i, kpi), textcoords="offset points",
                    xytext=(0, 14), ha='center', fontsize=8, fontweight='bold',
                    color='#b388ff')

    ax.set_xticks(list(x))
    ax.set_xticklabels(sorted_df["Name"], rotation=35, ha='right', fontsize=9)
    ax.set_ylabel("KPI Score", fontsize=11, fontweight='600')
    ax.set_title("KPI Trend Across Employees", fontsize=14, fontweight='700', pad=20, color='#e0e0ff')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', alpha=0.1)

    avg_kpi = df["KPI"].mean()
    ax.axhline(y=avg_kpi, color='#FFD700', linestyle='--', alpha=0.5, linewidth=1.5)
    ax.text(len(sorted_df) - 1, avg_kpi + 2, f'Avg: {avg_kpi:.1f}',
            color='#FFD700', fontweight='bold', fontsize=9, ha='right')

    plt.tight_layout()
    return fig


def create_pie_chart(df):
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(7, 7))
    metrics = ["Productivity", "Quality", "Attendance", "Task", "Efficiency"]
    avg_values = [df[m].mean() for m in metrics]
    pie_colors = ['#7c4dff', '#448aff', '#00e5ff', '#00e676', '#FFD700']

    wedges, texts, autotexts = ax.pie(
        avg_values, labels=None, autopct='%1.1f%%',
        colors=pie_colors, startangle=140,
        explode=[0.03] * 5, pctdistance=0.82,
        wedgeprops=dict(width=0.45, edgecolor='#0a0a1a', linewidth=2)
    )

    for t in autotexts:
        t.set_fontsize(9)
        t.set_fontweight('bold')
        t.set_color('#e0e0ff')

    ax.legend(
        [f'{m}: {v:.1f}' for m, v in zip(metrics, avg_values)],
        loc='lower center', bbox_to_anchor=(0.5, -0.1),
        ncol=2, fontsize=8.5, framealpha=0, labelcolor='#b0b0d0'
    )
    ax.set_title("Average Metric Distribution", fontsize=13, fontweight='700', pad=20, color='#e0e0ff')
    plt.tight_layout()
    return fig


def create_tier_pie(df):
    setup_chart_style()
    fig, ax = plt.subplots(figsize=(7, 7))
    tier_counts = get_tier_distribution(df)
    tier_colors = {
        "Elite (90+)": "#FFD700",
        "Excellent (75-89)": "#00E676",
        "Good (60-74)": "#29B6F6",
        "Average (45-59)": "#FFA726",
        "Below 45": "#EF5350"
    }
    non_zero = {k: v for k, v in tier_counts.items() if v > 0}

    if non_zero:
        labels = list(non_zero.keys())
        values = list(non_zero.values())
        colors = [tier_colors[k] for k in labels]

        wedges, texts, autotexts = ax.pie(
            values, labels=None, autopct='%1.0f%%',
            colors=colors, startangle=140, pctdistance=0.78,
            wedgeprops=dict(width=0.45, edgecolor='#0a0a1a', linewidth=2)
        )
        for t in autotexts:
            t.set_fontsize(10)
            t.set_fontweight('bold')
            t.set_color('#e0e0ff')

        ax.legend(
            [f'{l}: {v}' for l, v in zip(labels, values)],
            loc='lower center', bbox_to_anchor=(0.5, -0.1),
            ncol=2, fontsize=8.5, framealpha=0, labelcolor='#b0b0d0'
        )

    ax.set_title("Performance Tier Distribution", fontsize=13, fontweight='700', pad=20, color='#e0e0ff')
    plt.tight_layout()
    return fig


def create_radar_chart(df, employee_name):
    setup_chart_style()
    emp_data = df[df["Name"] == employee_name].iloc[0]
    metrics = ["Productivity", "Quality", "Attendance", "Task", "Efficiency"]
    values = [emp_data[m] for m in metrics]
    avg_values = [df[m].mean() for m in metrics]

    angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
    values_plot = values + [values[0]]
    avg_plot = avg_values + [avg_values[0]]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.set_facecolor('#0f0f2a')
    fig.patch.set_facecolor('#0a0a1a')

    ax.fill(angles, values_plot, alpha=0.2, color='#7c4dff')
    ax.plot(angles, values_plot, color='#b388ff', linewidth=2.5, marker='o',
            markersize=8, markerfacecolor='#7c4dff', markeredgecolor='#b388ff')

    ax.fill(angles, avg_plot, alpha=0.08, color='#FFD700')
    ax.plot(angles, avg_plot, color='#FFD700', linewidth=1.5, linestyle='--', alpha=0.5)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics, fontsize=9, fontweight='600', color='#b0b0d0')
    ax.set_ylim(0, 100)
    ax.set_rticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=7, color='#606090')
    ax.spines['polar'].set_color('rgba(255,255,255,0.1)')
    ax.grid(color='rgba(255,255,255,0.06)')

    tier, color = get_performance_tier(emp_data["KPI"])
    ax.set_title(f"{employee_name} — KPI: {emp_data['KPI']:.1f} ({tier})",
                  fontsize=13, fontweight='700', pad=30, color='#e0e0ff')
    ax.legend(['Employee', 'Team Average'], loc='lower right',
               bbox_to_anchor=(1.15, -0.05), fontsize=9, framealpha=0,
               labelcolor='#b0b0d0')
    plt.tight_layout()
    return fig
