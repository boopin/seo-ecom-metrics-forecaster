import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from io import StringIO

# Page configuration
st.set_page_config(
    page_title="SEO Forecasting Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# App title
st.title("SEO Forecasting Tool")
st.markdown("Forecast traffic, conversions, and revenue based on keyword ranking improvements")

# Sidebar for settings
st.sidebar.header("Settings")
category = st.sidebar.selectbox(
    "Product Category",
    ["BBQ & Outdoor Cooking", "Christmas & Seasonal", "Fashion & Apparel", 
     "Electronics & Technology", "Gardening & Outdoor", "Furniture & Home"]
)
projection_months = st.sidebar.radio("Projection Period", [6, 12])
conversion_rate = st.sidebar.slider("Conversion Rate (%)", 0.1, 10.0, 3.0, 0.1)
currency_options = {"GBP (£)": "£", "EUR (€)": "€", "USD ($)": "$", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼"}
currency_selection = st.sidebar.selectbox("Currency", list(currency_options.keys()))
currency_symbol = currency_options[currency_selection]
aov = st.sidebar.number_input(f"Average Order Value ({currency_symbol})", 10, 1000, 250, 10)
implementation_cost = st.sidebar.number_input(f"Implementation Cost ({currency_symbol})", 100, 20000, 5000, 100)

# File upload
st.header("Upload Keywords")
st.markdown("Upload a CSV or Excel file with keywords, search volumes, and current positions")

col1, col2 = st.columns([2, 1])
with col1:
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls"])
with col2:
    st.markdown("#### Supported Formats")
    st.markdown("- CSV files (.csv)")
    st.markdown("- Excel files (.xlsx, .xls)")
    st.markdown("#### Required Columns")
    st.markdown("- Keyword/Search Term")
    st.markdown("- Search Volume")
    st.markdown("- Current Position (optional)")

# Initialize data
if 'keywords' not in st.session_state:
    st.session_state.keywords = pd.DataFrame({
        "keyword": ["gas bbq", "charcoal bbq", "bbq grill"],
        "searchVolume": [8000, 6500, 5000],
        "position": [8, 12, 9],
        "targetPosition": [3, 5, 4]
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
        
        # Find the right columns (case insensitive)
        df.columns = df.columns.str.lower()
        
        keyword_col = next((col for col in df.columns if any(kw in col for kw in keyword_cols)), df.columns[0])
        volume_col = next((col for col in df.columns if any(vol in col for vol in volume_cols)), 
                        df.columns[1] if len(df.columns) > 1 else None)
        position_col = next((col for col in df.columns if any(pos in col for pos in position_cols)), 
                          df.columns[2] if len(df.columns) > 2 else None)
        
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
        
        st.session_state.keywords = new_df
        st.success(f"Successfully imported {len(new_df)} keywords!")
        
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Display and edit keywords
st.header("Keywords")

# Add new keyword form
with st.expander("Add New Keyword"):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        new_keyword = st.text_input("Keyword")
    with col2:
        new_volume = st.number_input("Search Volume", 0, 1000000, 1000)
    with col3:
        new_position = st.number_input("Current Position", 1, 100, 10)
    with col4:
        new_target = st.number_input("Target Position", 1, 100, 5)
        
    if st.button("Add Keyword"):
        if new_keyword:
            new_row = pd.DataFrame({
                "keyword": [new_keyword],
                "searchVolume": [new_volume],
                "position": [new_position],
                "targetPosition": [new_target]
            })
            st.session_state.keywords = pd.concat([st.session_state.keywords, new_row], ignore_index=True)
            st.success("Keyword added!")

# Display editable table
edited_df = st.data_editor(
    st.session_state.keywords,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "keyword": st.column_config.TextColumn("Keyword"),
        "searchVolume": st.column_config.NumberColumn("Search Volume", min_value=0, format="%d"),
        "position": st.column_config.NumberColumn("Current Position", min_value=1, max_value=100, step=1),
        "targetPosition": st.column_config.NumberColumn("Target Position", min_value=1, max_value=100, step=1)
    }
)
st.session_state.keywords = edited_df

# Calculate button
calculate_button = st.button("Calculate Forecast", type="primary", use_container_width=True)

if calculate_button:
    # CTR calculation function
    def get_ctr(position):
        if position == 1: return 0.25
        elif position == 2: return 0.15
        elif position == 3: return 0.10
        elif position <= 5: return 0.07
        elif position <= 10: return 0.03
        elif position <= 20: return 0.01
        else: return 0.005
    
    # Calculate metrics
    if len(st.session_state.keywords) > 0:
        keywords = st.session_state.keywords.copy()
        keywords['currentCTR'] = keywords['position'].apply(get_ctr)
        keywords['targetCTR'] = keywords['targetPosition'].apply(get_ctr)
        keywords['currentTraffic'] = keywords['searchVolume'] * keywords['currentCTR']
        keywords['targetTraffic'] = keywords['searchVolume'] * keywords['targetCTR']
        keywords['trafficGain'] = keywords['targetTraffic'] - keywords['currentTraffic']
        keywords['conversionGain'] = keywords['trafficGain'] * (conversion_rate / 100)
        keywords['revenueGain'] = keywords['conversionGain'] * aov
        
        # Display summary metrics
        st.header("Forecast Results")
        
        col1, col2, col3 = st.columns(3)
        
        # Calculate percentage changes safely
        traffic_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['trafficGain'].sum() / keywords['currentTraffic'].sum() * 100
        conv_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['conversionGain'].sum() / (keywords['currentTraffic'].sum() * conversion_rate / 100) * 100
        revenue_percent = 0 if keywords['currentTraffic'].sum() == 0 else keywords['revenueGain'].sum() / (keywords['currentTraffic'].sum() * conversion_rate / 100 * aov) * 100
        
        with col1:
            st.metric("Total Traffic Gain", f"{int(keywords['trafficGain'].sum()):,}", 
                    f"+{traffic_percent:.1f}%")
        with col2:
            st.metric("Total Conversion Gain", f"{keywords['conversionGain'].sum():.1f}", 
                    f"+{conv_percent:.1f}%")
        with col3:
            st.metric("Total Revenue Gain", f"{currency_symbol}{int(keywords['revenueGain'].sum()):,}", 
                    f"+{revenue_percent:.1f}%")
        
        # Generate monthly projections
        st.header(f"Monthly Projections ({projection_months} Months)")
        
        # Define seasonality factors
        seasonality = {
            "BBQ & Outdoor Cooking": [0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 2.0, 1.5, 1.0, 0.7, 0.7, 0.6],
            "Christmas & Seasonal": [0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 2.5],
            "Fashion & Apparel": [1.0, 0.8, 1.2, 1.5, 1.3, 1.0, 1.0, 1.5, 1.8, 1.3, 2.0, 1.8],
            "Electronics & Technology": [1.0, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1.0, 1.1, 1.3, 2.2, 2.5],
            "Gardening & Outdoor": [0.5, 0.7, 1.3, 1.8, 2.0, 1.8, 1.5, 1.3, 1.1, 0.8, 0.6, 0.5],
            "Furniture & Home": [1.2, 1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.2, 1.3, 1.2, 1.2, 0.9]
        }
        
        # Get current month index (0-11)
        current_month = pd.Timestamp.now().month - 1
        
        # Total metrics to distribute
        total_traffic_gain = keywords['trafficGain'].sum()
        total_conversion_gain = keywords['conversionGain'].sum()
        total_revenue_gain = keywords['revenueGain'].sum()
        
        # Create monthly projections
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
                "Cumulative": f"{cumulative_roi:.1f}%"
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
            "Cumulative": f"{cumulative_roi:.1f}%"
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
            }
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
            keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Revenue Gain']],
            hide_index=True,
            column_config={
                "keyword": "Keyword",
                "searchVolume": st.column_config.NumberColumn("Search Volume", format="%d"),
                "position": "Current Position",
                "targetPosition": "Target Position",
                "Current Traffic": st.column_config.NumberColumn("Current Traffic", format="%d"),
                "Target Traffic": st.column_config.NumberColumn("Target Traffic", format="%d"),
                "Traffic Gain": st.column_config.NumberColumn("Traffic Gain", format="%d"),
                "Revenue Gain": "Revenue Gain"
            }
        )
        
        # Download button for results
        csv = keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Revenue Gain']].to_csv(index=False).encode('utf-8')
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
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/yourusername/seo-forecasting-tool)")
