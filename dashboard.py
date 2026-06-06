import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib

st.set_page_config(
    page_title="Supply Chain Analytics",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; }

.stApp { background-color: #f5f6fa; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Top navbar ── */
.navbar {
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 14px 32px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.navbar-left { display: flex; align-items: center; gap: 16px; }
.navbar-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; color: white; font-weight: 800;
}
.navbar-title { font-size: 0.95rem; font-weight: 700; color: #0f172a; }
.navbar-sub { font-size: 0.72rem; color: #94a3b8; }
.navbar-right { display: flex; align-items: center; gap: 24px; }
.nav-stat { text-align: right; }
.nav-stat-val { font-size: 0.85rem; font-weight: 700; color: #0f172a; }
.nav-stat-label { font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.8px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0 !important;
    padding-top: 0 !important;
}
[data-testid="stSidebar"] * { color: #334155 !important; }
[data-testid="stSidebar"] strong { color: #0f172a !important; }
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #f8fafc !important;
    border-color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #f8fafc !important;
    border-color: #e2e8f0 !important;
}
.sidebar-section {
    font-size: 0.65rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin: 20px 0 8px;
}
.sidebar-logo {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
    border-radius: 0;
    padding: 20px 16px;
    margin: -1rem -1rem 1rem;
}
.sidebar-logo-title { font-size: 1rem; font-weight: 800; color: white !important; }
.sidebar-logo-sub { font-size: 0.72rem; color: rgba(255,255,255,0.7) !important; margin-top: 2px; }

/* ── Page wrapper ── */
.page-wrapper { padding: 24px 28px; }

/* ── Section title ── */
.section-title {
    font-size: 0.65rem; font-weight: 700; color: #94a3b8;
    text-transform: uppercase; letter-spacing: 1.2px;
    margin: 24px 0 12px;
    display: flex; align-items: center; gap: 8px;
}
.section-title::after {
    content: ''; flex: 1; height: 1px; background: #e2e8f0;
}

/* ── KPI Cards ── */
.kpi {
    background: white;
    border-radius: 10px;
    padding: 18px 16px;
    border: 1px solid #e2e8f0;
    position: relative;
    overflow: hidden;
    transition: all 0.2s ease;
    cursor: default;
}
.kpi:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-color: var(--ac);
}
.kpi-icon {
    width: 36px; height: 36px; border-radius: 8px;
    background: var(--ac-light);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; margin-bottom: 12px;
}
.kpi-value { font-size: 1.55rem; font-weight: 800; color: #0f172a; line-height: 1; }
.kpi-label { font-size: 0.68rem; color: #64748b; font-weight: 500;
             text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
.kpi-trend { font-size: 0.7rem; margin-top: 8px; font-weight: 600; }
.kpi-trend.up { color: #10b981; }
.kpi-trend.down { color: #ef4444; }
.kpi-trend.neutral { color: #64748b; }
.kpi-bar {
    position: absolute; bottom: 0; left: 0; right: 0;
    height: 3px; background: var(--ac);
    border-radius: 0 0 10px 10px;
}

/* ── Chart card ── */
.card {
    background: white;
    border-radius: 10px;
    padding: 18px 16px 8px;
    border: 1px solid #e2e8f0;
    margin-bottom: 16px;
    transition: all 0.2s ease;
}
.card:hover {
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
}
.card-header {
    display: flex; justify-content: space-between;
    align-items: flex-start; margin-bottom: 4px;
}
.card-title { font-size: 0.8rem; font-weight: 700; color: #0f172a; }
.card-sub { font-size: 0.68rem; color: #94a3b8; margin-top: 2px; margin-bottom: 12px; }
.card-badge {
    font-size: 0.62rem; font-weight: 600; color: #2563eb;
    background: #eff6ff; border-radius: 20px;
    padding: 2px 8px; border: 1px solid #bfdbfe;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important;
    border-radius: 8px; padding: 3px;
    border: 1px solid #e2e8f0 !important;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px; color: #64748b;
    font-weight: 600; font-size: 0.75rem;
    padding: 7px 18px;
    transition: all 0.15s ease;
}
.stTabs [data-baseweb="tab"]:hover { color: #0f172a; background: #f1f5f9 !important; }
.stTabs [aria-selected="true"] {
    background: #2563eb !important;
    color: white !important;
}

/* ── Mini metric ── */
.mini {
    background: white; border-radius: 10px;
    padding: 14px 16px; border: 1px solid #e2e8f0;
    border-left: 4px solid var(--ac);
    transition: all 0.2s ease;
}
.mini:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.07); }
.mini-val { font-size: 1.2rem; font-weight: 800; color: #0f172a; }
.mini-label { font-size: 0.65rem; color: #94a3b8; font-weight: 600;
              text-transform: uppercase; letter-spacing: 0.8px; margin-top: 3px; }

/* ── Risk card ── */
.risk {
    background: white; border-radius: 10px;
    padding: 28px 20px; text-align: center;
    border: 1px solid #e2e8f0;
    border-top: 4px solid var(--rc);
}
.risk-pct { font-size: 3.2rem; font-weight: 900; color: var(--rc); line-height: 1; }
.risk-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 2px;
              text-transform: uppercase; margin-top: 6px; color: var(--rc); }
.risk-pill {
    display: inline-block; margin-top: 12px;
    background: var(--rc-light); color: var(--rc);
    border-radius: 20px; padding: 4px 16px;
    font-size: 0.7rem; font-weight: 700;
}

/* ── Feat bar ── */
.feat-row { margin-bottom: 9px; }
.feat-top { display: flex; justify-content: space-between;
            font-size: 0.73rem; color: #334155; margin-bottom: 4px; }
.feat-score { color: #94a3b8; font-size: 0.7rem; }
.feat-track { background: #f1f5f9; border-radius: 4px; height: 5px; }
.feat-fill { background: #2563eb; height: 5px; border-radius: 4px; }

/* ── Download btn ── */
.stDownloadButton button {
    background: #2563eb !important; color: white !important;
    border: none !important; border-radius: 7px !important;
    font-weight: 600 !important; font-size: 0.75rem !important;
    width: 100% !important; padding: 8px !important;
}

/* ── Table ── */
.stDataFrame { border-radius: 8px; overflow: hidden; border: 1px solid #e2e8f0 !important; }

header[data-testid="stHeader"] { display: none; }
</style>
""", unsafe_allow_html=True)

# ── Chart base ────────────────────────────────────────────────────
def cl(h=300, **kw):
    return dict(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#64748b", family="Inter", size=11),
        height=h, margin=dict(l=0, r=0, t=8, b=0),
        xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0",
                   tickfont=dict(color="#94a3b8", size=10), zeroline=False),
        yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0",
                   tickfont=dict(color="#94a3b8", size=10), zeroline=False),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#64748b", size=10),
                    orientation="h", y=-0.15),
        **kw
    )

PAL = ["#2563eb","#7c3aed","#10b981","#f59e0b","#ef4444","#06b6d4","#ec4899","#84cc16"]

# ── Load ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("supply_chain_data.csv")
    df["is_delayed"]    = (df["Shipping times"] > df["Shipping times"].median()).astype(int)
    df["profit_margin"] = df["Revenue generated"] - df["Costs"] - df["Manufacturing costs"]
    df["high_defect"]   = (df["Defect rates"] > df["Defect rates"].median()).astype(int)
    df["cost_per_unit"] = df["Costs"] / df["Order quantities"]
    return df

@st.cache_resource
def load_model():
    model    = joblib.load("models/rf_model.pkl")
    encoders = joblib.load("models/label_encoders.pkl")
    features = joblib.load("models/feature_cols.pkl")
    return model, encoders, features

df = load_data()
model, encoders, feature_cols = load_model()

# ── Sidebar ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-title">Supply Chain</div>
        <div class="sidebar-logo-sub">Analytics Dashboard</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("**Kingsley Merafhe**")
    st.caption("Business Intelligence & Analytics")

    st.markdown('<div class="sidebar-section">Filters</div>', unsafe_allow_html=True)
    product_f    = st.multiselect("Product type",      df["Product type"].unique(),        default=df["Product type"].unique())
    location_f   = st.multiselect("Location",           df["Location"].unique(),             default=df["Location"].unique())
    transport_f  = st.multiselect("Transport mode",     df["Transportation modes"].unique(), default=df["Transportation modes"].unique())
    route_f      = st.multiselect("Route",              df["Routes"].unique(),               default=df["Routes"].unique())
    supplier_f   = st.multiselect("Supplier",           df["Supplier name"].unique(),        default=df["Supplier name"].unique())
    inspection_f = st.multiselect("Inspection result",  df["Inspection results"].unique(),   default=df["Inspection results"].unique())

    filtered = df[
        df["Product type"].isin(product_f) &
        df["Location"].isin(location_f) &
        df["Transportation modes"].isin(transport_f) &
        df["Routes"].isin(route_f) &
        df["Supplier name"].isin(supplier_f) &
        df["Inspection results"].isin(inspection_f)
    ]

    st.markdown('<div class="sidebar-section">Export</div>', unsafe_allow_html=True)
    st.caption(f"{len(filtered)} of {len(df)} SKUs selected")
    st.download_button("Download filtered data", filtered.to_csv(index=False), "data.csv", "text/csv")

# ── Navbar ────────────────────────────────────────────────────────
st.markdown(f"""
<div class="navbar">
    <div class="navbar-left">
        <div class="navbar-logo">SC</div>
        <div>
            <div class="navbar-title">Supply Chain Analytics</div>
            <div class="navbar-sub">Kingsley Merafhe &nbsp;·&nbsp; Business Intelligence &amp; Data Analytics</div>
        </div>
    </div>
    <div class="navbar-right">
        <div class="nav-stat">
            <div class="nav-stat-val">${filtered['Revenue generated'].sum():,.0f}</div>
            <div class="nav-stat-label">Total Revenue</div>
        </div>
        <div class="nav-stat">
            <div class="nav-stat-val">{filtered['is_delayed'].mean()*100:.0f}%</div>
            <div class="nav-stat-label">Delay Rate</div>
        </div>
        <div class="nav-stat">
            <div class="nav-stat-val">{filtered['Defect rates'].mean():.2f}%</div>
            <div class="nav-stat-label">Defect Rate</div>
        </div>
    </div>
</div>
<div class="page-wrapper">
""", unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

k = st.columns(5)
kpis = [
    ("#2563eb", "#eff6ff", "📦", "Total SKUs",       f"{len(filtered)}",                             "Active products", "neutral", f"{len(filtered)} tracked"),
    ("#10b981", "#f0fdf4", "💰", "Total Revenue",    f"${filtered['Revenue generated'].sum():,.0f}", "Gross total",     "up",      "Across all products"),
    ("#ef4444", "#fef2f2", "⚠", "Avg Defect Rate",  f"{filtered['Defect rates'].mean():.2f}%",      "Quality metric",  "down",    f"High: {df.groupby('Location')['Defect rates'].mean().idxmax()}"),
    ("#7c3aed", "#f5f3ff", "🚚", "Avg Ship Time",    f"{filtered['Shipping times'].mean():.1f}d",    "Delivery speed",  "neutral", f"Max {filtered['Shipping times'].max()} days"),
    ("#f59e0b", "#fffbeb", "⏱", "Delayed",          f"{filtered['is_delayed'].sum()}",              "Shipments",       "down",    f"{filtered['is_delayed'].mean()*100:.0f}% of total"),
]
for col, (ac, acl, icon, label, val, sub, trend, note) in zip(k, kpis):
    col.markdown(f"""
    <div class="kpi" style="--ac:{ac};--ac-light:{acl}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{val}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-trend {trend}">{note}</div>
        <div class="kpi-bar"></div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Shipping & Logistics", "Suppliers & Production", "ML Risk Predictor"])

# ══════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Revenue Analysis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1.2, 1, 0.8])

    with c1:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Revenue by Product Type</div>
            <div class="card-sub">Gross revenue per category</div></div>
            <span class="card-badge">Bar</span>
        </div>""", unsafe_allow_html=True)
        rev = filtered.groupby("Product type")["Revenue generated"].sum().reset_index().sort_values("Revenue generated", ascending=True)
        fig = px.bar(rev, x="Revenue generated", y="Product type",
                     orientation="h", color="Product type", color_discrete_sequence=PAL)
        fig.update_layout(**cl(220), showlegend=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Inspection Results</div>
            <div class="card-sub">Pass / Fail / Pending split</div></div>
            <span class="card-badge">Donut</span>
        </div>""", unsafe_allow_html=True)
        fig = px.pie(filtered, names="Inspection results", hole=0.62,
                     color="Inspection results",
                     color_discrete_map={"Pass":"#10b981","Fail":"#ef4444","Pending":"#f59e0b"})
        fig.update_layout(**cl(220), showlegend=True)
        fig.update_traces(textfont_size=10, textfont_color="white")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c3:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Profit Margin</div>
            <div class="card-sub">Avg margin by product</div></div>
        </div>""", unsafe_allow_html=True)
        pm = filtered.groupby("Product type")["profit_margin"].mean().reset_index()
        fig = px.bar(pm, x="Product type", y="profit_margin",
                     color="Product type", color_discrete_sequence=PAL)
        fig.update_layout(**cl(220), showlegend=False)
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Cost & Efficiency</div>', unsafe_allow_html=True)
    c4, c5 = st.columns([1.4, 0.6])

    with c4:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Revenue vs Total Costs</div>
            <div class="card-sub">Bubble size = products sold</div></div>
            <span class="card-badge">Scatter</span>
        </div>""", unsafe_allow_html=True)
        fig = px.scatter(filtered, x="Costs", y="Revenue generated",
                         color="Product type", size="Number of products sold",
                         hover_data=["SKU","Location"], color_discrete_sequence=PAL)
        fig.update_layout(**cl(240))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c5:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Cost per Unit</div>
            <div class="card-sub">By product type</div></div>
        </div>""", unsafe_allow_html=True)
        cpu = filtered.groupby("Product type")["cost_per_unit"].mean().reset_index()
        fig = px.funnel(cpu, x="cost_per_unit", y="Product type",
                        color_discrete_sequence=PAL)
        fig.update_layout(**cl(240), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 2 — SHIPPING
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Shipping KPIs</div>', unsafe_allow_html=True)
    m = st.columns(4)
    mets = [
        ("#2563eb", "Avg Shipping Cost",   f"${filtered['Shipping costs'].mean():.2f}"),
        ("#10b981", "Total Shipping Cost", f"${filtered['Shipping costs'].sum():,.0f}"),
        ("#7c3aed", "Fastest Delivery",    f"{filtered['Shipping times'].min()} days"),
        ("#ef4444", "Slowest Delivery",    f"{filtered['Shipping times'].max()} days"),
    ]
    for col, (ac, label, val) in zip(m, mets):
        col.markdown(f"""
        <div class="mini" style="--ac:{ac}">
            <div class="mini-val">{val}</div>
            <div class="mini-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Delay & Cost Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Delay Rate by Location</div>
            <div class="card-sub">% of delayed shipments per city</div></div>
            <span class="card-badge">Bar</span>
        </div>""", unsafe_allow_html=True)
        loc = filtered.groupby("Location")["is_delayed"].mean().reset_index().sort_values("is_delayed", ascending=True)
        loc["pct"] = (loc["is_delayed"] * 100).round(1)
        fig = px.bar(loc, x="pct", y="Location", orientation="h",
                     color="pct", color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
                     text="pct")
        fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
        fig.update_layout(**cl(260), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Shipping Time by Mode</div>
            <div class="card-sub">Distribution across transport types</div></div>
            <span class="card-badge">Box</span>
        </div>""", unsafe_allow_html=True)
        fig = px.box(filtered, x="Transportation modes", y="Shipping times",
                     color="Transportation modes", color_discrete_sequence=PAL,
                     points="outliers")
        fig.update_layout(**cl(260), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns([1, 1])

    with c3:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Cost vs Time by Transport</div>
            <div class="card-sub">Bubble size = order quantity</div></div>
            <span class="card-badge">Scatter</span>
        </div>""", unsafe_allow_html=True)
        fig = px.scatter(filtered, x="Shipping times", y="Shipping costs",
                         color="Transportation modes", size="Order quantities",
                         hover_data=["SKU","Routes"], color_discrete_sequence=PAL)
        fig.update_layout(**cl(250))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Avg Cost by Route</div>
            <div class="card-sub">Which route is most cost efficient</div></div>
            <span class="card-badge">Bar</span>
        </div>""", unsafe_allow_html=True)
        rc = filtered.groupby("Routes")["Shipping costs"].mean().reset_index().sort_values("Shipping costs")
        fig = px.bar(rc, x="Routes", y="Shipping costs",
                     color="Routes", color_discrete_sequence=PAL, text="Shipping costs")
        fig.update_traces(texttemplate="$%{text:.1f}", textposition="outside", marker_line_width=0)
        fig.update_layout(**cl(250), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Carrier Performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    carrier = filtered.groupby("Shipping carriers").agg(
        SKUs=("SKU","count"),
        Avg_Cost=("Shipping costs","mean"),
        Avg_Time=("Shipping times","mean"),
        Delayed=("is_delayed","sum"),
        Delay_Rate=("is_delayed","mean")
    ).reset_index()
    carrier["Delay_Rate"] = (carrier["Delay_Rate"] * 100).round(1).astype(str) + "%"
    st.dataframe(carrier.style.format({"Avg_Cost":"${:.2f}","Avg_Time":"{:.1f} days"}),
                 use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 3 — SUPPLIERS
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Supplier KPIs</div>', unsafe_allow_html=True)
    m = st.columns(4)
    mets = [
        ("#ef4444", "Avg Defect Rate",       f"{filtered['Defect rates'].mean():.2f}%"),
        ("#f59e0b", "High Defect SKUs",      f"{filtered['high_defect'].sum()}"),
        ("#10b981", "Avg Production Volume", f"{filtered['Production volumes'].mean():.0f}"),
        ("#7c3aed", "Avg Mfg Cost",          f"${filtered['Manufacturing costs'].mean():.2f}"),
    ]
    for col, (ac, label, val) in zip(m, mets):
        col.markdown(f"""
        <div class="mini" style="--ac:{ac}">
            <div class="mini-val">{val}</div>
            <div class="mini-label">{label}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Defect Analysis</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Defect Rate by Location</div>
            <div class="card-sub">Average defect % per city</div></div>
            <span class="card-badge">Bar</span>
        </div>""", unsafe_allow_html=True)
        ld = filtered.groupby("Location")["Defect rates"].mean().reset_index().sort_values("Defect rates", ascending=True)
        fig = px.bar(ld, x="Defect rates", y="Location", orientation="h",
                     color="Defect rates", color_continuous_scale=["#10b981","#f59e0b","#ef4444"],
                     text="Defect rates")
        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside", marker_line_width=0)
        fig.update_layout(**cl(260), showlegend=False, coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Defect Rate by Transport Mode</div>
            <div class="card-sub">Which mode has most quality issues</div></div>
            <span class="card-badge">Box</span>
        </div>""", unsafe_allow_html=True)
        fig = px.box(filtered, x="Transportation modes", y="Defect rates",
                     color="Transportation modes", color_discrete_sequence=PAL, points="outliers")
        fig.update_layout(**cl(260), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2)

    with c3:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Stock Levels by Supplier</div>
            <div class="card-sub">Average inventory per supplier</div></div>
            <span class="card-badge">Bar</span>
        </div>""", unsafe_allow_html=True)
        ss = filtered.groupby("Supplier name")["Stock levels"].mean().reset_index().sort_values("Stock levels", ascending=True)
        fig = px.bar(ss, x="Stock levels", y="Supplier name", orientation="h",
                     color="Supplier name", color_discrete_sequence=PAL, text="Stock levels")
        fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", marker_line_width=0)
        fig.update_layout(**cl(260), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown("""<div class="card">
        <div class="card-header">
            <div><div class="card-title">Mfg Cost vs Production Volume</div>
            <div class="card-sub">Bubble size = order quantity</div></div>
            <span class="card-badge">Scatter</span>
        </div>""", unsafe_allow_html=True)
        fig = px.scatter(filtered, x="Production volumes", y="Manufacturing costs",
                         color="Supplier name", size="Order quantities",
                         hover_data=["SKU","Product type"], color_discrete_sequence=PAL)
        fig.update_layout(**cl(260))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Supplier Summary</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    sup = filtered.groupby("Supplier name").agg(
        SKUs=("SKU","count"),
        Avg_Defect=("Defect rates","mean"),
        Avg_Stock=("Stock levels","mean"),
        Avg_Mfg_Cost=("Manufacturing costs","mean"),
        Total_Revenue=("Revenue generated","sum")
    ).reset_index()
    st.dataframe(sup.style.format({
        "Avg_Defect":"{:.2f}%","Avg_Stock":"{:.0f}",
        "Avg_Mfg_Cost":"${:.2f}","Total_Revenue":"${:,.0f}"
    }), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# TAB 4 — ML PREDICTOR
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">ML Delay Risk Predictor</div>', unsafe_allow_html=True)
    st.markdown("""<div class="card">
    <div class="card-header">
        <div><div class="card-title">Random Forest Classifier</div>
        <div class="card-sub">Adjust inputs to predict delay probability using your trained model</div></div>
        <span class="card-badge">Accuracy 60% · F1 0.50</span>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("**Costs & Quality**")
        shipping_cost = st.slider("Shipping cost ($)",      float(df["Shipping costs"].min()),        float(df["Shipping costs"].max()),        float(df["Shipping costs"].mean()))
        defect_rate   = st.slider("Defect rate (%)",        float(df["Defect rates"].min()),          float(df["Defect rates"].max()),          float(df["Defect rates"].mean()))
        mfg_cost      = st.slider("Manufacturing cost ($)", float(df["Manufacturing costs"].min()),   float(df["Manufacturing costs"].max()),   float(df["Manufacturing costs"].mean()))
        price         = st.slider("Price ($)",              float(df["Price"].min()),                 float(df["Price"].max()),                 float(df["Price"].mean()))

    with c2:
        st.markdown("**Operations**")
        order_qty     = st.slider("Order quantity",         int(df["Order quantities"].min()),        int(df["Order quantities"].max()),        int(df["Order quantities"].mean()))
        stock_level   = st.slider("Stock level",            int(df["Stock levels"].min()),            int(df["Stock levels"].max()),            int(df["Stock levels"].mean()))
        prod_volume   = st.slider("Production volume",      int(df["Production volumes"].min()),      int(df["Production volumes"].max()),      int(df["Production volumes"].mean()))
        availability  = st.slider("Availability (%)",       float(df["Availability"].min()),          float(df["Availability"].max()),          float(df["Availability"].mean()))
        products_sold = st.slider("Products sold",          int(df["Number of products sold"].min()), int(df["Number of products sold"].max()), int(df["Number of products sold"].mean()))

    with c3:
        st.markdown("**Logistics**")
        lead_time     = st.slider("Lead time (days)",       int(df["Lead times"].min()),              int(df["Lead times"].max()),              int(df["Lead times"].mean()))
        lead_time2    = st.slider("Lead time 2 (days)",     int(df["Lead time"].min()),               int(df["Lead time"].max()),               int(df["Lead time"].mean()))
        mfg_lead      = st.slider("Mfg lead time (days)",  int(df["Manufacturing lead time"].min()), int(df["Manufacturing lead time"].max()), int(df["Manufacturing lead time"].mean()))
        transport_sel = st.selectbox("Transport mode",      df["Transportation modes"].unique())
        route_sel     = st.selectbox("Route",               df["Routes"].unique())
        location_sel  = st.selectbox("Location",            df["Location"].unique())
        carrier_sel   = st.selectbox("Carrier",             df["Shipping carriers"].unique())
        product_sel   = st.selectbox("Product type",        df["Product type"].unique())

    input_data = {
        "Price": price, "Availability": availability,
        "Number of products sold": products_sold,
        "Stock levels": stock_level, "Lead times": lead_time,
        "Order quantities": order_qty, "Shipping costs": shipping_cost,
        "Lead time": lead_time2, "Production volumes": prod_volume,
        "Manufacturing lead time": mfg_lead, "Manufacturing costs": mfg_cost,
        "Defect rates": defect_rate,
        "Transportation modes_enc": encoders["Transportation modes"].transform([transport_sel])[0],
        "Routes_enc":               encoders["Routes"].transform([route_sel])[0],
        "Location_enc":             encoders["Location"].transform([location_sel])[0],
        "Shipping carriers_enc":    encoders["Shipping carriers"].transform([carrier_sel])[0],
        "Product type_enc":         encoders["Product type"].transform([product_sel])[0],
    }

    input_df   = pd.DataFrame([input_data])[feature_cols]
    proba      = model.predict_proba(input_df)[0]
    delay_prob = proba[1] * 100

    st.markdown("<br>", unsafe_allow_html=True)
    r1, r2 = st.columns([1, 2])

    with r1:
        if delay_prob >= 60:
            rc, rcl, verdict = "#ef4444", "#fef2f2", "HIGH RISK"
        elif delay_prob >= 40:
            rc, rcl, verdict = "#f59e0b", "#fffbeb", "MEDIUM RISK"
        else:
            rc, rcl, verdict = "#10b981", "#f0fdf4", "LOW RISK"

        st.markdown(f"""
        <div class="risk" style="--rc:{rc};--rc-light:{rcl}">
            <div style="font-size:0.62rem;color:#94a3b8;letter-spacing:1.5px;
                        text-transform:uppercase;font-weight:700;margin-bottom:14px">
                Prediction result
            </div>
            <div class="risk-pct">{delay_prob:.0f}%</div>
            <div style="font-size:0.68rem;color:#94a3b8;margin:4px 0">delay probability</div>
            <div class="risk-pill">{verdict}</div>
        </div>""", unsafe_allow_html=True)

    with r2:
        st.markdown("**Feature importance — what drives this prediction**")
        imp = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False).head(8)
        max_score = imp.max()
        for feat, score in imp.items():
            clean = feat.replace("_enc","").replace("_"," ").title()
            width = int((score / max_score) * 280)
            st.markdown(f"""
            <div class="feat-row">
                <div class="feat-top">
                    <span>{clean}</span>
                    <span class="feat-score">{score:.3f}</span>
                </div>
                <div class="feat-track">
                    <div class="feat-fill" style="width:{width}px"></div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Full Dataset</div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.dataframe(filtered, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
