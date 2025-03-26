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

# How to Start Using This Tool (For Non-Tech Users)
st.header("How to Start Using This Tool (For Non-Tech Users)")
st.markdown("""
If you're new to tools like this or not familiar with SEO, don’t worry! We’ll guide you through the basics to get started with EcomSEO Predictor. Follow these simple steps to see how improving your website’s search rankings can help your online store.

1. **Open the Tool**:
   - You’re already on the right page! Look at the sidebar on the left side of the screen. Click on **"Home"** to go to the main tool. It will say "EcomSEO Predictor - Main App" at the top.

2. **Tell the Tool About Your Business**:
   - On the left sidebar, you’ll see a section called **"Settings"**. These are the basic details the tool needs to make predictions for your store:
     - **Product Category**: Choose the type of products you sell (e.g., "Fashion & Apparel" if you sell clothes, or "BBQ & Outdoor Cooking" if you sell grills).
     - **Currency**: Pick the currency you use for your store (e.g., "USD ($)" for US dollars).
     - **Average Order Value**: Enter the average amount a customer spends when they buy from you. For example, if a typical order is $50, type "50".
     - **Implementation Cost**: This is how much you plan to spend on improving your website’s search rankings (e.g., hiring someone to help with SEO). If you’re not sure, you can leave it at $5000 for now.
   - Don’t worry about the other settings for now—they’re already set to good defaults!

3. **Add Your Keywords**:
   - Keywords are the words people type into Google to find your products, like "buy summer dress" or "best BBQ grill".
   - Scroll down to the section called **"Keywords"**. You’ll see a table with some example keywords like "gas bbq".
   - To add your own keywords:
     - Click on the box that says **"Add New Keyword"** to open it.
     - Fill in the details:
       - **Keyword**: Type the search term (e.g., "summer dress").
       - **Search Volume**: This is how many people search for this term each month. If you don’t know, you can guess for now (e.g., 1000).
       - **Current Position**: Where your website shows up in Google for this term (e.g., if you’re on the second page, it might be 15). If you’re not sure, leave it at 10.
       - **Target Position**: Where you’d like to show up (e.g., 3 to be near the top of the first page).
       - **Keyword Difficulty**: How hard it is to rank for this term (1 is easy, 10 is hard). If you’re not sure, leave it at 5.
     - Click the **"Add Keyword"** button to add it to the table.
   - You can add as many keywords as you like!

4. **Run Your Prediction**:
   - Once you’ve added at least one keyword, scroll down and find the big blue button that says **"Calculate Forecast"**.
   - Click this button, and the tool will show you how much extra traffic, sales, and revenue you might get by improving your search rankings.

5. **Look at Your Results**:
   - After clicking "Calculate Forecast", you’ll see a few sections:
     - **Forecast Results**: This shows the total extra visitors, sales, and money you might make.
     - **Break-Even Analysis**: This tells you how long it will take to make back the money you spend on SEO.
     - **Keyword Details**: This shows how each keyword you added will help your store.
   - Don’t worry if some numbers look complicated—the main ones to look at are the "Total Traffic Gain" (more visitors), "Total Conversion Gain" (more sales), and "Total Revenue Gain" (more money).

6. **What’s Next?**:
   - If you like the results, you can start working on your SEO to improve your rankings for those keywords.
   - If you’re not sure what to do next, you can reach out to an SEO expert for help. You can also download your results by clicking **"Download Results as CSV"** at the bottom of the "Keyword Details" section to share with someone who can help.

**You Did It!** 🎉 You’ve just used EcomSEO Predictor to see how SEO can grow your online store. If you get stuck or have questions, check out the "Additional Resources" section below for ways to get help.
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
