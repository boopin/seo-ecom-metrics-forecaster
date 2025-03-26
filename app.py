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
            "Revenue Value": f"{currency_symbol}" + keyword_df["revenueGain"].round(0).astype(int).astype(str)
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
st.markdown("Built with Streamlit • [GitHub Repo](https://github.com/yourusername/seo-forecasting-tool)")
