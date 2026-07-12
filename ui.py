import streamlit as st

def render_header():
    st.markdown("""
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:1.5rem;padding-bottom:1rem;border-bottom:1px solid #2d2d4e">
        <div style="width:52px;height:52px;border-radius:50%;background:#4f46e5;display:flex;align-items:center;justify-content:center;color:white;font-size:20px;font-weight:500">N</div>
        <div>
            <p style="color:var(--text-primary);font-size:15px;font-weight:500;margin:0">Nitesh — AI Interviewer</p>
            <p style="color:#22c55e;font-size:12px;margin:4px 0 0">● Interview in progress</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_question(question):
    st.markdown(f"""
    <div style="background:#1a1a2e;border-radius:12px;padding:1.25rem;border-left:4px solid #4f46e5;margin-bottom:1.25rem">
        <p style="font-size:11px;color:#6b7280;text-transform:uppercase;margin-bottom:8px">Current question</p>
        <p style="color:#e2e8f0;font-size:16px;line-height:1.7;margin:0">{question}</p>
    </div>
    """, unsafe_allow_html=True)

def render_css():
    st.markdown("""
    <style>
    .stApp { background-color: #0f0f1a; }
    h1 { color: white; text-align: center; border-bottom: 1px solid #2d2d4e; padding-bottom: 1rem; }
    .stButton > button { background: #4f46e5; color: white; border: none; border-radius: 8px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)