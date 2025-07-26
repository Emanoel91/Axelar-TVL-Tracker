import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

# --- Page Config ---
st.set_page_config(
    page_title="Axelar Network Performance Analysis",
    page_icon="https://axelarscan.io/logos/logo.png",
    layout="wide"
)

# خواندن داده‌ها
df = pd.read_csv("tvl_data.csv")

# تبدیل تاریخ
df["date"] = pd.to_datetime(df["date"], format="mixed", errors="coerce")
df = df.dropna(subset=["date"])

# تبدیل به عدد
df["tvl"] = pd.to_numeric(df["tvl"], errors="coerce")
df = df.dropna(subset=["tvl"])

# مرتب‌سازی
df = df.sort_values("date")

st.title("Axelar TVL Dashboard")

# تعریف رنگ‌ها ثابت برای asset_type
color_map = {
    "ITS": "#ff7400",
    "non-ITS": "#00a1f7"
}

# --- ردیف اول: Stacked Bar Chart با ITS بالای non-ITS اما رنگ ثابت ---
st.subheader("Axelar TVL Over Time - Stacked Bar")

# آماده‌سازی داده برای رسم دو trace جداگانه برای ITS و non-ITS
df_non_its = df[df["asset_type"] == "non-ITS"]
df_its = df[df["asset_type"] == "ITS"]

fig1 = go.Figure()

# رسم non-ITS (پایین)
fig1.add_trace(go.Bar(
    x=df_non_its["date"],
    y=df_non_its["tvl"],
    name="non-ITS",
    marker_color=color_map["non-ITS"],
    offsetgroup=1
))

# رسم ITS (بالا)
fig1.add_trace(go.Bar(
    x=df_its["date"],
    y=df_its["tvl"],
    name="ITS",
    marker_color=color_map["ITS"],
    offsetgroup=1
))

# مجموع TVL روزانه برای رسم خط مشکی
daily_total = df.groupby("date")["tvl"].sum().reset_index()
fig1.add_trace(go.Scatter(
    x=daily_total["date"],
    y=daily_total["tvl"],
    mode="lines",
    name="Total TVL",
    line=dict(color="black", width=2)
))

fig1.update_layout(
    barmode='stack',
    title="Axelar TVL Over Time",
    xaxis_title="Date",
    yaxis_title="TVL",
)

st.plotly_chart(fig1, use_container_width=True)

# --- ردیف دوم: Normalized Area Chart ---
st.subheader("Axelar TVL Over Time - Normalized Area")
df_grouped = df.groupby(["date", "asset_type"])["tvl"].sum().reset_index()
fig2 = px.area(
    df_grouped,
    x="date",
    y="tvl",
    color="asset_type",
    groupnorm="fraction",
    title="Normalized Axelar TVL by Asset Type",
    color_discrete_map=color_map,
    category_orders={"asset_type": ["non-ITS", "ITS"]}
)
st.plotly_chart(fig2, use_container_width=True)

# --- ردیف سوم: Donut chart و KPI ---
st.subheader("Latest Day TVL Breakdown")
latest_date = df["date"].max()
latest_df = df[df["date"] == latest_date]
total_tvl = latest_df["tvl"].sum()

col1, col2 = st.columns(2)
with col1:
    fig3 = px.pie(
        latest_df,
        names="asset_type",
        values="tvl",
        hole=0.5,
        title=f"TVL by Asset Type ({latest_date.date()})",
        color_discrete_map=color_map
    )
    st.plotly_chart(fig3, use_container_width=True)
with col2:
    st.metric(label="Total TVL", value=f"${total_tvl:,.0f}")

# --- ردیف چهارم: سه Area Chart ---
st.subheader("Monthly TVL Stats")
df_monthly = df.copy()
df_monthly["month"] = df_monthly["date"].dt.to_period("M")
monthly_stats = df_monthly.groupby(["month", "asset_type"])["tvl"].agg(
    ["max", "mean", "min"]
).reset_index()
monthly_stats["month"] = monthly_stats["month"].dt.to_timestamp()

col1, col2, col3 = st.columns(3)
with col1:
    fig_max = px.area(
        monthly_stats,
        x="month",
        y="max",
        color="asset_type",
        title="Maximum TVL per Month",
        color_discrete_map=color_map,
        category_orders={"asset_type": ["non-ITS", "ITS"]}
    )
    st.plotly_chart(fig_max, use_container_width=True)

with col2:
    fig_avg = px.area(
        monthly_stats,
        x="month",
        y="mean",
        color="asset_type",
        title="Average TVL per Month",
        color_discrete_map=color_map,
        category_orders={"asset_type": ["non-ITS", "ITS"]}
    )
    st.plotly_chart(fig_avg, use_container_width=True)

with col3:
    fig_min = px.area(
        monthly_stats,
        x="month",
        y="min",
        color="asset_type",
        title="Minimum TVL per Month",
        color_discrete_map=color_map,
        category_orders={"asset_type": ["non-ITS", "ITS"]}
    )
    st.plotly_chart(fig_min, use_container_width=True)
