import sqlite3
import re
from html import escape

import pandas as pd
import streamlit as st

try:

    from streamlit_autorefresh import st_autorefresh

except ImportError:

    st_autorefresh = None

from github_client import sync_failed_workflows


DB_PATH = "devops_agent.db"
ANSI_PATTERN = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")


def is_valid_url(value):

    if pd.isna(value):
        return False

    return str(value).startswith(
        (
            "http://",
            "https://"
        )
    )


def clean_text(value):

    if pd.isna(value):
        return ""

    return ANSI_PATTERN.sub("", str(value)).strip()


def short_text(value, limit=220):

    text = clean_text(value)

    if len(text) <= limit:
        return text

    return text[:limit].rstrip() + "..."


def html_text(value):

    return escape(clean_text(value))


@st.cache_data(ttl=5)
def load_incidents():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        id,
        timestamp,
        repository,
        workflow,
        status,
        category,
        root_cause,
        errors,
        suggestions,
        github_url,
        log_path
    FROM incidents
    ORDER BY id DESC
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    if not df.empty:

        df["mitigation"] = df["suggestions"].apply(clean_text)
        df["mitigation_preview"] = df["suggestions"].apply(short_text)
        df["problem_url"] = df["github_url"].where(
            df["github_url"].apply(is_valid_url),
            None
        )

    return df


@st.cache_data(ttl=60, show_spinner=False)
def sync_github_incidents():

    return sync_failed_workflows()


