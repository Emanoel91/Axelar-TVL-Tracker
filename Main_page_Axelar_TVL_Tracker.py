import streamlit as st
import pandas as pd
import plotly.express as px

# داده‌ها را بارگذاری کن
df = pd.read_csv("tvl_data.csv")
df["date"] = pd.to_datetime(df["date"])
latest_date = df["date"].max()
latest_df = df[df["date"] == latest_date]

st.title("Axelar TVL Dashboard")

# ---- ردیف اول: Stacked Bar Chart ----
st.subheader("Axelar TVL Over Time")
fig1 = px.bar(df, x="date", y="tvl", color="asset_type", title="Axelar TVL Over Time", barmode="stack")
st.plotly_chart(fig1, use_container_width=True)

# ---- ردیف دوم: Normalized Area Chart ----
st.subheader("Normalized Axelar TVL Distribution Over Time")
fig2 = px.area(
    df,
    x="date",
    y="tvl",
    color="asset_type",
    groupnorm="percent",  # این باعث نرمال شدن داده‌ها می‌شود
    title="Normalized Axelar TVL Distribution"
)
st.plotly_chart(fig2, use_container_width=True)

# ---- ردیف سوم: Donut Chart و KPI ----
st.subheader(f"TVL Breakdown on {latest_date.date()}")

col1, col2 = st.columns(2)

with col1:
    fig3 = px.pie(latest_df, values="tvl", names="asset_type", hole=0.5, title="TVL by Asset Type")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    total_tvl = latest_df["tvl"].sum()
    st.metric(label="Total TVL (ITS + non-ITS)", value=f"${total_tvl:,.2f}")

# ---- ردیف چهارم: 3 Area Charts ----
st.subheader("Monthly TVL Statistics")

# ابتدا داده‌های ماهانه را محاسبه کن
df_monthly = df.copy()
df_monthly["month"] = df_monthly["date"].dt.to_period("M")
monthly_stats = df_monthly.groupby("month")["tvl"].agg(["max", "mean", "min"]).reset_index()
monthly_stats["month"] = monthly_stats["month"].dt.to_timestamp()

col3, col4, col5 = st.columns(3)

with col3:
    fig4 = px.area(monthly_stats, x="month", y="max", title="Maximum TVL per Month")
    st.plotly_chart(fig4, use_container_width=True)

with col4:
    fig5 = px.area(monthly_stats, x="month", y="mean", title="Average TVL per Month")
    st.plotly_chart(fig5, use_container_width=True)

with col5:
    fig6 = px.area(monthly_stats, x="month", y="min", title="Minimum TVL per Month")
    st.plotly_chart(fig6, use_container_width=True)
