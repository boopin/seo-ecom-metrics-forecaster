import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional, Union, Tuple, Any
from datetime import datetime
import base64
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="SEO Forecasting Tool",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define types
KeywordData = pd.DataFrame
ProjectionData = List[Dict[str, Any]]

# App title
st.title("SEO Forecasting Tool")
st.markdown("Forecast traffic, conversions, and revenue based on keyword ranking improvements")

# Sidebar for settings
st.sidebar.header("Settings")

# Add Reset to Defaults button
if st.sidebar.button("Reset to Defaults"):
    for key in ["keywords", "print_mode", "what_if_analysis"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()

category = st.sidebar.selectbox(
    "Product Category",
    ["BBQ & Outdoor Cooking", "Christmas & Seasonal", "Fashion & Apparel", 
     "Electronics & Technology", "Gardening & Outdoor", "Furniture & Home"],
    help="Select your product category to apply appropriate seasonality factors"
)

projection_months = st.sidebar.radio(
    "Projection Period", 
    [6, 12], 
    help="Number of months to project SEO performance"
)

conversion_rate = st.sidebar.slider(
    "Conversion Rate (%)", 
    0.1, 10.0, 3.0, 0.1,
    help="The percentage of visitors who make a purchase (e.g., 3% means 3 out of 100 visitors convert)"
)

currency_options = {"GBP (£)": "£", "EUR (€)": "€", "USD ($)": "$", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼"}
currency_selection = st.sidebar.selectbox(
    "Currency", 
    list(currency_options.keys()),
    help="Select your preferred currency for monetary values"
)
currency_symbol = currency_options[currency_selection]

aov = st.sidebar.number_input(
    f"Average Order Value ({currency_symbol})", 
    10, 1000, 250, 10,
    help="The average amount spent when a customer makes a purchase"
)

implementation_cost = st.sidebar.number_input(
    f"Implementation Cost ({currency_symbol})", 
    100, 20000, 5000, 100,
    help="Total cost of implementing SEO improvements (developer time, content creation, etc.)"
)

# Add confidence interval setting
confidence_level = st.sidebar.slider(
    "Confidence Level (%)", 
    50, 95, 80,
    help="Level of certainty for projections. Higher values create wider ranges for estimates."
)

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
    st.markdown("- Difficulty (optional)")

# Initialize data
if 'keywords' not in st.session_state:
    st.session_state.keywords = pd.DataFrame({
        "keyword": ["gas bbq", "charcoal bbq", "bbq grill"],
        "searchVolume": [8000, 6500, 5000],
        "position": [8, 12, 9],
        "targetPosition": [3, 5, 4],
        "difficulty": [50, 65, 40]  # Added difficulty column
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
        difficulty_cols = ["difficulty", "competition", "comp", "keyword difficulty", "kd"]
        
        # Find the right columns (case insensitive)
        df.columns = df.columns.str.lower()
        
        keyword_col = next((col for col in df.columns if any(kw in col for kw in keyword_cols)), df.columns[0])
        volume_col = next((col for col in df.columns if any(vol in col for vol in volume_cols)), 
                        df.columns[1] if len(df.columns) > 1 else None)
        position_col = next((col for col in df.columns if any(pos in col for pos in position_cols)), 
                          df.columns[2] if len(df.columns) > 2 else None)
        difficulty_col = next((col for col in df.columns if any(diff in col for diff in difficulty_cols)), None)
        
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
            
        # Add difficulty if present, otherwise use default
        if difficulty_col:
            new_df['difficulty'] = pd.to_numeric(df[difficulty_col], errors='coerce').fillna(50).clip(1, 100).astype(int)
        else:
            new_df['difficulty'] = 50
            
        # Calculate target position based on current position and difficulty
        def calculate_target_position(row):
            current_pos = row['position']
            difficulty = row['difficulty']
            
            if difficulty < 30:  # Easy keywords
                improvement = current_pos * 0.7  # 70% improvement
            elif difficulty < 70:  # Medium keywords
                improvement = current_pos * 0.4  # 40% improvement
            else:  # Hard keywords
                improvement = current_pos * 0.2  # 20% improvement
                
            return max(1, int(current_pos - improvement))
        
        new_df['targetPosition'] = new_df.apply(calculate_target_position, axis=1)
        
        st.session_state.keywords = new_df
        st.success(f"Successfully imported {len(new_df)} keywords!")
        
    except Exception as e:
        st.error(f"Error processing file: {e}")

# Display and edit keywords
st.header("Keywords")

# Add new keyword form
with st.expander("Add New Keyword"):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        new_keyword = st.text_input("Keyword", help="Enter the search term you want to rank for")
    with col2:
        new_volume = st.number_input("Search Volume", 0, 1000000, 1000, help="Monthly searches for this keyword")
    with col3:
        new_position = st.number_input("Current Position", 1, 100, 10, help="Your current ranking position in search results")
    with col4:
        new_target = st.number_input("Target Position", 1, 100, 5, help="Your target ranking position after SEO improvements")
    with col5:
        new_difficulty = st.slider("Difficulty", 1, 100, 50, help="How hard it is to rank for this keyword (1=easy, 100=hard)")
        
    if st.button("Add Keyword"):
        if new_keyword:
            new_row = pd.DataFrame({
                "keyword": [new_keyword],
                "searchVolume": [new_volume],
                "position": [new_position],
                "targetPosition": [new_target],
                "difficulty": [new_difficulty]
            })
            st.session_state.keywords = pd.concat([st.session_state.keywords, new_row], ignore_index=True)
            st.success("Keyword added!")

# Display editable table
edited_df = st.data_editor(
    st.session_state.keywords,
    num_rows="dynamic",
    hide_index=True,
    column_config={
        "keyword": st.column_config.TextColumn("Keyword", help="The search term you want to rank for"),
        "searchVolume": st.column_config.NumberColumn("Search Volume", min_value=0, format="%d", help="Monthly searches for this keyword"),
        "position": st.column_config.NumberColumn("Current Position", min_value=1, max_value=100, step=1, help="Your current ranking position in search results"),
        "targetPosition": st.column_config.NumberColumn("Target Position", min_value=1, max_value=100, step=1, help="Your target ranking position after SEO improvements"),
        "difficulty": st.column_config.SliderColumn("Difficulty", min_value=1, max_value=100, step=1, help="How hard it is to rank for this keyword (1=easy, 100=hard)")
    }
)
st.session_state.keywords = edited_df

# Add "What-If" Analysis
if 'what_if_analysis' not in st.session_state:
    st.session_state.what_if_analysis = False

if st.checkbox("Enable What-If Analysis", value=st.session_state.what_if_analysis):
    st.session_state.what_if_analysis = True
    
    with st.expander("What-If Analysis", expanded=True):
        what_if_variable = st.selectbox(
            "Select variable to analyze:",
            ["Conversion Rate", "Average Order Value", "Target Positions"]
        )
        
        if what_if_variable == "Conversion Rate":
            min_value = st.slider("Minimum value (%)", 0.1, 10.0, max(0.1, conversion_rate - 2), 0.1)
            max_value = st.slider("Maximum value (%)", min_value, 15.0, min(15.0, conversion_rate + 2), 0.1)
            step = (max_value - min_value) / 4
            values = [round(v, 1) for v in np.arange(min_value, max_value + step/2, step)]
        
        elif what_if_variable == "Average Order Value":
            min_value = st.slider(f"Minimum value ({currency_symbol})", 10, 1000, max(10, aov - 100), 10)
            max_value = st.slider(f"Maximum value ({currency_symbol})", min_value, 2000, min(2000, aov + 100), 10)
            step = (max_value - min_value) / 4
            values = [round(v) for v in np.arange(min_value, max_value + step/2, step)]
        
        elif what_if_variable == "Target Positions":
            base_improvement = st.slider("Position improvement (%)", 10, 90, 50, 5, 
                              help="How much to improve positions (e.g., 50% means moving from position 10 to position 5)")
            # Will be used later in the calculation
else:
    st.session_state.what_if_analysis = False

# Add print-friendly option
col1, col2 = st.columns([1, 4])
with col1:
    print_button = st.button("Print-Friendly View", help="Generate a printer-friendly version of results")
with col2:
    download_csv = st.checkbox("Include CSV download links", value=True, help="Add downloadable CSV files in the results")

if print_button:
    st.session_state.print_mode = True

if st.session_state.get("print_mode", False):
    st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 0;}
    [data-testid="stSidebar"] {display: none;}
    button[kind="primary"] {display: none;}
    .stCheckbox {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Calculate button
calculate_button = st.button("Calculate Forecast", type="primary", use_container_width=True)

# Helper functions
def get_ctr(position: int) -> float:
    """Calculate CTR based on position."""
    if position == 1: return 0.25
    elif position == 2: return 0.15
    elif position == 3: return 0.10
    elif position <= 5: return 0.07
    elif position <= 10: return 0.03
    elif position <= 20: return 0.01
    else: return 0.005

def calculate_forecast(
    keywords: pd.DataFrame, 
    conversion_rate: float, 
    aov: float,
    what_if_params: Optional[Dict] = None
) -> Dict[str, Union[pd.DataFrame, float]]:
    """Calculate forecast metrics from keywords data with optional what-if parameters."""
    
    # Make a copy of the input data
    df = keywords.copy()
    
    # Apply what-if changes if provided
    if what_if_params:
        if what_if_params.get("variable") == "Target Positions":
            improvement = what_if_params.get("improvement", 50) / 100
            df["targetPosition"] = df["position"].apply(lambda pos: max(1, int(pos * (1 - improvement))))
        
        # Other what-if parameters are handled at the end
    
    # Calculate basic metrics
    df['currentCTR'] = df['position'].apply(get_ctr)
    df['targetCTR'] = df['targetPosition'].apply(get_ctr)
    df['currentTraffic'] = df['searchVolume'] * df['currentCTR']
    df['targetTraffic'] = df['searchVolume'] * df['targetCTR']
    df['trafficGain'] = df['targetTraffic'] - df['currentTraffic']
    
    # Apply conversion rate and AOV with what-if values if specified
    cr = what_if_params.get("conversion_rate", conversion_rate) if what_if_params else conversion_rate
    order_value = what_if_params.get("aov", aov) if what_if_params else aov
    
    df['conversionGain'] = df['trafficGain'] * (cr / 100)
    df['revenueGain'] = df['conversionGain'] *
    df['conversionGain'] = df['trafficGain'] * (cr / 100)
    df['revenueGain'] = df['conversionGain'] * order_value
    
    # Calculate totals
    results = {
        "keywords": df,
        "totalCurrentTraffic": df['currentTraffic'].sum(),
        "totalTargetTraffic": df['targetTraffic'].sum(),
        "totalTrafficGain": df['trafficGain'].sum(),
        "totalCurrentConversions": df['currentTraffic'].sum() * (cr / 100),
        "totalTargetConversions": df['targetTraffic'].sum() * (cr / 100),
        "totalConversionGain": df['conversionGain'].sum(),
        "totalCurrentRevenue": df['currentTraffic'].sum() * (cr / 100) * order_value,
        "totalTargetRevenue": df['targetTraffic'].sum() * (cr / 100) * order_value,
        "totalRevenueGain": df['revenueGain'].sum(),
    }
    
    # Calculate percentages
    if results["totalCurrentTraffic"] > 0:
        results["totalTrafficGainPercentage"] = (results["totalTrafficGain"] / results["totalCurrentTraffic"]) * 100
    else:
        results["totalTrafficGainPercentage"] = 0
        
    if results["totalCurrentConversions"] > 0:
        results["totalConversionGainPercentage"] = (results["totalConversionGain"] / results["totalCurrentConversions"]) * 100
    else:
        results["totalConversionGainPercentage"] = 0
        
    if results["totalCurrentRevenue"] > 0:
        results["totalRevenueGainPercentage"] = (results["totalRevenueGain"] / results["totalCurrentRevenue"]) * 100
    else:
        results["totalRevenueGainPercentage"] = 0
    
    return results

def generate_monthly_projections(
    total_traffic_gain: float,
    total_conversion_gain: float,
    total_revenue_gain: float,
    category: str,
    projection_months: int,
    implementation_cost: float,
    confidence_level: int
) -> List[Dict]:
    """Generate month-by-month projections with confidence intervals."""
    
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
    current_month = datetime.now().month - 1
    
    # Create monthly projections
    monthly_data = []
    cumulative_traffic = 0
    cumulative_conversions = 0
    cumulative_revenue = 0
    
    # Calculate uncertainty based on confidence level
    # Higher confidence = wider intervals
    uncertainty_factor = (confidence_level / 100) * 0.5  # 80% confidence = ±40% range
    
    for i in range(projection_months):
        # Calculate month index
        month_idx = (current_month + i) % 12
        month_name = datetime(year=2023, month=month_idx+1, day=1).strftime('%b')
        
        # Calculate growth factor using sigmoid function
        progress = i / (projection_months - 1) if projection_months > 1 else 1
        growth_factor = 1 / (1 + np.exp(-10 * (progress - 0.5)))
        
        # Get seasonal factor
        season_factor = seasonality[category][month_idx]
        
        # Calculate gains for this month
        month_factor = growth_factor * season_factor
        
        # Calculate denominator for normalization
        normalization_factor = sum([
            1 / (1 + np.exp(-10 * (j / (projection_months - 1) - 0.5))) * seasonality[category][(current_month + j) % 12] 
            for j in range(projection_months)
        ]) if projection_months > 1 else 1
        
        traffic_gain = total_traffic_gain * month_factor / normalization_factor
        conversion_gain = total_conversion_gain * month_factor / normalization_factor
        revenue_gain = total_revenue_gain * month_factor / normalization_factor
        
        # Calculate confidence intervals
        traffic_min = traffic_gain * (1 - uncertainty_factor)
        traffic_max = traffic_gain * (1 + uncertainty_factor)
        revenue_min = revenue_gain * (1 - uncertainty_factor)
        revenue_max = revenue_gain * (1 + uncertainty_factor)
        
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
            "Traffic Range": f"{int(traffic_min)} - {int(traffic_max)}",
            "Conversion Gain": round(conversion_gain, 1),
            "Revenue Gain": int(revenue_gain),
            "Revenue Range": f"{int(revenue_min)} - {int(revenue_max)}",
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
        "Traffic Range": "",
        "Conversion Gain": round(cumulative_conversions, 1),
        "Revenue Gain": int(cumulative_revenue),
        "Revenue Range": "",
        "Revenue": f"{currency_symbol}{int(cumulative_revenue):,}",
        "Monthly ROI": None,
        "Cumulative ROI": cumulative_roi,
        "ROI": "",
        "Cumulative": f"{cumulative_roi:.1f}%"
    })
    
    return monthly_data

def to_excel_download_link(df, filename="data.xlsx", text="Download Excel file"):
    """Generate a link to download the DataFrame as an Excel file."""
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    b64 = base64.b64encode(processed_data).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">{text}</a>'

def to_csv_download_link(df, filename="data.csv", text="Download CSV file"):
    """Generate a link to download the DataFrame as a CSV file."""
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'

if calculate_button or st.session_state.get("print_mode", False):
    # Calculate base forecast
    if len(st.session_state.keywords) > 0:
        results = calculate_forecast(st.session_state.keywords, conversion_rate, aov)
        
        # Display summary metrics
        st.header("Forecast Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Traffic Gain", f"{int(results['totalTrafficGain']):,}", 
                    f"+{results['totalTrafficGainPercentage']:.1f}%")
        with col2:
            st.metric("Total Conversion Gain", f"{results['totalConversionGain']:.1f}", 
                    f"+{results['totalConversionGainPercentage']:.1f}%")
        with col3:
            st.metric("Total Revenue Gain", f"{currency_symbol}{int(results['totalRevenueGain']):,}", 
                    f"+{results['totalRevenueGainPercentage']:.1f}%")
        
        # Generate monthly projections
        monthly_data = generate_monthly_projections(
            results['totalTrafficGain'],
            results['totalConversionGain'],
            results['totalRevenueGain'],
            category,
            projection_months,
            implementation_cost,
            confidence_level
        )
        
        # Display monthly projections
        st.header(f"Monthly Projections ({projection_months} Months)")
        
        # Format the metrics for display
        display_df = pd.DataFrame([
            {
                "Month": m["Month"],
                "Traffic Gain": m["Traffic Gain"],
                "Traffic Range": m["Traffic Range"] if m["Month"] != "TOTAL" else "",
                "Conversions": m["Conversion Gain"],
                "Revenue": m["Revenue"],
                "Revenue Range": m["Revenue Range"] if m["Month"] != "TOTAL" else "",
                "Monthly ROI": m["ROI"],
                "Cumulative ROI": m["Cumulative"]
            } for m in monthly_data
        ])
        
        st.dataframe(
            display_df,
            hide_index=True,
            column_config={
                "Month": "Month",
                "Traffic Gain": st.column_config.NumberColumn("Traffic", format="%d"),
                "Traffic Range": "Traffic Range (±)",
                "Conversions": st.column_config.NumberColumn("Conversions", format="%.1f"),
                "Revenue": "Revenue",
                "Revenue Range": "Revenue Range (±)",
                "Monthly ROI": "Monthly ROI",
                "Cumulative ROI": "Cumulative ROI"
            }
        )
        
        # Offer downloadable CSV if requested
        if download_csv and not st.session_state.get("print_mode", False):
            st.markdown(to_csv_download_link(display_df, "monthly_projections.csv", "📥 Download Monthly Projections CSV"), unsafe_allow_html=True)
        
        # Create break-even analysis
        st.header("Break-Even Analysis")
        
        # Calculate cumulative revenue for each month
        cumulative_revenue = np.cumsum([m["Revenue Gain"] for m in monthly_data[:-1]])  # Exclude total row
        
        # Find break-even point
        break_even_month = None
        for i, rev in enumerate(cumulative_revenue):
            if rev >= implementation_cost:
                break_even_month = i
                break
        
        if break_even_month is not None:
            st.success(f"You'll recover your {currency_symbol}{implementation_cost:,} investment by **{monthly_data[break_even_month]['Month']}** (Month {break_even_month + 1}).")
            
            # Create break-even chart
            break_even_data = pd.DataFrame({
                "Month": [m["Month"] for m in monthly_data[:-1]],
                "Cumulative Revenue": cumulative_revenue,
                "Investment": [implementation_cost] * len(monthly_data[:-1])
            })
            
            fig = px.line(break_even_data, x="Month", y=["Cumulative Revenue", "Investment"],
                        title="Break-Even Analysis", markers=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"The investment of {currency_symbol}{implementation_cost:,} will not be recovered within the {projection_months} month forecast period.")
        
        # Create visualization with plotly
        st.subheader("Monthly Projection Chart")
        
        chart_data = pd.DataFrame({
            "Month": [m["Month"] for m in monthly_data[:-1]],  # Exclude total row
            "Traffic Gain": [m["Traffic Gain"] for m in monthly_data[:-1]],
            "Revenue Gain": [m["Revenue Gain"] for m in monthly_data[:-1]]
        })
        
        fig = px.line(
            chart_data,
            x="Month",
            y=["Traffic Gain", "Revenue Gain"],
            title=f"SEO Performance Forecast for {projection_months} Months",
            labels={"value": "Metric Value", "variable": "Metric"},
            template="plotly_white"
        )
        
        # Add confidence intervals
        if confidence_level > 50:
            traffic_upper = [m["Traffic Gain"] * (1 + (confidence_level / 100) * 0.5) for m in monthly_data[:-1]]
            traffic_lower = [m["Traffic Gain"] * (1 - (confidence_level / 100) * 0.5) for m in monthly_data[:-1]]
            
            fig.add_trace(go.Scatter(
                name='Traffic Upper Bound',
                x=chart_data["Month"],
                y=traffic_upper,
                mode='lines',
                line=dict(width=0),
                showlegend=False
            ))
            
            fig.add_trace(go.Scatter(
                name='Traffic Lower Bound',
                x=chart_data["Month"],
                y=traffic_lower,
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(0, 0, 255, 0.1)',
                fill='tonexty',
                showlegend=False
            ))
        
        # Add markers to the lines
        fig.update_traces(mode="lines+markers")
        
        # Customize the
        # Add markers to the lines
        fig.update_traces(mode="lines+markers")
        
        # Customize the legend
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Keyword Contribution Analysis
        st.header("Keyword Contribution Analysis")
        
        # Create a DataFrame with contribution percentages
        keyword_df = results["keywords"]
        contributions = pd.DataFrame({
            "Keyword": keyword_df["keyword"],
            "Traffic Gain": keyword_df["trafficGain"].round(0).astype(int),
            "Traffic %": (keyword_df["trafficGain"] / keyword_df["trafficGain"].sum() * 100).round(1),
            "Revenue Gain": (keyword_df["revenueGain"]).round(0).astype(int),
            "Revenue %": (keyword_df["revenueGain"] / keyword_df["revenueGain"].sum() * 100).round(1),
            "Revenue Value": currency_symbol + keyword_df["revenueGain"].round(0).astype(int).astype(str)
        })
        
        # Display as a table with sorting
        st.dataframe(
            contributions.sort_values("Revenue %", ascending=False),
            hide_index=True,
            column_config={
                "Keyword": "Keyword",
                "Traffic Gain": st.column_config.NumberColumn("Traffic Gain", format="%d"),
                "Traffic %": "Traffic Contribution (%)",
                "Revenue Gain": st.column_config.NumberColumn("Revenue Gain", format="%d"),
                "Revenue %": "Revenue Contribution (%)",
                "Revenue Value": "Revenue Value"
            }
        )
        
        # Offer downloadable CSV if requested
        if download_csv and not st.session_state.get("print_mode", False):
            st.markdown(to_csv_download_link(contributions, "keyword_contributions.csv", "📥 Download Keyword Contributions CSV"), unsafe_allow_html=True)
        
        # Visualize as a pie chart
        if not contributions.empty and contributions["Revenue %"].sum() > 0:
            fig = px.pie(
                contributions, 
                values="Revenue %", 
                names="Keyword", 
                title="Revenue Contribution by Keyword",
                hover_data=["Revenue Value"]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # What-If Analysis Results
        if st.session_state.get("what_if_analysis", False):
            st.header("What-If Analysis Results")
            
            if what_if_variable == "Conversion Rate":
                what_if_results = []
                
                for cr_value in values:
                    # Calculate with different conversion rate
                    what_if = calculate_forecast(
                        st.session_state.keywords,
                        cr_value,
                        aov,
                        {"variable": "Conversion Rate", "conversion_rate": cr_value}
                    )
                    
                    what_if_results.append({
                        "Conversion Rate": f"{cr_value}%",
                        "Traffic": int(what_if["totalTrafficGain"]),
                        "Conversions": round(what_if["totalConversionGain"], 1),
                        "Revenue": int(what_if["totalRevenueGain"]),
                        "Revenue Value": f"{currency_symbol}{int(what_if['totalRevenueGain']):,}",
                        "ROI": f"{(what_if['totalRevenueGain'] - implementation_cost) / implementation_cost * 100:.1f}%"
                    })
                
                what_if_df = pd.DataFrame(what_if_results)
                st.dataframe(what_if_df)
                
                # Create bar chart
                fig = px.bar(
                    what_if_df,
                    x="Conversion Rate",
                    y="Revenue",
                    title="Impact of Conversion Rate on Revenue",
                    text="Revenue Value"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            elif what_if_variable == "Average Order Value":
                what_if_results = []
                
                for aov_value in values:
                    # Calculate with different AOV
                    what_if = calculate_forecast(
                        st.session_state.keywords,
                        conversion_rate,
                        aov_value,
                        {"variable": "AOV", "aov": aov_value}
                    )
                    
                    what_if_results.append({
                        "Average Order Value": f"{currency_symbol}{aov_value}",
                        "Traffic": int(what_if["totalTrafficGain"]),
                        "Conversions": round(what_if["totalConversionGain"], 1),
                        "Revenue": int(what_if["totalRevenueGain"]),
                        "Revenue Value": f"{currency_symbol}{int(what_if['totalRevenueGain']):,}",
                        "ROI": f"{(what_if['totalRevenueGain'] - implementation_cost) / implementation_cost * 100:.1f}%"
                    })
                
                what_if_df = pd.DataFrame(what_if_results)
                st.dataframe(what_if_df)
                
                # Create bar chart
                fig = px.bar(
                    what_if_df,
                    x="Average Order Value",
                    y="Revenue",
                    title="Impact of Average Order Value on Revenue",
                    text="Revenue Value"
                )
                st.plotly_chart(fig, use_container_width=True)
                
            elif what_if_variable == "Target Positions":
                what_if_results = []
                
                for improvement in [20, 40, 60, 80]:
                    # Calculate with different position improvements
                    what_if = calculate_forecast(
                        st.session_state.keywords,
                        conversion_rate,
                        aov,
                        {"variable": "Target Positions", "improvement": improvement}
                    )
                    
                    what_if_results.append({
                        "Position Improvement": f"{improvement}%",
                        "Traffic": int(what_if["totalTrafficGain"]),
                        "Conversions": round(what_if["totalConversionGain"], 1),
                        "Revenue": int(what_if["totalRevenueGain"]),
                        "Revenue Value": f"{currency_symbol}{int(what_if['totalRevenueGain']):,}",
                        "ROI": f"{(what_if['totalRevenueGain'] - implementation_cost) / implementation_cost * 100:.1f}%"
                    })
                
                what_if_df = pd.DataFrame(what_if_results)
                st.dataframe(what_if_df)
                
                # Create bar chart
                fig = px.bar(
                    what_if_df,
                    x="Position Improvement",
                    y="Revenue",
                    title="Impact of Position Improvement on Revenue",
                    text="Revenue Value"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Keyword details
        st.header("Keyword Details")
        
        # Format data for display
        keyword_display = keyword_df.copy()
        keyword_display['Current Traffic'] = keyword_display['currentTraffic'].round(0).astype(int)
        keyword_display['Target Traffic'] = keyword_display['targetTraffic'].round(0).astype(int)
        keyword_display['Traffic Gain'] = keyword_display['trafficGain'].round(0).astype(int)
        keyword_display['Revenue Gain'] = currency_symbol + keyword_display['revenueGain'].round(0).astype(int).astype(str)
        
        st.dataframe(
            keyword_display[['keyword', 'searchVolume', 'position', 'targetPosition', 'difficulty', 'Current Traffic', 'Target Traffic', 'Traffic Gain', 'Revenue Gain']],
            hide_index=True,
            column_config={
                "keyword": "Keyword",
                "searchVolume": st.column_config.NumberColumn("Search Volume", format="%d"),
                "position": "Current Position",
                "targetPosition": "Target Position",
                "difficulty": "Difficulty",
                "Current Traffic": st.column_config.NumberColumn("Current Traffic", format="%d"),
                "Target Traffic": st.column_config.NumberColumn("Target Traffic", format="%d"),
                "Traffic Gain": st.column_config.NumberColumn("Traffic Gain", format="%d"),
                "Revenue Gain": "Revenue Gain"
            }
        )
        
        # Offer downloadable Excel if requested
        if download_csv and not st.session_state.get("print_mode", False):
            full_results = keyword_display.copy()
            full_results["Month"] = datetime.now().strftime("%B %Y")
            full_results["Category"] = category
            full_results["Conversion Rate"] = f"{conversion_rate}%"
            full_results["AOV"] = f"{currency_symbol}{aov}"
            
            st.markdown(to_excel_download_link(full_results, "seo_forecast_results.xlsx", "📥 Download Complete Results (Excel)"), unsafe_allow_html=True)
        
        # Exit print mode button
        if st.session_state.get("print_mode", False):
            if st.button("Exit Print Mode"):
                st.session_state.print_mode = False
                st.experimental_rerun()
    else:
        st.warning("Please add at least one keyword before calculating the forecast.")

# Add tooltips for key concepts section
with st.expander("💡 Understanding Key Concepts"):
    st.markdown("""
    ### Click-Through Rate (CTR)
    The percentage of users who click on your link when it appears in search results. Higher positions get higher CTRs.
    
    | Position | Estimated CTR |
    |----------|--------------|
    | 1        | 25%          |
    | 2        | 15%          |
    | 3        | 10%          |
    | 4-5      | 7%           |
    | 6-10     | 3%           |
    | 11-20    | 1%           |
    | 21+      | 0.5%         |
    
    ### Difficulty Score
    A measure of how challenging it will be to improve rankings for a keyword:
    - **1-30**: Easy - Can expect significant improvement (70%)
    - **31-70**: Medium - Can expect moderate improvement (40%)
    - **71-100**: Hard - Can expect modest improvement (20%)
    
    ### Confidence Intervals
    The range within which results are likely to fall. Higher confidence levels mean wider ranges:
    - **80% confidence**: About ±40% range around the forecast
    - **95% confidence**: About ±47.5% range around the forecast
    """)
    
    st.markdown("### Seasonality Factors")
    
    # Create a DataFrame for seasonality
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    seasonality_df = pd.DataFrame({
        "Month": months,
        "BBQ": [0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 2.0, 1.5, 1.0, 0.7, 0.7, 0.6],
        "Christmas": [0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 2.5],
        "Fashion": [1.0, 0.8, 1.2, 1.5, 1.3, 1.0, 1.0, 1.5, 1.8, 1.3, 2.0, 1.8],
        "Electronics": [1.0, 0.8, 0.8, 0.9, 0.9, 0.9, 0.9, 1.0, 1.1, 1.3, 2.2, 2.5],
        "Gardening": [0.5, 0.7, 1.3, 1.8, 2.0, 1.8, 1.5, 1.3, 1.1, 0.8, 0.6, 0.5],
        "Furniture": [1.2, 1.0, 1.1, 1.2, 1.3, 1.3, 1.2, 1.2, 1.3, 1.2, 1.2, 0.9]
    })
    
    # Show the seasonality table
    st.table(seasonality_df)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/boopin/seo-ecom-metrics-forecaster/)")