def apply_theme(dark_mode):

    if dark_mode:

        colors = {
            "bg": "#111318",
            "panel": "#191d24",
            "panel_alt": "#20252e",
            "text": "#f4f6f8",
            "muted": "#aab3c0",
            "border": "#343b47",
            "accent": "#5cc8ff",
            "good": "#72d391"
        }

    else:

        colors = {
            "bg": "#f7f8fa",
            "panel": "#ffffff",
            "panel_alt": "#eef2f5",
            "text": "#1f2933",
            "muted": "#627083",
            "border": "#d9e0e7",
            "accent": "#1f78d1",
            "good": "#168a4a"
        }

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: {colors["bg"]};
                color: {colors["text"]};
            }}

            [data-testid="stSidebar"] {{
                background: {colors["panel"]};
                border-right: 1px solid {colors["border"]};
            }}

            h1, h2, h3, h4, h5, h6, p, label, span {{
                color: {colors["text"]};
            }}

            .block-container {{
                padding-top: 1.5rem;
                padding-bottom: 2rem;
                max-width: 1280px;
            }}

            [data-testid="stMetric"] {{
                background: {colors["panel"]};
                border: 1px solid {colors["border"]};
                border-radius: 8px;
                padding: 1rem;
            }}

            [data-testid="stMetricLabel"] p {{
                color: {colors["muted"]};
            }}

            [data-testid="stMetricValue"] {{
                color: {colors["text"]};
            }}

            div[data-testid="stAlert"] {{
                background: {colors["panel"]};
                border: 1px solid {colors["border"]};
                color: {colors["text"]};
            }}

            .status-pill {{
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                padding: 0.35rem 0.65rem;
                border-radius: 999px;
                background: {colors["panel_alt"]};
                border: 1px solid {colors["border"]};
                color: {colors["good"]};
                font-size: 0.9rem;
                font-weight: 600;
            }}

            .section-note {{
                color: {colors["muted"]};
                margin-top: -0.4rem;
                margin-bottom: 1rem;
            }}

            .latest-box {{
                background: {colors["panel"]};
                border: 1px solid {colors["border"]};
                border-radius: 8px;
                padding: 1rem;
            }}

            .latest-label {{
                color: {colors["muted"]};
                font-size: 0.82rem;
                text-transform: uppercase;
                letter-spacing: 0;
                margin-bottom: 0.2rem;
            }}

            .latest-value {{
                color: {colors["text"]};
                font-size: 1rem;
                line-height: 1.45;
                margin-bottom: 0.85rem;
            }}

            a {{
                color: {colors["accent"]};
            }}

            .skeleton-shell {{
                margin-top: 1rem;
            }}

            .skeleton-row {{
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 1rem;
                margin: 1.2rem 0;
            }}

            .skeleton-grid {{
                display: grid;
                grid-template-columns: 2fr 1fr;
                gap: 1rem;
                margin: 1.2rem 0;
            }}

            .skeleton-block {{
                min-height: 6rem;
                border-radius: 8px;
                border: 1px solid {colors["border"]};
                background: {colors["panel"]};
                padding: 1rem;
            }}

            .skeleton-table {{
                min-height: 18rem;
                border-radius: 8px;
                border: 1px solid {colors["border"]};
                background: {colors["panel"]};
                padding: 1rem;
                margin-top: 1rem;
            }}

            .skeleton-line {{
                height: 0.85rem;
                border-radius: 999px;
                margin-bottom: 0.75rem;
                background: linear-gradient(
                    90deg,
                    {colors["panel_alt"]} 25%,
                    {colors["border"]} 37%,
                    {colors["panel_alt"]} 63%
                );
                background-size: 400% 100%;
                animation: skeleton-shimmer 1.35s ease infinite;
            }}

            .skeleton-line.short {{
                width: 38%;
            }}

            .skeleton-line.medium {{
                width: 64%;
            }}

            .skeleton-line.long {{
                width: 88%;
            }}

            @keyframes skeleton-shimmer {{
                0% {{
                    background-position: 100% 0;
                }}
                100% {{
                    background-position: 0 0;
                }}
            }}

            @media (max-width: 760px) {{
                .skeleton-row,
                .skeleton-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )


def render_skeleton():

    st.markdown(
        """
        <div class="skeleton-shell" aria-label="Loading dashboard">
            <div class="skeleton-line medium"></div>
            <div class="skeleton-line short"></div>

            <div class="skeleton-row">
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                </div>
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                </div>
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                </div>
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                </div>
            </div>

            <div class="skeleton-grid">
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line long"></div>
                    <div class="skeleton-line medium"></div>
                    <div class="skeleton-line short"></div>
                </div>
                <div class="skeleton-block">
                    <div class="skeleton-line short"></div>
                    <div class="skeleton-line medium"></div>
                    <div class="skeleton-line long"></div>
                </div>
            </div>

            <div class="skeleton-table">
                <div class="skeleton-line long"></div>
                <div class="skeleton-line long"></div>
                <div class="skeleton-line medium"></div>
                <div class="skeleton-line long"></div>
                <div class="skeleton-line medium"></div>
                <div class="skeleton-line long"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.set_page_config(
    page_title="DevOps Investigation Agent",
    page_icon="DA",
    layout="wide"
)

if st_autorefresh is not None:

    st_autorefresh(
        interval=30000,
        key="refresh"
    )

with st.sidebar:

    st.title("DevOps Agent")
    dark_mode = st.toggle("Dark mode", value=False)
    auto_sync = st.toggle("Auto-sync GitHub", value=False)
    sync_now = st.button("Sync GitHub now", use_container_width=True)
    st.caption("Incident dashboard")

apply_theme(dark_mode)

skeleton = st.empty()

with skeleton.container():

    render_skeleton()

sync_result = None

if auto_sync or sync_now:

    if sync_now:

        sync_github_incidents.clear()
        load_incidents.clear()

    sync_result = sync_github_incidents()

df = load_incidents()
skeleton.empty()

st.title("DevOps Investigation Agent")
st.markdown(
    '<span class="status-pill">Agent Status: Running</span>',
    unsafe_allow_html=True
)

if df.empty:

    st.info("No incidents found yet. Run the agent against a log file to populate the dashboard.")
    st.stop()

latest = df.iloc[0]

if sync_result and sync_result["errors"]:

    st.warning(
        "GitHub sync had a problem: "
        + "; ".join(sync_result["errors"][:3])
    )

if sync_result and not sync_result["errors"]:

    st.caption(
        "GitHub sync: "
        f"{sync_result['synced']} opened, "
        f"{sync_result['resolved']} resolved, "
        f"{sync_result['skipped']} skipped."
    )

metric_1, metric_2, metric_3, metric_4 = st.columns(4)

metric_1.metric(
    "Open Incidents",
    int((df["status"] == "Open").sum())
)
metric_2.metric(
    "Resolved Incidents",
    int((df["status"] == "Resolved").sum())
)
metric_3.metric(
    "Total Recorded Incidents",
    len(df)
)
metric_4.metric(
    "Unknown Errors",
    int((df["category"] == "Unknown").sum())
)

st.divider()

st.subheader("Latest Incident")
st.markdown(
    '<div class="section-note">Most recent failure captured by the investigation agent.</div>',
    unsafe_allow_html=True
)

left, right = st.columns([2, 1])

with left:

    st.markdown(
        f"""
        <div class="latest-box">
            <div class="latest-label">Category</div>
            <div class="latest-value">{html_text(latest["category"])}</div>
            <div class="latest-label">Status</div>
            <div class="latest-value">{html_text(latest["status"])}</div>
            <div class="latest-label">Root Cause</div>
            <div class="latest-value">{html_text(latest["root_cause"])}</div>
            <div class="latest-label">Mitigation</div>
            <div class="latest-value">{html_text(short_text(latest["mitigation"], 500))}</div>
            <div class="latest-label">Detected At</div>
            <div class="latest-value">{html_text(latest["timestamp"])}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with right:

    st.metric("Confidence", "80%")

    if is_valid_url(latest["github_url"]):

        st.link_button(
            "Open GitHub Workflow",
            latest["github_url"],
            use_container_width=True
        )

    if latest["log_path"]:

        st.caption(f"Downloaded log: {latest['log_path']}")

st.divider()

filter_left, filter_right = st.columns(2)

with filter_left:

    search = st.text_input("Search root cause")

with filter_right:

    categories = ["All"] + sorted(df["category"].dropna().unique().tolist())
    selected = st.selectbox("Filter category", categories)

filtered_df = df.copy()

if search:
    filtered_df = filtered_df[
        filtered_df["root_cause"].astype(str).str.contains(
            str(search),
            case=False,
            na=False
        )
    ]

if selected != "All":
    filtered_df = filtered_df[
        filtered_df["category"] == selected
    ]
    
history_tab, insights_tab, details_tab = st.tabs(
    [
        "Incident History",
        "Insights",
        "Latest Details"
    ]
)

with history_tab:

    history_df = filtered_df[
        [
            "id",
            "timestamp",
            "repository",
            "workflow",
            "status",
            "category",
            "root_cause",
            "mitigation_preview",
            "problem_url",
            "log_path"
        ]
    ].rename(
        columns={
            "id": "ID",
            "timestamp": "Time",
            "repository": "Repository",
            "workflow": "Workflow",
            "status": "Status",
            "category": "Category",
            "root_cause": "Root Cause",
            "mitigation_preview": "Mitigation",
            "problem_url": "Problem Link",
            "log_path": "Log Path"
        }
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Problem Link": st.column_config.LinkColumn(
                "Problem Link",
                display_text="Open workflow"
            )
        }
    )

with insights_tab:

    chart_left, chart_right = st.columns(2)

    with chart_left:

        st.subheader("Categories")
        st.bar_chart(filtered_df["category"].value_counts())

    with chart_right:

        st.subheader("Root Causes")
        st.bar_chart(filtered_df["root_cause"].value_counts())

with details_tab:

    st.subheader("Error Log")
    st.code(clean_text(latest["errors"]), language="text")

    st.subheader("Mitigation")
    st.success(latest["mitigation"])

st.caption("DevOps Investigation Agent | Local AI | SQLite | Ollama | Rule Engine")
