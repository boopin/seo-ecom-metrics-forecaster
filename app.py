import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="EcomSEO Predictor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title with styling
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

# Sidebar for settings
st.sidebar.header("Settings")

# Default settings for reset functionality
default_settings = {
    "category": "BBQ & Outdoor Cooking",
    "projection_months": 6,
    "conversion_rate": 3.0,
    "currency_selection": "GBP (£)",
    "aov": 250,
    "implementation_cost": 5000,
    "ctr_model": "Default"
}

# Initialize session state for settings if not already present
if 'settings' not in st.session_state:
    st.session_state.settings = default_settings.copy()

# Define CTR models
ctr_models = {
    "Default": {1: 0.25, 2: 0.15, 3: 0.10, 4: 0.07, 5: 0.07, 6: 0.03, 7: 0.03, 8: 0.03, 9: 0.03, 10: 0.03, 11: 0.01, 20: 0.01, 21: 0.005},
    "E-commerce": {1: 0.30, 2: 0.20, 3: 0.12, 4: 0.08, 5: 0.06, 6: 0.04, 7: 0.03, 8: 0.02, 9: 0.02, 10: 0.01, 11: 0.008, 20: 0.005, 21: 0.002},
    "Informational": {1: 0.35, 2: 0.25, 3: 0.15, 4: 0.10, 5: 0.08, 6: 0.05, 7: 0.04, 8: 0.03, 9: 0.02, 10: 0.01, 11: 0.005, 20: 0.003, 21: 0.001}
}

# CTR calculation function with support for different models
def get_ctr(position, ctr_table):
    position = int(position)
    if position in ctr_table:
        return ctr_table[position]
    # Interpolate or use the closest higher position
    for i in range(position, 0, -1):
        if i in ctr_table:
            return ctr_table[i]
    for i in range(position, 100):
        if i in ctr_table:
            return ctr_table[i]
    return 0.005  # Default for positions beyond 20

# Settings with tooltips
category = st.sidebar.selectbox(
    "Product Category",
    ["BBQ & Outdoor Cooking", "Christmas & Seasonal", "Fashion & Apparel", 
     "Electronics & Technology", "Gardening & Outdoor", "Furniture & Home"],
    help="Select the product category to apply seasonal trends to your forecast."
)
projection_months = st.sidebar.radio(
    "Projection Period",
    [6, 12],
    help="Choose the number of months for the forecast (6 or 12 months)."
)
conversion_rate = st.sidebar.slider(
    "Conversion Rate (%)",
    0.1, 10.0, st.session_state.settings["conversion_rate"], 0.1,
    help="The percentage of visitors who make a purchase (e.g., 3% means 3 out of 100 visitors convert)."
)
currency_options = {"GBP (£)": "£", "EUR (€)": "€", "USD ($)": "$", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼"}
currency_selection = st.sidebar.selectbox(
    "Currency",
    list(currency_options.keys()),
    help="Select the currency for revenue calculations."
)
currency_symbol = currency_options[currency_selection]
aov = st.sidebar.number_input(
    f"Average Order Value ({currency_symbol})",
    10, 1000, st.session_state.settings["aov"], 10,
    help=f"The average amount spent per order in {currency_symbol} (e.g., if a customer typically spends {currency_symbol}250 per purchase, enter 250)."
)
implementation_cost = st.sidebar.number_input(
    f"Implementation Cost ({currency_symbol})",
    100, 20000, st.session_state.settings["implementation_cost"], 100,
    help=f"The total cost of implementing the SEO strategy in {currency_symbol} (e.g., agency fees, content creation)."
)
ctr_model = st.sidebar.selectbox(
    "CTR Model",
    list(ctr_models.keys()),
    help="Select the Click-Through Rate (CTR) model based on your industry. E-commerce sites typically have higher CTRs for top positions, while informational sites have higher CTRs overall but drop off faster."
)

# Update session state settings
st.session_state.settings.update({
    "category": category,
    "projection_months": projection_months,
    "conversion_rate": conversion_rate,
    "currency_selection": currency_selection,
    "aov": aov,
    "implementation_cost": implementation_cost,
    "ctr_model": ctr_model
})

# Reset to Defaults button
if st.sidebar.button("Reset to Defaults"):
    st.session_state.settings = default_settings.copy()
    st.session_state.keywords = pd.DataFrame({
        "keyword": ["gas bbq", "charcoal bbq", "bbq grill"],
        "searchVolume": [8000, 6500, 5000],
        "position": [8, 12, 9],
        "targetPosition": [3, 5, 4],
        "keywordDifficulty": [5, 5, 5]  # Updated to keywordDifficulty
    })
    st.experimental_rerun()

# File upload
st.header("Upload Keywords")
st.markdown("Upload a CSV or Excel file with keywords, search volumes, and current positions")

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"],
        help="Upload a CSV or Excel file containing your keyword data."
    )
