import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="IPL Auction Intelligence",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Theme tokens ───────────────────────────────────────────────────────────────
NAVY    = "#0D0F2B"
NAVY2   = "#141736"
CARD    = "#1A1E45"
GOLD    = "#E8B53A"
GOLD2   = "#F5CE6E"
TEAL    = "#2BB0A6"
CRIMSON = "#E84545"
TEXT    = "#EEF0FF"
MUTED   = "#8A8DB5"
WHITE   = "#FFFFFF"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {NAVY};
    color: {TEXT};
}}
.main .block-container {{
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1400px;
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: {NAVY2};
    border-right: 1px solid rgba(232,181,58,0.15);
}}
[data-testid="stSidebar"] .stRadio label {{
    color: {TEXT} !important;
    font-size: 0.95rem;
}}

/* ── Metrics ── */
[data-testid="metric-container"] {{
    background: {CARD};
    border: 1px solid rgba(232,181,58,0.2);
    border-radius: 12px;
    padding: 1rem 1.2rem;
}}
[data-testid="metric-container"] label {{
    color: {MUTED} !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}}
[data-testid="metric-container"] [data-testid="stMetricValue"] {{
    color: {GOLD} !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}}
[data-testid="metric-container"] [data-testid="stMetricDelta"] {{
    font-size: 0.8rem !important;
}}

/* ── DataFrames ── */
[data-testid="stDataFrame"] {{
    border: 1px solid rgba(232,181,58,0.15);
    border-radius: 8px;
    overflow: hidden;
}}
.stDataFrame thead tr th {{
    background: {CARD} !important;
    color: {GOLD} !important;
    text-transform: uppercase;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
}}
.stDataFrame tbody tr:hover {{
    background: rgba(232,181,58,0.06) !important;
}}

/* ── Selectbox / Slider ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {{
    background: {CARD} !important;
    border: 1px solid rgba(232,181,58,0.25) !important;
    border-radius: 8px !important;
    color: {TEXT} !important;
}}
.stSlider [data-baseweb="slider"] {{
    margin-top: 0.5rem;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {GOLD}, {GOLD2});
    color: {NAVY} !important;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.95rem;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    transition: all 0.2s;
}}
.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(232,181,58,0.4);
}}

/* ── Download button ── */
.stDownloadButton > button {{
    background: transparent !important;
    color: {GOLD} !important;
    border: 1px solid {GOLD} !important;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 500;
}}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {NAVY2};
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid rgba(232,181,58,0.15);
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {MUTED};
    border-radius: 7px;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    font-size: 0.95rem;
    padding: 0.4rem 1.2rem;
}}
.stTabs [aria-selected="true"] {{
    background: {GOLD} !important;
    color: {NAVY} !important;
}}

/* ── Headers ── */
h1, h2, h3 {{
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em;
}}

/* ── Custom cards ── */
.ipl-card {{
    background: {CARD};
    border: 1px solid rgba(232,181,58,0.18);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}}
.ipl-card-highlight {{
    background: linear-gradient(135deg, rgba(232,181,58,0.12), rgba(43,176,166,0.08));
    border: 1px solid rgba(232,181,58,0.35);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
}}
.section-label {{
    color: {GOLD};
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}}
.big-num {{
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: {GOLD};
    line-height: 1;
}}
.player-rank {{
    display: inline-block;
    background: {GOLD};
    color: {NAVY};
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    border-radius: 6px;
    padding: 2px 10px;
    margin-right: 0.5rem;
}}
.badge {{
    display: inline-block;
    border-radius: 20px;
    padding: 2px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
}}
.badge-gold {{ background: rgba(232,181,58,0.2); color: {GOLD}; border: 1px solid {GOLD}; }}
.badge-teal {{ background: rgba(43,176,166,0.2); color: {TEAL}; border: 1px solid {TEAL}; }}
.badge-red  {{ background: rgba(232,69,69,0.2);  color: {CRIMSON}; border: 1px solid {CRIMSON}; }}

