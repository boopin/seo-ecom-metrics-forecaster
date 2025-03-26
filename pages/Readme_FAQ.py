import streamlit as st

# Page title
st.markdown("""
    <div style='display: flex; align-items: center; margin-bottom: 8px;'>
        <svg style='height: 24px; width: 24px; color: #2563eb; margin-right: 8px;' fill='none' stroke='currentColor' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'>
            <path stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2V9a2 2 0 00-2-2h-2a2 2 0 00-2 2v10'></path>
        </svg>
        <span style='font-size: 14px; color: #2563eb;'>Powered by Boopin</span>
    </div>
    <h1 style='font-size: 2.25rem; font-weight: bold; margin-bottom: 16px;'>EcomSEO Predictor - Readme & FAQ</h1>
    <p style='margin-bottom: 16px; color: #4b5563; font-style: italic;'>Everything you need to know to get started with EcomSEO Predictor.</p>
""", unsafe_allow_html=True)

# Introduction
st.header("Welcome to EcomSEO Predictor")
st.markdown("""
EcomSEO Predictor is a powerful tool designed to help e-commerce businesses forecast the potential impact of SEO improvements on their website traffic, conversions, and revenue. Whether you're an SEO professional, a business owner, or a marketer, this tool provides actionable insights to guide your SEO strategy.
""")

# What Can This Tool Do?
st.header("What Can This Tool Do?")
st.markdown("""
- **Forecast SEO Performance**: Predict how improving your search engine rankings for specific keywords will impact your website traffic, conversions, and revenue over a 6 or 12-month period.
- **Keyword Analysis**: Analyze individual keywords to see their current traffic, potential traffic gains, and revenue impact based on target ranking positions.
- **Break-Even Analysis**: Determine how long it will take to recover your SEO investment (implementation cost) based on projected revenue gains.
- **What-If Analysis**: Experiment with different conversion rates to understand how they affect your forecast.
- **Seasonal Adjustments**: Account for seasonal trends in your industry (e.g., BBQ sales peak in summer, Christmas products peak in winter).
- **Confidence Intervals**: Provide 95% confidence intervals for traffic, conversion, and revenue forecasts to account for uncertainty in click-through rates.
- **Export Results**: Download your forecast results as a CSV file for further analysis.
""")

# What Can This Tool Not Do?
st.header("What Can This Tool Not Do?")
st.markdown("""
- **Guarantee Results**: The forecasts are based on assumptions (e.g., click-through rates, conversion rates, average order value) and simplified models. Actual SEO outcomes depend on many factors, including competition, algorithm changes, and execution quality.
- **Replace SEO Expertise**: This tool provides estimates to guide your strategy, but it does not replace the need for professional SEO knowledge and implementation.
- **Account for All Variables**: The tool does not consider external factors like changes in search volume, competitor actions, or Google algorithm updates.
- **Provide Real-Time Data**: Forecasts are based on the data you input (e.g., search volume, current position). The tool does not fetch live data from search engines.
- **Optimize Keywords for You**: While it helps you analyze keywords, it does not suggest or optimize keywords—you need to provide the keywords and their data.
""")

# How to Use This Tool
st.header("How to Use This Tool")
st.markdown("""
Follow these steps to get started with EcomSEO Predictor:

1. **Navigate to the Main App**:
   - Use the sidebar to go to the "Home" page if you're not already there.

2. **Configure Settings**:
   - In the sidebar, adjust the settings to match your business:
     - **Product Category**: Select your industry to apply seasonal trends (e.g., "BBQ & Outdoor Cooking").
     - **Projection Period**: Choose 6 or 12 months for your forecast.
     - **Conversion Rate (%)**: Enter your website's conversion rate (e.g., 3% if 3 out of 100 visitors make a purchase).
     - **Currency**: Select your preferred currency for revenue calculations (e.g., USD, GBP).
     - **Average Order Value (AOV)**: Enter the average amount a customer spends per order (e.g., $250).
     - **Implementation Cost**: Enter the cost of your SEO strategy (e.g., $5000 for agency fees, content creation).
     - **CTR Model**: Choose a click-through rate model based on your industry (e.g., "E-commerce").

3. **Input Keywords**:
   - **Upload a File**: Upload a CSV or Excel file with your keyword data (required columns: Keyword, Search Volume; optional: Current Position).
   - **Manually Add Keywords**: Use the "Add New Keyword" expander to manually enter keywords, their search volumes, current positions, target positions, and keyword difficulty (1-10).
   - **Edit Keywords**: Use the table to edit or delete keywords as needed.

4. **Run the Forecast**:
   - Click the "Calculate Forecast" button to generate your SEO performance forecast.
   - Review the results in the following sections:
     - **Forecast Results**: See the total traffic gain, conversion gain, revenue gain, and cost per acquisition (CPA), with 95% confidence intervals.
     - **Break-Even Analysis**: Understand when you'll recover your SEO investment.
     - **Monthly Projections**: View a month-by-month breakdown of traffic, conversions, and revenue.
     - **Keyword Details**: Analyze the impact of each keyword, including traffic and revenue gains (both absolute and percentage).

5. **Experiment with What-If Analysis**:
   - Use the "What-If Analysis" section to test how different conversion rates affect your forecast.

6. **Download Results**:
   - At the bottom of the "Keyword Details" section, click "Download Results as CSV" to export your forecast data.

**Tip**: If you need to start over, click "Reset to Defaults" in the sidebar to restore the default settings and keywords.
""")

# Additional Resources
st.header("Additional Resources")
st.markdown("""
- **GitHub Repository**: Visit the [GitHub Repo](https://github.com/boopin/seo-ecom-forecaster) for the source code and to report issues.
- **Support**: For questions or support, contact the Boopin team via the GitHub repository.
""")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/boopin/seo-ecom-forecaster)")
