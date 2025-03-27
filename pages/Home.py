import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="EcomSEO Predictor",
    page_icon="📈",
    layout="wide"
)

# Inject meta tags
st.markdown("""
    <head>
        <meta name="description" content="EcomSEO Predictor: Forecast your e-commerce SEO performance with precision—predict traffic, conversions, and revenue growth.">
        <meta name="keywords" content="SEO, e-commerce, forecasting, traffic prediction, conversion rate, revenue growth">
        <meta name="author" content="Boopin">
        <meta property="og:title" content="EcomSEO Predictor">
        <meta property="og:description" content="Forecast your e-commerce SEO performance with precision—predict traffic, conversions, and revenue growth.">
        <meta property="og:type" content="website">
        <meta property="og:url" content="https://seo-ecom-metrics-forecaster.streamlit.app/Home">
        <meta property="og:image" content="https://i.postimg.cc/8PqLq0zN/seo-forecasting.jpg">
    </head>
""", unsafe_allow_html=True)

# Global CSS (unchanged from original)
st.markdown("""
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #10b981;
            --neutral: #374151;
            --background: #f9fafb;
            --error: #ef4444;
        }
        h1, h2, h3, h4, h5, h6 { color: var(--primary); }
        .stSuccess { background-color: var(--secondary) !important; color: white !important; }
        .stError { background-color: var(--error) !important; color: white !important; }
        .stContainer { background-color: var(--background); padding: 20px; border-radius: 8px; border: 1px solid #e5e7eb; }
        .stButton > button { background-color: var(--primary); color: white; border-radius: 8px; border: none; padding: 10px 20px; }
        .stButton > button:hover { background-color: #1d4ed8; }
        .stButton > button[kind="secondary"] { background-color: #6b7280; color: white; }
        .stButton > button[kind="secondary"]:hover { background-color: #4b5563; }
        .tooltip { position: relative; display: inline-block; cursor: pointer; }
        .tooltip .tooltiptext { visibility: hidden; width: 220px; background-color: #555; color: #fff; text-align: center; 
            border-radius: 6px; padding: 8px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -110px; 
            opacity: 0; transition: opacity 0.3s; }
        .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
        .tooltip.active .tooltiptext { visibility: visible; opacity: 1; }
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(tooltip => {
                tooltip.addEventListener('click', function() { this.classList.toggle('active'); });
                document.addEventListener('click', function(e) { if (!tooltip.contains(e.target)) { tooltip.classList.remove('active'); } });
            });
        });
    </script>
""", unsafe_allow_html=True)

# Page title (unchanged)
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
        <svg style='height: 24px; width: 24px; color: #2563eb; margin-right: 8px;' fill='none' stroke='currentColor' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'>
            <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2V9a2 2 0 00-2-2h-2a2 2 0 00-2 2v10'></path>
        </svg>
        <span style='font-size: 14px; color: #2563eb;'>Powered by Boopin</span>
    </div>
    <h1 style='font-size: 2.25rem; font-weight: bold; margin-bottom: 16px;'>EcomSEO Predictor</h1>
    <p style='margin-bottom: 16px; color: #4b5563; font-style: italic;'>Forecast your e-commerce SEO performance with precision—predict traffic, conversions, and revenue growth.</p>
