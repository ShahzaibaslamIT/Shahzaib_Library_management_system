import streamlit as st
import pandas as pd
import json
import os
import datetime
import time
import plotly.express as px
import plotly.graph_objects as go
from streamlit_lottie import st_lottie
import requests

# Set page configuration
st.set_page_config(
    page_title="Library Management System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS with text color set to black
st.markdown("""
<style>
    body, h1, h2, h3, p, div, span, label {
        color: black !important;
    }
    .main-header {
        font-size:3rem !important;
        color:#1E3A8A !important;
        font-weight:700;
        margin-bottom:1rem;
        text-align:center;
        text-shadow:2px 2px 4px rgba(0,0,0,0.1);
    }
    .sub-header {
        font-size:1.8rem !important;
        color:#3B82F6 !important;
        font-weight:600;
        margin-top:1rem;
        margin-bottom:1rem;
    }
    .success-message {
        padding: 1rem;
        background-color:#ECFDF5;
        border-left:5px solid #10B981;
        border-radius:0.375rem;
        color: black !important;
    }
    .warning-message {
        padding: 1rem;
        background-color:#FEF2F2;
        border-left:5px solid #EF4444;
        border-radius:0.375rem;
        color: black !important;
    }
    .book-card {
        background-color:#F3F4F6;
        border-radius:0.5rem;
        padding:1rem;
        margin-bottom:1rem;
        border-left:5px solid #3B82F6;
        color: black !important;
    }
    .read-badge {
        background-color: #10B981;
        color: black !important;
        padding:0.25rem 0.75rem;
        border-radius:1rem;
        font-size:0.875rem;
        font-weight:600;
    }
    .unread-badge {
        background-color: #F87171;
        color: black !important;
        padding:0.25rem 0.75rem;
        border-radius:1rem;
        font-size:0.875rem;
        font-weight:600;
    }
</style>
""", unsafe_allow_html=True)
