import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Indonesia Sales Report",
    layout="wide",
    page_icon="🇮🇩",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-base:        #0A0A0A;
        --bg-panel:       #111111;
        --border-dark:    rgba(212, 175, 55, 0.12);
        --border-bright:  rgba(212, 175, 55, 0.35);
        --gold:           #D4AF37;
        --gold-light:     #F1C40F;
        --gold-dim:       rgba(212, 175, 55, 0.60);
        --accent:         #E67E22;
        --sidebar-text:   #B0B0B0;
        --sidebar-accent: #D4AF37;
    }

    * { font-family: 'Outfit', sans-serif; box-sizing: border-box; }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-base) !important;
    }

    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0;
        background-image: radial-gradient(circle, rgba(212,175,55,0.03) 1px, transparent 1px);
        background-size: 28px 28px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Hide ALL Streamlit chrome ── */
    #MainMenu                          { visibility: hidden !important; display: none !important; }
    footer                             { visibility: hidden !important; display: none !important; }
    header                             { visibility: hidden !important; display: none !important; }
    [data-testid="stToolbar"]          { display: none !important; }
    [data-testid="stDecoration"]       { display: none !important; }
    [data-testid="stStatusWidget"]     { display: none !important; }
    [data-testid="manage-app-button"]  { display: none !important; }
    .viewerBadge_container__r5tak     { display: none !important; }
    .viewerBadge_link__qRIco          { display: none !important; }
    [data-testid="stDeployButton"]     { display: none !important; }
    button[kind="deployButton"]        { display: none !important; }
    [data-testid="baseButton-headerNoPadding"] { display: none !important; }
    [data-testid="stActionButton"]     { display: none !important; }
    .st-emotion-cache-zq5wmm          { display: none !important; }
    .st-emotion-cache-1dp5vir         { display: none !important; }
    ._profileContainer_gzau3_53       { display: none !important; }
    ._profilePreview_gzau3_63         { display: none !important; }

    /* ── Sidebar collapse/expand tab ── */
    [data-testid="collapsedControl"] {
        top: 10px !important;
        height: 32px !important;
        width: 20px !important;
    }
    [data-testid="collapsedControl"] button,
    [data-testid="stSidebarCollapseButton"] button {
        width: 32px !important;
        height: 32px !important;
        border-radius: 8px !important;
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%) !important;
        border: 1px solid rgba(212, 175, 55, 0.45) !important;
        box-shadow: 0 2px 12px rgba(212, 175, 55, 0.18) !important;
        color: #D4AF37 !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="collapsedControl"] button:hover,
    [data-testid="stSidebarCollapseButton"] button:hover {
        border-color: #F1C40F !important;
        box-shadow: 0 4px 20px rgba(212, 175, 55, 0.40) !important;
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {
        stroke: #D4AF37 !important;
        fill: none !important;
    }
    [data-testid="stSidebarCollapseButton"] { top: 10px !important; }
    [data-testid="stSidebar"] > div:first-child { padding-top: 54px !important; }

    /* ── Report title ── */
    .report-title {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%);
        color: #D4AF37;
        padding: 18px 28px;
        border-radius: 12px;
        text-align: center;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 5px;
        text-transform: uppercase;
        margin-bottom: 14px;
        border: 1px solid var(--border-bright);
        box-shadow: 0 8px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212,175,55,0.15);
        position: relative;
        overflow: hidden;
    }
    .report-title::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, #E67E22, transparent);
    }
    .report-subtitle {
        font-size: 13px;
        color: rgba(212,175,55,0.6);
        letter-spacing: 3px;
        text-transform: uppercase;
        font-family: 'Outfit', sans-serif;
        font-weight: 500;
        margin-top: 4px;
    }

    /* ── KPI / metric cards ── */
    .metric-card {
        background: linear-gradient(145deg, #1A1A1A 0%, #101010 100%);
        border: 1px solid rgba(212, 175, 55, 0.25);
        border-radius: 12px;
        padding: 18px 14px;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 18px rgba(0,0,0,0.7), 0 0 8px rgba(212,175,55,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, #D4AF37, #F1C40F, transparent);
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 28px rgba(212,175,55,0.18);
    }
    .metric-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #FFFFFF;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 32px;
        font-weight: 900;
        letter-spacing: 2px;
        color: #D4AF37;
        line-height: 1;
    }
    .metric-icon { font-size: 20px; margin-bottom: 6px; }

    /* ── Section headings ── */
    .section-heading {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 22px;
        color: #D4AF37;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 16px;
        border-left: 3px solid #D4AF37;
        padding-left: 12px;
    }

    /* ── Chart containers ── */
    .chart-container {
        background: linear-gradient(160deg, #131313 0%, #111111 100%);
        border: 1px solid rgba(212, 175, 55, 0.20);
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 4px 22px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .chart-title {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        color: #D4AF37;
        margin-bottom: 4px;
    }

    /* ══════════════════════════════════════════════════════════════════
       Gold-theme HTML tables (same as India/Asia/Dubai)
       ══════════════════════════════════════════════════════════════════ */
    .card-title {
        background: #1C1C1C;
        color: #D4AF37;
        padding: 9px 16px;
        border-radius: 10px 10px 0 0;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        text-align: center;
        border: 1px solid rgba(212,175,55,0.25);
        border-bottom: 1px solid rgba(212,175,55,0.15);
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .table-scroll {
        overflow-y: auto;
        border: 1px solid rgba(212,175,55,0.2);
        border-top: none;
        border-radius: 0 0 10px 10px;
        box-shadow: 0 6px 22px rgba(0,0,0,0.6);
        margin-bottom: 0;
    }
    .table-scroll table {
        width: 100%;
        border-collapse: collapse;
        table-layout: auto;
        font-family: 'Outfit', sans-serif;
        font-size: 13px;
        font-weight: 800;
        color: #FFFFFF;
        background: #131313;
    }
    .table-scroll th {
        background-color: #F0F0F0 !important;
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 12.5px !important;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        padding: 10px 12px;
        text-align: left !important;
        white-space: nowrap;
        /* No borders on header */
        border: none !important;
        /* Sticky header */
        position: sticky;
        top: 0;
        z-index: 2;
    }
    .table-scroll th:not(:first-child) { text-align: center !important; }

    .table-scroll td {
        padding: 7px 12px;
        border-bottom: 1px solid rgba(212,175,55,0.10);
        border-right: 1px solid rgba(212,175,55,0.10);
        font-weight: 800;
        font-size: 13px;
        text-align: left;
        color: #FFFFFF;
        white-space: nowrap;
    }
    .table-scroll td:last-child { border-right: none; }

    /* Numeric columns (2nd onwards) — gold + centered */
    .table-scroll td:not(:first-child) {
        text-align: center;
        font-weight: 900;
        color: #D4AF37;
    }

    .table-scroll tr:nth-child(even) td { background-color: #191919; }
    .table-scroll tr:nth-child(odd)  td { background-color: #131313; }
    .table-scroll tr:hover td {
        background-color: #2A2A2A !important;
        color: #F1C40F !important;
    }

    /* ── Sidebar (no vertical line) ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0C0C0C 0%, #0A0A0A 100%) !important;
        border-right: none !important;
    }
    [data-testid="stAppViewContainer"] { border-right: none !important; }
    [data-testid="stMain"]            { border-right: none !important; }
    .block-container                  { border-right: none !important; }

    [data-testid="stSidebar"] * { color: var(--sidebar-text) !important; }
    [data-testid="stSidebar"] h3 {
        color: var(--sidebar-accent) !important;
        font-size: 11px !important;
        letter-spacing: 2px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] strong { color: #E6C300 !important; }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stRadio label {
        color: var(--gold-dim) !important;
        font-weight: 600 !important;
        font-size: 10px !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: #888 !important;
        font-size: 11px !important;
    }

    [data-testid="stSelectbox"] > div > div,
    [data-testid="stMultiSelect"] > div > div {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        color: #D4AF37 !important;
        border-radius: 8px !important;
        font-size: 12px !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #1A1A1A 0%, #0E0E0E 100%) !important;
        color: var(--gold-light) !important;
        border: 1px solid var(--border-bright) !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 11px !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
        box-shadow: 0 2px 10px rgba(212,175,55,0.12) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2A2A2A 0%, #1A1A1A 100%) !important;
        box-shadow: 0 4px 18px rgba(212,175,55,0.30) !important;
        border-color: var(--gold-light) !important;
    }

    [data-testid="stFileUploader"] {
        background: #1A1A1A !important;
        border: 2px dashed rgba(212,175,55,0.25) !important;
        border-radius: 12px !important;
        padding: 28px !important;
    }
    [data-testid="stAlert"] {
        background: #1A1A1A !important;
        border: 1px solid var(--border-dark) !important;
        border-radius: 8px !important;
        color: var(--sidebar-text) !important;
    }

    .stat-pill {
        background: #1A1A1A;
        border: 1px solid var(--border-dark);
        border-radius: 8px;
        padding: 6px 12px;
        font-size: 11px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }
    .stat-pill span:first-child { color: #999; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; }
    .stat-pill span:last-child  { font-weight: 700; color: var(--gold-light); }

    hr { border-color: var(--border-dark) !important; margin: 12px 0 !important; }
    p, .stMarkdown p { color: var(--sidebar-text) !important; font-size: 12px !important; }
    label { color: var(--gold-dim) !important; }

    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #0A0A0A; }
    ::-webkit-scrollbar-thumb { background: rgba(212,175,55,0.25); border-radius: 2px; }

    .block-container { padding: 3.5rem 1rem 0.5rem; }
    div[data-testid="stVerticalBlock"] > div { margin-top: 0; padding-top: 0; }
    .stColumn { padding: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Keyboard shortcut: R = open sidebar, O = close sidebar ────────────────────
components.html("""
<script>
(function() {
    function clickSidebarToggle(action) {
        const doc = window.parent.document;
        if (action === 'open') {
            const expandBtn = doc.querySelector('[data-testid="collapsedControl"] button');
            if (expandBtn) { expandBtn.click(); return; }
        }
        if (action === 'close') {
            const collapseBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"] button');
            if (collapseBtn) { collapseBtn.click(); return; }
        }
    }
    window.parent.document.addEventListener('keydown', function(e) {
        const tag = e.target.tagName;
        if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.isContentEditable) return;
        if (e.key === 'r' || e.key === 'R') { clickSidebarToggle('open');  }
        if (e.key === 'o' || e.key === 'O') { clickSidebarToggle('close'); }
    });
})();
</script>
""", height=0)

# ── Palette & chart helpers (dark gold, like the others) ──────────────────────
GOLD_PALETTE = [
    "#D4AF37", "#F1C40F", "#E67E22", "#E9C46A", "#F4A261",
    "#E76F51", "#B8860B", "#DAA520", "#CD853F", "#D2691E",
    "#FFD700", "#FFA500", "#FF8C00", "#C0A000", "#8B6914"
]

PLOT_BG    = "#0D0D0D"
PAPER_BG   = "#0D0D0D"
GRID_COLOR = "rgba(212,175,55,0.08)"
AXIS_COLOR = "rgba(212,175,55,0.30)"
TEXT_COLOR = "#D0D0D0"
TITLE_COLOR= "#D4AF37"

AXIS_FONT  = dict(size=12, color=TEXT_COLOR,  family="Outfit, sans-serif")
TICK_FONT  = dict(size=11, color=TEXT_COLOR,  family="Outfit, sans-serif")
TITLE_FONT = dict(size=15, color=TITLE_COLOR, family="Bebas Neue, sans-serif")


def _dark_layout(fig, xaxis_title, yaxis_title, extra_xaxis=None, height=500):
    xax = dict(
        title=dict(text=xaxis_title, font=AXIS_FONT, standoff=12),
        tickfont=TICK_FONT,
        tickangle=-90,
        linecolor=AXIS_COLOR,
        linewidth=1,
        showgrid=False,
        ticks="outside",
        ticklen=4,
        tickcolor=AXIS_COLOR,
        automargin=True,
    )
    if extra_xaxis:
        xax.update(extra_xaxis)
    fig.update_layout(
        height=height,
        font=dict(family="Outfit, sans-serif", size=11, color=TEXT_COLOR),
        title_font=TITLE_FONT,
        title_x=0.5,
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        margin=dict(t=70, b=140, l=70, r=30),
        xaxis=xax,
        yaxis=dict(
            title=dict(text=yaxis_title, font=AXIS_FONT, standoff=10),
            tickfont=TICK_FONT,
            linecolor=AXIS_COLOR,
            linewidth=1,
            gridcolor=GRID_COLOR,
            gridwidth=1,
            zeroline=False,
        ),
        coloraxis_showscale=False,
        showlegend=False,
    )
    fig.update_traces(
        textfont=dict(size=10, color="#ffffff", family="Outfit, sans-serif"),
        textangle=0,
        textposition="outside",
        cliponaxis=False,
    )
    return fig


# ── Gold-theme HTML table renderer (same as India/Asia/Dubai) ─────────────────
def render_gold_table(df, title, height=420):
    """Render a DataFrame as a gold-themed HTML table — first column white, rest gold."""
    headers = "".join(f"<th>{col}</th>" for col in df.columns)
    rows_html = ""
    for _, row in df.iterrows():
        cells = "".join(f"<td>{val}</td>" for val in row)
        rows_html += f"<tr>{cells}</tr>"

    html = (
        f'<div class="card-title">{title}</div>'
        f'<div class="table-scroll" style="max-height:{height}px;">'
        f'<table><thead><tr>{headers}</tr></thead>'
        f'<tbody>{rows_html}</tbody></table></div>'
    )
    st.markdown(html, unsafe_allow_html=True)


# ── Report title ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="report-title">
    🇮🇩  Indonesia Sales Report
    <div class="report-subtitle">Comprehensive Sales Analytics Dashboard</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Excel File with Sheets 'A' and 'B'", type=['xlsx', 'xls'])


@st.cache_data(ttl=3600)
def load_and_process_data(uploaded_file):
    try:
        sheet_a = pd.read_excel(uploaded_file, sheet_name='A')
        sheet_b = pd.read_excel(uploaded_file, sheet_name='B')

        sheet_a.columns = sheet_a.columns.astype(str).str.strip()
        sheet_b.columns = sheet_b.columns.astype(str).str.strip()

        def find_column(df, possible_names):
            df_cols_upper = {col.upper().strip(): col for col in df.columns}
            for name in possible_names:
                if name.upper().strip() in df_cols_upper:
                    return df_cols_upper[name.upper().strip()]
            return None

        # ── Sheet A columns ────────────────────────────────────────────────────
        sku_col_a       = find_column(sheet_a, ['SKU', 'Sku'])
        color_col       = find_column(sheet_a, ['COLOR', 'Color'])
        brand_col       = find_column(sheet_a, ['BRAND', 'Brand'])
        season_col      = find_column(sheet_a, ['SEASON', 'Season'])
        category_col    = find_column(sheet_a, ['CATEGORY', 'Category'])
        subcategory_col = find_column(sheet_a, ['SUB CATEGORY', 'Sub category', 'SUBCATEGORY', 'Sub Category'])
        total_sales_col = find_column(sheet_a, ['TOTAL SALES', 'Total Sales', 'Total_Sales'])
        initial_qty_col = find_column(sheet_a, ['INITIAL QTY', 'Initial qty', 'INITIAL_QTY', 'Initial Qty'])
        bal_col         = find_column(sheet_a, ['BAL', 'Bal', 'BALANCE', 'Balance'])
        disposed_col    = find_column(sheet_a, ['DISPOSED', 'Disposed'])

        required_cols_a = {
            'Sku': sku_col_a, 'Color': color_col, 'Brand': brand_col,
            'Season': season_col, 'Category': category_col,
            'Sub category': subcategory_col, 'Total Sales': total_sales_col,
            'Initial qty': initial_qty_col, 'Bal': bal_col, 'DISPOSED': disposed_col
        }
        missing_a = [k for k, v in required_cols_a.items() if v is None]
        if missing_a:
            st.error(f"❌ Missing required columns in Sheet A: {', '.join(missing_a)}")
            st.info("Available columns in Sheet A: " + ", ".join(sheet_a.columns))
            st.stop()

        sheet_a_clean = pd.DataFrame({
            'SKU':         sheet_a[sku_col_a].astype(str).str.strip().str.upper(),
            'COLOR':       sheet_a[color_col].astype(str).str.strip().str.upper(),
            'BRAND':       sheet_a[brand_col].astype(str).str.strip().str.upper(),
            'SEASON':      sheet_a[season_col].astype(str).str.strip().str.upper(),
            'CATEGORY':    sheet_a[category_col].astype(str).str.strip().str.upper(),
            'SUBCATEGORY': sheet_a[subcategory_col].astype(str).str.strip().str.upper(),
            'TOTAL_SALES': pd.to_numeric(sheet_a[total_sales_col], errors='coerce').fillna(0),
            'INITIAL_QTY': pd.to_numeric(sheet_a[initial_qty_col], errors='coerce').fillna(0),
            'BALANCE':     pd.to_numeric(sheet_a[bal_col], errors='coerce').fillna(0),
            'DISPOSED':    pd.to_numeric(sheet_a[disposed_col], errors='coerce').fillna(0),
        })

        sheet_a_unique = sheet_a_clean.drop_duplicates(subset=['SKU'], keep='first')

        # ── Sheet B columns ────────────────────────────────────────────────────
        sku_col_b      = find_column(sheet_b, ['SKU', 'Sku'])
        marketplace_col= find_column(sheet_b, ['MARKET PLACE', 'Market place', 'MARKETPLACE', 'Marketplace'])
        total_order_col= find_column(sheet_b, ['TOTAL ORDER', 'Total order', 'TOTAL_ORDER'])
        date_col       = find_column(sheet_b, ['DATE', 'Date'])
        status_col     = find_column(sheet_b, ['STATUS', 'Status'])
        final_yea_col  = find_column(sheet_b, ['FINAL YEA', 'Final yea', 'FINAL_YEA'])
        final_col      = find_column(sheet_b, ['FINAL', 'Final'])

        required_cols_b = {
            'Sku': sku_col_b, 'Market place': marketplace_col,
            'Total order': total_order_col, 'Date': date_col,
            'STATUS': status_col
        }
        missing_b = [k for k, v in required_cols_b.items() if v is None]
        if missing_b:
            st.error(f"❌ Missing required columns in Sheet B: {', '.join(missing_b)}")
            st.info("Available columns in Sheet B: " + ", ".join(sheet_b.columns))
            st.stop()

        sheet_b_raw = pd.DataFrame({
            'SKU':         sheet_b[sku_col_b].astype(str).str.strip().str.upper(),
            'MARKETPLACE': sheet_b[marketplace_col].astype(str).str.strip().str.upper(),
            'TOTAL_ORDER': pd.to_numeric(sheet_b[total_order_col], errors='coerce').fillna(0),
            'ORDER_DATE':  pd.to_datetime(sheet_b[date_col], errors='coerce'),
            'STATUS':      sheet_b[status_col].astype(str).str.strip().str.upper() if status_col else 'N/A',
            'FINAL_YEA':   sheet_b[final_yea_col].astype(str).str.strip() if final_yea_col else 'N/A',
            'FINAL':       sheet_b[final_col].astype(str).str.strip() if final_col else 'N/A',
        })

        sheet_b_raw['MONTH_NUM']  = sheet_b_raw['ORDER_DATE'].dt.month
        sheet_b_raw['YEAR_NUM']   = sheet_b_raw['ORDER_DATE'].dt.year
        sheet_b_raw['MONTH_YEAR'] = sheet_b_raw['ORDER_DATE'].dt.strftime('%b-%y')

        sheet_b_agg = sheet_b_raw.groupby('SKU').agg(
            MARKETPLACE=('MARKETPLACE', 'first'),
            TOTAL_ORDER=('TOTAL_ORDER', 'sum'),
            ORDER_DATE=('ORDER_DATE', 'first')
        ).reset_index()

        merged_df = pd.merge(
            sheet_a_unique, sheet_b_agg,
            on='SKU', how='right', suffixes=('_a', '_b')
        )

        for col in ['INITIAL_QTY', 'TOTAL_SALES', 'BALANCE', 'DISPOSED', 'TOTAL_ORDER']:
            merged_df[col] = merged_df[col].fillna(0)

        merged_df['SALES_PERCENTAGE'] = np.where(
            merged_df['INITIAL_QTY'] > 0,
            (merged_df['TOTAL_SALES'] / merged_df['INITIAL_QTY']) * 100, 0
        )
        merged_df['MONTH_YEAR'] = merged_df['ORDER_DATE'].dt.strftime('%b-%y')
        merged_df['YEAR_MONTH'] = merged_df['ORDER_DATE'].dt.to_period('M')

        return merged_df, sheet_a_unique, sheet_b_raw

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        import traceback
        st.write("Detailed error:", traceback.format_exc())
        st.stop()


if uploaded_file is not None:
    try:
        with st.spinner('🔍 Loading and processing data...'):
            merged_df, sheet_a_unique, sheet_b_raw = load_and_process_data(uploaded_file)

        # ── Variable for Return % (change this value as needed) ──────
        return_pct = 12.47

        st.success(f"✅ Data loaded successfully! {len(merged_df):,} records processed")
        st.markdown("<hr>", unsafe_allow_html=True)

        # ── Sidebar ────────────────────────────────────────────────────────────
        with st.sidebar:
            st.markdown("### SORT TABLES BY")
            sort_column = st.selectbox(
                "Measure",
                ['Total Sales', 'Initial Qty', 'Balance', 'Sales%', 'Disposed'],
                key='sort_measure'
            )
            sort_order = st.radio("Order", ['Descending', 'Ascending'], horizontal=True)
            st.markdown("---")

            brands        = sorted(sheet_a_unique['BRAND'].dropna().unique())
            seasons       = sorted(sheet_a_unique['SEASON'].dropna().unique())
            categories    = sorted(sheet_a_unique['CATEGORY'].dropna().unique())
            subcategories = sorted(sheet_a_unique['SUBCATEGORY'].dropna().unique())
            colors        = sorted(sheet_a_unique['COLOR'].dropna().unique())
            skus          = sorted(sheet_a_unique['SKU'].dropna().unique())
            marketplaces  = sorted(sheet_b_raw['MARKETPLACE'].dropna().unique())
            statuses      = sorted(
                sheet_b_raw[
                    sheet_b_raw['STATUS'].notna() &
                    (sheet_b_raw['STATUS'].str.strip() != '') &
                    (~sheet_b_raw['STATUS'].str.upper().isin(['NAN', 'NONE', 'N/A']))
                ]['STATUS'].unique()
            )

            my_df = sheet_b_raw[sheet_b_raw['ORDER_DATE'].notna()].copy()
            if not my_df.empty:
                my_df_agg = (
                    my_df.groupby(['MONTH_NUM', 'YEAR_NUM', 'MONTH_YEAR'])
                    .size().reset_index()
                    .sort_values(['YEAR_NUM', 'MONTH_NUM'])
                )
                month_years = my_df_agg['MONTH_YEAR'].tolist()
            else:
                month_years = []

            st.markdown("### FILTER DATA")
            selected_brands        = st.multiselect("Brand",        ['All'] + brands,        default='All')
            selected_seasons       = st.multiselect("Season",       ['All'] + seasons,       default='All')
            selected_categories    = st.multiselect("Category",     ['All'] + categories,    default='All')
            selected_subcategories = st.multiselect("Subcategory",  ['All'] + subcategories, default='All')
            selected_colors        = st.multiselect("Color",        ['All'] + colors,        default='All')
            selected_skus          = st.multiselect("SKU",          ['All'] + skus,          default='All')
            st.markdown("---")
            selected_marketplaces  = st.multiselect("Marketplace",  ['All'] + marketplaces,  default='All')
            selected_statuses      = st.multiselect("Status",       ['All'] + statuses,      default='All')
            selected_month_years   = st.multiselect("Month-Year",   ['All'] + month_years,   default='All')

            # Quick counts
            _fa = sheet_a_unique.copy()
            if 'All' not in selected_brands        and selected_brands:
                _fa = _fa[_fa['BRAND'].isin(selected_brands)]
            if 'All' not in selected_seasons       and selected_seasons:
                _fa = _fa[_fa['SEASON'].isin(selected_seasons)]
            if 'All' not in selected_categories    and selected_categories:
                _fa = _fa[_fa['CATEGORY'].isin(selected_categories)]
            if 'All' not in selected_subcategories and selected_subcategories:
                _fa = _fa[_fa['SUBCATEGORY'].isin(selected_subcategories)]
            if 'All' not in selected_colors        and selected_colors:
                _fa = _fa[_fa['COLOR'].isin(selected_colors)]
            if 'All' not in selected_skus          and selected_skus:
                _fa = _fa[_fa['SKU'].isin(selected_skus)]
            _vsk = set(_fa['SKU'].unique())
            _fb = sheet_b_raw[sheet_b_raw['SKU'].isin(_vsk)].copy()
            if 'All' not in selected_marketplaces  and selected_marketplaces:
                _fb = _fb[_fb['MARKETPLACE'].isin(selected_marketplaces)]
            if 'All' not in selected_statuses      and selected_statuses:
                _fb = _fb[_fb['STATUS'].isin(selected_statuses)]
            if 'All' not in selected_month_years   and selected_month_years:
                _fb = _fb[_fb['MONTH_YEAR'].isin(selected_month_years)]

            st.markdown("---")
            st.markdown("### DATASET")
            st.markdown(f"""
<div class="stat-pill"><span>SKUs</span><span>{len(_vsk):,}</span></div>
<div class="stat-pill"><span>Brands</span><span>{_fa['BRAND'].nunique()}</span></div>
<div class="stat-pill"><span>Categories</span><span>{_fa['CATEGORY'].nunique()}</span></div>
<div class="stat-pill"><span>Marketplaces</span><span>{_fb['MARKETPLACE'].nunique()}</span></div>
<div class="stat-pill"><span>Months</span><span>{_fb['MONTH_YEAR'].nunique()}</span></div>
""", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(
                '<p style="color:#555 !important; font-size:10px !important; text-align:center; letter-spacing:1px;">'
                'Press <b style="color:#D4AF37 !important;">R</b> to open &nbsp;·&nbsp; '
                '<b style="color:#D4AF37 !important;">O</b> to close</p>',
                unsafe_allow_html=True
            )

        # ── Apply filters (main area) ──────────────────────────────────────────
        filtered_skus_df = sheet_a_unique.copy()
        if 'All' not in selected_brands        and selected_brands:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['BRAND'].isin(selected_brands)]
        if 'All' not in selected_seasons       and selected_seasons:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['SEASON'].isin(selected_seasons)]
        if 'All' not in selected_categories    and selected_categories:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['CATEGORY'].isin(selected_categories)]
        if 'All' not in selected_subcategories and selected_subcategories:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['SUBCATEGORY'].isin(selected_subcategories)]
        if 'All' not in selected_colors        and selected_colors:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['COLOR'].isin(selected_colors)]
        if 'All' not in selected_skus          and selected_skus:
            filtered_skus_df = filtered_skus_df[filtered_skus_df['SKU'].isin(selected_skus)]

        valid_skus = set(filtered_skus_df['SKU'].unique())

        filtered_b = sheet_b_raw[sheet_b_raw['SKU'].isin(valid_skus)].copy()
        if 'All' not in selected_marketplaces  and selected_marketplaces:
            filtered_b = filtered_b[filtered_b['MARKETPLACE'].isin(selected_marketplaces)]
        if 'All' not in selected_statuses      and selected_statuses:
            filtered_b = filtered_b[filtered_b['STATUS'].isin(selected_statuses)]
        if 'All' not in selected_month_years   and selected_month_years:
            filtered_b = filtered_b[filtered_b['MONTH_YEAR'].isin(selected_month_years)]

        filtered_df = merged_df[merged_df['SKU'].isin(valid_skus)].copy()
        if 'All' not in selected_marketplaces  and selected_marketplaces:
            filtered_df = filtered_df[filtered_df['MARKETPLACE'].isin(selected_marketplaces)]

        if len(filtered_df) == 0:
            st.warning("⚠️ No data available for the selected filters.")
        else:
            # ── KPIs ────────────────────────────────────────────────────────────
            st.markdown('<div class="section-heading">◆ Key Performance Indicators</div>', unsafe_allow_html=True)

            filtered_sheet_a = sheet_a_unique[sheet_a_unique['SKU'].isin(valid_skus)]
            f_init     = filtered_sheet_a['INITIAL_QTY'].sum()
            f_sold     = filtered_sheet_a['TOTAL_SALES'].sum()
            f_bal      = filtered_sheet_a['BALANCE'].sum()
            f_disposed = filtered_sheet_a['DISPOSED'].sum()
            f_spct     = (f_sold / f_init * 100) if f_init > 0 else 0

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            kpis = [
                (col1, "📦", "Initial Qty",            f"{f_init:,.0f}"),
                (col2, "💰", "Total Qty Sold",         f"{f_sold:,.0f}"),
                (col3, "⚖️",  "Balance Qty",           f"{f_bal:,.0f}"),
                (col4, "🗑️", "Disposed Qty",          f"{f_disposed:,.0f}"),
                (col5, "📈", "Sales %",                f"{f_spct:.1f}%"),
                (col6, "🔄", "Return % Jan-Apr 2026",  f"{return_pct:.1f}%"),
            ]
            for col, icon, label, value in kpis:
                with col:
                    st.markdown(f"""
<div class='metric-card'>
  <div class='metric-icon'>{icon}</div>
  <div class='metric-label'>{label}</div>
  <div class='metric-value'>{value}</div>
</div>""", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Helper for grouped tables (gold theme) ─────────────────────────
            def analyze_group(group_col, display_name):
                if group_col not in filtered_sheet_a.columns:
                    return pd.DataFrame()

                grouped = filtered_sheet_a.groupby(group_col, observed=True).agg(
                    INITIAL_QTY=('INITIAL_QTY', 'sum'),
                    TOTAL_SALES=('TOTAL_SALES', 'sum'),
                    BALANCE=('BALANCE', 'sum'),
                    DISPOSED=('DISPOSED', 'sum'),
                ).reset_index()
                grouped['SALES_PERCENTAGE'] = np.where(
                    grouped['INITIAL_QTY'] > 0,
                    (grouped['TOTAL_SALES'] / grouped['INITIAL_QTY']) * 100, 0
                )
                sort_map = {
                    'Total Sales': 'TOTAL_SALES',
                    'Initial Qty': 'INITIAL_QTY',
                    'Balance': 'BALANCE',
                    'Sales%': 'SALES_PERCENTAGE',
                    'Disposed': 'DISPOSED'
                }
                grouped = grouped.sort_values(
                    sort_map[sort_column], ascending=(sort_order == 'Ascending')
                )
                display = pd.DataFrame()
                display[display_name]   = grouped[group_col].astype(str)
                display['Initial Qty']  = grouped['INITIAL_QTY'].apply(lambda v: f"{int(v):,}")
                display['Total Sales']  = grouped['TOTAL_SALES'].apply(lambda v: f"{int(v):,}")
                display['Balance Qty']  = grouped['BALANCE'].apply(lambda v: f"{int(v):,}")
                display['Disposed Qty'] = grouped['DISPOSED'].apply(lambda v: f"{int(v):,}")
                display['Sales %']      = grouped['SALES_PERCENTAGE'].apply(lambda v: f"{v:.1f}%")
                return display.reset_index(drop=True)

            # ── Distribution Tables ────────────────────────────────────────────
            st.markdown('<div class="section-heading">◆ Sales Distribution Tables</div>', unsafe_allow_html=True)

            tables_config = [
                ('BRAND', 'Brand'), ('SEASON', 'Season'),
                ('CATEGORY', 'Category'), ('SUBCATEGORY', 'Subcategory'),
                ('COLOR', 'Color'), ('SKU', 'SKU')
            ]

            for i in range(0, len(tables_config), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(tables_config):
                        col_name, display_name = tables_config[i + j]
                        with cols[j]:
                            table_data = analyze_group(col_name, display_name)
                            if not table_data.empty:
                                render_gold_table(
                                    table_data,
                                    f"◈ {display_name} Wise Distribution",
                                    height=420
                                )
                            else:
                                st.info(f"No data for {display_name}")
                st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

            # ── Visual Analytics ───────────────────────────────────────────────
            st.markdown('<div class="section-heading">◆ Visual Analytics</div>', unsafe_allow_html=True)

            # CHART 1: Marketplace
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>◈ MARKETPLACE WISE ORDERS</div>", unsafe_allow_html=True)

            marketplace_data = (
                filtered_b[
                    filtered_b['MARKETPLACE'].notna() &
                    (filtered_b['MARKETPLACE'].str.strip() != '') &
                    (~filtered_b['MARKETPLACE'].str.upper().isin(['NAN', 'NONE', 'N/A']))
                ]
                .groupby('MARKETPLACE')['TOTAL_ORDER'].sum()
                .reset_index()
                .sort_values('TOTAL_ORDER', ascending=False)
            )

            if not marketplace_data.empty:
                n = len(marketplace_data)
                colors_bars = [GOLD_PALETTE[i % len(GOLD_PALETTE)] for i in range(n)]
                fig_mp = go.Figure(go.Bar(
                    x=marketplace_data['MARKETPLACE'],
                    y=marketplace_data['TOTAL_ORDER'],
                    text=marketplace_data['TOTAL_ORDER'].apply(lambda v: f"{v:,.0f}"),
                    marker=dict(
                        color=colors_bars,
                        line=dict(color='rgba(255,255,255,0.06)', width=1),
                        cornerradius=6,
                    ),
                ))
                fig_mp.update_layout(title="Sales by Marketplace till Apr 2026")
                fig_mp = _dark_layout(
                    fig_mp, "Marketplace", "Total Orders",
                    extra_xaxis={'categoryorder': 'array',
                                 'categoryarray': marketplace_data['MARKETPLACE'].tolist()}
                )
                st.plotly_chart(fig_mp, use_container_width=True)
            else:
                st.info("No marketplace data available")
            st.markdown("</div>", unsafe_allow_html=True)

            # CHART 2: Month-Year
            st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
            st.markdown("<div class='chart-title'>◈ MONTH-YEAR WISE ORDER DISTRIBUTION</div>", unsafe_allow_html=True)

            monthly_b = filtered_b[filtered_b['ORDER_DATE'].notna()].copy()

            if not monthly_b.empty:
                monthly_b['MONTH_NUM']   = monthly_b['ORDER_DATE'].dt.month
                monthly_b['YEAR_NUM']    = monthly_b['ORDER_DATE'].dt.year
                monthly_b['MONTH_LABEL'] = monthly_b['ORDER_DATE'].dt.strftime('%b-%y')

                monthly_agg = (
                    monthly_b.groupby(['MONTH_NUM', 'YEAR_NUM', 'MONTH_LABEL'])['TOTAL_ORDER']
                    .sum().reset_index()
                    .sort_values(['MONTH_NUM', 'YEAR_NUM'])
                )
                ordered_labels = monthly_agg['MONTH_LABEL'].tolist()

                MONTH_COLORS = {
                    1:  "#D4AF37", 2:  "#F1C40F", 3:  "#E67E22",
                    4:  "#E9C46A", 5:  "#F4A261", 6:  "#E76F51",
                    7:  "#B8860B", 8:  "#DAA520", 9:  "#CD853F",
                    10: "#D2691E", 11: "#FFD700", 12: "#FFA500",
                }
                bar_colors = [MONTH_COLORS.get(m, "#D4AF37") for m in monthly_agg['MONTH_NUM']]

                fig_mo = go.Figure(go.Bar(
                    x=monthly_agg['MONTH_LABEL'],
                    y=monthly_agg['TOTAL_ORDER'],
                    text=monthly_agg['TOTAL_ORDER'].apply(lambda v: f"{v:,.0f}"),
                    marker=dict(
                        color=bar_colors,
                        line=dict(color='rgba(255,255,255,0.06)', width=1),
                        cornerradius=5,
                    ),
                ))
                fig_mo.update_layout(title="Sales by Month-Year till Apr 2026")
                fig_mo = _dark_layout(
                    fig_mo, "Month-Year", "Total Orders",
                    extra_xaxis={
                        'categoryorder': 'array',
                        'categoryarray': ordered_labels,
                    },
                    height=540
                )
                st.plotly_chart(fig_mo, use_container_width=True)
            else:
                st.info("No order date data available")
            st.markdown("</div>", unsafe_allow_html=True)

            # Raw data expander
            with st.expander("🔍 View Raw Data"):
                st.dataframe(filtered_b, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        import traceback
        st.write("Detailed error:", traceback.format_exc())

else:
    st.markdown("""
<div style='text-align:center; padding:50px 20px; color:rgba(212,175,55,0.5); font-size:15px; letter-spacing:2px;'>
  👆  Upload an Excel file to begin analysing your data.
</div>""", unsafe_allow_html=True)

    with st.expander("📋 Required Excel File Structure"):
        st.markdown("""
### **Sheet A Columns (Required):**
- `Sku` · `Color` · `Brand` · `Season` · `Category` · `Sub category`
- `Total Sales` · `Initial qty` · `Bal` · `DISPOSED`

### **Sheet B Columns (Required):**
- `Sku` · `Market place` · `Total order` · `Date` · `STATUS` · `Final yea` · `Final`

### **Sidebar Filters Available:**
**From Sheet A:** Brand · Season · Category · Subcategory · Color · SKU

**From Sheet B:** Marketplace · Status · Month-Year
""")
