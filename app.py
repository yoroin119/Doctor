import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Nash · Doctor Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── CSS — CLEAN WHITE PROFESSIONAL THEME ─────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, * { font-family: 'Space Grotesk', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1rem 2rem 2rem 2rem; }
.stApp { background: #FFFFFF !important; }
.stApp > div { background: #FFFFFF !important; }

:root {
    --teal:      #0A7B74;
    --teal-dk:   #065E59;
    --teal-lt:   #ECFDF8;
    --teal-bdr:  #6EE7B7;
    --accent:    #2563EB;
    --accent-lt: #EFF6FF;
    --accent-bdr:#BFDBFE;
    --red:       #DC2626;
    --red-lt:    #FEF2F2;
    --red-bdr:   #FECACA;
    --green:     #16A34A;
    --green-lt:  #F0FDF4;
    --green-bdr: #BBF7D0;
    --orange:    #EA580C;
    --orange-lt: #FFF7ED;
    --orange-bdr:#FED7AA;
    --gold:      #B45309;
    --gold-lt:   #FFFBEB;
    --gold-bdr:  #FDE68A;
    --text:      #111827;
    --text-sec:  #6B7280;
    --border:    #E5E7EB;
    --border2:   #D1D5DB;
    --surface:   #F9FAFB;
}

/* NAVBAR */
.doc-nav {
    background: linear-gradient(135deg, #0F172A 0%, #0A7B74 100%);
    border-radius: 16px; padding: 1.1rem 1.8rem; margin-bottom: 1.5rem;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 4px 20px rgba(10,123,116,0.18);
}
.doc-logo      { font-size:1.8rem; font-weight:700; color:#FFFFFF; letter-spacing:-0.5px; }
.doc-logo span { color:rgba(255,255,255,0.6); font-weight:400; }
.doc-sub       { font-size:0.7rem; color:rgba(255,255,255,0.5); letter-spacing:2px; text-transform:uppercase; margin-top:0.1rem; }
.nav-right     { display:flex; align-items:center; gap:0.8rem; }
.doc-badge     { background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.3);
                 color:white; padding:0.3rem 0.9rem; border-radius:20px; font-size:0.75rem; font-weight:600; }
.nav-date      { font-size:0.72rem; color:rgba(255,255,255,0.5); }

/* STAT CARDS */
.stat-card {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-radius:14px; padding:1.1rem 1.2rem;
    position:relative; overflow:hidden;
    box-shadow:0 1px 6px rgba(0,0,0,0.05);
}
.stat-card::after {
    content:''; position:absolute; bottom:0; left:0; right:0;
    height:3px; border-radius:0 0 14px 14px;
}
.stat-card.c-teal::after   { background:var(--teal);   }
.stat-card.c-red::after    { background:var(--red);    }
.stat-card.c-blue::after   { background:var(--accent); }
.stat-card.c-green::after  { background:var(--green);  }
.stat-icon { font-size:1.5rem; margin-bottom:0.4rem; }
.stat-val  { font-family:'JetBrains Mono',monospace; font-size:2.2rem; font-weight:700; color:var(--text); line-height:1; }
.stat-lbl  { font-size:0.68rem; color:var(--text-sec); margin-top:0.3rem; font-weight:600; text-transform:uppercase; letter-spacing:1px; }

/* SECTION HEADER */
.sec-hd {
    font-size:0.78rem; font-weight:700; color:var(--teal);
    text-transform:uppercase; letter-spacing:2px;
    margin:1.3rem 0 0.75rem 0;
    display:flex; align-items:center; gap:0.6rem;
}
.sec-line { flex:1; height:1px; background:var(--border); }

/* QUEUE ROW */
.q-row {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-radius:12px; padding:0.75rem 1rem; margin-bottom:0.4rem;
}
.q-row:hover { border-color:var(--teal); background:var(--teal-lt); }
.q-name { font-weight:600; color:var(--text); font-size:0.9rem; }
.q-meta { font-size:0.72rem; color:var(--text-sec); margin-top:0.12rem; }

/* VITAL MINI CARD */
.mv-card {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-radius:12px; padding:0.8rem 1rem; margin-bottom:0.5rem;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}
.mv-label { font-size:0.63rem; color:var(--text-sec); text-transform:uppercase; letter-spacing:1.2px; font-weight:700; }
.mv-val   { font-family:'JetBrains Mono',monospace; font-size:1.5rem; font-weight:700; line-height:1.2; }
.mv-unit  { font-size:0.72rem; color:var(--text-sec); font-weight:400; }

/* PILLS */
.pill     { display:inline-block; padding:0.18rem 0.65rem; border-radius:20px; font-size:0.68rem; font-weight:600; margin:0.1rem; }
.p-teal   { background:var(--teal-lt);   border:1px solid var(--teal-bdr);   color:var(--teal);   }
.p-red    { background:var(--red-lt);    border:1px solid var(--red-bdr);    color:var(--red);    }
.p-green  { background:var(--green-lt);  border:1px solid var(--green-bdr);  color:var(--green);  }
.p-orange { background:var(--orange-lt); border:1px solid var(--orange-bdr); color:var(--orange); }
.p-blue   { background:var(--accent-lt); border:1px solid var(--accent-bdr); color:var(--accent); }
.p-gold   { background:var(--gold-lt);   border:1px solid var(--gold-bdr);   color:var(--gold);   }

/* ALERT CARD */
.alert-card {
    background:var(--red-lt); border:1.5px solid var(--red-bdr);
    border-left:4px solid var(--red); border-radius:12px;
    padding:0.85rem 1rem; margin-bottom:0.5rem;
}
.alert-title  { font-weight:700; color:var(--red);      font-size:0.87rem; }
.alert-detail { font-size:0.75rem; color:var(--text-sec); margin-top:0.15rem; }
.alert-time   { font-size:0.67rem; color:var(--text-sec); margin-top:0.3rem;  }

/* VISIT CARD */
.visit-card {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-left:4px solid var(--teal); border-radius:12px;
    padding:0.85rem 1rem; margin-bottom:0.5rem;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}
.visit-num  { font-family:'JetBrains Mono',monospace; color:var(--teal); font-weight:700; font-size:0.78rem; }
.visit-date { font-size:0.72rem; color:var(--text-sec); }
.visit-note { font-size:0.78rem; color:var(--text); margin-top:0.3rem; line-height:1.4; }

/* PRESCRIPTION ROW */
.rx-row {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-radius:12px; padding:0.8rem 1rem; margin-bottom:0.5rem;
    display:flex; justify-content:space-between; align-items:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}
.rx-name   { font-weight:700; color:var(--text); font-size:0.9rem; }
.rx-detail { font-size:0.72rem; color:var(--text-sec); margin-top:0.15rem; }

/* REPORT ROW */
.report-row {
    background:#FFFFFF; border:1.5px solid var(--border);
    border-radius:12px; padding:0.85rem 1.1rem; margin-bottom:0.5rem;
    display:flex; justify-content:space-between; align-items:center;
    box-shadow:0 1px 4px rgba(0,0,0,0.04);
}

/* FORM LABEL */
.form-lbl {
    font-size:0.72rem; color:var(--teal); font-weight:700;
    text-transform:uppercase; letter-spacing:1px; margin-bottom:0.3rem;
}

/* LIVE BADGE */
.live-badge {
    display:inline-flex; align-items:center; gap:0.4rem;
    background:var(--green-lt); border:1px solid var(--green-bdr);
    color:var(--green); padding:0.28rem 0.75rem;
    border-radius:20px; font-size:0.7rem; font-weight:700; letter-spacing:0.8px;
}
.pulse-dot {
    width:7px; height:7px; background:var(--green);
    border-radius:50%; display:inline-block; animation:blink 1.4s infinite;
}
@keyframes blink{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.4;transform:scale(1.5)}}

/* DIVIDER */
.divider { height:1px; background:var(--border); margin:1rem 0; }

/* PAT HEADER */
.pat-header {
    background:#FFFFFF; border:1.5px solid var(--border); border-radius:16px;
    padding:1.2rem 1.5rem; margin-bottom:1rem;
    display:flex; align-items:center; gap:1.2rem;
    box-shadow:0 2px 8px rgba(0,0,0,0.05);
}
.pat-avatar {
    width:56px; height:56px; border-radius:50%;
    background:linear-gradient(135deg,#0A7B74,#065E59);
    display:flex; align-items:center; justify-content:center;
    font-size:1.5rem; flex-shrink:0;
}

/* PROGRESS SUMMARY */
.prog-summary {
    background:var(--green-lt); border:1.5px solid var(--green-bdr);
    border-left:4px solid var(--green); border-radius:12px;
    padding:0.9rem 1.1rem; margin-top:0.8rem;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap:4px; background:#F3F4F6; border-radius:12px;
    padding:4px; border:1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius:9px; padding:0.42rem 1rem;
    font-weight:600; font-size:0.83rem; color:var(--text-sec);
}
.stTabs [aria-selected="true"] { background:var(--teal) !important; color:white !important; }

/* INPUTS */
.stTextArea textarea, .stTextInput input {
    background:#FFFFFF !important; border:1.5px solid var(--border2) !important;
    color:var(--text) !important; border-radius:10px !important;
}
.stTextArea label, .stTextInput label, .stSelectbox label, .stDateInput label {
    color:var(--text-sec) !important; font-size:0.78rem !important; font-weight:600 !important;
}

/* BUTTONS */
.stButton>button {
    background:linear-gradient(135deg,var(--teal-dk),var(--teal)) !important;
    color:white !important; border:none !important; border-radius:10px !important;
    font-weight:700 !important; font-family:'Space Grotesk',sans-serif !important;
}

/* SCHEDULE ROW */
.sched-row {
    display:flex; align-items:center; gap:0.8rem;
    padding:0.5rem 0; border-bottom:1px solid var(--border);
}
.sched-time { font-family:'JetBrains Mono',monospace; color:var(--teal); font-size:0.82rem; font-weight:600; width:50px; }
</style>
""", unsafe_allow_html=True)

# ─── HELPERS ───────────────────────────────────────────────────────────────────
def hex_to_rgba(h, a=0.12):
    """Safely convert hex color to rgba string for Plotly fillcolor."""
    h = h.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{a})'

def make_chart(df, ycol, color, title, hlines=[], yrange=None):
    """Create a clean white-background Plotly line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['datetime'], y=df[ycol],
        mode='lines+markers',
        line=dict(color=color, width=2.5),
        marker=dict(size=5, color=color),
        fill='tozeroy',
        fillcolor=hex_to_rgba(color, 0.10)
    ))
    for val, lbl, lc in hlines:
        fig.add_hline(y=val, line_dash="dot", line_color=lc,
            annotation_text=lbl, annotation_font_size=9, annotation_font_color=lc)
    fig.update_layout(
        title=dict(text=title, font=dict(family='Space Grotesk', size=12, color='#374151')),
        height=215, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        margin=dict(l=10, r=10, t=38, b=10),
        font=dict(family='Space Grotesk', color='#6B7280', size=10),
        showlegend=False,
        xaxis=dict(showgrid=False, color='#E5E7EB'),
        yaxis=dict(gridcolor='#F3F4F6', color='#6B7280',
                   range=yrange if yrange else None)
    )
    return fig

def make_dual_chart(df, col1, col2, c1, c2, title, hlines=[]):
    """Create a dual-line white-background chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['datetime'], y=df[col1], mode='lines+markers',
        name='Systolic', line=dict(color=c1, width=2.5), marker=dict(size=5)))
    fig.add_trace(go.Scatter(x=df['datetime'], y=df[col2], mode='lines+markers',
        name='Diastolic', line=dict(color=c2, width=2.5), marker=dict(size=5)))
    for val, lbl, lc in hlines:
        fig.add_hline(y=val, line_dash="dot", line_color=lc,
            annotation_text=lbl, annotation_font_size=9, annotation_font_color=lc)
    fig.update_layout(
        title=dict(text=title, font=dict(family='Space Grotesk', size=12, color='#374151')),
        height=215, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        margin=dict(l=10, r=10, t=38, b=10),
        font=dict(family='Space Grotesk', color='#6B7280', size=10),
        xaxis=dict(showgrid=False), yaxis=dict(gridcolor='#F3F4F6'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(size=10))
    )
    return fig

# ─── MOCK DATA ─────────────────────────────────────────────────────────────────
def gen_vitals(days=14, seed=1):
    random.seed(seed)
    dates = [datetime.now() - timedelta(days=i, hours=random.randint(0, 8)) for i in range(days)]
    dates.reverse()
    return pd.DataFrame({
        "datetime":    dates,
        "temperature": [round(random.uniform(36.2, 38.5), 1) for _ in range(days)],
        "heart_rate":  [random.randint(62, 112)              for _ in range(days)],
        "spo2":        [random.randint(93, 100)               for _ in range(days)],
        "bp_sys":      [random.randint(112, 148)              for _ in range(days)],
        "bp_dia":      [random.randint(72, 94)                for _ in range(days)],
    })

QUEUE = [
    {"name": "Rahul Verma",   "age": 45, "id": "P-1042", "time": "09:00", "flag": "BP High",  "status": "Waiting",         "ward": "3B", "bed": "12"},
    {"name": "Meena Das",     "age": 62, "id": "P-1043", "time": "09:30", "flag": "Normal",    "status": "In Consultation", "ward": "4A", "bed": "7"},
    {"name": "Suresh Kumar",  "age": 38, "id": "P-1044", "time": "10:00", "flag": "SpO₂ Low",  "status": "Waiting",         "ward": "2C", "bed": "3"},
    {"name": "Lakshmi Patel", "age": 55, "id": "P-1045", "time": "10:30", "flag": "Normal",    "status": "Pending",         "ward": "3B", "bed": "15"},
    {"name": "Anil Joshi",    "age": 70, "id": "P-1046", "time": "11:00", "flag": "HR Alert",  "status": "Pending",         "ward": "5D", "bed": "9"},
]
ALERTS = [
    {"patient": "Suresh Kumar", "id": "P-1044", "msg": "SpO₂ dropped to 91% — immediate attention required", "time": "2 min ago"},
    {"patient": "Anil Joshi",   "id": "P-1046", "msg": "Heart rate irregular — 118 bpm recorded by Nash",    "time": "8 min ago"},
]
FLAG_PILL  = {"Normal": "p-green", "BP High": "p-red", "SpO₂ Low": "p-red", "HR Alert": "p-orange"}
STATUS_CSS = {"Waiting": "color:#EA580C", "In Consultation": "color:#0A7B74", "Pending": "color:#6B7280"}

# ─── NAVBAR ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="doc-nav">
  <div>
    <div class="doc-logo">🏥 Nash<span> · Doctor Portal</span></div>
    <div class="doc-sub">Clinical Management System</div>
  </div>
  <div class="nav-right">
    <div class="live-badge"><span class="pulse-dot"></span> NASH ONLINE</div>
    <div class="doc-badge">👨‍⚕️ Dr. Priya Sharma · Cardiologist</div>
    <div class="nav-date">{datetime.now().strftime('%a, %d %b %Y')}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Dashboard", "👥 Patients", "📋 Medical Reports", "💊 Prescriptions", "📈 Progress"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    sc1, sc2, sc3, sc4 = st.columns(4)
    for col, (val, lbl, icon, cls) in zip(
        [sc1, sc2, sc3, sc4],
        [("5",  "Today's Patients",  "👥", "c-teal"),
         ("2",  "Active Alerts",     "🚨", "c-red"),
         ("1",  "In Consultation",   "🩺", "c-blue"),
         ("12", "This Week",         "📊", "c-green")]
    ):
        col.markdown(f"""
        <div class="stat-card {cls}">
          <div class="stat-icon">{icon}</div>
          <div class="stat-val">{val}</div>
          <div class="stat-lbl">{lbl}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    d_left, d_right = st.columns([1.3, 1])

    with d_left:
        st.markdown('<div class="sec-hd">🚨 Active Alerts <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for a in ALERTS:
            st.markdown(f"""
            <div class="alert-card">
              <div class="alert-title">⚠️ {a['patient']} · {a['id']}</div>
              <div class="alert-detail">{a['msg']}</div>
              <div class="alert-time">🕐 {a['time']}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hd">🗂️ Today\'s Queue <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for p in QUEUE:
            pc = FLAG_PILL.get(p['flag'], 'p-green')
            sc = STATUS_CSS.get(p['status'], 'color:#6B7280')
            st.markdown(f"""
            <div class="q-row">
              <div style="display:flex;justify-content:space-between;align-items:center;">
                <div>
                  <div class="q-name">{p['name']}</div>
                  <div class="q-meta">⏰ {p['time']} · Age {p['age']} · {p['id']} · Ward {p['ward']} Bed {p['bed']}</div>
                </div>
                <div style="text-align:right;">
                  <span class="pill {pc}">{p['flag']}</span><br/>
                  <span style="font-size:0.7rem;font-weight:700;{sc}">{p['status']}</span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    with d_right:
        st.markdown('<div class="sec-hd">📡 Nash Live Feed <div class="sec-line"></div></div>', unsafe_allow_html=True)
        vdf_live = gen_vitals()
        fig_live = go.Figure()
        fig_live.add_trace(go.Scatter(x=vdf_live['datetime'][-7:], y=vdf_live['bp_sys'][-7:],
            mode='lines+markers', name='BP Sys',
            line=dict(color='#DC2626', width=2), marker=dict(size=5)))
        fig_live.add_trace(go.Scatter(x=vdf_live['datetime'][-7:], y=vdf_live['heart_rate'][-7:],
            mode='lines+markers', name='Heart Rate',
            line=dict(color='#0A7B74', width=2), marker=dict(size=5)))
        fig_live.update_layout(
            height=240, plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family='Space Grotesk', color='#6B7280', size=10),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(gridcolor='#F3F4F6'),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, font=dict(size=10))
        )
        st.plotly_chart(fig_live, use_container_width=True)

        st.markdown('<div class="sec-hd">📅 My Schedule Today <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for p in QUEUE:
            pc = FLAG_PILL.get(p['flag'], 'p-green')
            st.markdown(f"""
            <div class="sched-row">
              <div class="sched-time">{p['time']}</div>
              <div style="flex:1;">
                <div style="font-weight:600;color:#111827;font-size:0.85rem;">{p['name']}</div>
                <div style="font-size:0.68rem;color:#6B7280;">{p['id']}</div>
              </div>
              <span class="pill {pc}" style="font-size:0.62rem;">{p['flag']}</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — PATIENTS
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    sel = st.selectbox("Select Patient:",
        [f"{p['time']} · {p['name']} ({p['id']})" for p in QUEUE],
        label_visibility="collapsed")
    idx  = [f"{p['time']} · {p['name']} ({p['id']})" for p in QUEUE].index(sel)
    sp   = QUEUE[idx]
    vdf  = gen_vitals(seed=idx * 7 + 2)
    lat  = vdf.iloc[-1]

    st.markdown(f"""
    <div class="pat-header">
      <div class="pat-avatar">👤</div>
      <div style="flex:1;">
        <div style="font-size:1.15rem;font-weight:700;color:#111827;">{sp['name']}</div>
        <div style="font-size:0.78rem;color:#6B7280;margin-top:0.15rem;">
          Age {sp['age']} · {sp['id']} · Ward {sp['ward']} · Bed {sp['bed']}
        </div>
        <div style="margin-top:0.45rem;">
          <span class="pill p-teal">Hypertension</span>
          <span class="pill p-orange">No Known Allergies</span>
          <span class="pill p-blue">Blood Group O+</span>
        </div>
      </div>
      <div style="text-align:right;">
        <div class="live-badge"><span class="pulse-dot"></span> Nash Active</div>
        <div style="font-size:0.7rem;color:#6B7280;margin-top:0.4rem;">Last scan: 3 min ago</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hd">📡 Current Vitals <div class="sec-line"></div></div>', unsafe_allow_html=True)
    vc1, vc2, vc3, vc4, vc5 = st.columns(5)
    for col, icon, lbl, val, unit, color in [
        (vc1, "🌡️", "Temperature",   f"{lat['temperature']}",                      "°C",    "#EA580C"),
        (vc2, "💓", "Heart Rate",     f"{int(lat['heart_rate'])}",                  "bpm",   "#DC2626"),
        (vc3, "🫁", "SpO₂",           f"{int(lat['spo2'])}",                        "%",     "#0A7B74"),
        (vc4, "🩺", "Blood Pressure", f"{int(lat['bp_sys'])}/{int(lat['bp_dia'])}", "mmHg",  "#2563EB"),
        (vc5, "📈", "ECG",            "Sinus",                                      "Normal","#B45309"),
    ]:
        col.markdown(f"""
        <div class="mv-card" style="border-left:3px solid {color};">
          <div class="mv-label">{icon} {lbl}</div>
          <div class="mv-val" style="color:{color};">{val} <span class="mv-unit">{unit}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sec-hd">📊 14-Day Vitals Trend <div class="sec-line"></div></div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(make_dual_chart(vdf, 'bp_sys', 'bp_dia', '#DC2626', '#2563EB',
            '🩺 Blood Pressure (mmHg)', hlines=[(120, 'Target', '#B45309')]),
            use_container_width=True)
    with ch2:
        st.plotly_chart(make_chart(vdf, 'heart_rate', '#DC2626', '💓 Heart Rate (bpm)',
            hlines=[(100, 'Max', '#EA580C'), (60, 'Min', '#16A34A')]),
            use_container_width=True)

    ch3, ch4 = st.columns(2)
    with ch3:
        st.plotly_chart(make_chart(vdf, 'spo2', '#0A7B74', '🫁 SpO₂ (%)',
            hlines=[(95, 'Min Normal', '#EA580C')], yrange=[88, 102]),
            use_container_width=True)
    with ch4:
        st.plotly_chart(make_chart(vdf, 'temperature', '#B45309', '🌡️ Temperature (°C)',
            hlines=[(37.2, 'Fever', '#DC2626')]),
            use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — MEDICAL REPORTS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    rl, rr = st.columns([1.3, 1])

    with rl:
        st.markdown('<div class="sec-hd">📋 Write Medical Report <div class="sec-line"></div></div>', unsafe_allow_html=True)
        st.selectbox("Patient:", [f"{p['name']} ({p['id']})" for p in QUEUE], key="rp")

        st.markdown('<div class="form-lbl">Chief Complaint</div>', unsafe_allow_html=True)
        st.text_area("", "Patient presents with chest tightness and exertional dyspnea for 3 days. Associated with mild headache.", height=75, key="cc", label_visibility="collapsed")

        rd1, rd2 = st.columns(2)
        with rd1:
            st.markdown('<div class="form-lbl">Diagnosis</div>', unsafe_allow_html=True)
            st.text_input("", "Hypertension Stage 1", key="dg", label_visibility="collapsed")
        with rd2:
            st.markdown('<div class="form-lbl">Investigations</div>', unsafe_allow_html=True)
            st.text_input("", "ECG, Lipid Profile, Echo", key="iv", label_visibility="collapsed")

        st.markdown('<div class="form-lbl">Clinical Examination Notes</div>', unsafe_allow_html=True)
        st.text_area("", "BP 142/92 mmHg on both arms. Heart sounds S1 S2 normal. No murmurs. Lungs clear on auscultation. No pedal oedema.", height=80, key="ex", label_visibility="collapsed")

        st.markdown('<div class="form-lbl">Treatment Plan</div>', unsafe_allow_html=True)
        st.text_area("", "Start Amlodipine 5mg OD. Low-sodium diet advised. Daily BP self-monitoring. Review in 2 weeks.", height=65, key="tp", label_visibility="collapsed")

        rb1, rb2 = st.columns(2)
        with rb1:
            if st.button("💾 Save Report", use_container_width=True, key="svr"):
                st.success("✅ Report saved & shared with patient!")
        with rb2:
            if st.button("📄 Export PDF", use_container_width=True, key="epdf"):
                st.info("📄 Generating PDF report...")

        st.markdown('<div class="sec-hd" style="margin-top:1rem;">📡 Vitals at This Visit <div class="sec-line"></div></div>', unsafe_allow_html=True)
        vdf2 = gen_vitals(); lat2 = vdf2.iloc[-1]
        vv1, vv2 = st.columns(2)
        for i, (icon, lbl, val, color) in enumerate([
            ("🌡️", "Temp",         f"{lat2['temperature']}°C",                        "#EA580C"),
            ("💓", "Heart Rate",   f"{int(lat2['heart_rate'])} bpm",                  "#DC2626"),
            ("🫁", "SpO₂",         f"{int(lat2['spo2'])}%",                            "#0A7B74"),
            ("🩺", "Blood Pressure",f"{int(lat2['bp_sys'])}/{int(lat2['bp_dia'])} mmHg","#2563EB"),
        ]):
            (vv1 if i % 2 == 0 else vv2).markdown(f"""
            <div class="mv-card" style="border-left:3px solid {color};margin-bottom:0.4rem;">
              <div class="mv-label">{icon} {lbl}</div>
              <div style="font-family:'JetBrains Mono',monospace;font-size:1.1rem;font-weight:700;color:{color};">{val}</div>
            </div>""", unsafe_allow_html=True)

    with rr:
        st.markdown('<div class="sec-hd">🗂️ Past Reports <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for r in [
            {"date": "1 May 2025",  "pat": "Rahul Verma",    "diag": "Hypertension Stage 1",   "type": "Follow-up"},
            {"date": "24 Apr 2025", "pat": "Rahul Verma",    "diag": "Initial BP Assessment",   "type": "First Visit"},
            {"date": "20 Apr 2025", "pat": "Meena Das",      "diag": "Type 2 Diabetes Review",  "type": "Follow-up"},
            {"date": "15 Apr 2025", "pat": "Suresh Kumar",   "diag": "Respiratory Infection",   "type": "Acute"},
            {"date": "10 Apr 2025", "pat": "Lakshmi Patel",  "diag": "Routine Cardiac Check",   "type": "Routine"},
        ]:
            st.markdown(f"""
            <div class="report-row">
              <div>
                <div style="font-weight:700;color:#111827;font-size:0.88rem;">{r['pat']}</div>
                <div style="font-size:0.75rem;color:#0A7B74;margin:0.15rem 0;">{r['diag']}</div>
                <div style="font-size:0.7rem;color:#6B7280;">📅 {r['date']}</div>
              </div>
              <div style="text-align:right;">
                <span class="pill p-blue">{r['type']}</span>
                <div style="font-size:0.68rem;color:#0A7B74;margin-top:0.35rem;cursor:pointer;">View →</div>
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PRESCRIPTIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    pl, pr = st.columns([1.3, 1])

    with pl:
        st.markdown('<div class="sec-hd">💊 Write Prescription <div class="sec-line"></div></div>', unsafe_allow_html=True)
        st.selectbox("Patient:", [f"{p['name']} ({p['id']})" for p in QUEUE], key="pp")

        st.markdown('<div class="form-lbl">Medicine Name</div>', unsafe_allow_html=True)
        med = st.text_input("", "Amlodipine 5mg", key="mn", label_visibility="collapsed")

        pc1, pc2, pc3 = st.columns(3)
        with pc1:
            st.markdown('<div class="form-lbl">Dosage</div>', unsafe_allow_html=True)
            dos = st.text_input("", "5mg", key="ds", label_visibility="collapsed")
        with pc2:
            st.markdown('<div class="form-lbl">Frequency</div>', unsafe_allow_html=True)
            frq = st.selectbox("", ["Once daily","Twice daily","Thrice daily","SOS","Weekly"], key="fr", label_visibility="collapsed")
        with pc3:
            st.markdown('<div class="form-lbl">Duration</div>', unsafe_allow_html=True)
            dur = st.text_input("", "30 days", key="du", label_visibility="collapsed")

        st.markdown('<div class="form-lbl">Special Instructions</div>', unsafe_allow_html=True)
        inst = st.text_input("", "Take after food. Avoid grapefruit. Monitor BP daily.", key="ins", label_visibility="collapsed")

        st.markdown(f"""
        <div style="background:#ECFDF8;border:1.5px dashed #0A7B74;border-radius:12px;
                    padding:0.9rem 1.1rem;margin:0.7rem 0;">
          <div style="font-size:0.65rem;color:#6B7280;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:0.4rem;font-weight:700;">Prescription Preview</div>
          <div style="font-weight:700;color:#111827;font-size:0.95rem;">💊 {med}</div>
          <div style="margin:0.35rem 0;">
            <span class="pill p-teal">{dos}</span>
            <span class="pill p-blue">{frq}</span>
            <span class="pill p-gold">{dur}</span>
          </div>
          <div style="font-size:0.73rem;color:#6B7280;">📌 {inst}</div>
        </div>""", unsafe_allow_html=True)

        pb1, pb2 = st.columns(2)
        with pb1:
            if st.button("➕ Add Medicine", use_container_width=True, key="am"):
                st.success("Medicine added to prescription!")
        with pb2:
            if st.button("📄 Generate & Share PDF", use_container_width=True, key="gp"):
                st.success("📄 Prescription shared with patient!")

    with pr:
        st.markdown('<div class="sec-hd">📜 Prescription History <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for rx in [
            {"pat": "Rahul Verma",   "med": "Amlodipine 5mg",    "frq": "Once daily",  "dur": "30 days", "date": "1 May 2025"},
            {"pat": "Meena Das",     "med": "Metformin 500mg",    "frq": "Twice daily", "dur": "90 days", "date": "20 Apr 2025"},
            {"pat": "Suresh Kumar",  "med": "Azithromycin 500mg", "frq": "Once daily",  "dur": "5 days",  "date": "15 Apr 2025"},
            {"pat": "Rahul Verma",   "med": "Atorvastatin 10mg",  "frq": "Once daily",  "dur": "60 days", "date": "10 Apr 2025"},
            {"pat": "Lakshmi Patel", "med": "Aspirin 75mg",       "frq": "Once daily",  "dur": "Ongoing", "date": "5 Apr 2025"},
        ]:
            st.markdown(f"""
            <div class="rx-row">
              <div>
                <div class="rx-name">💊 {rx['med']}</div>
                <div class="rx-detail">{rx['pat']} · {rx['date']}</div>
                <div style="margin-top:0.3rem;">
                  <span class="pill p-teal"  style="font-size:0.62rem;">{rx['frq']}</span>
                  <span class="pill p-blue"  style="font-size:0.62rem;">{rx['dur']}</span>
                </div>
              </div>
              <span style="color:#0A7B74;font-size:0.72rem;font-weight:600;cursor:pointer;">📄 View</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — PROGRESS TRACKER
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-hd">📈 Patient Progress Tracker <div class="sec-line"></div></div>', unsafe_allow_html=True)

    prog_sel = st.selectbox("Track Patient:",
        [f"{p['name']} ({p['id']})" for p in QUEUE], key="ps")
    pi   = [f"{p['name']} ({p['id']})" for p in QUEUE].index(prog_sel)
    pvdf = gen_vitals(seed=pi * 5 + 3)

    pg1, pg2 = st.columns(2)
    with pg1:
        st.plotly_chart(make_dual_chart(pvdf, 'bp_sys', 'bp_dia', '#DC2626', '#2563EB',
            '🩺 Blood Pressure Progress (mmHg)', hlines=[(120, 'Target Systolic', '#B45309')]),
            use_container_width=True)
    with pg2:
        st.plotly_chart(make_chart(pvdf, 'spo2', '#0A7B74', '🫁 SpO₂ Progress (%)',
            hlines=[(95, 'Min Normal', '#EA580C')], yrange=[88, 102]),
            use_container_width=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    tl, tr = st.columns([1, 1.5])

    with tl:
        st.markdown('<div class="sec-hd">🗓️ Visit Timeline <div class="sec-line"></div></div>', unsafe_allow_html=True)
        for v in [
            {"v": "Visit 3", "date": "7 May 2025",  "bp": "132/86", "hr": "84", "spo2": "97", "note": "Good progress. BP reducing steadily. Continue Amlodipine."},
            {"v": "Visit 2", "date": "1 May 2025",  "bp": "138/90", "hr": "88", "spo2": "96", "note": "Moderate improvement. Medication response positive."},
            {"v": "Visit 1", "date": "24 Apr 2025", "bp": "148/96", "hr": "95", "spo2": "94", "note": "Initial diagnosis. BP severely elevated. Started Amlodipine 5mg."},
        ]:
            st.markdown(f"""
            <div class="visit-card">
              <div style="display:flex;justify-content:space-between;margin-bottom:0.3rem;">
                <span class="visit-num">{v['v']}</span>
                <span class="visit-date">📅 {v['date']}</span>
              </div>
              <div style="margin-bottom:0.3rem;">
                <span class="pill p-red"  style="font-size:0.62rem;">BP {v['bp']}</span>
                <span class="pill p-teal" style="font-size:0.62rem;">HR {v['hr']}</span>
                <span class="pill p-blue" style="font-size:0.62rem;">SpO₂ {v['spo2']}%</span>
              </div>
              <div class="visit-note">{v['note']}</div>
            </div>""", unsafe_allow_html=True)

    with tr:
        st.markdown('<div class="sec-hd">📝 Doctor\'s Notes & Follow-up <div class="sec-line"></div></div>', unsafe_allow_html=True)
        st.text_area("",
            "Patient showing consistent improvement on Amlodipine 5mg. BP reduced from 148/96 → 132/86 over 3 visits. Target <120/80. Review lipid profile results next visit. Consider ACE inhibitor if BP not at target in 2 weeks.",
            height=130, key="dn", label_visibility="collapsed")

        st.markdown('<div class="form-lbl" style="margin-top:0.7rem;">Next Follow-up Date</div>', unsafe_allow_html=True)
        fu_date = st.date_input("", min_value=datetime.today(), key="fu", label_visibility="collapsed")

        st.markdown('<div class="form-lbl" style="margin-top:0.5rem;">Follow-up Instructions</div>', unsafe_allow_html=True)
        st.text_input("", "Follow-up BP check + lipid profile review", key="fn", label_visibility="collapsed")

        if st.button("💾 Save Notes & Schedule Follow-up", use_container_width=True, key="spn"):
            st.success(f"✅ Notes saved. Follow-up scheduled for {fu_date}. Patient notified!")

        st.markdown("""
        <div class="prog-summary">
          <div style="font-size:0.65rem;color:#16A34A;font-weight:700;text-transform:uppercase;
                      letter-spacing:1px;margin-bottom:0.5rem;">📊 Progress Summary</div>
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.45rem;">
            <div style="font-size:0.78rem;color:#6B7280;">BP Sys Reduction</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#16A34A;font-weight:700;">−16 mmHg ↓</div>
            <div style="font-size:0.78rem;color:#6B7280;">BP Dia Reduction</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#16A34A;font-weight:700;">−10 mmHg ↓</div>
            <div style="font-size:0.78rem;color:#6B7280;">HR Improvement</div>
            <div style="font-family:'JetBrains Mono',monospace;font-size:0.82rem;color:#16A34A;font-weight:700;">−11 bpm ↓</div>
            <div style="font-size:0.78rem;color:#6B7280;">Overall Trend</div>
            <div style="font-size:0.78rem;color:#16A34A;font-weight:700;">✅ Improving</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:1.5rem 0 0.5rem;
            font-size:0.7rem;color:#9CA3AF;border-top:1px solid #E5E7EB;margin-top:2rem;">
  🏥 Nash Doctor Portal · Apollo Hospital Bangalore · Clinical Management System v1.0
</div>
""", unsafe_allow_html=True)
