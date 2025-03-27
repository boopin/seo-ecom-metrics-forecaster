# E-Com SEO Metrics Predictor

An interactive web application to forecast SEO performance, traffic, conversions, and revenue based on keyword rankings.

## Features

- **File Upload**: Import keywords from CSV and Excel files
- **Keyword Management**: Add, edit, and remove keywords
- **Multi-Currency Support**: GBP, EUR, USD, AED, SAR
- **Category-Specific Forecasting**: Built-in seasonality models for different e-commerce categories
- **Flexible Projections**: 6-month and 12-month forecasting options
- **Detailed Metrics**: Traffic, conversion, and revenue projections with 95% confidence intervals
- **ROI Analysis**: First-month, ongoing, and cumulative ROI calculations
- **Visualizations**: Interactive charts for performance tracking
- **Custom CTR Model**: Define your own click-through rates for positions 1-10 and beyond, with realistic defaults (e.g., 30% for position 1)
- **SERP Feature Adjustments**: Adjust CTRs for featured snippets and FAQs, with custom control options

## Installation

1. Clone this repository: 
git clone https://github.com/yourusername/seo-forecasting-tool.git
cd seo-forecasting-tool

2. Install the required dependencies:
pip install -r requirements.txt

3. Run the application:
streamlit run app.py


## Usage

### File Upload
- Upload your keywords CSV or Excel file using the file uploader
- The tool supports various column formats from SEO tools like SEMrush, Ahrefs, etc.

### Manual Keyword Entry
- Add keywords manually using the "Add New Keyword" form
- Edit existing keywords directly in the table

### Configuring Settings
- Select product category to apply appropriate seasonality factors
- Choose projection period (6 or 12 months)
- Set your conversion rate and average order value
- Input implementation cost for ROI calculations
- Select your preferred currency
- Choose a CTR model: "Default", "E-commerce", "Informational", or "Custom"
  - For "Custom", set your own CTR values (e.g., enter 20 for 20% at position 1)
- Adjust SERP features: Check "Featured Snippet Present" or "FAQ Present" and specify if your site appears in them

### Generating Forecasts
- Click "Calculate Forecast" to generate predictions
- View summary metrics (traffic, conversions, revenue) with confidence intervals
- Explore detailed monthly projections in the table and chart
- Use "What-If Analysis" to test different conversion rates

## How It Works

1. **CTR Model**: Estimates traffic based on search position using industry-standard CTR curves ("Default", "E-commerce", "Informational") or user-defined custom CTRs with realistic defaults (e.g., 30% for position 1, decreasing to 0.5% beyond 10)
2. **SERP Adjustments**: Modifies CTRs for featured snippets (e.g., +10% if your site is in it, -20% if not) and FAQs (+10% if included, -10% if not), with manual control for custom CTRs
3. **Growth Model**: Uses a sigmoid function to model realistic SEO improvement over time
4. **Seasonality**: Applies category-specific seasonal multipliers for each month
5. **Conversion Modeling**: Calculates conversions and revenue based on user-defined rates
6. **ROI Calculation**: Computes return on investment metrics including initial costs

## Input File Format

The tool accepts CSV and Excel files with the following columns:
- **Keyword**: The search term (also accepts "term", "query", "search term")
- **Search Volume**: Monthly searches (also accepts "volume", "monthly searches")
- **Current Position**: Current ranking (also accepts "rank", "ranking", "position")
- **Target Position (optional)**: Desired ranking position
- **Keyword Difficulty (optional)**: Difficulty score (1-10)

## Example

For a dataset of BBQ-related keywords:
1. Upload your keywords from a SEMrush export
2. Select "BBQ & Outdoor Cooking" as the category
3. Set projection period to 6 months
4. Enter your site's conversion rate (e.g., 3%)
5. Set average order value (e.g., £250)
6. Choose "Custom" CTR model and adjust values (e.g., Position 1: 25, Position 2: 15, Position 3: 10, beyond 10: 0.5)
7. Check "Featured Snippet Present" and "My site is in the Featured Snippet" for relevant keywords
8. Click "Calculate Forecast"

The tool will show you expected traffic, conversion, and revenue improvements over the next 6 months, factoring in summer peak seasonality for BBQ products, custom CTRs, and a CTR boost from the featured snippet.

## Deployment

This application can be deployed for free on Streamlit Cloud:

1. Push your code to GitHub
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your GitHub repository
4. Deploy the application

## License

MIT

## Author

Boopin SEO Team
