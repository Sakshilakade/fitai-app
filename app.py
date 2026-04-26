"""
FitAI - Personalized Fitness & Meal Planner
Main Streamlit application
"""
import streamlit as st
import auth
import utils
import ml_model
import datetime
import re

# Page configuration
st.set_page_config(
    page_title="FitAI - Personal Fitness & Meal Planner",
    page_icon="💪",
    layout="centered"
)

# Custom CSS for mobile app styling
st.markdown("""
    <style>
    :root {
        --primary: #4b6043;
        --accent: #87ab69;
        --text-dark: #0F172A;
        --bg-light: #ddead1;
        --surface: #eef4e2;
        --border-soft: #c7ddb5;
        --shadow-soft: 0 8px 24px rgba(75, 96, 67, 0.12);
        --shadow-hover: 0 12px 28px rgba(75, 96, 67, 0.18);
        --font-heading: 'Poppins', 'Inter', sans-serif;
        --font-body: 'Inter', 'Roboto', sans-serif;
        --space-16: 16px;
        --space-24: 24px;
        --card-gap: 14px;
        --radius-sm: 12px;
        --radius-md: 16px;
        --radius-lg: 20px;
    }
            
            .stButton > button {
    border-radius: var(--radius-lg);
    padding: var(--space-16);
    font-size: 15px;
}

.card {
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}
            
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Poppins:wght@500;600;700&family=Roboto:wght@300;400;500&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Icons&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Icons+Outlined&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css');

    .material-icons,
    .material-icons-outlined,
    .material-symbols-outlined {
        font-family: 'Material Icons', 'Material Icons Outlined', 'Material Symbols Outlined', sans-serif !important;
        font-feature-settings: 'liga' 1 !important;
        speak: none !important;
    }
    
    /* Main styles */
    body, div, p, span, label, li, input, button, select, textarea, a {
        font-family: var(--font-body);
        line-height: 1.6;
        font-weight: 400;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: var(--font-heading) !important;
        font-weight: 700 !important;
        line-height: 1.25;
        letter-spacing: -0.01em;
    }

    h1 { font-size: 2.15rem !important; }
    h2 { font-size: 1.75rem !important; }
    h3 { font-size: 1.45rem !important; }
    h4 { font-size: 1.2rem !important; }
    h5 { font-size: 1.05rem !important; }
    h6 { font-size: 0.95rem !important; }

    p, span, div, label, li {
        line-height: 1.65;
    }
    
    .stApp {
        background-color: var(--bg-light);
        max-width: 420px;
        margin: 0 auto;
        padding: var(--space-16);
        color: var(--text-dark);
    }
    
    /* Mobile container */
    .mobile-container {
        background-color: var(--bg-light);
        min-height: 100vh;
        padding: var(--space-24) var(--space-16);
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Header */
    .gradient-header {
        background-color: var(--primary);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        text-align: center;
        color: white;
        margin-bottom: var(--space-16);
        box-shadow: var(--shadow-soft);
    }
    
    .gradient-header h1 {
        margin: 0;
        font-size: 34px;
        font-weight: 700;
    }
    
    .gradient-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        opacity: 0.9;
    }
    
    /* Card styles */
    .card {
        background-color: var(--surface);
        border-radius: var(--radius-md);
        padding: var(--space-16);
        margin-bottom: var(--card-gap);
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-soft);
    }
    
    .card, .card p, .card span, .card div {
        color: var(--text-dark) !important;
    }
    
    .card-title {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-dark);
        margin-bottom: var(--space-16);
    }
    
    /* Login card */
    .login-card {
        background-color: var(--surface);
        border-radius: var(--radius-lg);
        padding: var(--space-24);
        box-shadow: var(--shadow-soft);
        margin-top: var(--space-24);
        margin-bottom: var(--space-16);
        border: 1px solid var(--border-soft);
    }
    
    .login-card, .login-card p, .login-card span, .login-card div {
        color: var(--text-dark) !important;
    }
    
    .login-title {
        text-align: center;
        font-size: 40px;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 5px;
    }
    
    .login-subtitle {
        text-align: center;
        color: #475569 !important;
        font-size: 15px;
        font-weight: 400;
        line-height: 1.6;
        margin-bottom: var(--space-24);
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: var(--radius-sm);
        padding: 12px var(--space-16);
        border: 2px solid var(--border-soft);
        background-color: #F1F5F9;
        transition: all 0.3s;
        color: var(--text-dark) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--primary);
        background-color: var(--surface);
        box-shadow: 0 0 0 3px rgba(75, 96, 67, 0.15);
        color: var(--text-dark) !important;
    }
    
    .stTextInput label, .stSelectbox label, .stNumberInput label {
        color: var(--text-dark) !important;
    }
    
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input {
        color: var(--text-dark) !important;
    }

    .stSelectbox > div > div > div {
        border-radius: var(--radius-sm);
        padding: 12px;
        border: 2px solid var(--border-soft);
        color: var(--text-dark) !important;
        background-color: #eef4e2;
    }

    .stSelectbox div[data-baseweb="select"] {
        background-color: #eef4e2 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        color: black !important;
        font-weight: 500;
        min-height: 50px !important;
        background-color: #eef4e2 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div > div,
    .stSelectbox div[data-baseweb="select"] span,
    .stSelectbox div[data-baseweb="select"] input {
        color: black !important;
        font-weight: 500 !important;
        line-height: 1.4 !important;
    }

    .stSelectbox div[data-baseweb="select"] > div > div {
        background-color: #eef4e2 !important;
        padding-left: 14px !important;
        overflow: visible !important;
        white-space: nowrap !important;
        text-overflow: clip !important;
    }

    .field-label {
        display: flex;
        align-items: center;
        gap: 8px;
        margin: 8px 0 6px 0;
        color: var(--text-dark);
        font-size: 14px;
        font-weight: 500;
    }

    .field-label .fa-solid {
        color: var(--primary);
        font-size: 14px;
        line-height: 1;
    }
    
    /* Buttons */
    .stButton > button {
        border-radius: var(--radius-sm);
        padding: 12px var(--space-16);
        font-weight: 500;
        width: 100%;
        transition: transform 0.24s ease, box-shadow 0.24s ease, filter 0.24s ease, background 0.3s ease;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        color: white;
        border: none;
        box-shadow: 0 6px 16px rgba(75, 96, 67, 0.25);
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 12px 24px rgba(75, 96, 67, 0.24);
        filter: brightness(1.03);
    }

    .stButton > button:active {
        transform: translateY(0) scale(0.99);
        box-shadow: 0 6px 12px rgba(75, 96, 67, 0.18);
    }
    
    .primary-btn {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-hover);
    }
    
    .secondary-btn {
        background: none !important;
        background-color: #eef4e2 !important;
        color: var(--text-dark) !important;
        border: 1px solid #c7ddb5 !important;
        box-shadow: none !important;
    }
    
    /* Dashboard greeting */
    .greeting {
        font-size: 26px;
        font-weight: 700;
        color: var(--text-dark);
    }
    
    .sub-greeting {
        color: #475569 !important;
        font-size: 14px;
        margin-top: 5px;
    }
    
    .gradient-header, .gradient-header p, .gradient-header h1 {
        color: white !important;
    }
    
    .gradient-header h1 {
        color: white !important;
    }
    
    /* Dashboard grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--card-gap);
        margin-top: var(--space-16);
    }
    
    .dash-card {
        background-color: var(--surface);
        border-radius: var(--radius-md);
        padding: var(--space-16);
        text-align: center;
        box-shadow: var(--shadow-soft);
        border: 1px solid var(--border-soft);
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .dash-card:hover {
        transform: translateY(-3px);
        box-shadow: var(--shadow-hover);
        border-color: var(--accent);
    }
    
    .dash-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }
    
    .dash-label {
        font-size: 15px;
        font-weight: 500;
        color: var(--text-dark);
    }
    
    .dash-badge {
        display: inline-block;
        background-color: #fff3e0;
        color: #ff9800;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        margin-top: 8px;
        font-weight: 500;
    }
    
    /* Plan card */
    .plan-section {
        margin-bottom: var(--space-24);
    }
    
    .plan-header {
        background-color: var(--primary);
        border-radius: var(--radius-md);
        padding: var(--space-24);
        color: white;
        text-align: center;
        margin-bottom: var(--space-16);
        box-shadow: var(--shadow-soft);
    }
    
    .plan-header h2 {
        margin: 0;
        font-size: 30px;
        font-weight: 700;
    }
    
    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: var(--space-16);
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .exercise-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--space-16);
        background-color: var(--surface);
        border-radius: var(--radius-sm);
        margin-bottom: 12px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .exercise-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.12);
    }

    .exercise-main {
        display: flex;
        align-items: center;
        gap: 10px;
        min-width: 0;
    }

    .exercise-icon {
        font-size: 18px;
        line-height: 1;
    }
    
    .exercise-name {
        font-weight: 400;
        color: var(--text-dark);
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .exercise-meta {
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        justify-content: flex-end;
    }

    .exercise-detail {
        color: #475569 !important;
        font-size: 13px;
        font-weight: 500;
    }

    .activity-tag {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        border-radius: var(--radius-lg);
        font-size: 12px;
        font-weight: 500;
        border: 1px solid transparent;
    }

    .activity-tag-run {
        background-color: #ddead1;
        color: var(--primary) !important;
        border-color: #c7ddb5;
    }

    .activity-tag-cycle {
        background-color: #a3c585;
        color: #0F172A !important;
        border-color: #95bb72;
    }

    .activity-tag-skip {
        background-color: #ddead1;
        color: #4b6043 !important;
        border-color: #c7ddb5;
    }

    .activity-tag-default {
        background-color: #eef4e2;
        color: var(--primary) !important;
        border-color: #c7ddb5;
    }

    .workout-card {
        background: var(--surface);
        border-radius: var(--radius-md);
        border: 1px solid var(--border-soft);
        box-shadow: var(--shadow-soft);
        padding: var(--space-16);
        margin-bottom: 12px;
        animation: fade-slide-in 0.35s ease both;
    }

    .workout-card.recommended {
        border-color: #86EFAC;
        box-shadow: 0 12px 26px rgba(75, 96, 67, 0.18);
    }

    .workout-card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 10px;
    }

    .workout-name {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text-dark);
        font-size: 15px;
        font-weight: 500;
    }

    .recommended-tag {
        background: #ddead1;
        color: var(--primary) !important;
        border: 1px solid #95bb72;
        border-radius: var(--radius-lg);
        padding: 4px 10px;
        font-size: 12px;
        font-weight: 500;
    }

    .progress-track {
        width: 100%;
        height: 8px;
        background: #ddead1;
        border-radius: 999px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
        border-radius: 999px;
    }

    .workout-meta {
        margin-top: 8px;
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #475569 !important;
    }

    .dashboard-premium {
        background: #eef4e2;
        border: 1px solid var(--border-soft);
        border-radius: var(--radius-md);
        box-shadow: var(--shadow-soft);
        padding: var(--space-16);
        margin: 0 0 var(--space-16) 0;
    }

    .dashboard-premium-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }

    .dashboard-premium-title-left {
        display: flex;
        gap: 8px;
        align-items: center;
        min-width: 0;
    }

    .dashboard-premium-title-icon {
        color: var(--primary);
        font-size: 15px;
        line-height: 1;
    }

    .dashboard-premium-title span {
        color: #475569 !important;
        font-size: 13px;
        white-space: nowrap;
    }

    .daily-stats-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
    }

    .daily-stat-card {
        background: var(--surface);
        border: 1px solid var(--border-soft);
        border-radius: var(--radius-sm);
        padding: 12px;
        text-align: left;
    }

    .daily-stat-icon {
        font-size: 16px;
        margin-bottom: 4px;
    }

    .daily-stat-value {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-dark);
        line-height: 1.3;
        word-break: break-word;
    }

    .daily-stat-label {
        font-size: 12px;
        color: #64748B !important;
    }

    .daily-stat-progress {
        margin-top: 8px;
    }

    .daily-stat-progress-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 11px;
        color: #64748B !important;
        margin-bottom: 4px;
    }

    .daily-progress-track {
        width: 100%;
        height: 6px;
        background: #ddead1;
        border-radius: 999px;
        overflow: hidden;
    }

    .daily-progress-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transition: width 0.3s ease;
    }

    .daily-over-goal {
        color: #B45309 !important;
        font-weight: 600;
    }

    .progress-ring-wrap {
        display: flex;
        justify-content: center;
        margin: 14px 0 10px 0;
    }

    .progress-ring {
        width: 108px;
        height: 108px;
        border-radius: 50%;
        display: grid;
        place-items: center;
        background: conic-gradient(var(--primary) calc(var(--progress) * 1%), #ddead1 0);
        box-shadow: inset 0 0 0 1px rgba(15, 23, 42, 0.08);
    }

    .progress-ring-inner {
        width: 82px;
        height: 82px;
        border-radius: 50%;
        background: var(--surface);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .progress-ring-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--text-dark);
        line-height: 1;
    }

    .progress-ring-label {
        font-size: 11px;
        color: #64748B !important;
        margin-top: 4px;
    }

    .plan-loading {
        background: var(--surface);
        border: 1px solid var(--border-soft);
        border-radius: var(--radius-md);
        padding: var(--space-16);
        box-shadow: var(--shadow-soft);
        margin: 10px 0 var(--space-16) 0;
    }

    .plan-loading-row {
        display: flex;
        align-items: center;
        gap: 10px;
        color: var(--text-dark);
        font-size: 14px;
    }

    .plan-loading-spinner {
        width: 16px;
        height: 16px;
        border-radius: 50%;
        border: 2px solid #D1FAE5;
        border-top-color: var(--primary);
        animation: spin 0.8s linear infinite;
    }

    .plan-loading-bar {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        margin-top: 10px;
        background: #ddead1;
        overflow: hidden;
    }

    .plan-loading-bar::after {
        content: "";
        display: block;
        width: 45%;
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        animation: loading-sweep 1.1s ease-in-out infinite;
    }
    
    .meal-section {
        margin-bottom: var(--space-16);
    }

    .meal-section-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
        color: var(--text-dark);
        font-size: 16px;
        font-weight: 500;
    }

    .meal-item {
        display: flex;
        align-items: center;
        padding: var(--space-16);
        background-color: var(--surface);
        border-radius: var(--radius-sm);
        margin-bottom: 12px;
        gap: 12px;
        border: 1px solid var(--border-soft);
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
        animation: fade-slide-in 0.35s ease both;
    }

    .meal-emoji {
        font-size: 22px;
        line-height: 1;
    }
    
    .meal-time {
        background-color: #ddead1;
        color: #4b6043;
        padding: 5px 12px;
        border-radius: var(--radius-lg);
        font-size: 12px;
        font-weight: 500;
        min-width: 84px;
        text-align: center;
        border: 1px solid #c7ddb5;
    }

    .meal-time-breakfast {
        background-color: #c7ddb5;
        color: #0F172A !important;
        border-color: #95bb72;
    }

    .meal-time-lunch {
        background-color: #95bb72;
        color: #0F172A !important;
        border-color: #87ab69;
    }

    .meal-time-dinner {
        background-color: #87ab69;
        color: #0F172A !important;
        border-color: #75975e;
    }

    .meal-time-snack {
        background-color: #a3c585;
        color: #0F172A !important;
        border-color: #95bb72;
    }

    .meal-time-default {
        background-color: #eef4e2;
        color: #334155 !important;
        border-color: #CBD5E1;
    }

    .meal-kcal {
        margin-top: 4px;
        color: #64748B !important;
        font-size: 12px;
    }

    .meal-info {
        flex: 1;
    }
    
    .meal-name {
        font-weight: 400;
        color: var(--text-dark);
        font-size: 15px;
        line-height: 1.6;
    }
    

    
    .tip-item {
        display: flex;
        align-items: flex-start;
        padding: 12px 0;
        gap: 12px;
        border-bottom: 1px solid var(--border-soft);
        transition: transform 0.2s ease, background-color 0.2s ease;
    }

    .tip-item:hover {
        transform: translateX(2px);
        background-color: #eef4e2;
    }
    
    .tip-item:last-child {
        border-bottom: none;
    }
    
    .tip-check {
        color: var(--primary);
        font-size: 18px;
    }
    
    .tip-text {
        color: var(--text-dark);
        font-size: 15px;
        line-height: 1.7;
    }
    
    /* BMI Result */
    .bmi-result-card {
        text-align: center;
        padding: var(--space-24);
    }
    
    .bmi-value {
        font-size: 56px;
        font-weight: 700;
        color: var(--primary);
    }
    
    .bmi-category {
        display: inline-block;
        padding: 8px 16px;
        border-radius: var(--radius-lg);
        font-weight: 500;
        font-size: 16px;
        margin: 12px 0;
    }
    
    .bmi-normal {
        background-color: #e8f5e9;
        color: #2e7d32;
    }
    
    .bmi-warning {
        background-color: #fff3e0;
        color: #ef6c00;
    }
    
    .bmi-danger {
        background-color: #ffebee;
        color: #c62828;
    }
    
    .bmi-message {
        color: var(--text-dark) !important;
        font-size: 15px;
        margin-top: var(--space-16);
        line-height: 1.7;
    }
    
    .section-title, .section-title p {
        color: var(--primary) !important;
    }
    
    .plan-header h2 {
        color: white !important;
    }
    
    .exercise-name, .exercise-detail, .meal-name, .tip-text {
        color: var(--text-dark) !important;
    }
    
    /* Logout button */
    .logout-btn {
        position: absolute;
        top: 15px;
        right: 15px;
    }
    
    /* Back button */
    .back-btn {
        margin-top: var(--space-16);
    }
    
    /* Link styles */
    .auth-link {
        text-align: center;
        margin-top: var(--space-16);
        font-size: 15px;
        font-weight: 400;
        color: #475569;
    }
    
    .auth-link a {
        color: var(--primary);
        font-weight: 500;
        text-decoration: none;
    }
    
    .auth-link a:hover {
        text-decoration: underline;
    }
    
    /* Error/Success messages */
    .message {
        padding: 12px var(--space-16);
        border-radius: var(--radius-sm);
        margin-bottom: var(--card-gap);
        font-size: 14px;
    }
    
    .message-error {
        background-color: #ffebee;
        color: #c62828;
        border: 1px solid #ffcdd2;
    }
    
    .message-success {
        background-color: #e8f5e9;
        color: #2e7d32;
        border: 1px solid #c8e6c9;
    }
    
    /* Divider */
    .divider {
        text-align: center;
        margin: var(--space-24) 0;
        position: relative;
    }
    
    .divider::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background-color: var(--border-soft);
    }
    
    .divider span {
        background-color: var(--surface);
        padding: 0 12px;
        color: #888;
        font-size: 12px;
        position: relative;
    }
    
    /* Hide some Streamlit defaults */
    .stRadio > div {
        flex-direction: row;
    }
    
    /* Force dark text on content */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div {
        color: var(--text-dark) !important;
    }
    
    p, span, div {
        color: var(--text-dark) !important;
    }
    
    /* Header text color override */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-dark) !important;
    }
    
    /* Streamlit text color fix */
    .stApp {
        color: var(--text-dark);
    }

    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    @keyframes loading-sweep {
        0% { transform: translateX(-110%); }
        100% { transform: translateX(250%); }
    }

    @keyframes fade-slide-in {
        from {
            opacity: 0;
            transform: translateY(8px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #ddead1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #658354;
        border-radius: 3px;
    }
    </style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialize session state variables"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "page" not in st.session_state:
        st.session_state.page = "login"
    if "user_data" not in st.session_state:
        st.session_state.user_data = None


def _default_daily_goal_state(today_iso):
    """Return default daily progress/goals structure."""
    return {
        "last_saved_date": today_iso,
        "calories": {"current": 0, "goal": 2200},
        "steps": {"current": 0, "goal": 8000},
        "water": {"current": 0.0, "goal": 3.0}
    }


def _normalize_daily_goal_state(daily_state, today_iso):
    """Ensure daily goal state has valid keys and values."""
    if not isinstance(daily_state, dict):
        daily_state = _default_daily_goal_state(today_iso)

    defaults = _default_daily_goal_state(today_iso)
    for stat_key in ["calories", "steps", "water"]:
        if stat_key not in daily_state or not isinstance(daily_state[stat_key], dict):
            daily_state[stat_key] = defaults[stat_key].copy()
        daily_state[stat_key]["current"] = float(daily_state[stat_key].get("current", defaults[stat_key]["current"]))
        daily_state[stat_key]["goal"] = float(daily_state[stat_key].get("goal", defaults[stat_key]["goal"]))

    if "last_saved_date" not in daily_state:
        daily_state["last_saved_date"] = today_iso

    return daily_state


def _calculate_progress_percent(current, goal):
    """Return progress percentage (can exceed 100)."""
    if goal <= 0:
        return 0.0
    return (current / goal) * 100


def show_login():
    """Display login screen"""
    # Top title card
    st.markdown("""
        <div class="login-card">
            <h1 class="login-title">FitAI</h1>
            <p class="login-subtitle">Personalized Fitness & Meal Planner</p>
        </div>
    """, unsafe_allow_html=True)

    # Inputs (these stay!)
    username = st.text_input("Username", key="login_username", placeholder="Enter your username")
    password = st.text_input("Password", key="login_password", type="password", placeholder="Enter your password")

    # Login button
    if st.button("Login", key="login_btn", type="primary"):
        success, message = auth.login_user(username, password)
        if success:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "dashboard"
            st.rerun()
        else:
            st.markdown(f'<div class="message message-error">{message}</div>', unsafe_allow_html=True)

    # Link to open registration
    st.markdown("""
        <div class="auth-link">
            Don't have an account? <a href="#" onclick="document.getElementById('register_btn').click();">Register</a>
        </div>
    """, unsafe_allow_html=True)

    # Register toggle button
    if "show_register" not in st.session_state:
        st.session_state.show_register = False
        
    if st.button("Register", key="register_btn", type="secondary"):
        st.session_state.show_register = not st.session_state.show_register

    # Registration form
    if st.session_state.show_register:
        st.markdown("---")
        st.markdown("### Create Account")

        new_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
        new_password = st.text_input("Password", key="reg_password", type="password", placeholder="Choose a password")
        confirm_password = st.text_input("Confirm Password", key="reg_confirm", type="password", placeholder="Confirm password")

        if st.button("Sign Up", key="signup_btn", type="primary"):
            if new_password != confirm_password:
                st.markdown('<div class="message message-error">Passwords do not match!</div>', unsafe_allow_html=True)
            else:
                success, message = auth.register_user(new_username, new_password)
                if success:
                    st.markdown(f'<div class="message message-success">{message}</div>', unsafe_allow_html=True)
                    st.session_state.show_register = False
                else:
                    st.markdown(f'<div class="message message-error">{message}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # CLOSE login-card

def show_dashboard():
    """Display dashboard screen"""
    current_hour = datetime.datetime.now().hour
    greeting_time = "Morning" if current_hour < 17 else "Evening"

    # Top gradient header
    st.markdown(f"""
        <div class="gradient-header">
            <h1>Good {greeting_time}, {st.session_state.username} 👋</h1>
            <p>Consistency beats intensity</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Logout button
    col1, col2 = st.columns([4, 2])
    with col2:
        if st.button("back to login", key="logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.page = "login"
            st.rerun()

    # Premium daily stats panel (dynamic + persisted)
    today_iso = datetime.date.today().isoformat()
    user_data = auth.get_user_data(st.session_state.username)
    profile = user_data.get("profile", {}) if user_data else {}
    stored_daily_state = profile.get("daily_goals")
    if not stored_daily_state and "daily_goals" in st.session_state:
        stored_daily_state = st.session_state.daily_goals
    daily_state = _normalize_daily_goal_state(stored_daily_state, today_iso)
    has_new_day = daily_state["last_saved_date"] != today_iso
    if has_new_day:
        for stat_key in ["calories", "steps", "water"]:
            daily_state[stat_key]["current"] = 0
        daily_state["last_saved_date"] = today_iso

    # Persist daily goals in profile storage so values survive refresh/login
    if user_data and user_data.get("profile"):
        if has_new_day or profile.get("daily_goals") != daily_state:
            profile["daily_goals"] = daily_state
            auth.update_user_profile(st.session_state.username, profile)
    else:
        # Fallback persistence in session state when profile store is unavailable
        st.session_state.daily_goals = daily_state

    # Keep goals, current values, and progress calculation clearly separated.
    goals = {
        "calories": int(daily_state["calories"]["goal"]),
        "steps": int(daily_state["steps"]["goal"]),
        "water": float(daily_state["water"]["goal"]),
    }
    current_stats = {
        "calories": int(daily_state["calories"]["current"]),
        "steps": int(daily_state["steps"]["current"]),
        "water": float(daily_state["water"]["current"]),
    }
    progress = {
        "calories": _calculate_progress_percent(current_stats['calories'], goals['calories']),
        "steps": _calculate_progress_percent(current_stats['steps'], goals['steps']),
        "water": _calculate_progress_percent(current_stats['water'], goals['water']),
    }

    overall_pct = (progress['calories'] + progress['steps'] + progress['water']) / 3
    ring_pct_for_visual = min(overall_pct, 100)

    st.markdown(f"""
        <div class="dashboard-premium">
            <div class="dashboard-premium-title">
                <div class="dashboard-premium-title-left">
                    <i class="fa-solid fa-chart-line dashboard-premium-title-icon"></i>
                    <h3 style="margin:0;">Today's daily stats</h3>
                </div>
                <span>Today's readiness</span>
            </div>
            <div class="progress-ring-wrap">
                <div class="progress-ring" style="--progress:{ring_pct_for_visual:.1f};">
                    <div class="progress-ring-inner">
                        <div class="progress-ring-value">{overall_pct:.0f}%</div>
                        <div class="progress-ring-label">Goal Progress</div>
                    </div>
                </div>
            </div>
            <div class="daily-stats-grid">
                <div class="daily-stat-card">
                    <div class="daily-stat-icon">🔥</div>
                    <div class="daily-stat-value">{current_stats['calories']} / {goals['calories']}</div>
                    <div class="daily-stat-label">Calories</div>
                    <div class="daily-stat-progress">
                        <div class="daily-stat-progress-top">
                            <span>{progress['calories']:.0f}%</span>
                            <span class="{"daily-over-goal" if progress['calories'] > 100 else ""}">{"Over goal" if progress['calories'] > 100 else "On track"}</span>
                        </div>
                        <div class="daily-progress-track">
                            <div class="daily-progress-fill" style="width: {min(progress['calories'], 100):.1f}%"></div>
                        </div>
                    </div>
                </div>
                <div class="daily-stat-card">
                    <div class="daily-stat-icon">👣</div>
                    <div class="daily-stat-value">{current_stats['steps']} / {goals['steps']}</div>
                    <div class="daily-stat-label">Steps</div>
                    <div class="daily-stat-progress">
                        <div class="daily-stat-progress-top">
                            <span>{progress['steps']:.0f}%</span>
                            <span class="{"daily-over-goal" if progress['steps'] > 100 else ""}">{"Over goal" if progress['steps'] > 100 else "On track"}</span>
                        </div>
                        <div class="daily-progress-track">
                            <div class="daily-progress-fill" style="width: {min(progress['steps'], 100):.1f}%"></div>
                        </div>
                    </div>
                </div>
                <div class="daily-stat-card">
                    <div class="daily-stat-icon">💧</div>
                    <div class="daily-stat-value">{current_stats['water']:.1f} / {goals['water']:.1f}L</div>
                    <div class="daily-stat-label">Water</div>
                    <div class="daily-stat-progress">
                        <div class="daily-stat-progress-top">
                            <span>{progress['water']:.0f}%</span>
                            <span class="{"daily-over-goal" if progress['water'] > 100 else ""}">{"Over goal" if progress['water'] > 100 else "On track"}</span>
                        </div>
                        <div class="daily-progress-track">
                            <div class="daily-progress-fill" style="width: {min(progress['water'], 100):.1f}%"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("Set / Edit daily goals", expanded=False):
        goal_col1, goal_col2, goal_col3 = st.columns(3)
        with goal_col1:
            calories_goal_input = st.number_input(
                "Calories goal (kcal)",
                min_value=800,
                max_value=6000,
                value=goals['calories'],
                step=50
            )
        with goal_col2:
            steps_goal_input = st.number_input(
                "Steps goal",
                min_value=1000,
                max_value=50000,
                value=goals['steps'],
                step=500
            )
        with goal_col3:
            water_unit = st.selectbox("Water goal unit", ["Liters", "Milliliters"], key="water_goal_unit")
            default_water_display = goals['water'] if water_unit == "Liters" else goals['water'] * 1000
            water_goal_input = st.number_input(
                f"Water goal ({'L' if water_unit == 'Liters' else 'ml'})",
                min_value=0.5 if water_unit == "Liters" else 500.0,
                max_value=10.0 if water_unit == "Liters" else 10000.0,
                value=float(default_water_display),
                step=0.1 if water_unit == "Liters" else 100.0
            )

        if st.button("Save goals", key="save_daily_goals"):
            water_goal_liters = float(water_goal_input if water_unit == "Liters" else water_goal_input / 1000)
            if calories_goal_input <= 0 or steps_goal_input <= 0 or water_goal_liters <= 0:
                st.error("Goals must be greater than 0.")
            elif steps_goal_input < 1000:
                st.error("Steps goal must be at least 1000.")
            else:
                daily_state["calories"]["goal"] = int(calories_goal_input)
                daily_state["steps"]["goal"] = int(steps_goal_input)
                daily_state["water"]["goal"] = round(water_goal_liters, 2)
                daily_state["last_saved_date"] = today_iso

                if user_data and user_data.get("profile"):
                    profile["daily_goals"] = daily_state
                    auth.update_user_profile(st.session_state.username, profile)
                else:
                    st.session_state.daily_goals = daily_state

                st.success("Daily goals updated.")
                st.rerun()

    with st.expander("Update current values", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            calories_input = st.number_input("Calories current", min_value=0, value=current_stats['calories'], step=50)
        with col2:
            steps_input = st.number_input("Steps current", min_value=0, value=current_stats['steps'], step=100)
        with col3:
            water_input = st.number_input("Water current (L)", min_value=0.0, value=current_stats['water'], step=0.1)

        if st.button("Save daily stats", key="save_daily_stats"):
            daily_state["calories"]["current"] = int(calories_input)
            daily_state["steps"]["current"] = int(steps_input)
            daily_state["water"]["current"] = round(float(water_input), 1)
            daily_state["last_saved_date"] = today_iso

            if user_data and user_data.get("profile"):
                profile["daily_goals"] = daily_state
                auth.update_user_profile(st.session_state.username, profile)
            else:
                st.session_state.daily_goals = daily_state

            st.success("Daily stats saved.")
            st.rerun()


def show_features():
    """Display features hub screen"""
    st.markdown("""
        <div class="gradient-header">
            <h1>Features</h1>
            <p>Choose a tool and get started</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### Tools")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Generate Plan", key="features_generate_plan", use_container_width=True):
            st.session_state.page = "generate_plan"
            st.rerun()
        if st.button("⚖️ BMI Calculator", key="features_bmi_calc", use_container_width=True):
            st.session_state.page = "bmi"
            st.rerun()
    with col2:
        if st.button("📊 Progress Tracking", key="features_progress_tracking", use_container_width=True):
            st.session_state.page = "progress"
            st.rerun()


def show_generate_plan():
    """Display generate plan screen"""
    def render_icon_label(icon_html, label_text):
        st.markdown(
            f'<div class="field-label">{icon_html}<span>{label_text}</span></div>',
            unsafe_allow_html=True
        )
    
    # Back button
    if st.button("← Back", key="back_dashboard"):
        st.session_state.page = "features"
        st.rerun()

    # Banner
    st.markdown("""
        <div class="plan-header">
            <h2>Get Your Plan Now</h2>
        </div>
    """, unsafe_allow_html=True)

    # ---- USER INPUTS ----
    render_icon_label('<i class="fa-solid fa-user"></i>', "Age")
    age = st.number_input(
        "Age",
        min_value=10,
        max_value=80,
        value=21,
        label_visibility="collapsed"
    )

    col1, col2 = st.columns(2)
    with col1:
        render_icon_label('<i class="fa-solid fa-weight-scale"></i>', "Weight")
        weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            value=70.0,
            label_visibility="collapsed"
        )
    with col2:
        render_icon_label('<i class="fa-solid fa-ruler"></i>', "Height")
        height = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=220.0,
            value=170.0,
            label_visibility="collapsed"
        )

    gender = st.selectbox("Gender", ["Male", "Female"])
    activity = st.selectbox("Activity Level", ["Low", "Moderate", "High"])
    render_icon_label('<i class="fa-solid fa-utensils"></i>', "Diet")
    diet = st.selectbox(
        "Diet Preference",
        ["Veg", "Non-Veg", "Vegan", "Veg + Non-Veg"],
        label_visibility="collapsed"
    )


    render_icon_label('<i class="fa-solid fa-bullseye"></i>', "Goal")
    goal = st.selectbox(
        "Select Goal",
        ["Weight Loss", "Muscle Gain", "Maintain Weight"],
        label_visibility="collapsed"
    )

    # Convert goal to ML-compatible
    goal_map = {
        "Weight Loss": "weight_loss",
        "Muscle Gain": "muscle_gain",
        "Maintain Weight": "maintain"
    }
    goal_value = goal_map[goal]

    # ---- GENERATE PLAN ----
    if st.button("Create My Plan", type="primary"):
        height_m = height / 100
        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
            <div class="plan-loading">
                <div class="plan-loading-row">
                    <span class="plan-loading-spinner"></span>
                    <span>Generating your personalized plan...</span>
                </div>
                <div class="plan-loading-bar"></div>
            </div>
        """, unsafe_allow_html=True)

        # ⭐ FIXED ML CALL ⭐
        with st.spinner("Building workout and meal recommendations..."):
            ml_result = ml_model.predict_workout(weight, height_m, age, gender, activity, diet, goal_value)
            workout_result = ml_result["workout"]

        # Meal plan - format it properly
        raw_meal_plan = ml_result["food_plan"]
        meal_times = ["Breakfast (8:00 AM)", "Snack 1 (10:00 AM)", "Lunch (12:00 PM)", "Snack 2 (3:00 PM)", "Dinner (7:00 PM)", "Snack 3 (9:00 PM)"]
        formatted_meal_plan = {}
        for i, meal in enumerate(raw_meal_plan["meals"][:6]):
            formatted_meal_plan[meal_times[i]] = {
                "time": meal_times[i],
                "meal": meal,
                "calories": "Approx 300-500 kcal"
            }

        # Tips
        tips = utils.get_fitness_tips(goal_value)

        # Save to session
        st.session_state.plan_results = {
            "workout": ml_result["workout"],
            "meal_plan": formatted_meal_plan,
            "tips": tips
        }

        loading_placeholder.empty()
        st.session_state.show_plan = True
        st.rerun()

    # ---- SHOW RESULTS ----
    if st.session_state.get("show_plan", False):
        results = st.session_state.plan_results

        def get_activity_style(exercise_name):
            """Return icon and badge class by activity keyword."""
            name = exercise_name.lower()
            if "run" in name:
                return "🏃", "Running", "activity-tag-run"
            if "cycl" in name or "bike" in name:
                return "🚴", "Cycling", "activity-tag-cycle"
            if "skip" in name or "jump rope" in name:
                return "🔥", "Skipping", "activity-tag-skip"
            return "💪", "Workout", "activity-tag-default"

        def estimate_progress_percent(detail_text):
            """Estimate progress value from reps/duration text."""
            detail = str(detail_text).lower()
            numbers = [int(n) for n in re.findall(r"\d+", detail)]
            if not numbers:
                return 55
            peak = max(numbers)
            if "min" in detail:
                return min(100, max(35, int((peak / 30) * 100)))
            if "sec" in detail:
                return min(100, max(25, int((peak / 120) * 100)))
            return min(100, max(30, int((peak / 30) * 100)))

        def get_meal_group(meal_time):
            """Group meal slots into visual sections."""
            time_text = str(meal_time).lower()
            if "breakfast" in time_text:
                return "Breakfast"
            if "lunch" in time_text:
                return "Lunch"
            if "dinner" in time_text:
                return "Dinner"
            if "snack" in time_text:
                return "Snacks"
            return "Other"

        def get_meal_style(group_name, meal_text):
            """Return icon and color label class for meal cards."""
            meal = str(meal_text).lower()
            emoji = "🍽️"
            if any(word in meal for word in ["oat", "egg", "toast", "idli", "dosa", "poha"]):
                emoji = "🥣"
            elif any(word in meal for word in ["rice", "roti", "dal", "chicken", "paneer"]):
                emoji = "🍛"
            elif any(word in meal for word in ["salad", "soup", "grill", "fish"]):
                emoji = "🥗"
            elif any(word in meal for word in ["fruit", "nuts", "yogurt", "smoothie"]):
                emoji = "🍎"

            if group_name == "Breakfast":
                return emoji, "meal-time-breakfast", "🌅 Breakfast"
            if group_name == "Lunch":
                return emoji, "meal-time-lunch", "☀️ Lunch"
            if group_name == "Dinner":
                return emoji, "meal-time-dinner", "🌙 Dinner"
            if group_name == "Snacks":
                return emoji, "meal-time-snack", "🍿 Snacks"
            return emoji, "meal-time-default", "🍽️ Meals"

        # Workout
        st.markdown("""
            <div class="plan-section">
                <h3 class="section-title">💪 Workout Plan</h3>
            </div>
        """, unsafe_allow_html=True)

        workout = results.get("workout", {})

        if isinstance(workout, dict):
            workout_type = workout.get("workout_type", "Workout Plan")
        else:
            workout_type = str(workout)

        workout_html = (
            '<div class="card">'
            f'<p style="color:var(--primary); font-weight:500; margin:0;">{workout_type}</p>'
            '</div>'
        )
        st.markdown(workout_html, unsafe_allow_html=True)

        exercises = workout.get("exercises", [])

        if not exercises:
            st.warning("⚠️ No exercises found. Check ML output.")
        else:
            st.markdown("#### Build Progress")
            for idx, ex in enumerate(exercises):
                exercise_name = ex.get("name", "Exercise")
                exercise_detail = ex.get("reps", ex.get("duration", ""))
                icon, tag_label, tag_class = get_activity_style(exercise_name)
                progress_percent = estimate_progress_percent(exercise_detail)
                recommended_tag = '<span class="recommended-tag">Recommended</span>' if idx == 0 else ""
                recommended_class = " recommended" if idx == 0 else ""
                exercise_html = (
                    f'<div class="workout-card{recommended_class}">'
                    '<div class="workout-card-top">'
                    '<div class="workout-name">'
                    f'<span class="exercise-icon">{icon}</span>'
                    f'<span>{exercise_name}</span>'
                    f'<span class="activity-tag {tag_class}">{tag_label}</span>'
                    '</div>'
                    f'{recommended_tag}'
                    '</div>'
                    '<div class="progress-track">'
                    f'<div class="progress-fill" style="width: {progress_percent}%;"></div>'
                    '</div>'
                    '<div class="workout-meta">'
                    f'<span>{exercise_detail}</span>'
                    f'<span>{progress_percent}% target</span>'
                    '</div>'
                    '</div>'
                )
                st.markdown(exercise_html, unsafe_allow_html=True)

            if st.button("▶ Start Workout", key="start_workout_btn", type="primary", use_container_width=True):
                st.success("Workout started! Track your sets and stay consistent.")
               
        st.markdown("""
            <div class="plan-section">
                <h3 class="section-title">🍽️ Meal Plan</h3>
            </div>
        """, unsafe_allow_html=True)

        meal_sections = {"Breakfast": [], "Lunch": [], "Dinner": [], "Snacks": [], "Other": []}
        for _, meal_data in results["meal_plan"].items():
            group = get_meal_group(meal_data["time"])
            meal_sections[group].append(meal_data)

        for group_name in ["Breakfast", "Lunch", "Dinner", "Snacks", "Other"]:
            if not meal_sections[group_name]:
                continue

            _, _, section_title = get_meal_style(group_name, "")
            st.markdown(
                f'<div class="meal-section-header">{section_title}</div>',
                unsafe_allow_html=True
            )

            for meal_data in meal_sections[group_name]:
                emoji, time_class, _ = get_meal_style(group_name, meal_data["meal"])
                st.markdown(f"""
                    <div class="meal-item">
                        <span class="meal-emoji">{emoji}</span>
                        <span class="meal-time {time_class}">{meal_data["time"]}</span>
                        <div class="meal-info">
                            <div class="meal-name">{meal_data["meal"]}</div>
                            <div class="meal-kcal">{meal_data["calories"]}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

        # Tips
        st.markdown("""
            <div class="plan-section">
                <h3 class="section-title">💡 Fitness Tips</h3>
            </div>
        """, unsafe_allow_html=True)

        for tip in results["tips"]:
            st.markdown(f"""
                <div class="tip-item">
                    <span class="tip-check">✓</span>
                    <span class="tip-text">{tip}</span>
                </div>
            """, unsafe_allow_html=True)

        # Back Button
        if st.button("← Back to Features", key="back_from_plan"):
            st.session_state.show_plan = False
            st.session_state.page = "features"
            st.rerun()


def show_bmi():
    """Display BMI calculator screen"""
    def render_icon_label(icon_html, label_text):
        st.markdown(
            f'<div class="field-label">{icon_html}<span>{label_text}</span></div>',
            unsafe_allow_html=True
        )
    # Back button
    if st.button("← Back", key="back_dashboard_bmi"):
        st.session_state.page = "features"
        st.rerun()
    
    # Header
    st.markdown("""
        <div class="gradient-header">
            <h1>BMI Calculator</h1>
            <p>Check your Body Mass Index</p>
        </div>
    """, unsafe_allow_html=True)
    

    col1, col2 = st.columns(2)
    with col1:
        render_icon_label('<i class="fa-solid fa-weight-scale"></i>', "Weight")
        bmi_weight = st.number_input(
            "Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            value=70.0,
            step=0.5,
            key="bmi_weight",
            label_visibility="collapsed"
        )
    with col2:
        render_icon_label('<i class="fa-solid fa-ruler"></i>', "Height")
        bmi_height_cm = st.number_input(
            "Height (cm)",
            min_value=100.0,
            max_value=220.0,
            value=170.0,
            step=1.0,
            key="bmi_height",
            label_visibility="collapsed"
        )
    
    if st.button("Calculate BMI", type="primary"):
        bmi_height_m = bmi_height_cm / 100
        result = utils.calculate_bmi(bmi_weight, bmi_height_m)
        
        # Determine category class
        if result["category"] == "Normal":
            cat_class = "bmi-normal"
        elif result["category"] in ["Overweight"]:
            cat_class = "bmi-warning"
        else:
            cat_class = "bmi-danger"
        
        # Store result
        st.session_state.bmi_result = result
        st.session_state.show_bmi_result = True
        st.rerun()
    
    # Show result if calculated
    if st.session_state.get("show_bmi_result", False):
        result = st.session_state.bmi_result
        
        if result["category"] == "Normal":
            cat_class = "bmi-normal"
        elif result["category"] in ["Overweight"]:
            cat_class = "bmi-warning"
        else:
            cat_class = "bmi-danger"
        
        st.markdown(f'''
            <div class="card bmi-result-card">
                <div class="bmi-value">{result["bmi"]}</div>
                <div class="bmi-category {cat_class}">{result["category"]}</div>
                <p class="bmi-message">{result["message"]}</p>
            </div>
        ''', unsafe_allow_html=True)


def show_progress():
    """Display progress tracking screen"""
    def render_icon_label(icon_html, label_text):
        st.markdown(
            f'<div class="field-label">{icon_html}<span>{label_text}</span></div>',
            unsafe_allow_html=True
        )
    # Back button
    if st.button("← Back", key="back_progress"):
        st.session_state.page = "features"
        st.rerun()
    
    st.markdown("""
        <div class="gradient-header">
            <h1>📊 Progress Tracking</h1>
            <p>Track your fitness journey</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load user data
    user_data = auth.get_user_data(st.session_state.username)
    if user_data:
        profile = user_data["profile"]
        stats = utils.get_progress_stats(profile)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Workouts", stats['total_workouts'])
        with col2:
            st.metric("Streak", f"{stats['current_streak']} days 🔥")
        with col3:
            st.metric("Avg Completion", f"{stats['avg_completion']:.1%}")
        
        chart_data = utils.get_weight_chart_data(profile)
        if chart_data is not None:
            st.line_chart({
                "Weight": chart_data["values"]
            })
        else:
            st.info("📈 Add weight entries to see your progress chart!")
        
        st.markdown("### 💪 Log Today's Workout")
        
        workout_types = ["HIIT", "Strength Training", "Cardio", "Yoga", "Custom"]
        workout_type = st.selectbox("Workout Type", workout_types)
        
        # Sample exercises based on type (static for simplicity)
        if workout_type == "HIIT":
            exercises = ["Jumping Jacks", "Burpees", "Mountain Climbers", "High Knees"]
        elif workout_type == "Strength Training":
            exercises = ["Squats", "Push-ups", "Lunges", "Plank"]
        elif workout_type == "Cardio":
            exercises = ["Running", "Cycling", "Jump Rope", "Brisk Walking"]
        else:
            exercises = ["Session 1", "Session 2", "Session 3"]
        
        selected_exercises = st.multiselect("Completed Exercises", exercises, default=exercises[:2])
        
        if st.button("✅ Log Workout", type="primary"):
            if selected_exercises:
                updated_profile = utils.log_workout(profile, workout_type, selected_exercises)
                if auth.update_user_profile(st.session_state.username, updated_profile):
                    st.success("🎉 Workout logged successfully!")
                    st.rerun()
                else:
                    st.error("Failed to save workout log.")
            else:
                st.warning("Select at least one exercise.")
        
        st.markdown("### ⚖️ Update Weight")
        render_icon_label('<i class="fa-solid fa-weight-scale"></i>', "Weight")
        current_weight = st.number_input(
            "Current Weight (kg)",
            min_value=30.0,
            max_value=200.0,
            step=0.1,
            label_visibility="collapsed"
        )
        if st.button("📝 Update Weight", type="secondary"):
            new_entry = {
                "date": datetime.date.today().isoformat(),
                "weight": current_weight
            }
            profile["weight_history"].append(new_entry)
            if auth.update_user_profile(st.session_state.username, profile):
                st.success("✅ Weight updated!")
                st.rerun()
            else:
                st.error("Failed to save weight.")
    else:
        st.warning("No user data found.")


def main():
    """Main application"""
    # Initialize session state
    init_session_state()
    
    # Check if user is logged in
    if not st.session_state.logged_in:
        show_login()
    else:
        # Load user data for logged in user
        if st.session_state.user_data is None:
            st.session_state.user_data = auth.get_user_data(st.session_state.username)

        # App navigation: Dashboard and Features are separate top-level pages.
        nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
        with nav_col1:
            if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
        with nav_col2:
            if st.button("🧩 Features", key="nav_features", use_container_width=True):
                st.session_state.page = "features"
                st.rerun()
        with nav_col3:
            if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.username = ""
                st.session_state.page = "login"
                st.rerun()
        
        # Route to appropriate page
        if st.session_state.page == "dashboard":
            show_dashboard()
        elif st.session_state.page == "features":
            show_features()
        elif st.session_state.page == "generate_plan":
            show_generate_plan()
        elif st.session_state.page == "bmi":
            show_bmi()
        elif st.session_state.page == "progress":
            show_progress()
        else:
            show_dashboard()


if __name__ == "__main__":
    main()
