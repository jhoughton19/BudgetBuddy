"""
BudgetBuddy Data Ingestion Module
Handles Munis and Caselle financial system exports

Key Functions:
- Parse CSV/Excel exports from Munis/Caselle
- Standardize data structure across systems
- Validate and clean fund/account data
- Prepare data for forecasting and narrative generation
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class BudgetDataIngester:
    """Main class for ingesting and standardizing budget data"""
    
    # Standard column mappings for different systems
    MUNIS_COLUMN_MAP = {
        'Fund': 'fund_code',
        'Department': 'dept_code',
        'Account': 'account_code',
        'FY': 'fiscal_year',
        'Budget': 'budgeted_amount',
        'Actual': 'actual_amount',
        'Encumbrance': 'encumbered_amount',
        'Description': 'description'
    }
    
    CASELLE_COLUMN_MAP = {
        'Fund Code': 'fund_code',
        'Dept Code': 'dept_code',
        'GL Account': 'account_code',
        'Fiscal Year': 'fiscal_year',
        'Budgeted': 'budgeted_amount',
        'Actuals': 'actual_amount',
        'Encumbrances': 'encumbered_amount',
        'Account Description': 'description'
    }
    
    def __init__(self, system_type: str = 'munis'):
        """
        Initialize ingester for specific financial system
        
        Args:
            system_type: 'munis' or 'caselle'
        """
        self.system_type = system_type.lower()
        self.column_map = self._get_column_map()
        self.raw_data = None
        self.standardized_data = None
        
    def _get_column_map(self) -> Dict:
        """Get appropriate column mapping for system type"""
        if self.system_type == 'munis':
            return self.MUNIS_COLUMN_MAP
        elif self.system_type == 'caselle':
            return self.CASELLE_COLUMN_MAP
        else:
            raise ValueError(f"Unsupported system type: {self.system_type}")
    
    def load_file(self, filepath: str) -> pd.DataFrame:
        """
        Load export file (CSV or Excel)
        
        Args:
            filepath: Path to export file
            
        Returns:
            Raw DataFrame
        """
        file_path = Path(filepath)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        # Determine file type and load
        if file_path.suffix.lower() in ['.xlsx', '.xls']:
            self.raw_data = pd.read_excel(filepath)
        elif file_path.suffix.lower() == '.csv':
            self.raw_data = pd.read_csv(filepath)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        print(f"✓ Loaded {len(self.raw_data)} rows from {file_path.name}")
        return self.raw_data
    
    def standardize_columns(self) -> pd.DataFrame:
        """
        Map vendor-specific columns to standard schema
        
        Returns:
            DataFrame with standardized column names
        """
        if self.raw_data is None:
            raise ValueError("No data loaded. Call load_file() first.")
        
        # Identify which columns exist in the data
        available_mappings = {
            old: new for old, new in self.column_map.items() 
            if old in self.raw_data.columns
        }
        
        if not available_mappings:
            print("⚠ Warning: No standard columns found. Using original column names.")
            self.standardized_data = self.raw_data.copy()
        else:
            # Rename columns and keep any extras
            self.standardized_data = self.raw_data.rename(columns=available_mappings)
            print(f"✓ Standardized {len(available_mappings)} columns")
        
        return self.standardized_data
    
    def validate_data(self) -> Tuple[bool, List[str]]:
        """
        Validate data quality and completeness
        
        Returns:
            (is_valid, list of issues)
        """
        if self.standardized_data is None:
            raise ValueError("No standardized data. Call standardize_columns() first.")
        
        issues = []
        
        # Required columns check
        required = ['fund_code', 'account_code', 'fiscal_year']
        missing = [col for col in required if col not in self.standardized_data.columns]
        if missing:
            issues.append(f"Missing required columns: {missing}")
        
        # Check for amount columns (at least one should exist)
        amount_cols = ['budgeted_amount', 'actual_amount']
        has_amounts = any(col in self.standardized_data.columns for col in amount_cols)
        if not has_amounts:
            issues.append("No budget or actual amount columns found")
        
        # Data quality checks
        if 'fiscal_year' in self.standardized_data.columns:
            # Convert to numeric for validation
            fy_numeric = pd.to_numeric(self.standardized_data['fiscal_year'], errors='coerce')
            invalid_years = self.standardized_data[
                (fy_numeric < 1990) | 
                (fy_numeric > 2050) |
                (fy_numeric.isna())
            ]
            if len(invalid_years) > 0:
                issues.append(f"Found {len(invalid_years)} rows with invalid fiscal years")
        
        # Check for nulls in key columns
        for col in ['fund_code', 'account_code']:
            if col in self.standardized_data.columns:
                null_count = self.standardized_data[col].isna().sum()
                if null_count > 0:
                    issues.append(f"{col} has {null_count} null values")
        
        is_valid = len(issues) == 0
        
        if is_valid:
            print("✓ Data validation passed")
        else:
            print(f"⚠ Data validation found {len(issues)} issues:")
            for issue in issues:
                print(f"  - {issue}")
        
        return is_valid, issues
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and prepare data for analysis
        
        Returns:
            Cleaned DataFrame
        """
        if self.standardized_data is None:
            raise ValueError("No standardized data available")
        
        df = self.standardized_data.copy()
        
        # Convert fiscal year to int where possible
        if 'fiscal_year' in df.columns:
            df['fiscal_year'] = pd.to_numeric(df['fiscal_year'], errors='coerce').astype('Int64')
        
        # Clean and convert amount columns
        amount_cols = ['budgeted_amount', 'actual_amount', 'encumbered_amount']
        for col in amount_cols:
            if col in df.columns:
                # Remove currency symbols, commas
                if df[col].dtype == 'object':
                    df[col] = df[col].str.replace('[$,]', '', regex=True)
                # Convert to float
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Trim whitespace from string columns
        string_cols = df.select_dtypes(include=['object']).columns
        for col in string_cols:
            df[col] = df[col].str.strip() if df[col].dtype == 'object' else df[col]
        
        # Add calculated fields
        if 'budgeted_amount' in df.columns and 'actual_amount' in df.columns:
            df['variance'] = df['actual_amount'] - df['budgeted_amount']
            df['variance_pct'] = np.where(
                df['budgeted_amount'] != 0,
                (df['variance'] / df['budgeted_amount']) * 100,
                0
            )
        
        # Add available balance (if encumbrances exist)
        if all(col in df.columns for col in ['budgeted_amount', 'actual_amount', 'encumbered_amount']):
            df['available_balance'] = df['budgeted_amount'] - df['actual_amount'] - df['encumbered_amount']
        
        self.standardized_data = df
        print(f"✓ Data cleaned: {len(df)} rows, {len(df.columns)} columns")
        
        return df
    
    def get_fund_summary(self) -> pd.DataFrame:
        """
        Generate fund-level summary for quick analysis
        
        Returns:
            Summary DataFrame grouped by fund and fiscal year
        """
        if self.standardized_data is None:
            raise ValueError("No data available")
        
        group_cols = ['fund_code', 'fiscal_year']
        available_groups = [col for col in group_cols if col in self.standardized_data.columns]
        
        if not available_groups:
            print("⚠ Cannot create fund summary - missing grouping columns")
            return pd.DataFrame()
        
        agg_dict = {}
        if 'budgeted_amount' in self.standardized_data.columns:
            agg_dict['budgeted_amount'] = 'sum'
        if 'actual_amount' in self.standardized_data.columns:
            agg_dict['actual_amount'] = 'sum'
        if 'encumbered_amount' in self.standardized_data.columns:
            agg_dict['encumbered_amount'] = 'sum'
        
        if not agg_dict:
            print("⚠ No amount columns to summarize")
            return pd.DataFrame()
        
        summary = self.standardized_data.groupby(available_groups).agg(agg_dict).reset_index()
        
        # Recalculate summary-level metrics
        if 'budgeted_amount' in summary.columns and 'actual_amount' in summary.columns:
            summary['variance'] = summary['actual_amount'] - summary['budgeted_amount']
            summary['variance_pct'] = np.where(
                summary['budgeted_amount'] != 0,
                (summary['variance'] / summary['budgeted_amount']) * 100,
                0
            )
        
        return summary
    
    def export_standardized(self, output_path: str, include_summary: bool = True):
        """
        Export standardized data to file
        
        Args:
            output_path: Path for output file
            include_summary: Whether to include fund summary sheet (Excel only)
        """
        if self.standardized_data is None:
            raise ValueError("No standardized data to export")
        
        output_path = Path(output_path)
        
        if output_path.suffix.lower() in ['.xlsx', '.xls']:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                self.standardized_data.to_excel(writer, sheet_name='Detail', index=False)
                
                if include_summary:
                    summary = self.get_fund_summary()
                    if not summary.empty:
                        summary.to_excel(writer, sheet_name='Fund Summary', index=False)
            
            print(f"✓ Exported to {output_path}")
        
        elif output_path.suffix.lower() == '.csv':
            self.standardized_data.to_csv(output_path, index=False)
            print(f"✓ Exported to {output_path}")
        
        else:
            raise ValueError(f"Unsupported export format: {output_path.suffix}")


def quick_ingest(filepath: str, system_type: str = 'munis') -> pd.DataFrame:
    """
    Convenience function for one-line data ingestion
    
    Args:
        filepath: Path to export file
        system_type: 'munis' or 'caselle'
    
    Returns:
        Cleaned, standardized DataFrame
    """
    ingester = BudgetDataIngester(system_type=system_type)
    ingester.load_file(filepath)
    ingester.standardize_columns()
    ingester.validate_data()
    ingester.clean_data()
    
    return ingester.standardized_data


if __name__ == "__main__":
    print("BudgetBuddy Data Ingestion Module")
    print("=" * 50)
    print("\nUsage:")
    print("  from data_ingestion import BudgetDataIngester, quick_ingest")
    print("\nQuick start:")
    print("  df = quick_ingest('munis_export.csv', system_type='munis')")
