import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Config: Tab Title & Icon ---
st.set_page_config(
    page_title="Axelar TVL Monitoring: ITS vs. Non-ITS",
    page_icon="https://axelarscan.io/logos/logo.png",
    layout="wide"
)

# خواندن داده‌ها
df = pd.read_csv("tvl_data.csv")

# تبدیل تاریخ به datetime
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# حذف مقادیر تاریخ نامعتبر
df = df.dropna(subset=["date"])

# نقشه رنگ‌ها
color_map = {
    "ITS": "#ff7400",
    "non-ITS": "#00a1f7"
}

# ردیف اول: Stacked Bar Chart
if not df.empty:
    fig1 = px.bar(
        df,
        x="date",
        y="tvl",
        color="asset_type",
        title="Axelar TVL Over Time",
        labels={"tvl": "TVL", "date": "Date"},
        color_discrete_map=color_map,
        category_orders={"asset_type": ["non-ITS", "ITS"]}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No data available for Axelar TVL Over Time.")

# ردیف دوم: Normalized Area Chart
if not df.empty:
    fig2 = px.area(
        df,
        x="date",
        y="tvl",
        color="asset_type",
        groupnorm="fraction",
        title="Axelar TVL Over Time (Normalized)",
        labels={"tvl": "TVL Share", "date": "Date"},
        color_discrete_map=color_map,
        category_orders={"asset_type": ["non-ITS", "ITS"]}
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("No data available for normalized TVL chart.")

# داده‌های آخرین روز
if not df.empty:
    last_date = df["date"].max()
    last_day_df = df[df["date"] == last_date]
else:
    last_day_df = pd.DataFrame()

# ردیف سوم: Donut Chart + KPI
col1, col2 = st.columns([2, 1])

with col1:
    if not last_day_df.empty:
        fig3 = px.pie(
            last_day_df,
            names="asset_type",
            values="tvl",
            title=f"TVL Distribution on {last_date.date()}",
            color="asset_type",
            color_discrete_map=color_map,
            hole=0.5
        )
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("No data available for donut chart.")

with col2:
    total_tvl = last_day_df["tvl"].sum() if not last_day_df.empty else None
    if pd.notna(total_tvl):
        st.metric(label="Total TVL", value=f"${total_tvl:,.0f}")
    else:
        st.metric(label="Total TVL", value="No data")

# ردیف چهارم: Maximum, Average, Minimum TVL per Month
if not df.empty:
    df["month"] = df["date"].dt.to_period("M")

    monthly = df.groupby(["month", "asset_type"])["tvl"].agg(
        max_tvl="max", avg_tvl="mean", min_tvl="min"
    ).reset_index()
    monthly["month"] = monthly["month"].dt.to_timestamp()

    if monthly.empty:
        st.warning("No monthly data available to display.")
    else:
        col3, col4, col5 = st.columns(3)

        with col3:
            fig4 = px.area(
                monthly,
                x="month",
                y="max_tvl",
                color="asset_type",
                title="Maximum TVL per Month",
                color_discrete_map=color_map,
                category_orders={"asset_type": ["non-ITS", "ITS"]}
            )
            st.plotly_chart(fig4, use_container_width=True)

        with col4:
            fig5 = px.area(
                monthly,
                x="month",
                y="avg_tvl",
                color="asset_type",
                title="Average TVL per Month",
                color_discrete_map=color_map,
                category_orders={"asset_type": ["non-ITS", "ITS"]}
            )
            st.plotly_chart(fig5, use_container_width=True)

        with col5:
            fig6 = px.area(
                monthly,
                x="month",
                y="min_tvl",
                color="asset_type",
                title="Minimum TVL per Month",
                color_discrete_map=color_map,
                category_orders={"asset_type": ["non-ITS", "ITS"]}
            )
            st.plotly_chart(fig6, use_container_width=True)
else:
    st.warning("No data available for monthly charts.")
