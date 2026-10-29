from pathlib import Path
import streamlit as st

def apply_custom_ui():
    css_path = Path(__file__).resolve().parent / "assets" / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    st.markdown("""
    <style>
      .notice-card { background:#fff; padding:14px; border-radius:10px; border:1px solid #dfe6f1; margin-bottom:10px; }
      .stAlert { border-radius:10px; }
    </style>
    """, unsafe_allow_html=True)
