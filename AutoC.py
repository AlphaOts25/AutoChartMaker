import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import io

# ==========================================
# 1. PAGE CONFIG & DARK THEME CSS
# ==========================================
st.set_page_config(
    page_title="Survey Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

dark_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background-color: #0e1525; }

[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1f2d45;
}
[data-testid="stSidebar"] * { color: #c9d1e0 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stButton button {
    background-color: #1e40af !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    width: 100%;
}
[data-testid="stSidebar"] .stButton button:hover { background-color: #2563eb !important; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

h1 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #f1f5f9 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}
h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1a2744 0%, #162035 100%) !important;
    border: 1px solid #2a3f66 !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
}
[data-testid="stMetricValue"] {
    color: #60a5fa !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 2rem !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}
[data-testid="stMetricDelta"] { color: #34d399 !important; font-size: 0.85rem !important; }

.chart-card {
    background: linear-gradient(160deg, #1a2744 0%, #131d35 100%);
    border: 1px solid #2a3f66;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.35);
}
.chart-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: #e2e8f0;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.chart-subtitle { font-size: 0.78rem; color: #64748b; margin-bottom: 16px; }

.quality-bar-bg {
    background: #1f2d45;
    border-radius: 4px;
    height: 6px;
    width: 100%;
    margin-top: 3px;
}
.quality-bar-fill {
    height: 6px;
    border-radius: 4px;
    background: linear-gradient(90deg, #3b82f6, #10b981);
}

.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    color: #475569;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    padding: 6px 0 4px 0;
    border-bottom: 1px solid #1f2d45;
    margin-bottom: 8px;
}

.badge {
    display: inline-block;
    background: #1e40af22;
    border: 1px solid #3b82f644;
    color: #60a5fa;
    border-radius: 20px;
    font-size: 0.7rem;
    padding: 1px 8px;
    margin-left: 4px;
}
.badge-warn {
    background: #92400e22;
    border-color: #f59e0b44;
    color: #fbbf24;
}
.badge-ok {
    background: #064e3b22;
    border-color: #10b98144;
    color: #34d399;
}

[data-baseweb="tab-list"] {
    background-color: #111827 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border-bottom: none !important;
}
[data-baseweb="tab"] {
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    padding: 8px 20px !important;
    border: none !important;
    background: transparent !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background-color: #1e40af !important;
    color: white !important;
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background-color: #1a2744 !important;
    border: 1px solid #2a3f66 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
.stTextInput input {
    background-color: #1a2744 !important;
    border: 1px solid #2a3f66 !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
}
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    border: 1px solid #2a3f66 !important;
}
hr { border-color: #1f2d45 !important; }
.stAlert {
    border-radius: 10px !important;
    background-color: #1a2744 !important;
    border: 1px solid #2a3f66 !important;
    color: #c9d1e0 !important;
}
[data-testid="stRadio"] label { color: #c9d1e0 !important; }
[data-testid="stFileUploader"] {
    background-color: #1a2744 !important;
    border: 1px dashed #2a3f66 !important;
    border-radius: 10px !important;
}
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0e1525; }
::-webkit-scrollbar-thumb { background: #2a3f66; border-radius: 5px; }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ==========================================
# PLOTLY DARK THEME CONFIG
# ==========================================
CHART_COLORS = ["#3b82f6","#10b981","#f59e0b","#ef4444","#8b5cf6","#06b6d4","#ec4899"]

DARK_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#94a3b8", family="DM Sans, sans-serif", size=12),
    title_font=dict(color="#e2e8f0", family="Space Grotesk, sans-serif", size=14),
    legend=dict(bgcolor="rgba(26,39,68,0.8)", bordercolor="#2a3f66", borderwidth=1, font=dict(color="#c9d1e0")),
    xaxis=dict(gridcolor="#1f2d45", linecolor="#2a3f66", tickcolor="#2a3f66", tickfont=dict(color="#64748b"), zerolinecolor="#2a3f66"),
    yaxis=dict(gridcolor="#1f2d45", linecolor="#2a3f66", tickcolor="#2a3f66", tickfont=dict(color="#64748b"), zerolinecolor="#2a3f66"),
    title="",
    margin=dict(l=10, r=10, t=30, b=10),
    hoverlabel=dict(bgcolor="#1a2744", bordercolor="#2a3f66", font=dict(color="#e2e8f0"))
)

def apply_dark_theme(fig):
    fig.update_layout(**DARK_LAYOUT)
    return fig


# ==========================================
# HELPER FUNCTIONS
# ==========================================
def read_csv_with_fallback(uploaded_file):
    """
    Attempts to read an uploaded CSV file using multiple common encodings.
    If all fail, reads with utf-8 but replaces invalid bytes with '?'.
    """
    encodings_to_try = ['utf-8', 'cp1252', 'latin1', 'iso-8859-1']
    
    for enc in encodings_to_try:
        try:
            uploaded_file.seek(0)  # Reset the file pointer to the start
            return pd.read_csv(uploaded_file, encoding=enc)
        except UnicodeDecodeError:
            continue  # If it fails, move on to the next encoding
            
    # Fallback: force read and replace weird characters
    uploaded_file.seek(0)
    st.warning("⚠️ Some special characters couldn't be read perfectly and were replaced.")
    return pd.read_csv(uploaded_file, encoding='utf-8', encoding_errors='replace')

def fix_duplicate_columns(df):
    df_clean = df.copy()
    base_columns = {}
    for col in df_clean.columns:
        base_name = re.sub(r'\.\d+$', '', col)
        if base_name not in base_columns:
            base_columns[base_name] = []
        base_columns[base_name].append(col)
    for base_name, cols in base_columns.items():
        if len(cols) > 1:
            df_clean[base_name] = df_clean[cols].bfill(axis=1).iloc[:, 0]
            cols_to_drop = [c for c in cols if c != base_name]
            df_clean = df_clean.drop(columns=cols_to_drop)
    return df_clean

def extract_grid_questions(df):
    grid_groups = {}
    for col in df.columns:
        if '[' in col and col.endswith(']'):
            base_name = col.rsplit('[', 1)[0].strip()
            if base_name not in grid_groups:
                grid_groups[base_name] = []
            grid_groups[base_name].append(col)
    return {k: v for k, v in grid_groups.items() if len(v) > 1}

def card(title, subtitle=""):
    st.markdown(f'<div class="chart-title">{title}</div><div class="chart-subtitle">{subtitle}</div>', unsafe_allow_html=True)

def section_header(label):
    st.markdown(f'<div class="section-header">{label}</div>', unsafe_allow_html=True)

def normalize_phone(val):
    """Strip spaces, ensure leading 0, 11-digit PH format."""
    if pd.isna(val) or str(val).strip() == "":
        return val
    digits = re.sub(r'\D', '', str(val))
    if len(digits) == 10 and not digits.startswith('0'):
        digits = '0' + digits
    if len(digits) == 11 and digits.startswith('09'):
        return digits
    return val  # return original if unrecognizable

LOAD_SPENDING_MAP = {
    "seldom": "1-10",
    "normal": "Unknown",
    "above 140": "141+",
    "above140": "141+",
}

def normalize_load_spending(val):
    if pd.isna(val): return val
    normalized = str(val).strip().lower()
    return LOAD_SPENDING_MAP.get(normalized, val)

def get_data_quality(df):
    total = len(df)
    rows = []
    for col in df.columns:
        blanks = df[col].isna().sum() + (df[col] == "").sum() + (df[col] == "No Answer").sum()
        fill_pct = round((1 - blanks / total) * 100, 1) if total > 0 else 100
        rows.append({"Column": col, "Filled %": fill_pct, "Blank": int(blanks)})
    return pd.DataFrame(rows).sort_values("Filled %", ascending=True)


# ==========================================
# SESSION STATE INIT
# ==========================================
for key, default in {
    "rename_dict": {},
    "cols_to_drop": [],
    "active_filters": {},
    "cleaning_log": [],
    "value_merge_rules": [],   # list of {col, values, canonical}
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    # ── UPLOAD ──────────────────────────────
    section_header("📂 Data Upload")
    file_current = st.file_uploader("Current Period CSV", type=["csv"], key="current")
    file_previous = st.file_uploader("Previous Period CSV *(optional)*", type=["csv"], key="previous")

    st.divider()

    # ── CHART TYPE ──────────────────────────
    section_header("🎨 Chart Type")
    chart_type = st.radio(
        "chart",
        ["📊 Bar Chart", "🥧 Pie / Donut", "📈 Line Chart", "📉 Scatter Plot", "☑️ Grid / Checkbox", "🔢 Cross-Tab Count"],
        label_visibility="collapsed"
    )

    st.divider()

    # ══════════════════════════════════════════
    # 🧹 DATA CLEANING PANEL
    # ══════════════════════════════════════════
    section_header("🧹 Data Cleaning")

    with st.expander("✨ Quick Auto-Clean", expanded=False):
        fix_nans_mode = st.selectbox(
            "Fill blank / NaN cells with:",
            ["(Leave blank)", "No Answer", "N/A", "Unknown", "➜ Drop those rows"],
            index=1
        )
        clean_headers = st.toggle("Auto-rename common columns (Phone Type, Age, Gender…)", value=False)
        fix_phones = st.toggle("Standardize PH contact numbers (09XXXXXXXXX)", value=False)
        fix_load = st.toggle("Normalize load-spending text (Seldom, normal…)", value=False)
        fix_whitespace = st.toggle("Trim whitespace from all text cells", value=True)
        fix_case = st.selectbox(
            "Normalize text case:",
            ["(None)", "Title Case", "UPPER CASE", "lower case"],
            index=0
        )

    with st.expander("🔁 Deduplicate Rows", expanded=False):
        dedup_mode = st.selectbox(
            "Deduplicate by:",
            ["(Off)", "All columns", "Email Address", "Contact Number", "Name of Respondent"],
            index=0
        )
        dedup_keep = st.radio("Keep:", ["First occurrence", "Last occurrence"], horizontal=True)

    with st.expander("🗑️ Drop Preset Columns", expanded=False):
        st.markdown("<small style='color:#64748b'>Quick-remove columns that are rarely useful for visualization.</small>", unsafe_allow_html=True)
        drop_consent = st.toggle("Drop Consent column (long legal text)", value=False)
        drop_timestamp = st.toggle("Drop Timestamp column", value=False)
        drop_email = st.toggle("Drop Email Address column", value=False)
        drop_contact = st.toggle("Drop Contact Number column", value=False)

    with st.expander("🔎 Find & Replace Value", expanded=False):
        fr_col_placeholder = st.empty()   # populated after df is loaded
        fr_find    = st.text_input("Find value (exact):", key="fr_find")
        fr_replace = st.text_input("Replace with:",       key="fr_replace")
        apply_fr   = st.button("Apply Find & Replace")

    with st.expander("🔀 Merge Duplicate Values", expanded=False):
        st.markdown(
            "<small style='color:#64748b'>Pick a column, select all the variants "
            "you want to consolidate, then set the one canonical name to keep.</small>",
            unsafe_allow_html=True,
        )
        merge_col_ph      = st.empty()   # column selector — filled after df loads
        merge_vals_ph     = st.empty()   # value multiselect — filled after df loads
        merge_canon_ph    = st.empty()   # canonical text input — filled after df loads
        merge_btn_ph      = st.empty()   # Add Rule button — filled after df loads

        # Show existing rules
        if st.session_state.value_merge_rules:
            st.markdown("<small style='color:#64748b'>Active merge rules:</small>", unsafe_allow_html=True)
            for i, rule in enumerate(st.session_state.value_merge_rules):
                col_label  = rule["col"]
                vals_label = ", ".join(rule["values"])
                canon      = rule["canonical"]
                r1, r2 = st.columns([4, 1])
                with r1:
                    st.markdown(
                        f"<span style='color:#60a5fa;font-size:0.72rem'>"
                        f"<b>{col_label}</b>: {vals_label} "
                        f"<span style='color:#34d399'>→ {canon}</span></span>",
                        unsafe_allow_html=True,
                    )
                with r2:
                    if st.button("✕", key=f"del_merge_{i}"):
                        st.session_state.value_merge_rules.pop(i)
                        st.session_state.cleaning_log.append(f"Removed merge rule #{i+1} on '{col_label}'")
                        st.rerun()
            if st.button("🗑 Clear All Merge Rules", key="clear_all_merges"):
                st.session_state.value_merge_rules = []
                st.rerun()

    st.divider()

    # ══════════════════════════════════════════
    # 🔽 FILTER & SEGMENT
    # ══════════════════════════════════════════
    section_header("🔽 Filter & Segment")

    with st.expander("Add Column Filter", expanded=False):
        filter_col_placeholder = st.empty()
        filter_val_placeholder = st.empty()
        col1f, col2f = st.columns(2)
        with col1f:
            add_filter_btn   = st.button("➕ Add Filter")
        with col2f:
            clear_filter_btn = st.button("🗑 Clear All")

    if st.session_state.active_filters:
        st.markdown("<small style='color:#64748b'>Active filters:</small>", unsafe_allow_html=True)
        for fc, fv in st.session_state.active_filters.items():
            st.markdown(f"<span style='color:#60a5fa;font-size:0.78rem'>▸ {fc}: {', '.join(str(x) for x in fv)}</span>", unsafe_allow_html=True)

    st.divider()

    # ══════════════════════════════════════════
    # 🛠️ COLUMN MANAGEMENT
    # ══════════════════════════════════════════
    section_header("🛠️ Column Management")

    with st.expander("✏️ Rename a Column", expanded=False):
        rename_col_placeholder = st.empty()
        new_col_name_placeholder = st.empty()
        rename_btn_placeholder = st.empty()

    with st.expander("👁️ Hide / Restore Columns", expanded=False):
        hide_col_placeholder = st.empty()
        hc1, hc2 = st.columns(2)
        with hc1:
            hide_btn = st.button("Hide Selected")
        with hc2:
            restore_btn = st.button("Restore All")

    if st.session_state.rename_dict:
        st.markdown(
            "<small style='color:#64748b'>Active renames: " +
            ", ".join(f"{k}→{v}" for k,v in st.session_state.rename_dict.items()) +
            "</small>", unsafe_allow_html=True
        )

    st.divider()

    # ══════════════════════════════════════════
    # 📤 EXPORT
    # ══════════════════════════════════════════
    section_header("📤 Export")
    export_placeholder = st.empty()

    st.divider()

    # ══════════════════════════════════════════
    # 📋 CLEANING LOG
    # ══════════════════════════════════════════
    section_header("📋 Cleaning Log")
    if st.session_state.cleaning_log:
        for entry in st.session_state.cleaning_log[-8:]:
            st.markdown(f"<span style='color:#64748b;font-size:0.72rem'>✔ {entry}</span>", unsafe_allow_html=True)
        if st.button("Clear Log"):
            st.session_state.cleaning_log = []
            st.rerun()
    else:
        st.markdown("<span style='color:#334155;font-size:0.78rem'>No cleaning actions yet.</span>", unsafe_allow_html=True)


# ==========================================
# MAIN AREA
# ==========================================
st.markdown("# 📈 Survey Analytics Dashboard")
st.markdown(
    "<p style='color:#64748b;margin-top:-10px;margin-bottom:24px;font-size:0.9rem;'>"
    "Upload a CSV to begin. Supports Google Forms exports with grid/checkbox questions.</p>",
    unsafe_allow_html=True
)

if file_current is not None:

    # ── READ & CONCAT ────────────────────────
    df_current = read_csv_with_fallback(file_current)
    df_current = fix_duplicate_columns(df_current)
    df_current["Period"] = "Current"

    if file_previous is not None:
        df_previous = read_csv_with_fallback(file_previous)
        df_previous = fix_duplicate_columns(df_previous)
        df_previous["Period"] = "Previous"
        df = pd.concat([df_current, df_previous], ignore_index=True)
        is_comparing = True
    else:
        df = df_current.copy()
        is_comparing = False

    raw_len = len(df)

    # ══════════════════════════════════════════
    # APPLY CLEANING STEPS
    # ══════════════════════════════════════════

    # ── Preset column drops ──
    preset_drops = []
    if drop_consent:
        matches = [c for c in df.columns if "agree" in c.lower() or "consent" in c.lower() or "data privacy" in c.lower()]
        preset_drops += matches
    if drop_timestamp:
        matches = [c for c in df.columns if "timestamp" in c.lower()]
        preset_drops += matches
    if drop_email:
        matches = [c for c in df.columns if "email" in c.lower()]
        preset_drops += matches
    if drop_contact:
        matches = [c for c in df.columns if "contact" in c.lower()]
        preset_drops += matches
    for col in preset_drops:
        if col in df.columns:
            df = df.drop(columns=[col])
            if f"Dropped preset: {col}" not in st.session_state.cleaning_log:
                st.session_state.cleaning_log.append(f"Dropped preset: {col}")

    # ── Whitespace trim ──
    if fix_whitespace:
        str_cols = df.select_dtypes(include="object").columns
        df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())

    # ── Phone normalization ──
    if fix_phones:
        phone_cols = [c for c in df.columns if "contact" in c.lower() or "phone" in c.lower() or "number" in c.lower()]
        for pc in phone_cols:
            df[pc] = df[pc].apply(normalize_phone)
        if phone_cols:
            st.session_state.cleaning_log.append(f"Standardized phones: {', '.join(phone_cols)}")

    # ── Load spending normalization ──
    if fix_load:
        load_cols = [c for c in df.columns if "load" in c.lower() and "spend" in c.lower()]
        for lc in load_cols:
            df[lc] = df[lc].apply(normalize_load_spending)
        if load_cols:
            st.session_state.cleaning_log.append(f"Normalized load spending: {len(load_cols)} col(s)")

    # ── Text case ──
    if fix_case != "(None)":
        str_cols = df.select_dtypes(include="object").columns
        if fix_case == "Title Case":
            df[str_cols] = df[str_cols].apply(lambda c: c.str.title())
        elif fix_case == "UPPER CASE":
            df[str_cols] = df[str_cols].apply(lambda c: c.str.upper())
        elif fix_case == "lower case":
            df[str_cols] = df[str_cols].apply(lambda c: c.str.lower())
        st.session_state.cleaning_log.append(f"Applied text case: {fix_case}")

    # ── NaN fill / drop ──
    if fix_nans_mode == "➜ Drop those rows":
        before = len(df)
        df = df.dropna()
        dropped = before - len(df)
        if dropped:
            st.session_state.cleaning_log.append(f"Dropped {dropped} rows with blanks")
    elif fix_nans_mode != "(Leave blank)":
        df = df.fillna(fix_nans_mode)
        df.replace("", fix_nans_mode, inplace=True)

    # ── Auto-rename common columns ──
    if clean_headers:
        rename_map = {
            "What type of mobile  phone do you use?": "Phone_Type",
            "Age Range": "Age",
            "Sex": "Gender",
            "Name of Respondent": "Name",
            "Contact Number": "Contact",
            "Occupation": "Occupation",
        }
        df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})
        st.session_state.cleaning_log.append("Auto-renamed common columns")

    # ── Deduplication ──
    if dedup_mode != "(Off)":
        before = len(df)
        keep_val = "first" if "First" in dedup_keep else "last"
        if dedup_mode == "All columns":
            df = df.drop_duplicates(keep=keep_val)
        else:
            col_match = [c for c in df.columns if dedup_mode.lower() in c.lower()]
            if col_match:
                df = df.drop_duplicates(subset=[col_match[0]], keep=keep_val)
        removed = before - len(df)
        if removed:
            st.session_state.cleaning_log.append(f"Deduplication ({dedup_mode}): removed {removed} rows")

    # ── Sidebar: dynamic placeholders for rename/hide/filter (need df columns) ──
    with rename_col_placeholder:
        col_to_rename = st.selectbox("Column:", df.columns, key="rename_sel")
    with new_col_name_placeholder:
        new_col_name = st.text_input("New name:", value=col_to_rename, key="new_name_input")
    with rename_btn_placeholder:
        if st.button("Apply Rename"):
            if new_col_name and new_col_name != col_to_rename:
                st.session_state.rename_dict[col_to_rename] = new_col_name
                st.session_state.cleaning_log.append(f"Renamed '{col_to_rename}' → '{new_col_name}'")
                st.rerun()

    available_cols = [c for c in df.columns if c not in st.session_state.cols_to_drop]
    with hide_col_placeholder:
        cols_selected_to_drop = st.multiselect("Select to hide:", available_cols, key="hide_sel")
    if hide_btn:
        if cols_selected_to_drop:
            st.session_state.cols_to_drop.extend(cols_selected_to_drop)
            st.session_state.cleaning_log.append(f"Hidden: {', '.join(cols_selected_to_drop)}")
            st.rerun()
    if restore_btn:
        st.session_state.cols_to_drop = []
        st.rerun()

    # ── Find & Replace ──
    fr_col_options = list(df.select_dtypes(include="object").columns)
    with fr_col_placeholder:
        fr_col = st.selectbox("In column:", fr_col_options, key="fr_col")
    if apply_fr and fr_find and fr_col in df.columns:
        count = (df[fr_col] == fr_find).sum()
        df[fr_col] = df[fr_col].replace(fr_find, fr_replace)
        st.session_state.cleaning_log.append(f"Find & Replace in '{fr_col}': '{fr_find}'→'{fr_replace}' ({count} cells)")

    # ── Merge Duplicate Values — populate UI ──
    merge_cat_cols = list(df.select_dtypes(include="object").columns)
    merge_cat_cols = [c for c in merge_cat_cols if c != "Period"]
    with merge_col_ph:
        merge_sel_col = st.selectbox("Column to merge values in:", merge_cat_cols, key="merge_col_sel")
    merge_unique_vals = sorted(df[merge_sel_col].dropna().unique().tolist()) if merge_sel_col in df.columns else []
    with merge_vals_ph:
        merge_selected_vals = st.multiselect(
            "Select values to consolidate:",
            merge_unique_vals,
            key="merge_vals_sel",
            help="Pick all the variant spellings / duplicates you want to collapse into one.",
        )
    # Suggest canonical = the most frequent of the selected values
    if merge_selected_vals and merge_sel_col in df.columns:
        freq_counts = df[merge_sel_col].value_counts()
        suggested = max(merge_selected_vals, key=lambda v: freq_counts.get(v, 0))
    else:
        suggested = ""
    with merge_canon_ph:
        merge_canonical = st.text_input(
            "Canonical (unified) name:",
            value=suggested,
            key="merge_canon_input",
            help="All selected values will be replaced with this name.",
        )
    with merge_btn_ph:
        if st.button("➕ Add Merge Rule", key="add_merge_rule"):
            if merge_sel_col and merge_selected_vals and merge_canonical.strip():
                # Prevent duplicate rule for same col+values
                new_rule = {
                    "col": merge_sel_col,
                    "values": merge_selected_vals,
                    "canonical": merge_canonical.strip(),
                }
                st.session_state.value_merge_rules.append(new_rule)
                st.session_state.cleaning_log.append(
                    f"Merge rule: [{', '.join(merge_selected_vals)}] → '{merge_canonical.strip()}' in '{merge_sel_col}'"
                )
                st.rerun()
            else:
                st.warning("Select a column, at least one value, and enter a canonical name.")

    # ── Apply all merge rules to df ──
    for rule in st.session_state.value_merge_rules:
        col_r, vals_r, canon_r = rule["col"], rule["values"], rule["canonical"]
        if col_r in df.columns:
            df[col_r] = df[col_r].apply(lambda x: canon_r if str(x) in [str(v) for v in vals_r] else x)

    # ── Apply renames & drops ──
    if st.session_state.rename_dict:
        df = df.rename(columns=st.session_state.rename_dict)
    if st.session_state.cols_to_drop:
        existing = [c for c in st.session_state.cols_to_drop if c in df.columns]
        df = df.drop(columns=existing)

    # ── Filters ──
    filterable_cols = [c for c in df.columns if c != "Period"]
    with filter_col_placeholder:
        f_col = st.selectbox("Filter column:", filterable_cols, key="filter_col_sel")
    unique_vals = sorted(df[f_col].dropna().unique().tolist()) if f_col in df.columns else []
    with filter_val_placeholder:
        f_vals = st.multiselect("Filter values:", unique_vals, key="filter_val_sel")
    if add_filter_btn and f_col and f_vals:
        st.session_state.active_filters[f_col] = f_vals
        st.session_state.cleaning_log.append(f"Filter added: {f_col} in {f_vals}")
        st.rerun()
    if clear_filter_btn:
        st.session_state.active_filters = {}
        st.rerun()

    for fc, fv in st.session_state.active_filters.items():
        if fc in df.columns:
            df = df[df[fc].astype(str).isin([str(v) for v in fv])]

    # ── Export button ──
    csv_bytes = df.to_csv(index=False).encode("utf-8")
    with export_placeholder:
        st.download_button(
            label="⬇️  Download Cleaned CSV",
            data=csv_bytes,
            file_name="cleaned_survey.csv",
            mime="text/csv",
        )

    # ══════════════════════════════════════════
    # EXTRACT GRIDS
    # ══════════════════════════════════════════
    grid_dict = extract_grid_questions(df)
    all_grid_columns = [col for cols in grid_dict.values() for col in cols]
    standard_columns = [col for col in df.columns if col not in all_grid_columns and col != "Period"]

    # ══════════════════════════════════════════
    # METRIC CARDS
    # ══════════════════════════════════════════
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.metric("Total Responses", len(df_current))
    with m2:
        st.metric("After Cleaning", len(df), delta=f"{len(df)-raw_len:+d} rows" if len(df) != raw_len else None)
    with m3:
        delta_str = f"+{len(df) - len(df_current)} from previous" if is_comparing else None
        st.metric("Combined Records", len(df), delta=delta_str)
    with m4:
        completeness = round((1 - df.isin(["No Answer", "N/A", "Unknown"]).mean().mean()) * 100, 1)
        st.metric("Completeness", f"{completeness}%")
    with m5:
        dup_count = df.duplicated().sum()
        st.metric("Duplicate Rows", dup_count, delta="clean" if dup_count == 0 else f"{dup_count} found")

    st.markdown("<div style='margin-top:8px'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════
    # TABS
    # ══════════════════════════════════════════
    tab1, tab2, tab3 = st.tabs(["📊  Visualizations", "🗃️  Raw Data", "📋  Data Quality"])

    # ─────────────────────────────────────────
    # TAB 1: VISUALIZATIONS
    # ─────────────────────────────────────────
    with tab1:
        try:
            if chart_type not in ["☑️ Grid / Checkbox", "🔢 Cross-Tab Count"]:
                sel_col, _, _ = st.columns([1, 1, 2])
                with sel_col:
                    x_axis = st.selectbox("Select column to visualize:", standard_columns, key="x_axis")

                if x_axis:
                    if chart_type == "📊 Bar Chart":
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        card(f"Count of {x_axis}", "Grouped by response value")
                        if is_comparing:
                            chart_data = df.groupby([x_axis, "Period"]).size().reset_index(name="Count")
                            fig = px.bar(chart_data, x=x_axis, y="Count", color="Period", barmode="group", color_discrete_sequence=CHART_COLORS)
                        else:
                            chart_data = df[x_axis].value_counts().reset_index()
                            chart_data.columns = [x_axis, "Count"]
                            fig = px.bar(chart_data, x=x_axis, y="Count", color=x_axis, color_discrete_sequence=CHART_COLORS)
                        fig.update_traces(marker_line_width=0)
                        apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    elif chart_type == "🥧 Pie / Donut":
                        chart_data = df[x_axis].value_counts().reset_index()
                        chart_data.columns = [x_axis, "Count"]
                        if is_comparing:
                            c_left, c_right = st.columns(2)
                            cur_data = df_current[x_axis].value_counts().reset_index()
                            cur_data.columns = [x_axis, "Count"]
                            prev_data = df_previous[x_axis].value_counts().reset_index()
                            prev_data.columns = [x_axis, "Count"]
                            with c_left:
                                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                                card(f"Current — {x_axis}")
                                fig_cur = px.pie(cur_data, names=x_axis, values="Count", hole=0.55, color_discrete_sequence=CHART_COLORS)
                                fig_cur.update_traces(textfont_color="white")
                                apply_dark_theme(fig_cur)
                                st.plotly_chart(fig_cur, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                            with c_right:
                                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                                card(f"Previous — {x_axis}")
                                fig_prev = px.pie(prev_data, names=x_axis, values="Count", hole=0.55, color_discrete_sequence=CHART_COLORS)
                                fig_prev.update_traces(textfont_color="white")
                                apply_dark_theme(fig_prev)
                                st.plotly_chart(fig_prev, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                        else:
                            c_left, c_right = st.columns(2)
                            with c_left:
                                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                                card(f"Distribution of {x_axis}", "Pie chart")
                                fig_pie = px.pie(chart_data, names=x_axis, values="Count", color_discrete_sequence=CHART_COLORS)
                                fig_pie.update_traces(textfont_color="white")
                                apply_dark_theme(fig_pie)
                                st.plotly_chart(fig_pie, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)
                            with c_right:
                                st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                                card(f"Distribution of {x_axis}", "Donut chart")
                                fig_donut = px.pie(chart_data, names=x_axis, values="Count", hole=0.55, color_discrete_sequence=CHART_COLORS)
                                fig_donut.update_traces(textfont_color="white")
                                apply_dark_theme(fig_donut)
                                st.plotly_chart(fig_donut, use_container_width=True)
                                st.markdown("</div>", unsafe_allow_html=True)

                    elif chart_type == "📈 Line Chart":
                        is_numeric_col = pd.api.types.is_numeric_dtype(df[x_axis])
                        other_cols = [c for c in standard_columns if c != x_axis]

                        ctl1, ctl2, ctl3 = st.columns([1, 1, 2])
                        with ctl1:
                            y_mode = st.radio("Y-Axis", ["📊 Count", "📋 Column"], key="line_y_mode", horizontal=True)
                        with ctl2:
                            y_col = None
                            if y_mode == "📋 Column":
                                if other_cols:
                                    y_col = st.selectbox("Y-Axis column:", other_cols, key="line_y_col")
                                else:
                                    st.warning("No other columns available.")
                        with ctl3:
                            n_bins = 20
                            if y_mode == "📊 Count" and is_numeric_col:
                                n_bins = st.slider("Bins (numeric X)", 5, 50, 20, key="line_bins")

                        def bin_col_series(source_df, col, n_bins=20):
                            if pd.api.types.is_numeric_dtype(source_df[col]):
                                intervals = pd.cut(source_df[col].dropna(), bins=n_bins)
                                counts = intervals.value_counts().reset_index()
                                counts.columns = [col, "Count"]
                                counts["_left"] = counts[col].apply(lambda iv: iv.left)
                                counts = counts.sort_values("_left").drop(columns="_left")
                                counts[col] = counts[col].astype(str)
                            else:
                                s = source_df[col].dropna().astype(str)
                                counts = s.value_counts().reset_index()
                                counts.columns = [col, "Count"]
                                counts = counts.sort_values(col)
                            return counts

                        def numeric_sort_key(label):
                            try:
                                return float(label.lstrip("(").split(",")[0])
                            except Exception:
                                return label

                        def safe_reindex(counts_df, col, all_labels):
                            """Reindex without crashing on duplicate index values."""
                            counts_df = counts_df.drop_duplicates(subset=[col])
                            counts_df = counts_df.set_index(col).reindex(all_labels, fill_value=0).reset_index()
                            counts_df.columns = [col, "Count"]
                            return counts_df

                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        fig = None

                        if y_mode == "📊 Count":
                            subtitle = "Binned ranges · count" if is_numeric_col else "Response count per value"
                            if is_comparing:
                                card(f"{x_axis} — Count", f"Current vs Previous — {subtitle}")
                                # Use cleaned df split by Period tag (not raw df_current/df_previous)
                                df_cur_clean  = df[df["Period"] == "Current"]
                                df_prev_clean = df[df["Period"] == "Previous"]
                                cur_c  = bin_col_series(df_cur_clean,  x_axis, n_bins)
                                prev_c = bin_col_series(df_prev_clean, x_axis, n_bins)
                                all_labels_set = set(cur_c[x_axis]) | set(prev_c[x_axis])
                                all_labels = sorted(all_labels_set, key=numeric_sort_key) if is_numeric_col else sorted(all_labels_set)
                                cur_c  = safe_reindex(cur_c,  x_axis, all_labels); cur_c["Period"]  = "Current"
                                prev_c = safe_reindex(prev_c, x_axis, all_labels); prev_c["Period"] = "Previous"
                                chart_data = pd.concat([cur_c, prev_c], ignore_index=True)
                                fig = px.line(chart_data, x=x_axis, y="Count", color="Period", markers=True,
                                              category_orders={x_axis: all_labels},
                                              color_discrete_map={"Current": CHART_COLORS[0], "Previous": CHART_COLORS[2]})
                            else:
                                card(f"{x_axis} — Count", subtitle)
                                chart_data = bin_col_series(df, x_axis, n_bins)
                                fig = px.line(chart_data, x=x_axis, y="Count", markers=True,
                                              color_discrete_sequence=CHART_COLORS,
                                              category_orders={x_axis: list(chart_data[x_axis])})
                            if fig: fig.update_layout(xaxis_tickangle=-35)
                        else:
                            if y_col:
                                card(f"{y_col} vs {x_axis}")
                                plot_df = df.sort_values(y_col)
                                color_arg = "Period" if is_comparing else None
                                fig = px.line(plot_df, x=y_col, y=x_axis, color=color_arg,
                                              markers=True, line_shape="spline",
                                              color_discrete_sequence=CHART_COLORS)

                        if fig:
                            fig.update_traces(line_width=3, marker_size=9)
                            apply_dark_theme(fig)
                            st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    elif chart_type == "📉 Scatter Plot":
                        cat_cols = df.select_dtypes(exclude="number").columns.tolist()
                        cat_cols = [c for c in cat_cols if c != "Period"]
                        df_encoded = df.copy()
                        if cat_cols:
                            ohe = pd.get_dummies(df_encoded[cat_cols], prefix=cat_cols, dtype=int)
                            df_encoded = pd.concat([df_encoded.drop(columns=cat_cols), ohe], axis=1)
                        scatter_cols = [c for c in df_encoded.columns if c != "Period"]
                        s1, s2, s3 = st.columns(3)
                        with s1:
                            x_num = st.selectbox("X-Axis:", scatter_cols, key="sc_x")
                        with s2:
                            remaining = [c for c in scatter_cols if c != x_num]
                            y_num = st.selectbox("Y-Axis:", remaining, key="sc_y")
                        with s3:
                            color_options = ["None"] + (["Period"] if is_comparing else []) + standard_columns
                            color_col = st.selectbox("Color by:", color_options, key="sc_c")
                        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                        card(f"{x_num} vs {y_num}", "Scatter · categorical columns one-hot encoded")
                        color_arg = None if color_col == "None" else color_col
                        if color_arg and color_arg in df.columns and color_arg not in df_encoded.columns:
                            df_encoded[color_arg] = df[color_arg].values
                        fig = px.scatter(df_encoded, x=x_num, y=y_num, color=color_arg,
                                         color_discrete_sequence=CHART_COLORS, opacity=0.75)
                        fig.update_traces(marker_size=9)
                        apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)
                        st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("No columns available.")

            elif chart_type == "☑️ Grid / Checkbox":
                if not grid_dict:
                    st.warning("No grid/checkbox questions found.")
                else:
                    g_sel, _ = st.columns([2, 2])
                    with g_sel:
                        selected_grid = st.selectbox("Select question group:", list(grid_dict.keys()))
                    grid_cols = grid_dict[selected_grid]
                    id_vars = ["Period"] if is_comparing else []
                    melted_df = df.melt(id_vars=id_vars, value_vars=grid_cols, var_name="Option", value_name="Response")
                    melted_df["Option"] = melted_df["Option"].apply(lambda x: x.rsplit("[", 1)[-1].replace("]", "").strip())
                    clean_responses = melted_df.dropna(subset=["Response"])
                    clean_responses = clean_responses[~clean_responses["Response"].isin(["No Answer", "N/A", "Unknown"])]
                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    card(selected_grid, "Response distribution across options")
                    if is_comparing:
                        chart_data = clean_responses.groupby(["Option", "Response", "Period"]).size().reset_index(name="Count")
                        fig = px.bar(chart_data, x="Option", y="Count", color="Period", facet_row="Response", barmode="group", color_discrete_sequence=CHART_COLORS)
                    else:
                        chart_data = clean_responses.groupby(["Option", "Response"]).size().reset_index(name="Count")
                        fig = px.bar(chart_data, x="Option", y="Count", color="Response", barmode="group", color_discrete_sequence=CHART_COLORS)
                    fig.update_traces(marker_line_width=0)
                    apply_dark_theme(fig)
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

            # ═══════════════════════════════════════
            # 🔢 CROSS-TAB COUNT
            # ═══════════════════════════════════════
            elif chart_type == "🔢 Cross-Tab Count":
                st.markdown(
                    "<p style='color:#64748b;font-size:0.85rem;margin-bottom:12px;'>"
                    "Pick a <b style='color:#94a3b8'>Filter column</b> (e.g. Yes/No question) and a "
                    "<b style='color:#94a3b8'>Breakdown column</b> to see how counts differ across each answer.</p>",
                    unsafe_allow_html=True,
                )

                ct1, ct2, ct3 = st.columns([1, 1, 1])
                with ct1:
                    filter_col = st.selectbox(
                        "① Filter column (e.g. Yes / No):",
                        standard_columns,
                        key="ct_filter_col",
                        help="The column whose values will split the data into groups.",
                    )
                with ct2:
                    breakdown_options = [c for c in standard_columns if c != filter_col]
                    breakdown_col = st.selectbox(
                        "② Breakdown column (what to count):",
                        breakdown_options,
                        key="ct_breakdown_col",
                        help="The column whose distribution you want to see inside each group.",
                    )
                with ct3:
                    # Let user optionally restrict which filter values to show
                    filter_unique = sorted(df[filter_col].dropna().unique().tolist())
                    selected_filter_vals = st.multiselect(
                        "③ Show only these filter values (optional):",
                        filter_unique,
                        default=filter_unique,
                        key="ct_filter_vals",
                        help="Uncheck values to hide them from the chart.",
                    )

                ct_display = st.radio(
                    "Display as:",
                    ["Grouped Bar", "Stacked Bar (count)", "Stacked Bar (% of filter group)", "Heatmap"],
                    horizontal=True,
                    key="ct_display_mode",
                )

                if filter_col and breakdown_col and selected_filter_vals:
                    ct_df = df[df[filter_col].astype(str).isin([str(v) for v in selected_filter_vals])].copy()
                    ct_df[filter_col] = ct_df[filter_col].astype(str)
                    ct_df[breakdown_col] = ct_df[breakdown_col].astype(str)

                    # Build cross-tab counts
                    cross = (
                        ct_df.groupby([filter_col, breakdown_col])
                        .size()
                        .reset_index(name="Count")
                    )

                    # Percentage within each filter group
                    group_totals = cross.groupby(filter_col)["Count"].transform("sum")
                    cross["Pct"] = (cross["Count"] / group_totals * 100).round(1)

                    # ── Sort breakdown col by total descending for readability ──
                    bd_order = (
                        cross.groupby(breakdown_col)["Count"]
                        .sum()
                        .sort_values(ascending=False)
                        .index.tolist()
                    )

                    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
                    card(
                        f"{breakdown_col}  ×  {filter_col}",
                        f"Count of '{breakdown_col}' broken down by each answer in '{filter_col}'"
                    )

                    if ct_display == "Grouped Bar":
                        # ── Top-N control to avoid overcrowding ──
                        top_n = st.slider(
                            "Show top N breakdown values (by total count):",
                            min_value=5, max_value=min(50, len(bd_order)),
                            value=min(15, len(bd_order)),
                            key="ct_topn",
                        )
                        bd_order_trimmed = bd_order[:top_n]
                        cross_trimmed = cross[cross[breakdown_col].isin(bd_order_trimmed)]

                        n_groups    = len(bd_order_trimmed)
                        n_colors    = cross_trimmed[filter_col].nunique()
                        chart_h     = max(420, n_groups * 28)
                        bar_w       = max(0.25, min(0.7, 0.9 / max(n_colors, 1)))

                        fig = px.bar(
                            cross_trimmed,
                            x=breakdown_col,
                            y="Count",
                            color=filter_col,
                            barmode="group",
                            text="Count",
                            category_orders={breakdown_col: bd_order_trimmed},
                            color_discrete_sequence=CHART_COLORS,
                            custom_data=[filter_col, "Pct"],
                        )
                        fig.update_traces(
                            marker_line_width=0,
                            width=bar_w,
                            textposition="outside",
                            textfont=dict(color="#cbd5e1", size=11, family="DM Sans, sans-serif"),
                            hovertemplate=(
                                "<b>%{x}</b><br>"
                                f"{filter_col}: <b>%{{customdata[0]}}</b><br>"
                                "Count: <b>%{y}</b><br>"
                                "Share in group: <b>%{customdata[1]}%</b>"
                                "<extra></extra>"
                            ),
                        )
                        fig.update_layout(
                            height=chart_h,
                            bargap=0.25,
                            bargroupgap=0.08,
                            xaxis=dict(
                                tickangle=-38,
                                tickfont=dict(size=11, color="#94a3b8"),
                                showgrid=False,
                                categoryorder="array",
                                categoryarray=bd_order_trimmed,
                            ),
                            yaxis=dict(
                                gridcolor="#1f2d45",
                                gridwidth=1,
                                griddash="dot",
                                tickfont=dict(size=11, color="#64748b"),
                                title=dict(text="Count", font=dict(color="#64748b", size=12)),
                                zeroline=True,
                                zerolinecolor="#2a3f66",
                                zerolinewidth=1,
                            ),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="left",
                                x=0,
                                bgcolor="rgba(26,39,68,0.85)",
                                bordercolor="#2a3f66",
                                borderwidth=1,
                                font=dict(color="#c9d1e0", size=11),
                                title=dict(
                                    text=filter_col[:40] + ("…" if len(filter_col) > 40 else ""),
                                    font=dict(color="#64748b", size=10),
                                ),
                            ),
                            uniformtext_minsize=9,
                            uniformtext_mode="hide",
                            margin=dict(l=10, r=10, t=60, b=80),
                        )
                        apply_dark_theme(fig)
                        # Restore per-axis overrides after apply_dark_theme
                        fig.update_xaxes(showgrid=False, tickangle=-38)
                        fig.update_yaxes(gridcolor="#1f2d45", griddash="dot")
                        st.plotly_chart(fig, use_container_width=True)

                    elif ct_display == "Stacked Bar (count)":
                        fig = px.bar(
                            cross,
                            x=filter_col,
                            y="Count",
                            color=breakdown_col,
                            barmode="stack",
                            text="Count",
                            category_orders={breakdown_col: bd_order},
                            color_discrete_sequence=CHART_COLORS,
                        )
                        fig.update_traces(marker_line_width=0, textposition="inside", textfont_color="white")
                        apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)

                    elif ct_display == "Stacked Bar (% of filter group)":
                        fig = px.bar(
                            cross,
                            x=filter_col,
                            y="Pct",
                            color=breakdown_col,
                            barmode="stack",
                            text="Pct",
                            category_orders={breakdown_col: bd_order},
                            color_discrete_sequence=CHART_COLORS,
                            labels={"Pct": "% of group"},
                        )
                        fig.update_traces(
                            marker_line_width=0,
                            texttemplate="%{text}%",
                            textposition="inside",
                            textfont_color="white",
                        )
                        fig.update_layout(yaxis_title="% of group")
                        apply_dark_theme(fig)
                        st.plotly_chart(fig, use_container_width=True)

                    elif ct_display == "Heatmap":
                        pivot = cross.pivot_table(
                            index=breakdown_col,
                            columns=filter_col,
                            values="Count",
                            fill_value=0,
                        )
                        # Sort rows by total
                        pivot = pivot.loc[bd_order] if all(v in pivot.index for v in bd_order) else pivot
                        fig = px.imshow(
                            pivot,
                            text_auto=True,
                            color_continuous_scale=["#0e1525", "#1e40af", "#3b82f6", "#60a5fa", "#bfdbfe"],
                            aspect="auto",
                        )
                        fig.update_traces(textfont_color="white")
                        fig.update_layout(
                            xaxis_title=filter_col,
                            yaxis_title=breakdown_col,
                            coloraxis_showscale=True,
                        )
                        apply_dark_theme(fig)
                        fig.update_layout(height=max(300, len(bd_order) * 28 + 80))
                        st.plotly_chart(fig, use_container_width=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                    # ── Summary table ──
                    with st.expander("📋 View Cross-Tab Table", expanded=False):
                        pivot_tbl = cross.pivot_table(
                            index=breakdown_col,
                            columns=filter_col,
                            values="Count",
                            fill_value=0,
                            aggfunc="sum",
                        )
                        pivot_tbl["TOTAL"] = pivot_tbl.sum(axis=1)
                        pivot_tbl = pivot_tbl.sort_values("TOTAL", ascending=False)
                        st.dataframe(pivot_tbl, use_container_width=True)

                        pct_tbl = cross.pivot_table(
                            index=breakdown_col,
                            columns=filter_col,
                            values="Pct",
                            fill_value=0,
                            aggfunc="sum",
                        ).round(1)
                        st.markdown("<small style='color:#64748b'>% share within each filter group:</small>", unsafe_allow_html=True)
                        st.dataframe(pct_tbl.style.format("{:.1f}%"), use_container_width=True)
                else:
                    st.info("Select both a filter column and a breakdown column above.")

        except Exception as e:
            st.error(f"Chart error: {e}")

    # ─────────────────────────────────────────
    # TAB 2: RAW DATA
    # ─────────────────────────────────────────
    with tab2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        card("Raw Data Preview", f"{len(df)} rows · {len(df.columns)} columns")

        search_term = st.text_input("🔍 Search table (any column):", placeholder="Type to filter rows…", key="search_input")
        if search_term:
            mask = df.apply(lambda col: col.astype(str).str.contains(search_term, case=False, na=False)).any(axis=1)
            display_df = df[mask]
            st.markdown(f"<small style='color:#64748b'>Showing {len(display_df)} of {len(df)} rows matching <b style='color:#60a5fa'>{search_term}</b></small>", unsafe_allow_html=True)
        else:
            display_df = df

        st.dataframe(display_df, use_container_width=True, height=450)
        st.markdown("</div>", unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # TAB 3: DATA QUALITY REPORT
    # ─────────────────────────────────────────
    with tab3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        card("Data Quality Report", "Completeness per column · sorted by fill rate ascending")

        quality_df = get_data_quality(df)

        # Visual completeness bars
        for _, row in quality_df.iterrows():
            pct = row["Filled %"]
            color = "#10b981" if pct >= 90 else ("#f59e0b" if pct >= 60 else "#ef4444")
            badge_cls = "badge-ok" if pct >= 90 else ("badge-warn" if pct >= 60 else "badge")
            badge_label = "Good" if pct >= 90 else ("Fair" if pct >= 60 else "Low"  )
            col_short = row["Column"][:52] + "…" if len(row["Column"]) > 55 else row["Column"]
            st.markdown(f"""
            <div style='margin-bottom:10px'>
                <div style='display:flex;justify-content:space-between;align-items:center;'>
                    <span style='color:#c9d1e0;font-size:0.78rem;'>{col_short}</span>
                    <span>
                        <span class='badge {badge_cls}'>{badge_label}</span>
                        <span style='color:#60a5fa;font-size:0.78rem;margin-left:6px'>{pct}%</span>
                        <span style='color:#475569;font-size:0.72rem;margin-left:4px'>({row['Blank']} blank)</span>
                    </span>
                </div>
                <div class='quality-bar-bg'>
                    <div class='quality-bar-fill' style='width:{pct}%;background:{"linear-gradient(90deg,#10b981,#34d399)" if pct>=90 else ("linear-gradient(90deg,#f59e0b,#fbbf24)" if pct>=60 else "linear-gradient(90deg,#ef4444,#f87171)") }'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Summary stats
        good = (quality_df["Filled %"] >= 90).sum()
        fair = ((quality_df["Filled %"] >= 60) & (quality_df["Filled %"] < 90)).sum()
        low  = (quality_df["Filled %"] < 60).sum()
        qc1, qc2, qc3 = st.columns(3)
        with qc1:
            st.metric("✅ Good (≥90%)", good)
        with qc2:
            st.metric("⚠️ Fair (60–89%)", fair)
        with qc3:
            st.metric("❌ Low (<60%)", low)

        st.divider()

        # Duplicate check
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            st.warning(f"⚠️ {dup_count} duplicate rows detected. Use **Deduplicate Rows** in the sidebar to remove them.")
        else:
            st.success("✅ No duplicate rows found.")

        # Unique value distribution for categorical columns
        st.markdown("---")
        card("Unique Value Counts", "Top categorical columns")
        cat_summary = []
        for col in df.select_dtypes(include="object").columns:
            if col == "Period": continue
            ucount = df[col].nunique()
            top_val = df[col].mode().iloc[0] if not df[col].mode().empty else "—"
            cat_summary.append({"Column": col, "Unique Values": ucount, "Most Common": str(top_val)})
        if cat_summary:
            st.dataframe(pd.DataFrame(cat_summary), use_container_width=True, height=300)

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="
        text-align:center;
        padding: 80px 40px;
        background: linear-gradient(160deg, #1a2744 0%, #131d35 100%);
        border: 1px dashed #2a3f66;
        border-radius: 16px;
        margin-top: 20px;
    ">
        <div style="font-size:3rem;margin-bottom:16px;">📂</div>
        <h2 style="color:#e2e8f0;font-family:'Space Grotesk',sans-serif;margin-bottom:8px;">No Data Loaded</h2>
        <p style="color:#64748b;font-size:0.95rem;">
            Upload a <strong style="color:#94a3b8">Current Period CSV</strong> from the sidebar to begin.<br>
            Supports Google Forms exports · Auto-detects grid & checkbox questions.
        </p>
    </div>
    """, unsafe_allow_html=True)