""", unsafe_allow_html=True)

# Progress stepper (unchanged)
st.markdown("""
    <style>
        .stepper { display: flex; justify-content: space-between; margin: 20px 0; padding: 0; list-style: none; }
        .stepper li { flex: 1; text-align: center; position: relative; }
        .stepper li span { display: inline-block; width: 30px; height: 30px; line-height: 30px; border-radius: 50%; 
            background-color: #e5e7eb; color: #4b5563; font-weight: bold; margin-bottom: 8px; }
        .stepper li.active span { background-color: #2563eb; color: white; }
        .stepper li p { margin: 0; font-size: 14px; color: #4b5563; }
        .stepper li:not(:last-child)::after { content: ''; position: absolute; top: 15px; left: 50%; width: 100%; 
            height: 2px; background-color: #e5e7eb; z-index: -1; }
        .stepper li.active:not(:last-child)::after { background-color: #2563eb; }
    </style>
    <ul class='stepper'>
        <li class='active'><span>1</span><p>Configure Settings</p></li>
        <li class='active'><span>2</span><p>Add Keywords</p></li>
        <li><span>3</span><p>Calculate Forecast</p></li>
        <li><span>4</span><p>Explore What-If</p></li>
        <li><span>5</span><p>View Results</p></li>
    </ul>
""", unsafe_allow_html=True)

# Sidebar for settings
st.sidebar.header("Settings")

# Default settings
default_settings = {
    "category": "BBQ & Outdoor Cooking",
    "projection_months": 6,
    "conversion_rate": 3.0,
    "currency_selection": "USD ($)",
    "aov": 250,
    "implementation_cost": 5000,
    "ctr_model": "E-commerce",  # Changed to E-commerce for more realistic default
    "featured_snippet_present": False,
    "in_featured_snippet": False,
    "faq_present": False,
    "in_faq": False
}

# Initialize session state
if 'settings' not in st.session_state:
    st.session_state.settings = default_settings.copy()
else:
    for key, value in default_settings.items():
        if key not in st.session_state.settings:
            st.session_state.settings[key] = value

# Initialize keywords with more ambitious targets
if 'keywords' not in st.session_state:
    st.session_state.keywords = pd.DataFrame({
        "keyword": ["gas bbq", "charcoal bbq", "bbq grill"],
        "searchVolume": [8000, 6500, 5000],
        "position": [8, 12, 9],
        "targetPosition": [1, 3, 2],  # More ambitious targets
        "keywordDifficulty": [5, 5, 5]
    })

# CTR models
ctr_models = {
    "Default": {1: 0.25, 2: 0.15, 3: 0.10, 4: 0.07, 5: 0.07, 6: 0.03, 7: 0.03, 8: 0.03, 9: 0.03, 10: 0.03, 11: 0.01, 20: 0.01, 21: 0.005},
    "E-commerce": {1: 0.30, 2: 0.20, 3: 0.12, 4: 0.08, 5: 0.06, 6: 0.04, 7: 0.03, 8: 0.02, 9: 0.02, 10: 0.01, 11: 0.008, 20: 0.005, 21: 0.002},
    "Informational": {1: 0.35, 2: 0.25, 3: 0.15, 4: 0.10, 5: 0.08, 6: 0.05, 7: 0.04, 8: 0.03, 9: 0.02, 10: 0.01, 11: 0.005, 20: 0.003, 21: 0.001},
    "Custom": {}
}

# Initialize custom CTR with realistic defaults
if 'custom_ctr' not in st.session_state:
    st.session_state.custom_ctr = {pos: ctr_models["E-commerce"][pos] for pos in range(1, 11)}
    st.session_state.custom_ctr['beyond_10'] = 0.005
else:
    # Ensure custom CTR has valid values
    for pos in range(1, 11):
        if pos not in st.session_state.custom_ctr or st.session_state.custom_ctr[pos] == 0.0:
            st.session_state.custom_ctr[pos] = ctr_models["E-commerce"][pos]
    if 'beyond_10' not in st.session_state.custom_ctr or st.session_state.custom_ctr['beyond_10'] == 0.0:
        st.session_state.custom_ctr['beyond_10'] = 0.005

# Modified CTR calculation function
def get_ctr(position, ctr_table, featured_snippet_present=False, in_featured_snippet=False, faq_present=False, in_faq=False):
    position = int(position)
    
    if not ctr_table:  # Custom model
        ctr = st.session_state.custom_ctr.get(position, st.session_state.custom_ctr['beyond_10'])
    else:  # Predefined model
        if position in ctr_table:
            ctr = ctr_table[position]
        else:
            for i in range(position, 0, -1):
                if i in ctr_table:
                    ctr = ctr_table[i]
                    break
            else:
                for i in range(position, 100):
                    if i in ctr_table:
                        ctr = ctr_table[i]
                        break
                else:
                    ctr = 0.005

    # Apply SERP feature modifiers
    if ctr_table and featured_snippet_present:
        if position == 1:
            ctr *= 1.1 if in_featured_snippet else 0.8
        elif 2 <= position <= 5:
            ctr *= 0.9
    if ctr_table and faq_present and position == 1:
        ctr *= 1.1 if in_faq else 0.9

    return max(0.001, ctr)

# Quick Start button
if st.sidebar.button("Quick Start"):
    st.session_state.settings = default_settings.copy()
    st.session_state.settings["conversion_rate"] = 3.0
    st.session_state.settings["aov"] = 250
    st.session_state.settings["implementation_cost"] = 5000
    st.session_state.settings["projection_months"] = 6
    st.session_state.settings["category"] = "Fashion & Apparel"
    st.session_state.settings["currency_selection"] = "USD ($)"
    st.session_state.settings["ctr_model"] = "E-commerce"
    st.rerun()

# Settings inputs (mostly unchanged)
category = st.sidebar.selectbox("Product Category", ["BBQ & Outdoor Cooking", "Christmas & Seasonal", "Fashion & Apparel", 
    "Electronics & Technology", "Gardening & Outdoor", "Furniture & Home"])
projection_months = st.sidebar.radio("Projection Period", [6, 12])
conversion_rate = st.sidebar.slider("Conversion Rate (%)", 0.1, 10.0, st.session_state.settings["conversion_rate"], 0.1)
currency_options = {"GBP (£)": "£", "EUR (€)": "€", "USD ($)": "$", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼"}
currency_selection = st.sidebar.selectbox("Currency", list(currency_options.keys()), 
    index=list(currency_options.keys()).index(st.session_state.settings["currency_selection"]))
currency_symbol = currency_options[currency_selection]
aov = st.sidebar.number_input(f"Average Order Value ({currency_symbol})", 10, 1000, st.session_state.settings["aov"], 10)
implementation_cost = st.sidebar.number_input(f"Implementation Cost ({currency_symbol})", 100, 20000, 
    st.session_state.settings["implementation_cost"], 100)

# CTR Model selection
st.sidebar.markdown("""
    <div style='display: flex; align-items: center; gap: 5px;'>
        <span>CTR Model</span>
        <div class='tooltip'>
            <span style='color: #2563eb;'>ℹ️</span>
            <span class='tooltiptext'>Click-Through Rate (CTR) model determines how likely users are to click on your site based on its search position.</span>
        </div>
    </div>
""", unsafe_allow_html=True)
ctr_model = st.sidebar.selectbox("", list(ctr_models.keys()))

# Custom CTR input
if ctr_model == "Custom":
    st.sidebar.markdown("### Custom CTR Values (%)")
    cols = st.sidebar.columns(5)
    for i in range(1, 11):
        with cols[(i-1) % 5]:
            st.session_state.custom_ctr[i] = st.number_input(f"Pos {i}", min_value=0.0, max_value=100.0, 
                value=st.session_state.custom_ctr[i] * 100, step=0.1, format="%.1f", key=f"custom_ctr_{i}") / 100.0
    st.session_state.custom_ctr['beyond_10'] = st.sidebar.number_input("Positions > 10", min_value=0.0, max_value=100.0, 
        value=st.session_state.custom_ctr['beyond_10'] * 100, step=0.1, format="%.1f") / 100.0

# SERP Features
st.sidebar.markdown("### SERP Features Adjustments")
featured_snippet_present = st.sidebar.checkbox("Featured Snippet Present", value=st.session_state.settings["featured_snippet_present"])
in_featured_snippet = st.sidebar.checkbox("My site is in the Featured Snippet", 
    value=st.session_state.settings["in_featured_snippet"]) if featured_snippet_present else False
faq_present = st.sidebar.checkbox("FAQ Present", value=st.session_state.settings["faq_present"])
in_faq = st.sidebar.checkbox("My site is in the FAQ", value=st.session_state.settings["in_faq"]) if faq_present else False

# Update settings
st.session_state.settings.update({
    "category": category,
    "projection_months": projection_months,
    "conversion_rate": conversion_rate,
    "currency_selection": currency_selection,
    "aov": aov,
    "implementation_cost": implementation_cost,
    "ctr_model": ctr_model,
    "featured_snippet_present": featured_snippet_present,
    "in_featured_snippet": in_featured_snippet,
    "faq_present": faq_present,
    "in_faq": in_faq
})

# Reset button
if st.sidebar.button("Reset to Defaults", type="secondary"):
    for key in ['settings', 'keywords', 'custom_ctr']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Main content (Prepare Your Data section remains largely unchanged)
with st.container():
    st.markdown("### Step 1: Prepare Your Data")
    st.header("Upload Keywords")
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
    with col2:
        st.markdown("#### Supported Formats\n- CSV files (.csv)\n- Excel files (.xlsx, .xls)\n#### Required Columns\n- Keyword/Search Term\n- Search Volume\n- Current Position (optional)")

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            df.columns = df.columns.str.lower()
            keyword_col = next((col for col in df.columns if any(kw in col for kw in ["keyword", "term", "query", "search term"])), df.columns[0])
            volume_col = next((col for col in df.columns if any(vol in col for vol in ["volume", "search volume", "monthly searches"])), 
                            df.columns[1] if len(df.columns) > 1 else None)
            position_col = next((col for col in df.columns if any(pos in col for pos in ["position", "rank", "ranking", "pos", "serp"])), 
                              df.columns[2] if len(df.columns) > 2 else None)
            difficulty_col = next((col for col in df.columns if any(diff in col for diff in ["difficulty", "keyword difficulty"])), None)
            
            new_df = pd.DataFrame()
            new_df['keyword'] = df[keyword_col]
            new_df['searchVolume'] = pd.to_numeric(df[volume_col], errors='coerce').fillna(0).astype(int) if volume_col else 0
            new_df['position'] = pd.to_numeric(df[position_col], errors='coerce').fillna(20).astype(int) if position_col else 20
            new_df['targetPosition'] = new_df['position'].apply(lambda x: max(1, int(x * 0.5)))
            new_df['keywordDifficulty'] = pd.to_numeric(df[difficulty_col], errors='coerce').clip(1, 10).fillna(5).astype(int) if difficulty_col else 5
            
            st.session_state.keywords = new_df
            st.success(f"Successfully imported {len(new_df)} keywords!")
        except Exception as e:
            st.error(f"Error processing file: {e}")

    st.header("Keywords")
    with st.expander("Add New Keyword"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1: new_keyword = st.text_input("Keyword")
        with col2: new_volume = st.number_input("Search Volume", 0, 1000000, 1000)
        with col3: new_position = st.number_input("Current Position", 1, 100, 10)
        with col4: new_target = st.number_input("Target Position", 1, 100, 5)
        with col5:
            st.markdown("""
                <div style='display: flex; align-items: center; gap: 5px;'>
                    <span>Keyword Difficulty</span>
                    <div class='tooltip'><span style='color: #2563eb;'>ℹ️</span>
                    <span class='tooltiptext'>A score from 1 to 10 indicating how hard it is to rank for this keyword.</span></div>
                </div>
            """, unsafe_allow_html=True)
            new_difficulty = st.number_input("", 1, 10, 5)
        
        if st.button("Add Keyword", key="add_keyword") and new_keyword:
            new_row = pd.DataFrame({"keyword": [new_keyword], "searchVolume": [new_volume], "position": [new_position], 
                                   "targetPosition": [new_target], "keywordDifficulty": [new_difficulty]})
            st.session_state.keywords = pd.concat([st.session_state.keywords, new_row], ignore_index=True)
            st.success("Keyword added!")

    edited_df = st.data_editor(st.session_state.keywords, num_rows="dynamic", hide_index=True, 
        column_config={
            "keyword": st.column_config.TextColumn("Keyword"),
            "searchVolume": st.column_config.NumberColumn("Search Volume", min_value=0, format="%d"),
            "position": st.column_config.NumberColumn("Current Position", min_value=1, max_value=100, step=1),
            "targetPosition": st.column_config.NumberColumn("Target Position", min_value=1, max_value=100, step=1),
            "keywordDifficulty": st.column_config.NumberColumn("Keyword Difficulty", min_value=1, max_value=10, step=1)
        }, use_container_width=True)
    st.session_state.keywords = edited_df

    if st.button("Preview Forecast"):
        if len(st.session_state.keywords) > 0:
            keywords = st.session_state.keywords.copy()
            selected_ctr_table = {} if ctr_model == "Custom" else ctr_models[ctr_model]
            keywords['currentCTR'] = keywords['position'].apply(lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq))
            keywords['adjustedTargetPosition'] = keywords.apply(
                lambda row: max(1, int(row['position'] - (row['position'] - row['targetPosition']) * (1 - row['keywordDifficulty'] / 15))), axis=1)  # Adjusted divisor
            keywords['targetCTR'] = keywords['adjustedTargetPosition'].apply(lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq))
            keywords['currentTraffic'] = keywords['searchVolume'] * keywords['currentCTR']
            keywords['targetTraffic'] = keywords['searchVolume'] * keywords['targetCTR']
            traffic_gain = (keywords['targetTraffic'] - keywords['currentTraffic']).sum()
            st.info(f"**Estimated Traffic Gain**: {int(traffic_gain):,} visitors per month")
        else:
            st.warning("Please add at least one keyword.")

    if st.button("Clear Keywords"):
        st.session_state.keywords = pd.DataFrame(columns=["keyword", "searchVolume", "position", "targetPosition", "keywordDifficulty"])
        st.rerun()

# Calculate button
st.markdown("""
    <style>
        .calculate-button { display: flex; justify-content: center; margin: 20px 0; }
        .calculate-button button { display: flex; align-items: center; gap: 8px; font-size: 16px; font-weight: bold; }
        .calculate-button button:hover { transform: scale(1.05); transition: transform 0.2s ease-in-out; }
    </style>
    <div class='calculate-button'>
""", unsafe_allow_html=True)
calculate_button = st.button("Calculate Forecast 📊", type="primary", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# What-If Analysis (unchanged except for CTR table selection)
st.header("What-If Analysis")
with st.expander("Adjust Conversion Rate"):
    col1, col2 = st.columns(2)
    with col1: min_conversion = st.number_input("Minimum Conversion Rate (%)", 0.1, 10.0, conversion_rate - 1.0, 0.1)
    with col2: max_conversion = st.number_input("Maximum Conversion Rate (%)", 0.1, 10.0, conversion_rate + 1.0, 0.1)

    if st.button("Run What-If Analysis"):
        if min_conversion >= max_conversion:
            st.error("Minimum conversion rate must be less than maximum conversion rate.")
        else:
            steps = 5
            conversion_range = np.linspace(min_conversion, max_conversion, steps)
            what_if_data = []
            selected_ctr_table = {} if ctr_model == "Custom" else ctr_models[ctr_model]

            for cr in conversion_range:
                keywords = st.session_state.keywords.copy()
                keywords['adjustedTargetPosition'] = keywords.apply(
                    lambda row: max(1, int(row['position'] - (row['position'] - row['targetPosition']) * (1 - row['keywordDifficulty'] / 15))), axis=1)
                current_traffic = keywords['position'].apply(lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq)) * keywords['searchVolume']
                target_traffic = keywords['adjustedTargetPosition'].apply(lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq)) * keywords['searchVolume']
                traffic_gain = target_traffic - current_traffic
                conversion_gain = traffic_gain * (cr / 100)
                revenue_gain = conversion_gain * aov

                what_if_data.append({
                    "Conversion Rate (%)": cr,
                    "Traffic Gain": int(traffic_gain.sum()),
                    "Conversion Gain": int(round(conversion_gain.sum())),
                    "Revenue Gain": f"{currency_symbol}{int(revenue_gain.sum()):,}"
                })

            what_if_df = pd.DataFrame(what_if_data)
            st.dataframe(what_if_df, hide_index=True, column_config={
                "Conversion Rate (%)": st.column_config.NumberColumn(format="%.1f"),
                "Traffic Gain": st.column_config.NumberColumn(format="%d"),
                "Conversion Gain": st.column_config.NumberColumn("Conversions", format="%d"),
                "Revenue Gain": "Revenue Gain"
            }, use_container_width=True)

            fig = px.line(what_if_df, x="Conversion Rate (%)", y=["Traffic Gain", "Conversion Gain"], 
                         title="Impact of Conversion Rate on Forecast", labels={"value": "Metric Value", "variable": "Metric"})
            fig.update_traces(mode="lines+markers")
            st.plotly_chart(fig, use_container_width=True)

# Forecast calculation with fixes
if calculate_button:
    if len(st.session_state.keywords) > 0:
        keywords = st.session_state.keywords.copy()
        selected_ctr_table = {} if ctr_model == "Custom" else ctr_models[ctr_model]
        
        # Calculate CTRs and traffic
        keywords['currentCTR'] = keywords['position'].apply(
            lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq))
        keywords['adjustedTargetPosition'] = keywords.apply(
            lambda row: max(1, min(row['position'], int(row['position'] - (row['position'] - row['targetPosition']) * (1 - row['keywordDifficulty'] / 15)))), axis=1)
        keywords['targetCTR'] = keywords['adjustedTargetPosition'].apply(
            lambda pos: get_ctr(pos, selected_ctr_table, featured_snippet_present, in_featured_snippet, faq_present, in_faq))
        keywords['currentTraffic'] = keywords['searchVolume'] * keywords['currentCTR']
        keywords['targetTraffic'] = keywords['searchVolume'] * keywords['targetCTR']
        keywords['trafficGain'] = keywords['targetTraffic'] - keywords['currentTraffic']
        keywords['conversionGain'] = keywords['trafficGain'] * (conversion_rate / 100)
        keywords['revenueGain'] = keywords['conversionGain'] * aov
        
        # Confidence intervals
        ctr_std = 0.10
        z_score = 1.96
        keywords['currentTraffic_std'] = keywords['searchVolume'] * keywords['currentCTR'] * ctr_std
        keywords['targetTraffic_std'] = keywords['searchVolume'] * keywords['targetCTR'] * ctr_std
        keywords['trafficGain_std'] = np.sqrt(keywords['currentTraffic_std']**2 + keywords['targetTraffic_std']**2)
        
        total_traffic_gain = keywords['trafficGain'].sum()
        total_traffic_gain_std = np.sqrt((keywords['trafficGain_std']**2).sum())
        traffic_ci_lower = total_traffic_gain - z_score * total_traffic_gain_std
        traffic_ci_upper = total_traffic_gain + z_score * total_traffic_gain_std
        
        total_conversion_gain = int(round(keywords['conversionGain'].sum()))
        total_conversion_gain_std = total_traffic_gain_std * (conversion_rate / 100)
        conversion_ci_lower = int(round(total_conversion_gain - z_score * total_conversion_gain_std))
        conversion_ci_upper = int(round(total_conversion_gain + z_score * total_conversion_gain_std))
        
        total_revenue_gain = total_conversion_gain * aov
        total_revenue_gain_std = total_conversion_gain_std * aov
        revenue_ci_lower = total_revenue_gain - z_score * total_revenue_gain_std
        revenue_ci_upper = total_revenue_gain + z_score * total_revenue_gain_std
        
        cpa = implementation_cost / total_conversion_gain if total_conversion_gain > 0 else float('inf')
        
        # Display results
        st.header("Forecast Results")
        st.markdown("""
            <style>
            .tooltip { position: relative; display: inline-block; cursor: pointer; }
            .tooltip .tooltiptext { visibility: hidden; width: 220px; background-color: #555; color: #fff; text-align: center; 
                border-radius: 6px; padding: 5px; position: absolute; z-index: 1; bottom: 125%; left: 50%; margin-left: -110px; 
                opacity: 0; transition: opacity 0.3s; }
            .tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
            .ci-text { font-size: 12px; color: #666; margin-top: -8px; }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        traffic_percent = keywords['trafficGain'].sum() / keywords['currentTraffic'].sum() * 100 if keywords['currentTraffic'].sum() != 0 else 0
        conv_percent = total_conversion_gain / (keywords['currentTraffic'].sum() * conversion_rate / 100) * 100 if keywords['currentTraffic'].sum() != 0 else 0
        revenue_percent = total_revenue_gain / (keywords['currentTraffic'].sum() * conversion_rate / 100 * aov) * 100 if keywords['currentTraffic'].sum() != 0 else 0
        
        with col1:
            st.markdown("""<div class="tooltip">Total Traffic Gain<span class="tooltiptext">This range shows where we expect the true traffic gain to fall, with 95% confidence.</span></div>""", unsafe_allow_html=True)
            st.metric("", f"{int(total_traffic_gain):,}", f"{traffic_percent:+.1f}%")
            st.markdown(f'<div class="ci-text">95% CI: {int(traffic_ci_lower):,} - {int(traffic_ci_upper):,}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown("""<div class="tooltip">Total Conversion Gain<span class="tooltiptext">This range shows where we expect the true number of conversions to fall, with 95% confidence.</span></div>""", unsafe_allow_html=True)
            st.metric("", f"{total_conversion_gain:,}", f"{conv_percent:+.1f}%")
            st.markdown(f'<div class="ci-text">95% CI: {conversion_ci_lower:,} - {conversion_ci_upper:,}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown("""<div class="tooltip">Total Revenue Gain<span class="tooltiptext">This range shows where we expect the true revenue gain to fall, with 95% confidence.</span></div>""", unsafe_allow_html=True)
            st.metric("", f"{currency_symbol}{int(total_revenue_gain):,}", f"{revenue_percent:+.1f}%")
            revenue_ci_lower_display = f"{int(revenue_ci_lower/1000)}K" if revenue_ci_lower >= 10000 else f"{int(revenue_ci_lower)}"
            revenue_ci_upper_display = f"{int(revenue_ci_upper/1000)}K" if revenue_ci_upper >= 10000 else f"{int(revenue_ci_upper)}"
            st.markdown(f'<div class="ci-text">95% CI: {currency_symbol}{revenue_ci_lower_display} - {currency_symbol}{revenue_ci_upper_display}</div>', unsafe_allow_html=True)
        with col4:
            st.markdown("Cost Per Acquisition (CPA)")
            st.metric("", f"{currency_symbol}{cpa:.2f}" if cpa != float('inf') else "N/A")
        
        # Break-even analysis
        st.markdown("### Break-Even Analysis")
        monthly_data_temp = []
        cumulative_traffic = 0
        cumulative_conversions = 0
        cumulative_revenue = 0
        current_month = pd.Timestamp.now().month - 1
        seasonality = {
            "BBQ & Outdoor Cooking": [0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 2.0, 1.5, 1.0, 0.7, 0.7, 0.6],
            "Christmas & Seasonal": [0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 2.5],
            "Fashion & Apparel": [1.0, 0.8, 1.2, 1.5, 1.3, 1.0, 1.0, 1.5, 1.8, 1.3, 2.0, 1.8],
            "Electronics & Technology": [1.0, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1.0, 1.1, 1.3, 2.2, 2.5],
            "Gardening & Outdoor": [0.5, 0.7, 1.3, 1.8, 2.0, 1.8, 1.5, 1.3, 1.1, 0.8, 0.6, 0.5],
            "Furniture & Home": [1.2, 1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.2, 1.3, 1.2, 1.2, 0.9]
        }
        
        for i in range(projection_months):
            month_idx = (current_month + i) % 12
            month_name = pd.Timestamp(year=2023, month=month_idx+1, day=1).strftime('%b')
            progress = i / (projection_months - 1) if projection_months > 1 else 1
            avg_difficulty = keywords['keywordDifficulty'].mean()
            k = 10 / (1 + avg_difficulty / 2)
            delay = 0.2
            growth_factor = 1 / (1 + np.exp(-k * (progress - delay)))
            season_factor = seasonality[category][month_idx]
            month_factor = growth_factor * season_factor
            traffic_gain = total_traffic_gain * month_factor / sum([1 / (1 + np.exp(-k * (j / (projection_months - 1) - delay))) * 
                                                                 seasonality[category][(current_month + j) % 12] 
                                                                 for j in range(projection_months)])
            conversion_gain = traffic_gain * (conversion_rate / 100)
            revenue_gain = conversion_gain * aov
            cumulative_traffic += traffic_gain
            cumulative_conversions += conversion_gain
            cumulative_revenue += revenue_gain
            monthly_data_temp.append({"Month": month_name, "Cumulative Revenue": cumulative_revenue})
        
        break_even_month = next((i + 1 for i, row in enumerate(monthly_data_temp) if row['Cumulative Revenue'] >= implementation_cost), None)
        
        if break_even_month:
            st.markdown(f"""
                <div style='background-color: #e6f3ff; padding: 20px; border-radius: 10px; border: 2px solid #2563eb; margin: 20px 0;'>
                    <h3 style='color: #2563eb; margin-top: 0;'>🎯 Break-Even Point Reached</h3>
                    <p style='font-size: 18px; margin: 0;'>Achieved in <b>month {break_even_month}</b> with a cumulative revenue of <b>{currency_symbol}{int(monthly_data_temp[break_even_month-1]['Cumulative Revenue']):,}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style='background-color: #ffe6e6; padding: 20px; border-radius: 10px; border: 2px solid #ff4d4d; margin: 20px 0;'>
                    <h3 style='color: #ff4d4d; margin-top: 0;'>⚠️ Break-Even Point Not Reached</h3>
                    <p style='font-size: 18px; margin: 0;'>Not achieved within {projection_months} months. Final cumulative revenue: <b>{currency_symbol}{int(cumulative_revenue):,}</b>.</p>
                </div>
            """, unsafe_allow_html=True)
        
        break_even_df = pd.DataFrame(monthly_data_temp)
        fig = px.line(break_even_df, x="Month", y="Cumulative Revenue", title="Break-Even Progress Over Time", 
                     labels={"Cumulative Revenue": f"Cumulative Revenue ({currency_symbol})"})
        fig.add_hline(y=implementation_cost, line_dash="dash", line_color="red", annotation_text="Break-Even Point", annotation_position="top right")
        fig.update_traces(mode="lines+markers")
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly Projections
        st.header(f"Monthly Projections ({projection_months} Months)")
        monthly_data = []
        cumulative_traffic = 0
        cumulative_conversions = 0
        cumulative_revenue = 0
        
        for i in range(projection_months):
            month_idx = (current_month + i) % 12
            month_name = pd.Timestamp(year=2023, month=month_idx+1, day=1).strftime('%b')
            progress = i / (projection_months - 1) if projection_months > 1 else 1
            growth_factor = 1 / (1 + np.exp(-k * (progress - delay)))
            season_factor = seasonality[category][month_idx]
            month_factor = growth_factor * season_factor
            traffic_gain = total_traffic_gain * month_factor / sum([1 / (1 + np.exp(-k * (j / (projection_months - 1) - delay))) * 
                                                                 seasonality[category][(current_month + j) % 12] 
                                                                 for j in range(projection_months)])
            conversion_gain = int(round(traffic_gain * (conversion_rate / 100)))
            revenue_gain = conversion_gain * aov
            cumulative_traffic += traffic_gain
            cumulative_conversions += conversion_gain
            cumulative_revenue += revenue_gain
            monthly_cost = implementation_cost if i == 0 else 0
            roi = ((revenue_gain - monthly_cost) / implementation_cost) * 100 if implementation_cost > 0 else 0
            cumulative_roi = ((cumulative_revenue - implementation_cost) / implementation_cost) * 100 if implementation_cost > 0 else 0
            
            monthly_data.append({
                "Month": month_name, "Traffic Gain": int(traffic_gain), "Conversion Gain": conversion_gain,
                "Revenue": f"{currency_symbol}{int(revenue_gain):,}", "ROI": f"{roi:.1f}%", "Cumulative": f"{cumulative_roi:.1f}%",
                "Revenue Gain": int(revenue_gain)
            })
        
        monthly_data.append({
            "Month": "TOTAL", "Traffic Gain": int(cumulative_traffic), "Conversion Gain": int(cumulative_conversions),
            "Revenue": f"{currency_symbol}{int(cumulative_revenue):,}", "ROI": "", "Cumulative": f"{cumulative_roi:.1f}%",
            "Revenue Gain": int(cumulative_revenue)
        })
        
        monthly_df = pd.DataFrame(monthly_data)
        st.dataframe(monthly_df[["Month", "Traffic Gain", "Conversion Gain", "Revenue", "ROI", "Cumulative"]], hide_index=True, 
            column_config={"Traffic Gain": st.column_config.NumberColumn(format="%d"), "Conversion Gain": st.column_config.NumberColumn("Conversions", format="%d")}, 
            use_container_width=True)
        
        st.subheader("Monthly Projection Chart")
        fig = px.line(monthly_df[:-1], x="Month", y=["Traffic Gain", "Revenue Gain"], title=f"SEO Performance Forecast for {projection_months} Months",
                     labels={"value": "Metric Value", "variable": "Metric"})
        fig.update_traces(mode="lines+markers")
        fig.update_layout(yaxis_title="Traffic", yaxis2=dict(title="Revenue", overlaying="y", side="right"))
        st.plotly_chart(fig, use_container_width=True)
        
        # Keyword Details
        st.header("Keyword Details")
        keyword_display = keywords.copy()
        keyword_display['Current Traffic'] = keyword_display['currentTraffic'].round(0).astype(int)
        keyword_display['Target Traffic'] = keyword_display['targetTraffic'].round(0).astype(int)
        keyword_display['Traffic Gain'] = keyword_display['trafficGain'].round(0).astype(int)
        keyword_display['Revenue Gain'] = keyword_display['revenueGain'].round(0).astype(int).apply(lambda x: f"{currency_symbol}{x}")
        keyword_display['Traffic Gain %'] = keyword_display.apply(lambda row: f"{(row['trafficGain'] / row['currentTraffic'] * 100):.1f}%" if row['currentTraffic'] != 0 else "0.0%", axis=1)
        
        st.dataframe(keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'keywordDifficulty', 'adjustedTargetPosition', 
                                     'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Traffic Gain %', 'Revenue Gain']], 
                     hide_index=True, use_container_width=True)
        
        csv = keyword_display.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results as CSV", csv, "seo_forecast_results.csv", "text/csv")
    else:
        st.warning("Please add at least one keyword before calculating the forecast.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/boopin/seo-ecom-forecaster)")
