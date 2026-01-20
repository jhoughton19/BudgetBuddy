"""
BudgetBuddy Web Application
AI-Powered Budget Analysis for Utah Counties

Designed for 3rd-6th class county finance departments
"""

import streamlit as st
import pandas as pd
import sys
import tempfile
import os
from pathlib import Path
from io import BytesIO

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from data_ingestion import BudgetDataIngester

# Page configuration
st.set_page_config(
    page_title="BudgetBuddy - County Budget Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f4788;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f4788;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def format_currency(value):
    """Format number as currency"""
    return f"${value:,.2f}"

def create_excel_download(ingester):
    """Create Excel file in memory for download"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Detail sheet
        ingester.standardized_data.to_excel(writer, sheet_name='Detail', index=False)
        
        # Fund summary sheet
        summary = ingester.get_fund_summary()
        if not summary.empty:
            summary.to_excel(writer, sheet_name='Fund Summary', index=False)
    
    output.seek(0)
    return output

def main():
    # Header
    st.markdown('<p class="main-header">📊 BudgetBuddy</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Budget Analysis for Utah Counties</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/1f4788/ffffff?text=BudgetBuddy", 
                 use_container_width=True)
        
        st.markdown("### About")
        st.info(
            """
            **BudgetBuddy** streamlines budget book creation and analysis 
            for small county finance departments.
            
            **Perfect for:**
            - 3rd-6th class Utah counties
            - Auditors & Finance Directors
            - Budget preparation season
            """
        )
        
        st.markdown("### Support")
        st.markdown("""
        - 📧 Email: support@budgetbuddy.com
        - 📞 Phone: (555) 123-4567
        - 🌐 [Documentation](https://docs.budgetbuddy.com)
        """)
        
        st.markdown("---")
        st.caption("Built for Utah counties by financial data experts")
    
    # Main content
    st.markdown("## Step 1: Select Your Financial System")
    
    col1, col2 = st.columns(2)
    with col1:
        system_type = st.radio(
            "Which system does your county use?",
            options=["Munis (Tyler Technologies)", "Caselle (Harris Computer)"],
            help="Select your county's financial management system"
        )
    
    system = "munis" if "Munis" in system_type else "caselle"
    
    with col2:
        st.info(f"""
        **Selected: {system_type}**
        
        BudgetBuddy will automatically map your {system_type.split()[0]} 
        export columns to a standardized format.
        """)
    
    st.markdown("---")
    st.markdown("## Step 2: Upload Your Budget Export")
    
    # File upload with instructions
    with st.expander("📋 How to export from your system", expanded=False):
        if system == "munis":
            st.markdown("""
            **Munis Export Instructions:**
            1. Navigate to: General Ledger → Reports → Budget vs Actual
            2. Select: All funds, All departments, Current FY + Prior FY
            3. Include columns: Fund, Department, Account, FY, Budget, Actual, Encumbrance
            4. Export as CSV or Excel
            """)
        else:
            st.markdown("""
            **Caselle Export Instructions:**
            1. Navigate to: Financial Reports → Budget Detail
            2. Select: All funds, Multi-year comparison (minimum 2 years)
            3. Include columns: Fund Code, Dept Code, GL Account, Fiscal Year, Budgeted, Actuals
            4. Export as CSV or Excel
            """)
    
    uploaded_file = st.file_uploader(
        "Upload your budget export file",
        type=['csv', 'xlsx', 'xls'],
        help="Accepts CSV or Excel files from Munis or Caselle"
    )
    
    if uploaded_file is not None:
        st.markdown("---")
        st.markdown("## Step 3: Process & Review")
        
        # Process button
        if st.button("🚀 Process Budget Data", type="primary", use_container_width=True):
            with st.spinner("Processing your budget data..."):
                try:
                    # Initialize ingester
                    ingester = BudgetDataIngester(system_type=system)
                    
                    # Save uploaded file temporarily (Windows-compatible)
                    temp_dir = tempfile.gettempdir()
                    temp_path = os.path.join(temp_dir, uploaded_file.name)
                    with open(temp_path, 'wb') as f:
                        f.write(uploaded_file.getvalue())
                    
                    # Process data
                    ingester.load_file(temp_path)
                    ingester.standardize_columns()
                    is_valid, issues = ingester.validate_data()
                    
                    # Show validation results
                    if not is_valid:
                        st.markdown('<div class="warning-box">', unsafe_allow_html=True)
                        st.warning("⚠️ Data Quality Issues Detected")
                        for issue in issues:
                            st.write(f"- {issue}")
                        st.markdown('</div>', unsafe_allow_html=True)
                        st.info("Proceeding with data cleaning - please review results carefully")
                    
                    # Clean data
                    df = ingester.clean_data()
                    
                    # Success message
                    st.markdown('<div class="success-box">', unsafe_allow_html=True)
                    st.success(f"✓ Successfully processed {len(df):,} budget line items!")
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # Store in session state
                    st.session_state.ingester = ingester
                    st.session_state.processed_data = df
                    st.session_state.is_valid = is_valid
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
                    st.info("Please check that your file matches the expected format for your system")
                    return
        
        # Display results if processed
        if 'processed_data' in st.session_state:
            df = st.session_state.processed_data
            ingester = st.session_state.ingester
            
            st.markdown("---")
            st.markdown("## 📈 Budget Summary")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_budget = df['budgeted_amount'].sum()
            total_actual = df['actual_amount'].sum()
            total_variance = total_actual - total_budget
            variance_pct = (total_variance / total_budget * 100) if total_budget != 0 else 0
            
            with col1:
                st.metric(
                    "Total Budget",
                    format_currency(total_budget),
                    help="Total budgeted amount across all funds"
                )
            
            with col2:
                st.metric(
                    "Actual Spending",
                    format_currency(total_actual),
                    help="Year-to-date actual expenditures"
                )
            
            with col3:
                st.metric(
                    "Variance",
                    format_currency(total_variance),
                    delta=f"{variance_pct:.1f}%",
                    delta_color="inverse",
                    help="Difference between actual and budget"
                )
            
            with col4:
                if 'encumbered_amount' in df.columns:
                    total_encumbered = df['encumbered_amount'].sum()
                    st.metric(
                        "Encumbrances",
                        format_currency(total_encumbered),
                        help="Outstanding purchase orders and commitments"
                    )
            
            # Tabs for different views
            tab1, tab2, tab3 = st.tabs(["📊 Fund Summary", "📋 Detail Data", "📁 Export"])
            
            with tab1:
                st.markdown("### Fund-Level Summary")
                summary = ingester.get_fund_summary()
                
                if not summary.empty:
                    # Format currency columns
                    display_summary = summary.copy()
                    for col in ['budgeted_amount', 'actual_amount', 'variance']:
                        if col in display_summary.columns:
                            display_summary[col] = display_summary[col].apply(format_currency)
                    
                    if 'variance_pct' in display_summary.columns:
                        display_summary['variance_pct'] = display_summary['variance_pct'].apply(
                            lambda x: f"{x:.2f}%"
                        )
                    
                    st.dataframe(
                        display_summary,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # Chart
                    if 'fiscal_year' in summary.columns and len(summary['fiscal_year'].unique()) > 1:
                        st.markdown("### Budget Trends by Fund")
                        
                        chart_data = summary.pivot(
                            index='fiscal_year',
                            columns='fund_code',
                            values='budgeted_amount'
                        )
                        
                        st.line_chart(chart_data)
            
            with tab2:
                st.markdown("### Detailed Budget Data")
                st.info(f"Showing first 100 rows of {len(df):,} total records")
                
                # Format for display
                display_df = df.head(100).copy()
                for col in ['budgeted_amount', 'actual_amount', 'variance']:
                    if col in display_df.columns:
                        display_df[col] = display_df[col].apply(format_currency)
                
                if 'variance_pct' in display_df.columns:
                    display_df['variance_pct'] = display_df['variance_pct'].apply(
                        lambda x: f"{x:.2f}%"
                    )
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            with tab3:
                st.markdown("### Download Standardized Data")
                
                st.info("""
                **What's included:**
                - Detail sheet: All budget line items with calculated fields
                - Fund Summary sheet: Aggregated totals by fund and fiscal year
                - Standardized column names for easy analysis
                """)
                
                # Create download
                excel_file = create_excel_download(ingester)
                
                st.download_button(
                    label="📥 Download Excel Report",
                    data=excel_file,
                    file_name=f"budget_standardized_{pd.Timestamp.now().strftime('%Y%m%d')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary",
                    use_container_width=True
                )
                
                st.markdown("---")
                st.markdown("### 🚀 Coming Soon")
                st.markdown("""
                - **AI Budget Narratives**: Auto-generate GFOA-compliant descriptions
                - **Fund Balance Forecasting**: 3-5 year projections using Prophet
                - **Cost Reduction Recommendations**: AI-powered efficiency analysis
                - **Performance Measures**: Automated metric tracking
                """)
    
    else:
        # Show example/demo section when no file uploaded
        st.markdown("---")
        st.markdown("## 💡 New to BudgetBuddy?")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### ⚡ Fast")
            st.write("Upload your export and get clean, standardized data in seconds")
        
        with col2:
            st.markdown("### ✅ Accurate")
            st.write("Automatic validation ensures data quality before analysis")
        
        with col3:
            st.markdown("### 📊 GFOA Ready")
            st.write("Generate compliant budget narratives and reports")
        
        st.info("""
        **Try it now!** Upload your Munis or Caselle budget export above to see BudgetBuddy in action.
        
        No account required for basic features. Premium features (forecasting, AI narratives) 
        available with subscription starting at $5,000/year.
        """)

if __name__ == "__main__":
    main()