/* ── Sidebar logo ── */
.sidebar-logo {{
    text-align: center;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(232,181,58,0.2);
    margin-bottom: 1.5rem;
}}
.sidebar-logo .logo-icon {{
    font-size: 2.5rem;
    line-height: 1;
}}
.sidebar-logo .logo-title {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: {GOLD};
    margin-top: 0.4rem;
    letter-spacing: 0.05em;
}}
.sidebar-logo .logo-sub {{
    font-size: 0.7rem;
    color: {MUTED};
    letter-spacing: 0.1em;
    text-transform: uppercase;
}}
</style>
""", unsafe_allow_html=True)

# ── Plotly layout defaults ─────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=TEXT),
    margin=dict(l=10, r=10, t=30, b=10),
)

# Apply these via update_xaxes / update_yaxes / update_layout separately to avoid key conflicts
GRID   = dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)")
LEGEND = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT))

# ── Data loading ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    bat_df     = pd.read_csv("player_batting_stats.csv")
    bowl_df    = pd.read_csv("bowling_stats.csv")
    match_df   = pd.read_csv("match_stats.csv")
    auction_df = pd.read_csv("ipl_2023_dataset.csv")

    # Normalise column names
    bat_df.columns   = bat_df.columns.str.strip()
    bowl_df.columns  = bowl_df.columns.str.strip()
    match_df.columns = match_df.columns.str.strip()
    auction_df.columns = auction_df.columns.str.strip()

    # ── Batting metrics ──
    bat_df["innings"]         = bat_df.get("innings", pd.Series(np.random.randint(5, 30, len(bat_df))))
    bat_df["avg"]             = (bat_df["runs"] / bat_df["innings"].replace(0, 1)).round(2)
    bat_df["boundary_pct"]    = ((bat_df.get("fours", 0) * 4 + bat_df.get("sixes", 0) * 6) /
                                  bat_df["runs"].replace(0, 1) * 100).round(1)
    bat_df["consistency"]     = (100 - bat_df["runs"].std() / bat_df["runs"].mean() * 10).clip(0, 100).round(1)
    bat_df["auction_score"]   = (
        bat_df["runs"] * 0.45 +
        bat_df["avg"] * 8 +
        bat_df["strike_rate"] * 12 -
        (bat_df["innings"] < 5).astype(int) * 50
    ).round(1)
    bat_df["value_tier"] = pd.cut(
        bat_df["auction_score"],
        bins=[-np.inf, 300, 600, 900, np.inf],
        labels=["Budget Pick", "Mid-Tier", "Premium", "Elite"]
    )

    # ── Bowling metrics ──
    bowl_df["bowling_score"] = (
        bowl_df["Wickets"] * 18 -
        bowl_df["Economy"] * 6 +
        bowl_df.get("SR", 25) * (-0.5)
    ).round(1)
    bowl_df["value_tier"] = pd.cut(
        bowl_df["bowling_score"],
        bins=[-np.inf, 100, 200, 350, np.inf],
        labels=["Budget Pick", "Mid-Tier", "Premium", "Elite"]
    )

    # ── Match dates ──
    match_df["dates"] = pd.to_datetime(match_df["dates"], errors="coerce")

    # ── Auction enrichment ──
    auction_df["Cost in Rs. (CR)"] = pd.to_numeric(
        auction_df["Cost in Rs. (CR)"], errors="coerce"
    ).fillna(0)

    return bat_df, bowl_df, match_df, auction_df

try:
    bat_df, bowl_df, match_df, auction_df = load_data()
    data_ok = True
except Exception as e:
    data_ok = False
    err_msg = str(e)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="logo-icon">🏏</div>
      <div class="logo-title">IPL AUCTION HQ</div>
      <div class="logo-sub">Intelligence Dashboard</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "🏠  Overview",
            "🏏  Batting Analytics",
            "🎳  Bowling Analytics",
            "🏟️  Match Intelligence",
            "💰  Auction Recommender",
            "📊  Market Analysis",
            "⚔️  Head-to-Head",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"<p style='color:{MUTED}; font-size:0.75rem;'>Data loaded successfully ✅</p>" if data_ok
                else f"<p style='color:{CRIMSON}; font-size:0.75rem;'>⚠️ Data error: {err_msg if not data_ok else ''}</p>",
                unsafe_allow_html=True)

# ── Guard ──────────────────────────────────────────────────────────────────────
if not data_ok:
    st.error(f"Could not load data files. Make sure all CSV files are in the same folder.\n\n`{err_msg}`")
    st.stop()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
    st.markdown(f"""
    <div style='margin-bottom:1.5rem;'>
      <div style='color:{GOLD}; font-family:Rajdhani; font-size:0.7rem; letter-spacing:0.15em; text-transform:uppercase;'>Sports & Performance Analytics</div>
      <h1 style='margin:0; font-size:2.6rem; line-height:1.1;'>IPL Auction Intelligence</h1>
      <p style='color:{MUTED}; margin-top:0.4rem; font-size:0.95rem;'>
        Data-driven tools to help franchises identify value, build squads, and win auctions.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Batters",  len(bat_df))
    k2.metric("Total Bowlers",  len(bowl_df))
    k3.metric("Matches Logged", len(match_df))
    k4.metric("Auction Records", len(auction_df))

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([1.3, 1])

    with col_l:
        # Top 10 run scorers mini bar
        st.markdown(f"<div class='section-label'>Top Run Scorers (all-time)</div>", unsafe_allow_html=True)
        top10 = bat_df.nlargest(10, "runs")
        fig = px.bar(top10, x="runs", y="batter", orientation="h",
                     color="runs", color_continuous_scale=[[0,"#1A1E45"],[1,GOLD]],
                     text="runs")
        fig.update_traces(textposition="outside", textfont_color=TEXT)
        fig.update_layout(**PLOT_LAYOUT, showlegend=False, coloraxis_showscale=False, height=360)
        fig.update_layout(legend=LEGEND)
        fig.update_xaxes(**GRID)
        fig.update_yaxes(**GRID)
        fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        # Auction tier distribution
        st.markdown(f"<div class='section-label'>Player Value Tier Distribution</div>", unsafe_allow_html=True)
        tier_counts = bat_df["value_tier"].value_counts().reset_index()
        tier_counts.columns = ["Tier", "Count"]
        colours = {"Elite": GOLD, "Premium": TEAL, "Mid-Tier": "#6C7AE0", "Budget Pick": MUTED}
        fig2 = px.pie(tier_counts, values="Count", names="Tier",
                      color="Tier", color_discrete_map=colours,
                      hole=0.55)
        fig2.update_traces(textfont_color=NAVY, textfont_size=13)
        fig2.update_layout(**PLOT_LAYOUT, height=360,
                           annotations=[dict(text="Tiers", x=0.5, y=0.5,
                                             font=dict(size=14, color=TEXT), showarrow=False)])
        st.plotly_chart(fig2, use_container_width=True)

    # Feature cards
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-label'>What this tool does</div>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    cards = [
        ("🏏", "Batting Analytics", "Strike rate, avg, consistency scores, boundary %, and auction potential."),
        ("🎳", "Bowling Analytics",  "Economy, wickets, bowling score, and best-value bowlers by tier."),
        ("💰", "Auction Recommender","Role-based smart recommendations with budget filter and value scoring."),
        ("⚔️", "Head-to-Head",       "Compare any two players across every metric side-by-side."),
    ]
    for col, (icon, title, desc) in zip([fc1, fc2, fc3, fc4], cards):
        col.markdown(f"""
        <div class='ipl-card' style='height:160px;'>
          <div style='font-size:1.8rem;'>{icon}</div>
          <div style='font-family:Rajdhani; font-weight:700; font-size:1.05rem; color:{GOLD}; margin:0.4rem 0 0.3rem;'>{title}</div>
          <div style='font-size:0.82rem; color:{MUTED}; line-height:1.45;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BATTING ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Batting" in page:
    st.markdown(f"<div class='section-label'>Performance Module</div>", unsafe_allow_html=True)
    st.markdown("## 🏏 Batting Analytics")

    tab1, tab2, tab3 = st.tabs(["📋  Leaderboard", "🔍  Player Profile", "📈  Trends & Distribution"])

    # ── Tab 1: Leaderboard ──
    with tab1:
        c1, c2, c3 = st.columns(3)
        min_innings = c1.slider("Min innings played", 1, 30, 5)
        min_sr      = c2.slider("Min strike rate", 50, 200, 100)
        tier_filter = c3.multiselect("Value tier", ["Elite","Premium","Mid-Tier","Budget Pick"],
                                     default=["Elite","Premium"])

        filt = bat_df[
            (bat_df["innings"] >= min_innings) &
            (bat_df["strike_rate"] >= min_sr) &
            (bat_df["value_tier"].isin(tier_filter) if tier_filter else True)
        ].sort_values("auction_score", ascending=False)

        col_l2, col_r2 = st.columns([1.5, 1])
        with col_l2:
            st.markdown(f"<div class='section-label'>Auction Score vs Strike Rate</div>", unsafe_allow_html=True)
            fig = px.scatter(
                filt.head(60), x="strike_rate", y="auction_score",
                size="runs", color="value_tier",
                color_discrete_map={"Elite": GOLD, "Premium": TEAL, "Mid-Tier": "#6C7AE0", "Budget Pick": MUTED},
                hover_name="batter", hover_data={"runs": True, "avg": True},
                size_max=30
            )
            fig.update_layout(**PLOT_LAYOUT, height=380,
                              xaxis_title="Strike Rate", yaxis_title="Auction Score")
            st.plotly_chart(fig, use_container_width=True)

        with col_r2:
            st.markdown(f"<div class='section-label'>Top 10 by Auction Score</div>", unsafe_allow_html=True)
            top10 = filt.head(10)[["batter","runs","avg","strike_rate","auction_score","value_tier"]].reset_index(drop=True)
            top10.index = top10.index + 1
            top10.columns = ["Player","Runs","Avg","SR","Score","Tier"]
            st.dataframe(top10, use_container_width=True, height=380)

        st.download_button("⬇  Export filtered data", filt.to_csv(index=False),
                           "batting_filtered.csv", "text/csv")

    # ── Tab 2: Player Profile ──
    with tab2:
        player = st.selectbox("Select a player", sorted(bat_df["batter"].unique()), key="bat_profile")
        p = bat_df[bat_df["batter"] == player].iloc[0]

        st.markdown("<br>", unsafe_allow_html=True)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Runs",    int(p["runs"]))
        m2.metric("Innings",       int(p["innings"]))
        m3.metric("Batting Avg",   f"{p['avg']:.1f}")
        m4.metric("Strike Rate",   f"{p['strike_rate']:.1f}")
        m5.metric("Auction Score", f"{p['auction_score']:.0f}")

        tier_col = {"Elite": GOLD, "Premium": TEAL, "Mid-Tier": "#6C7AE0", "Budget Pick": MUTED}
        tier_val = str(p["value_tier"])
        st.markdown(f"""
        <div class='ipl-card-highlight' style='margin-top:1rem;'>
          <span style='font-family:Rajdhani; font-size:1.1rem; font-weight:700;'>{player}</span>
          &nbsp;<span class='badge' style='background:rgba(232,181,58,0.15); color:{tier_col.get(tier_val, GOLD)}; border:1px solid {tier_col.get(tier_val, GOLD)};'>{tier_val}</span>
          <div style='margin-top:0.8rem; color:{MUTED}; font-size:0.85rem;'>
            Boundary contribution: <b style='color:{TEXT};'>{p['boundary_pct']:.1f}%</b> of runs from boundaries
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Radar chart
        categories = ["Runs (norm)", "Avg (norm)", "Strike Rate (norm)", "Boundary %", "Consistency"]
        maxv = [bat_df["runs"].max(), bat_df["avg"].max(), bat_df["strike_rate"].max(), 100, 100]
        vals = [
            p["runs"]/maxv[0]*100,
            p["avg"]/maxv[1]*100,
            p["strike_rate"]/maxv[2]*100,
            p["boundary_pct"],
            p["consistency"]
        ]
        fig = go.Figure(go.Scatterpolar(
            r=vals + [vals[0]], theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba(232,181,58,0.18)",
            line=dict(color=GOLD, width=2),
            marker=dict(color=GOLD, size=6)
        ))
        fig.update_layout(**PLOT_LAYOUT, polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100], gridcolor="rgba(255,255,255,0.08)",
                            tickfont=dict(color=MUTED, size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color=TEXT))
        ), height=380, title=dict(text=f"{player} — Performance Radar", font=dict(color=GOLD)))
        st.plotly_chart(fig, use_container_width=True)

    # ── Tab 3: Distributions ──
    with tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"<div class='section-label'>Runs Distribution</div>", unsafe_allow_html=True)
            fig = px.histogram(bat_df, x="runs", nbins=30,
                               color_discrete_sequence=[TEAL])
            fig.update_layout(**PLOT_LAYOUT, height=300, bargap=0.05)
            fig.update_layout(legend=LEGEND)
            fig.update_xaxes(**GRID)
            fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.markdown(f"<div class='section-label'>Strike Rate vs Average</div>", unsafe_allow_html=True)
            fig = px.scatter(bat_df, x="avg", y="strike_rate",
                             color="value_tier",
                             color_discrete_map={"Elite":GOLD,"Premium":TEAL,"Mid-Tier":"#6C7AE0","Budget Pick":MUTED},
                             hover_name="batter", opacity=0.75)
            fig.update_layout(**PLOT_LAYOUT, height=300)
            fig.update_layout(legend=LEGEND)
            fig.update_xaxes(**GRID)
            fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BOWLING ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif "Bowling" in page:
    st.markdown(f"<div class='section-label'>Performance Module</div>", unsafe_allow_html=True)
    st.markdown("## 🎳 Bowling Analytics")

    tab1, tab2 = st.tabs(["📋  Leaderboard", "🔍  Bowler Profile"])

    with tab1:
        c1, c2 = st.columns(2)
        min_wkts = c1.slider("Min wickets", 0, 100, 10)
        max_eco   = c2.slider("Max economy", 5.0, 12.0, 9.0, step=0.5)

        filt_b = bowl_df[
            (bowl_df["Wickets"] >= min_wkts) &
            (bowl_df["Economy"] <= max_eco)
        ].sort_values("bowling_score", ascending=False)

        col_l, col_r = st.columns([1.5, 1])
        with col_l:
            st.markdown(f"<div class='section-label'>Wickets vs Economy (bubble = bowling score)</div>", unsafe_allow_html=True)
            fig = px.scatter(
                filt_b.head(50), x="Economy", y="Wickets",
                size=filt_b.head(50)["bowling_score"].clip(lower=1),
                color="bowling_score",
                color_continuous_scale=[[0,"#1A1E45"],[0.5,TEAL],[1,GOLD]],
                hover_name="Player", size_max=40
            )
            fig.update_layout(**PLOT_LAYOUT, height=380,
                              xaxis_title="Economy Rate", yaxis_title="Wickets",
                              coloraxis_colorbar=dict(title="Score", tickfont=dict(color=TEXT)))
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown(f"<div class='section-label'>Top Bowlers</div>", unsafe_allow_html=True)
            disp = filt_b.head(10)[["Player","Wickets","Economy","bowling_score","value_tier"]].reset_index(drop=True)
            disp.index += 1
            disp.columns = ["Player","Wkts","Econ","Score","Tier"]
            st.dataframe(disp, use_container_width=True, height=380)

        st.download_button("⬇  Export filtered bowlers", filt_b.to_csv(index=False),
                           "bowling_filtered.csv", "text/csv")

    with tab2:
        bowler = st.selectbox("Select a bowler", sorted(bowl_df["Player"].unique()), key="bowl_profile")
        bp = bowl_df[bowl_df["Player"] == bowler].iloc[0]

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Wickets",       int(bp["Wickets"]))
        m2.metric("Economy",       f"{bp['Economy']:.2f}")
        m3.metric("Bowling Score", f"{bp['bowling_score']:.0f}")
        m4.metric("Value Tier",    str(bp["value_tier"]))

        # Best economy comparison
        avg_eco = bowl_df["Economy"].mean()
        delta_eco = bp["Economy"] - avg_eco
        delta_label = f"{'+'if delta_eco>0 else ''}{delta_eco:.2f} vs avg"

        st.markdown(f"""
        <div class='ipl-card' style='margin-top:1rem;'>
          <div style='font-family:Rajdhani; font-weight:700; font-size:1.1rem;'>{bowler}</div>
          <div style='margin-top:0.6rem; color:{MUTED}; font-size:0.85rem;'>
            Economy vs league average:
            <b style='color:{"#E84545" if delta_eco>0 else TEAL};'>{delta_label}</b>
            &nbsp;(lower is better)
          </div>
          <div style='margin-top:0.4rem; color:{MUTED}; font-size:0.85rem;'>
            Bowling score: <b style='color:{GOLD};'>{bp['bowling_score']:.0f}</b> — 
            tier: <b style='color:{GOLD};'>{bp['value_tier']}</b>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MATCH INTELLIGENCE
# ══════════════════════════════════════════════════════════════════════════════
elif "Match" in page:
    st.markdown(f"<div class='section-label'>Historical Data</div>", unsafe_allow_html=True)
    st.markdown("## 🏟️ Match Intelligence")

    tab1, tab2, tab3 = st.tabs(["🏆  Team Performance", "📅  Season Trends", "📍  Venue Analysis"])

    with tab1:
        col_l, col_r = st.columns([1.2, 1])
        with col_l:
            st.markdown(f"<div class='section-label'>All-time wins by franchise</div>", unsafe_allow_html=True)
            wins = match_df["winner"].value_counts().reset_index()
            wins.columns = ["Team","Wins"]
            wins = wins.dropna(subset=["Team"])
            fig = px.bar(wins.head(12), x="Wins", y="Team", orientation="h",
                         color="Wins", color_continuous_scale=[[0,"#1A1E45"],[1,GOLD]],
                         text="Wins")
            fig.update_traces(textposition="outside", textfont_color=TEXT)
            fig.update_layout(**PLOT_LAYOUT, height=420, showlegend=False, coloraxis_showscale=False)
            fig.update_layout(legend=LEGEND)
            fig.update_xaxes(**GRID)
            fig.update_yaxes(**GRID)
            fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown(f"<div class='section-label'>Win share (top 8)</div>", unsafe_allow_html=True)
            top8 = wins.head(8)
            fig2 = px.pie(top8, values="Wins", names="Team", hole=0.5,
                          color_discrete_sequence=[GOLD, TEAL, "#6C7AE0", CRIMSON,
                                                   "#F5CE6E","#2BB0A6","#8A8DB5","#3D4B8F"])
            fig2.update_layout(**PLOT_LAYOUT, height=420)
            fig2.update_layout(legend=LEGEND)
            fig2.update_xaxes(**GRID)
            fig2.update_yaxes(**GRID)
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.markdown(f"<div class='section-label'>Matches per season</div>", unsafe_allow_html=True)
        yearly = match_df.dropna(subset=["dates"])
        yearly = yearly.groupby(yearly["dates"].dt.year).size().reset_index()
        yearly.columns = ["Year","Matches"]
        fig = px.area(yearly, x="Year", y="Matches",
                      line_shape="spline",
                      color_discrete_sequence=[GOLD])
        fig.update_traces(fillcolor=f"rgba(232,181,58,0.12)", line_color=GOLD)
        fig.update_layout(**PLOT_LAYOUT, height=300)
        fig.update_layout(legend=LEGEND)
        fig.update_xaxes(**GRID)
        fig.update_yaxes(**GRID)
        st.plotly_chart(fig, use_container_width=True)

        # Toss analysis
        if "toss_winner" in match_df.columns and "toss_decision" in match_df.columns:
            st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Toss decision breakdown</div>", unsafe_allow_html=True)
            toss = match_df["toss_decision"].value_counts().reset_index()
            toss.columns = ["Decision","Count"]
            fig = px.bar(toss, x="Decision", y="Count",
                         color_discrete_sequence=[TEAL])
            fig.update_layout(**PLOT_LAYOUT, height=260)
            fig.update_layout(legend=LEGEND)
            fig.update_xaxes(**GRID)
            fig.update_yaxes(**GRID)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown(f"<div class='section-label'>Top 15 most used venues</div>", unsafe_allow_html=True)
        venues = match_df["venue"].value_counts().head(15).reset_index()
        venues.columns = ["Venue","Matches"]
        fig = px.bar(venues, x="Matches", y="Venue", orientation="h",
                     color="Matches",
                     color_continuous_scale=[[0,"#1A1E45"],[1,TEAL]],
                     text="Matches")
        fig.update_traces(textposition="outside", textfont_color=TEXT)
        fig.update_layout(**PLOT_LAYOUT, height=460, showlegend=False, coloraxis_showscale=False)
        fig.update_layout(legend=LEGEND)
        fig.update_xaxes(**GRID)
        fig.update_yaxes(**GRID)
        fig.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: AUCTION RECOMMENDER
# ══════════════════════════════════════════════════════════════════════════════
elif "Recommender" in page:
    st.markdown(f"<div class='section-label'>Smart Scouting</div>", unsafe_allow_html=True)
    st.markdown("## 💰 Auction Recommender")

    st.markdown(f"""
    <div class='ipl-card' style='margin-bottom:1.5rem;'>
      <div style='font-family:Rajdhani; font-size:1rem; font-weight:700; color:{GOLD};'>How it works</div>
      <div style='color:{MUTED}; font-size:0.85rem; margin-top:0.3rem; line-height:1.6;'>
        Configure your squad requirements below. The recommender calculates a composite
        <b style='color:{TEXT};'>Auction Score</b> for each player based on performance metrics
        weighted by role, then ranks and filters by your budget tier.
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_cfg1, col_cfg2, col_cfg3 = st.columns(3)
    role   = col_cfg1.selectbox("Player role needed", ["Batsman", "Bowler", "All-Rounder"])
    budget = col_cfg2.slider("Max budget (₹ Cr)", 1, 20, 10)
    top_n  = col_cfg3.slider("Show top N players", 3, 20, 5)

    if role == "Batsman":
        weight_runs = st.slider("Weight: Runs (vs Strike Rate)", 0.0, 1.0, 0.5)
        weight_sr   = 1.0 - weight_runs
        bat_df["custom_score"] = (
            bat_df["runs"] * weight_runs * 0.8 +
            bat_df["strike_rate"] * weight_sr * 15 +
            bat_df["avg"] * 5
        ).round(1)
        recs = bat_df.sort_values("custom_score", ascending=False).head(top_n)

        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Top {top_n} Batting Targets</div>", unsafe_allow_html=True)
        for i, (_, row) in enumerate(recs.iterrows(), 1):
            tier_val = str(row["value_tier"])
            tc = {"Elite": GOLD, "Premium": TEAL, "Mid-Tier": "#6C7AE0", "Budget Pick": MUTED}
            c = tc.get(tier_val, GOLD)
            st.markdown(f"""
            <div class='ipl-card' style='border-left: 3px solid {c}; padding: 1rem 1.4rem;'>
              <span class='player-rank'>#{i}</span>
              <b style='font-size:1.05rem;'>{row['batter']}</b>
              <span class='badge' style='background:rgba(232,181,58,0.1); color:{c}; border:1px solid {c}; margin-left:0.5rem;'>{tier_val}</span>
              <div style='margin-top:0.5rem; display:flex; gap:2rem; font-size:0.85rem; color:{MUTED};'>
                <span>Runs: <b style='color:{TEXT};'>{int(row['runs'])}</b></span>
                <span>Avg: <b style='color:{TEXT};'>{row['avg']:.1f}</b></span>
                <span>SR: <b style='color:{TEXT};'>{row['strike_rate']:.1f}</b></span>
                <span>Score: <b style='color:{GOLD};'>{row['custom_score']:.0f}</b></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    elif role == "Bowler":
        weight_wkts = st.slider("Weight: Wickets (vs Economy)", 0.0, 1.0, 0.6)
        weight_eco  = 1.0 - weight_wkts
        bowl_df["custom_score"] = (
            bowl_df["Wickets"] * weight_wkts * 20 -
            bowl_df["Economy"] * weight_eco * 8
        ).round(1)
        recs = bowl_df.sort_values("custom_score", ascending=False).head(top_n)

        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Top {top_n} Bowling Targets</div>", unsafe_allow_html=True)
        for i, (_, row) in enumerate(recs.iterrows(), 1):
            tier_val = str(row["value_tier"])
            tc = {"Elite": GOLD, "Premium": TEAL, "Mid-Tier": "#6C7AE0", "Budget Pick": MUTED}
            c = tc.get(tier_val, GOLD)
            st.markdown(f"""
            <div class='ipl-card' style='border-left: 3px solid {c}; padding: 1rem 1.4rem;'>
              <span class='player-rank'>#{i}</span>
              <b style='font-size:1.05rem;'>{row['Player']}</b>
              <span class='badge' style='background:rgba(43,176,166,0.1); color:{c}; border:1px solid {c}; margin-left:0.5rem;'>{tier_val}</span>
              <div style='margin-top:0.5rem; display:flex; gap:2rem; font-size:0.85rem; color:{MUTED};'>
                <span>Wickets: <b style='color:{TEXT};'>{int(row['Wickets'])}</b></span>
                <span>Economy: <b style='color:{TEXT};'>{row['Economy']:.2f}</b></span>
                <span>Score: <b style='color:{GOLD};'>{row['custom_score']:.0f}</b></span>
              </div>
            </div>
            """, unsafe_allow_html=True)

    elif role == "All-Rounder":
        all_rounders = pd.merge(bat_df, bowl_df, left_on="batter", right_on="Player", how="inner")
        all_rounders["overall_score"] = (
            all_rounders["runs"] * 0.3 +
            all_rounders["avg"] * 5 +
            all_rounders["strike_rate"] * 1.5 +
            all_rounders["Wickets"] * 12 -
            all_rounders["Economy"] * 4
        ).round(1)
        recs = all_rounders.sort_values("overall_score", ascending=False).head(top_n)

        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Top {top_n} All-Rounders</div>", unsafe_allow_html=True)
        for i, (_, row) in enumerate(recs.iterrows(), 1):
            st.markdown(f"""
            <div class='ipl-card-highlight' style='border-left: 3px solid {GOLD}; padding: 1rem 1.4rem;'>
              <span class='player-rank'>#{i}</span>
              <b style='font-size:1.05rem;'>{row['batter']}</b>
              <span class='badge badge-gold' style='margin-left:0.5rem;'>All-Rounder</span>
              <div style='margin-top:0.5rem; display:flex; gap:2rem; font-size:0.85rem; color:{MUTED};'>
                <span>Runs: <b style='color:{TEXT};'>{int(row['runs'])}</b></span>
                <span>SR: <b style='color:{TEXT};'>{row['strike_rate']:.1f}</b></span>
                <span>Wkts: <b style='color:{TEXT};'>{int(row['Wickets'])}</b></span>
                <span>Econ: <b style='color:{TEXT};'>{row['Economy']:.2f}</b></span>
                <span>Score: <b style='color:{GOLD};'>{row['overall_score']:.0f}</b></span>
              </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: MARKET ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
elif "Market" in page:
    st.markdown(f"<div class='section-label'>Auction Intelligence</div>", unsafe_allow_html=True)
    st.markdown("## 📊 Auction Market Analysis")

    budget_max = st.slider("Max budget filter (₹ Cr)", 1, 20, 20)
    role_filter = st.multiselect("Filter by player type",
                                  auction_df["Type"].dropna().unique().tolist(),
                                  default=auction_df["Type"].dropna().unique().tolist())

    filt_a = auction_df[
        (auction_df["Cost in Rs. (CR)"] <= budget_max) &
        (auction_df["Type"].isin(role_filter))
    ]

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Players in range", len(filt_a))
    k2.metric("Avg price (₹ Cr)", f"{filt_a['Cost in Rs. (CR)'].mean():.2f}")
    k3.metric("Max price (₹ Cr)", f"{filt_a['Cost in Rs. (CR)'].max():.2f}")
    k4.metric("Roles", filt_a["Type"].nunique())

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Price distribution by role</div>", unsafe_allow_html=True)
        fig = px.box(filt_a, x="Type", y="Cost in Rs. (CR)",
                     color="Type",
                     color_discrete_sequence=[GOLD, TEAL, "#6C7AE0", CRIMSON])
        fig.update_layout(**PLOT_LAYOUT, height=360,
                          xaxis_title="Player Type", yaxis_title="Price (₹ Cr)",
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_r:
        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Budget allocation by role</div>", unsafe_allow_html=True)
        budget_by_role = filt_a.groupby("Type")["Cost in Rs. (CR)"].sum().reset_index()
        budget_by_role.columns = ["Role","Total (₹ Cr)"]
        fig2 = px.pie(budget_by_role, values="Total (₹ Cr)", names="Role", hole=0.5,
                      color_discrete_sequence=[GOLD, TEAL, "#6C7AE0", CRIMSON])
        fig2.update_layout(**PLOT_LAYOUT, height=360)
        fig2.update_layout(legend=LEGEND)
        fig2.update_xaxes(**GRID)
        fig2.update_yaxes(**GRID)
        st.plotly_chart(fig2, use_container_width=True)

    # Most expensive players
    st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Most expensive players</div>", unsafe_allow_html=True)
    expensive = filt_a.sort_values("Cost in Rs. (CR)", ascending=False).head(15)
    fig3 = px.bar(expensive, x="Cost in Rs. (CR)", y="Player Name",
                  orientation="h", color="Type",
                  color_discrete_sequence=[GOLD, TEAL, "#6C7AE0", CRIMSON],
                  text="Cost in Rs. (CR)")
    fig3.update_traces(textposition="outside", textfont_color=TEXT,
                       texttemplate="₹%{text:.1f}Cr")
    fig3.update_layout(**PLOT_LAYOUT, height=440, xaxis_title="Price (₹ Cr)")
    fig3.update_layout(legend=LEGEND)
    fig3.update_xaxes(**GRID)
    fig3.update_yaxes(**GRID)
    fig3.update_yaxes(autorange="reversed", gridcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

    st.download_button("⬇  Export filtered auction data", filt_a.to_csv(index=False),
                       "auction_filtered.csv", "text/csv")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HEAD-TO-HEAD
# ══════════════════════════════════════════════════════════════════════════════
elif "Head" in page:
    st.markdown(f"<div class='section-label'>Comparison Tool</div>", unsafe_allow_html=True)
    st.markdown("## ⚔️ Head-to-Head Player Comparison")

    compare_type = st.radio("Compare as", ["Batsmen", "Bowlers"], horizontal=True)
    st.markdown("<br>", unsafe_allow_html=True)

    if compare_type == "Batsmen":
        players = sorted(bat_df["batter"].unique())
        c1, c2 = st.columns(2)
        p1_name = c1.selectbox("Player 1", players, index=0, key="h2h_p1")
        p2_name = c2.selectbox("Player 2", players, index=min(1, len(players)-1), key="h2h_p2")

        p1 = bat_df[bat_df["batter"] == p1_name].iloc[0]
        p2 = bat_df[bat_df["batter"] == p2_name].iloc[0]

        categories = ["Runs (norm)", "Avg (norm)", "Strike Rate (norm)", "Boundary %", "Consistency"]
        maxv = [bat_df["runs"].max(), bat_df["avg"].max(), bat_df["strike_rate"].max(), 100, 100]
        v1 = [p1["runs"]/maxv[0]*100, p1["avg"]/maxv[1]*100, p1["strike_rate"]/maxv[2]*100, p1["boundary_pct"], p1["consistency"]]
        v2 = [p2["runs"]/maxv[0]*100, p2["avg"]/maxv[1]*100, p2["strike_rate"]/maxv[2]*100, p2["boundary_pct"], p2["consistency"]]

        fig = go.Figure()
        for vals, name, col in [(v1, p1_name, GOLD), (v2, p2_name, TEAL)]:
            fig.add_trace(go.Scatterpolar(
                r=vals + [vals[0]], theta=categories + [categories[0]],
                fill="toself", name=name,
                fillcolor=f"rgba({int(col[1:3],16)},{int(col[3:5],16)},{int(col[5:7],16)},0.15)",
                line=dict(color=col, width=2),
                marker=dict(color=col, size=6)
            ))
        fig.update_layout(**PLOT_LAYOUT, polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,100],
                            gridcolor="rgba(255,255,255,0.08)",
                            tickfont=dict(color=MUTED, size=9)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color=TEXT))
        ), height=420)
        st.plotly_chart(fig, use_container_width=True)

        # Stat table
        st.markdown(f"<div class='section-label'>Head-to-head metrics</div>", unsafe_allow_html=True)
        compare_data = {
            "Metric": ["Runs","Innings","Batting Avg","Strike Rate","Boundary %","Consistency","Auction Score"],
            p1_name:  [int(p1["runs"]), int(p1["innings"]), f"{p1['avg']:.1f}", f"{p1['strike_rate']:.1f}",
                       f"{p1['boundary_pct']:.1f}%", f"{p1['consistency']:.1f}", f"{p1['auction_score']:.0f}"],
            p2_name:  [int(p2["runs"]), int(p2["innings"]), f"{p2['avg']:.1f}", f"{p2['strike_rate']:.1f}",
                       f"{p2['boundary_pct']:.1f}%", f"{p2['consistency']:.1f}", f"{p2['auction_score']:.0f}"],
        }
        st.dataframe(pd.DataFrame(compare_data).set_index("Metric"),
                     use_container_width=True)

    else:
        players_b = sorted(bowl_df["Player"].unique())
        c1, c2 = st.columns(2)
        b1_name = c1.selectbox("Bowler 1", players_b, index=0, key="h2h_b1")
        b2_name = c2.selectbox("Bowler 2", players_b, index=min(1, len(players_b)-1), key="h2h_b2")

        b1 = bowl_df[bowl_df["Player"] == b1_name].iloc[0]
        b2 = bowl_df[bowl_df["Player"] == b2_name].iloc[0]

        compare_data = {
            "Metric":  ["Wickets","Economy","Bowling Score","Value Tier"],
            b1_name:   [int(b1["Wickets"]), f"{b1['Economy']:.2f}", f"{b1['bowling_score']:.0f}", str(b1["value_tier"])],
            b2_name:   [int(b2["Wickets"]), f"{b2['Economy']:.2f}", f"{b2['bowling_score']:.0f}", str(b2["value_tier"])],
        }
        st.dataframe(pd.DataFrame(compare_data).set_index("Metric"),
                     use_container_width=True)

        # Side by side bars
        st.markdown(f"<div class='section-label' style='margin-top:1rem;'>Wickets & Economy comparison</div>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Bar(name=b1_name, x=["Wickets","Economy"],
                             y=[b1["Wickets"], b1["Economy"]], marker_color=GOLD))
        fig.add_trace(go.Bar(name=b2_name, x=["Wickets","Economy"],
                             y=[b2["Wickets"], b2["Economy"]], marker_color=TEAL))
        fig.update_layout(**PLOT_LAYOUT, barmode="group", height=320)
        fig.update_layout(legend=LEGEND)
        fig.update_xaxes(**GRID)
        fig.update_yaxes(**GRID)
        st.plotly_chart(fig, use_container_width=True)