with col2:
    st.markdown("#### Supported Formats")
    st.markdown("- CSV files (.csv)")
    st.markdown("- Excel files (.xlsx, .xls)")
    st.markdown("#### Required Columns")
    st.markdown("- Keyword/Search Term")
    st.markdown("- Search Volume")
    st.markdown("- Current Position (optional)")

# Initialize data with keyword difficulty
if 'keywords' not in st.session_state:
    st.session_state.keywords = pd.DataFrame({
        "keyword": ["gas bbq", "charcoal bbq", "bbq grill"],
        "searchVolume": [8000, 6500, 5000],
        "position": [8, 12, 9],
        "targetPosition": [3, 5, 4],
        "keywordDifficulty": [5, 5, 5]  # Updated to keywordDifficulty
    })

# Process uploaded file
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # Try to map columns
        keyword_cols = ["keyword", "term", "query", "search term"]
        volume_cols = ["volume", "search volume", "monthly searches", "monthly search volume", "monthly volume", "searches"]
        position_cols = ["position", "rank", "ranking", "pos", "serp"]
        difficulty_cols = ["difficulty", "keyword difficulty", "kw difficulty", "seo difficulty"]  # Updated to keyword difficulty
        
        # Find the right columns (case insensitive)
        df.columns = df.columns.str.lower()
        
        keyword_col = next((col for col in df.columns if any(kw in col for kw in keyword_cols)), df.columns[0])
        volume_col = next((col for col in df.columns if any(vol in col for vol in volume_cols)), 
                        df.columns[1] if len(df.columns) > 1 else None)
        position_col = next((col for col in df.columns if any(pos in col for pos in position_cols)), 
                          df.columns[2] if len(df.columns) > 2 else None)
        difficulty_col = next((col for col in df.columns if any(diff in col for diff in difficulty_cols)), 
                              None)
        
        # Create new dataframe
        new_df = pd.DataFrame()
        new_df['keyword'] = df[keyword_col]
        
        if volume_col:
            new_df['searchVolume'] = pd.to_numeric(df[volume_col], errors='coerce').fillna(0).astype(int)
        else:
            new_df['searchVolume'] = 0
            
        if position_col:
            new_df['position'] = pd.to_numeric(df[position_col], errors='coerce').fillna(20).astype(int)
        else:
            new_df['position'] = 20
            
        # Calculate target position - improve by 50% but not below 1
        new_df['targetPosition'] = new_df['position'].apply(lambda x: max(1, int(x * 0.5)))
        
        # Add keyword difficulty (default to 5 if not in file)
        if difficulty_col:
            new_df['keywordDifficulty'] = pd.to_numeric(df[difficulty_col], errors='coerce').clip(1, 10).fillna(5).astype(int)
        else:
            new_df['keywordDifficulty'] = 5
        
        st.session_state.keywords = new_df
        st.success(f"Successfully imported {len(new_df)} keywords!")
        
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Display and edit keywords
st.header("Keywords")

