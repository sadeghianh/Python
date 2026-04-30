#!/usr/bin/env python3
"""
Kaggle Dataset Analysis - Calculate Mean Values

This script downloads a dataset from Kaggle and calculates statistical measures.
Supports both Kaggle API authentication and public dataset sources.

Dataset: Iris Flower Dataset (public, no authentication required)
Features: Sepal length, Sepal width, Petal length, Petal width
Target: Species classification
"""

import csv
import json
import sys
from io import StringIO
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from kaggle.api.kaggle_api_extended import KaggleApi
    HAS_KAGGLE_API = True
except ImportError:
    HAS_KAGGLE_API = False


class DatasetAnalyzer:
    """Analyze Kaggle datasets and calculate statistical measures."""
    
    def __init__(self, dataset_name="iris"):
        self.dataset_name = dataset_name
        self.data = []
        self.numeric_columns = {}
        
    def download_from_kaggle_api(self, dataset_id):
        """Download dataset using Kaggle API."""
        if not HAS_KAGGLE_API:
            print("⚠ Kaggle API not installed")
            print("Install: pip install kaggle")
            return False
        
        try:
            print(f"Authenticating with Kaggle API...")
            api = KaggleApi()
            api.authenticate()
            
            print(f"Downloading {dataset_id}...")
            api.dataset_download_files(dataset_id, path='.', unzip=True)
            print("✓ Download successful")
            return True
        except Exception as e:
            print(f"✗ Kaggle API error: {e}")
            return False
    
    def download_from_github(self):
        """Download Iris dataset from GitHub (public source)."""
        if not HAS_REQUESTS:
            print("⚠ requests library not installed")
            return False
        
        print("Downloading Iris dataset from GitHub...")
        url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            csv_reader = csv.DictReader(StringIO(response.text))
            self.data = list(csv_reader)
            
            print(f"✓ Downloaded {len(self.data)} records")
            return True
        except Exception as e:
            print(f"✗ Download failed: {e}")
            return False
    
    def load_local_file(self, filepath):
        """Load dataset from local CSV file."""
        try:
            with open(filepath, 'r') as f:
                csv_reader = csv.DictReader(f)
                self.data = list(csv_reader)
            print(f"✓ Loaded {len(self.data)} records from {filepath}")
            return True
        except Exception as e:
            print(f"✗ Failed to load file: {e}")
            return False
    
    def identify_numeric_columns(self):
        """Identify which columns contain numeric data."""
        if not self.data:
            print("No data loaded")
            return False
        
        first_row = self.data[0]
        numeric_cols = {}
        
        for key in first_row.keys():
            try:
                # Try to convert first value to float
                float(first_row[key])
                numeric_cols[key] = []
                numeric_cols[key].append(float(first_row[key]))
            except (ValueError, TypeError):
                pass
        
        # Collect all numeric values
        for row in self.data[1:]:
            for col in numeric_cols:
                try:
                    numeric_cols[col].append(float(row[col]))
                except (ValueError, TypeError):
                    pass
        
        self.numeric_columns = numeric_cols
        return len(numeric_cols) > 0
    
    def calculate_mean(self):
        """Calculate mean for all numeric columns."""
        means = {}
        
        for column, values in self.numeric_columns.items():
            if values:
                mean = sum(values) / len(values)
                means[column] = round(mean, 4)
        
        return means
    
    def calculate_statistics(self):
        """Calculate comprehensive statistics for all numeric columns."""
        stats = {}
        
        for column, values in self.numeric_columns.items():
            if not values:
                continue
            
            # Sort for median calculation
            sorted_values = sorted(values)
            n = len(sorted_values)
            
            # Calculate median
            if n % 2 == 1:
                median = sorted_values[n // 2]
            else:
                median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
            
            # Calculate mean
            mean = sum(values) / n
            
            # Calculate standard deviation
            variance = sum((x - mean) ** 2 for x in values) / n
            std_dev = variance ** 0.5
            
            stats[column] = {
                'mean': round(mean, 4),
                'median': round(median, 4),
                'std_dev': round(std_dev, 4),
                'min': round(min(values), 4),
                'max': round(max(values), 4),
                'count': n
            }
        
        return stats
    
    def save_results(self, stats):
        """Save statistics to JSON and CSV files."""
        # Save as JSON
        json_filename = f"{self.dataset_name}_statistics.json"
        with open(json_filename, 'w') as f:
            json.dump(stats, f, indent=2)
        print(f"✓ Statistics saved to {json_filename}")
        
        # Save as CSV
        csv_filename = f"{self.dataset_name}_statistics.csv"
        with open(csv_filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Column', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Count'])
            
            for column, values in stats.items():
                writer.writerow([
                    column,
                    values['mean'],
                    values['median'],
                    values['std_dev'],
                    values['min'],
                    values['max'],
                    values['count']
                ])
        
        print(f"✓ Statistics saved to {csv_filename}")
    
    def display_results(self, stats):
        """Display results in console."""
        print("\n" + "=" * 70)
        print(f"Dataset: {self.dataset_name.upper()}")
        print("=" * 70)
        print(f"Total records: {len(self.data)}\n")
        
        for column, values in stats.items():
            print(f"{column}:")
            print(f"  Mean:   {values['mean']}")
            print(f"  Median: {values['median']}")
            print(f"  Std Dev: {values['std_dev']}")
            print(f"  Min:    {values['min']}")
            print(f"  Max:    {values['max']}")
            print(f"  Count:  {values['count']}")
            print()


def main():
    """Main function."""
    print("=" * 70)
    print("Kaggle Dataset Analysis Tool")
    print("=" * 70)
    
    # Initialize analyzer
    analyzer = DatasetAnalyzer("iris")
    
    # Try to load data from various sources
    data_loaded = False
    
    # Try GitHub first (no authentication needed)
    if HAS_REQUESTS:
        data_loaded = analyzer.download_from_github()
    
    # Fallback to local file if available
    if not data_loaded and Path('iris.csv').exists():
        data_loaded = analyzer.load_local_file('iris.csv')
    
    # Try Kaggle API if available
    if not data_loaded and HAS_KAGGLE_API:
        print("\nAttempting Kaggle API...")
        analyzer.download_from_kaggle_api('uciml/iris')
        data_loaded = True
    
    if not data_loaded:
        print("\n✗ Could not load data")
        print("Options:")
        print("  1. Install requests: pip install requests")
        print("  2. Install kaggle API: pip install kaggle")
        print("  3. Place iris.csv in current directory")
        sys.exit(1)
    
    # Identify numeric columns
    if not analyzer.identify_numeric_columns():
        print("✗ No numeric columns found")
        sys.exit(1)
    
    print(f"✓ Found {len(analyzer.numeric_columns)} numeric columns")
    
    # Calculate statistics
    stats = analyzer.calculate_statistics()
    
    # Display results
    analyzer.display_results(stats)
    
    # Save results
    analyzer.save_results(stats)
    
    print("=" * 70)
    print("✓ Analysis complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