# Add new keyword form with tooltips
with st.expander("Add New Keyword"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        new_keyword = st.text_input(
            "Keyword",
            help="Enter the keyword or search term (e.g., 'gas bbq')."
        )
    with col2:
        new_volume = st.number_input(
            "Search Volume",
            0, 1000000, 1000,
            help="The average monthly search volume for the keyword (e.g., 8000 searches per month)."
        )
    with col3:
        new_position = st.number_input(
            "Current Position",
            1, 100, 10,
            help="The current ranking position in search results (1-100, where 1 is the top position)."
        )
    with col4:
        new_target = st.number_input(
            "Target Position",
            1, 100, 5,
            help="The desired ranking position to achieve (1-100, typically better than the current position)."
        )
    with col5:
        new_difficulty = st.number_input(
            "Keyword Difficulty",
            1, 10, 5,
            help="A score from 1 to 10 indicating how difficult it is to rank for this keyword (1 = easy, 10 = very hard)."
        )
        
    if st.button("Add Keyword"):
        if new_keyword:
            new_row = pd.DataFrame({
                "keyword": [new_keyword],
                "searchVolume": [new_volume],
                "position": [new_position],
                "targetPosition": [new_target],
                "keywordDifficulty": [new_difficulty]
            })
            st.session_state.keywords = pd.concat([st.session_state.keywords, new_row], ignore_index=True)
            st.success("Keyword added!")

# Display editable table with responsive design
st.markdown("""
    <style>
        @media (max-width: 640px) {
            .stDataFrame {
                font-size: 12px;
            }
            .stDataFrame th, .stDataFrame td {
                padding: 4px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

edited_df = st.data_editor(
    st.session_state.keywords,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "keyword": st.column_config.TextColumn(
            "Keyword",
            help="The keyword or search term."
        ),
        "searchVolume": st.column_config.NumberColumn(
            "Search Volume",
            min_value=0,
            format="%d",
            help="The average monthly search volume for the keyword."
        ),
        "position": st.column_config.NumberColumn(
            "Current Position",
            min_value=1,
            max_value=100,
            step=1,
            help="The current ranking position in search results (1-100)."
        ),
        "targetPosition": st.column_config.NumberColumn(
            "Target Position",
            min_value=1,
            max_value=100,
            step=1,
            help="The desired ranking position to achieve (1-100)."
        ),
        "keywordDifficulty": st.column_config.NumberColumn(
            "Keyword Difficulty",
            min_value=1,
            max_value=10,
            step=1,
            help="A score from 1 to 10 indicating how difficult it is to rank for this keyword (1 = easy, 10 = very hard)."
        )
    },
    use_container_width=True
)
st.session_state.keywords = edited_df

# What-If Analysis Tool
st.header("What-If Analysis")
st.markdown("Analyze how changes in conversion rate impact your forecast.")

with st.expander("Adjust Conversion Rate"):
    col1, col2 = st.columns(2)
    with col1:
        min_conversion = st.number_input(
            "Minimum Conversion Rate (%)",
            0.1, 10.0, conversion_rate - 1.0, 0.1,
            help="The lower bound for the conversion rate range to analyze."
        )
    with col2:
        max_conversion = st.number_input(
            "Maximum Conversion Rate (%)",
            0.1, 10.0, conversion_rate + 1.0, 0.1,
            help="The upper bound for the conversion rate range to analyze."
        )

    if st.button("Run What-If Analysis"):
        if min_conversion >= max_conversion:
            st.error("Minimum conversion rate must be less than maximum conversion rate.")
        else:
            # Generate range of conversion rates
            steps = 5
            conversion_range = np.linspace(min_conversion, max_conversion, steps)
            what_if_data = []

            # Get the CTR table for the selected model
            selected_ctr_table = ctr_models[ctr_model]

            for cr in conversion_range:
                keywords = st.session_state.keywords.copy()
                # Adjust target position based on keyword difficulty
                keywords['adjustedTargetPosition'] = keywords.apply(
                    lambda row: max(1, int(row['position'] - (row['position'] - row['targetPosition']) * (1 - row['keywordDifficulty'] / 10))), axis=1
                )
                current_traffic = keywords['position'].apply(lambda pos: get_ctr(pos, selected_ctr_table)) * keywords['searchVolume']
                target_traffic = keywords['adjustedTargetPosition'].apply(lambda pos: get_ctr(pos, selected_ctr_table)) * keywords['searchVolume']
                traffic_gain = target_traffic - current_traffic
                conversion_gain = traffic_gain * (cr / 100)
                revenue_gain = conversion_gain * aov

                what_if_data.append({
                    "Conversion Rate (%)": cr,
                    "Traffic Gain": int(traffic_gain.sum()),
                    "Conversion Gain": round(conversion_gain.sum(), 1),
                    "Revenue Gain": f"{currency_symbol}{int(revenue_gain.sum()):,}"
                })

            what_if_df = pd.DataFrame(what_if_data)
            st.dataframe(
                what_if_df,
                hide_index=True,
                column_config={
                    "Conversion Rate (%)": st.column_config.NumberColumn("Conversion Rate (%)", format="%.1f"),
                    "Traffic Gain": st.column_config.NumberColumn("Traffic Gain", format="%d"),
                    "Conversion Gain": st.column_config.NumberColumn("Conversions", format="%.1f"),
                    "Revenue Gain": "Revenue Gain"
                },
                use_container_width=True
            )

            # Plot the what-if analysis
            fig = px.line(
                what_if_df,
                x="Conversion Rate (%)",
                y=["Traffic Gain", "Conversion Gain"],
                title="Impact of Conversion Rate on Forecast",
                labels={"value": "Metric Value", "variable": "Metric"},
                template="plotly_white"
            )
            fig.update_traces(mode="lines+markers")
            fig.update_layout(
                yaxis_title="Traffic / Conversions",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

# Calculate button
calculate_button = st.button("Calculate Forecast", type="primary", use_container_width=True)

if calculate_button:
    if len(st.session_state.keywords) > 0:
        keywords = st.session_state.keywords.copy()
        # Get the CTR table for the selected model
        selected_ctr_table = ctr_models[ctr_model]
        keywords['currentCTR'] = keywords['position'].apply(lambda pos: get_ctr(pos, selected_ctr_table))
        # Adjust target position based on keyword difficulty
        keywords['adjustedTargetPosition'] = keywords.apply(
            lambda row: max(1, int(row['position'] - (row['position'] - row['targetPosition']) * (1 - row['keywordDifficulty'] / 10))), axis=1
        )
        keywords['targetCTR'] = keywords['adjustedTargetPosition'].apply(lambda pos: get_ctr(pos, selected_ctr_table))
        keywords['currentTraffic'] = keywords['searchVolume'] * keywords['currentCTR']
        keywords['targetTraffic'] = keywords['searchVolume'] * keywords['targetCTR']
        keywords['trafficGain'] = keywords['targetTraffic'] - keywords['currentTraffic']
        keywords['conversionGain'] = keywords['trafficGain'] * (conversion_rate / 100)
        keywords['revenueGain'] = keywords['conversionGain'] * aov
        
        # Add confidence intervals
        ctr_std = 0.10  # Assume 10% standard deviation for CTR
        z_score = 1.96  # For 95% confidence interval
        keywords['currentCTR_std'] = keywords['currentCTR'] * ctr_std
        keywords['targetCTR_std'] = keywords['targetCTR'] * ctr_std
        keywords['currentTraffic_std'] = keywords['searchVolume'] * keywords['currentCTR_std']
        keywords['targetTraffic_std'] = keywords['searchVolume'] * keywords['targetCTR_std']
        keywords['trafficGain_std'] = np.sqrt(keywords['currentTraffic_std']**2 + keywords['targetTraffic_std']**2)
        total_traffic_gain = keywords['trafficGain'].sum()
        total_traffic_gain_std = np.sqrt((keywords['trafficGain_std']**2).sum())
        traffic_ci_lower = total_traffic_gain - z_score * total_traffic_gain_std
        traffic_ci_upper = total_traffic_gain + z_score * total_traffic_gain_std
        
        total_conversion_gain = keywords['conversionGain'].sum()
        total_conversion_gain_std = total_traffic_gain_std * (conversion_rate / 100)
        conversion_ci_lower = total_conversion_gain - z_score * total_conversion_gain_std
        conversion_ci_upper = total_conversion_gain + z_score * total_conversion_gain_std
        
        total_revenue_gain = keywords['revenueGain'].sum()
        total_revenue_gain_std = total_conversion_gain_std * aov
        revenue_ci_lower = total_revenue_gain - z_score * total_revenue_gain_std
        revenue_ci_upper = total_revenue_gain + z_score * total_revenue_gain_std
        
        # Display summary metrics with confidence intervals
        st.header("Forecast Results")
        
        col1, col2, col3 = st.columns(3)
        
        # Calculate percentage changes safely
        traffic_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['trafficGain'].sum() / keywords['currentTraffic'].sum() * 100
        conv_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['conversionGain'].sum() / (keywords['currentTraffic'].sum() * conversion_rate / 100) * 100
        revenue_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['revenueGain'].sum() / (keywords['currentTraffic'].sum() * conversion_rate / 100 * aov) * 100
        
        with col1:
            st.metric("Total Traffic Gain", f"{int(total_traffic_gain):,}", 
                      f"+{traffic_percent:.1f}% (95% CI: {int(traffic_ci_lower):,} - {int(traffic_ci_upper):,})")
        with col2:
            st.metric("Total Conversion Gain", f"{total_conversion_gain:.1f}", 
                      f"+{conv_percent:.1f}% (95% CI: {conversion_ci_lower:.1f} - {conversion_ci_upper:.1f})")
        with col3:
            st.metric("Total Revenue Gain", f"{currency_symbol}{int(total_revenue_gain):,}", 
                      f"+{revenue_percent:.1f}% (95% CI: {currency_symbol}{int(revenue_ci_lower):,} - {currency_symbol}{int(revenue_ci_upper):,})")
        
        # Break-Even Analysis (Moved and Enhanced)
        st.markdown("### Break-Even Analysis", unsafe_allow_html=True)
        # Calculate monthly projections for break-even analysis
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
            growth_factor = 1 / (1 + np.exp(-10 * (progress - 0.5)))
            season_factor = seasonality[category][month_idx]
            month_factor = growth_factor * season_factor
            traffic_gain = total_traffic_gain * month_factor / sum([1 / (1 + np.exp(-10 * (j / (projection_months - 1) - 0.5))) * 
                                                                 seasonality[category][(current_month + j) % 12] 
                                                                 for j in range(projection_months)])
            conversion_gain = traffic_gain * (conversion_rate / 100)
            revenue_gain = conversion_gain * aov
            cumulative_traffic += traffic_gain
            cumulative_conversions += conversion_gain
            cumulative_revenue += revenue_gain
            monthly_data_temp.append({
                "Month": month_name,
                "Cumulative Revenue": cumulative_revenue
            })
        
        break_even_month = None
        for i, row in enumerate(monthly_data_temp):
            if row['Cumulative Revenue'] >= implementation_cost and break_even_month is None:
                break_even_month = i + 1
                break
        
        # Display Break-Even Analysis in a styled container
        if break_even_month:
            st.markdown(
                f"""
                <div style='background-color: #e6f3ff; padding: 20px; border-radius: 10px; border: 2px solid #2563eb; margin: 20px 0;'>
                    <h3 style='color: #2563eb; margin-top: 0;'>🎯 Break-Even Point Reached</h3>
                    <p style='font-size: 18px; margin: 0;'>Achieved in <b>month {break_even_month}</b> with a cumulative revenue of <b>{currency_symbol}{int(monthly_data_temp[break_even_month-1]['Cumulative Revenue']):,}</b>.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style='background-color: #ffe6e6; padding: 20px; border-radius: 10px; border: 2px solid #ff4d4d; margin: 20px 0;'>
                    <h3 style='color: #ff4d4d; margin-top: 0;'>⚠️ Break-Even Point Not Reached</h3>
                    <p style='font-size: 18px; margin: 0;'>Not achieved within {projection_months} months. Final cumulative revenue: <b>{currency_symbol}{int(cumulative_revenue):,}</b>.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Generate monthly projections
        st.header(f"Monthly Projections ({projection_months} Months)")
        
        # Define seasonality factors (already defined above, reusing for clarity)
        monthly_data = []
        cumulative_traffic = 0
        cumulative_conversions = 0
        cumulative_revenue = 0
        
        for i in range(projection_months):
            # Calculate month index
            month_idx = (current_month + i) % 12
            month_name = pd.Timestamp(year=2023, month=month_idx+1, day=1).strftime('%b')
            
            # Calculate growth factor using sigmoid function
            progress = i / (projection_months - 1) if projection_months > 1 else 1
            growth_factor = 1 / (1 + np.exp(-10 * (progress - 0.5)))
            
            # Get seasonal factor
            season_factor = seasonality[category][month_idx]
            
            # Calculate gains for this month
            month_factor = growth_factor * season_factor
            traffic_gain = total_traffic_gain * month_factor / sum([1 / (1 + np.exp(-10 * (j / (projection_months - 1) - 0.5))) * 
                                                                 seasonality[category][(current_month + j) % 12] 
                                                                 for j in range(projection_months)])
            
            conversion_gain = traffic_gain * (conversion_rate / 100)
            revenue_gain = conversion_gain * aov
            
            # Update cumulative metrics
            cumulative_traffic += traffic_gain
            cumulative_conversions += conversion_gain
            cumulative_revenue += revenue_gain
            
            # Calculate ROI
            monthly_cost = implementation_cost if i == 0 else 0
            roi = ((revenue_gain - monthly_cost) / implementation_cost) * 100
            cumulative_roi = ((cumulative_revenue - implementation_cost) / implementation_cost) * 100
            
            monthly_data.append({
                "Month": month_name,
                "Growth Factor": growth_factor,
                "Seasonal Factor": season_factor,
                "Traffic Gain": int(traffic_gain),
                "Conversion Gain": round(conversion_gain, 1),
                "Revenue Gain": int(revenue_gain),
                "Revenue": f"{currency_symbol}{int(revenue_gain):,}",
                "Monthly ROI": roi,
                "Cumulative ROI": cumulative_roi,
                "ROI": f"{roi:.1f}%",
                "Cumulative": f"{cumulative_roi:.1f}%",
                "Cumulative Revenue": cumulative_revenue
            })
        
        # Add total row
        monthly_data.append({
            "Month": "TOTAL",
            "Growth Factor": None,
            "Seasonal Factor": None,
            "Traffic Gain": int(cumulative_traffic),
            "Conversion Gain": round(cumulative_conversions, 1),
            "Revenue Gain": int(cumulative_revenue),
            "Revenue": f"{currency_symbol}{int(cumulative_revenue):,}",
            "Monthly ROI": None,
            "Cumulative ROI": cumulative_roi,
            "ROI": "",
            "Cumulative": f"{cumulative_roi:.1f}%",
            "Cumulative Revenue": cumulative_revenue
        })
        
        # Display monthly projections
        monthly_df = pd.DataFrame(monthly_data)
        display_df = monthly_df[["Month", "Traffic Gain", "Conversion Gain", "Revenue", "ROI", "Cumulative"]].copy()
        
        # Format the metrics
        st.dataframe(
            display_df,
            hide_index=True,
            column_config={
                "Month": "Month",
                "Traffic Gain": st.column_config.NumberColumn("Traffic", format="%d"),
                "Conversion Gain": st.column_config.NumberColumn("Conversions", format="%.1f"),
                "Revenue": "Revenue",
                "ROI": "Monthly ROI",
                "Cumulative": "Cumulative ROI"
            },
            use_container_width=True
        )
        
        # Create visualization with plotly
        st.subheader("Monthly Projection Chart")
        
        fig = px.line(
            monthly_df[:-1],  # Exclude the total row
            x="Month",
            y=["Traffic Gain", "Revenue Gain"],
            title=f"SEO Performance Forecast for {projection_months} Months",
            labels={"value": "Metric Value", "variable": "Metric"},
            template="plotly_white"
        )
        
        # Add markers to the lines
        fig.update_traces(mode="lines+markers")
        
        # Update y-axis titles
        fig.update_layout(
            yaxis_title="Traffic",
            yaxis2=dict(
                title="Revenue",
                overlaying="y",
                side="right"
            )
        )
        
        # Customize the legend
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Keyword details
        st.header("Keyword Details")
        
        # Format data for display
        keyword_display = keywords.copy()
        keyword_display['Current Traffic'] = keyword_display['currentTraffic'].round(0).astype(int)
        keyword_display['Target Traffic'] = keyword_display['targetTraffic'].round(0).astype(int)
        keyword_display['Traffic Gain'] = keyword_display['trafficGain'].round(0).astype(int)
        keyword_display['Revenue Gain'] = currency_symbol + keyword_display['revenueGain'].round(0).astype(int).astype(str)
        
        st.dataframe(
            keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'keywordDifficulty', 'adjustedTargetPosition', 'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Revenue Gain']],
            hide_index=True,
            column_config={
                "keyword": "Keyword",
                "searchVolume": st.column_config.NumberColumn("Search Volume", format="%d"),
                "position": "Current Position",
                "targetPosition": "Target Position",
                "keywordDifficulty": "Keyword Difficulty",
                "adjustedTargetPosition": "Adjusted Target Position",
                "Current Traffic": st.column_config.NumberColumn("Current Traffic", format="%d"),
                "Target Traffic": st.column_config.NumberColumn("Target Traffic", format="%d"),
                "Traffic Gain": st.column_config.NumberColumn("Traffic Gain", format="%d"),
                "Revenue Gain": "Revenue Gain"
            },
            use_container_width=True
        )
        
        # Download button for results
        csv = keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'keywordDifficulty', 'adjustedTargetPosition', 'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Revenue Gain']].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="seo_forecast_results.csv",
            mime="text/csv",
        )
    else:
        st.warning("Please add at least one keyword before calculating the forecast.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/boopin/seo-ecom-forecaster)")
