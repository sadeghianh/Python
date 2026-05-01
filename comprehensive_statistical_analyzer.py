#!/usr/bin/env python3
"""
Comprehensive Statistical Analysis Tool with PDF Generation

Calculates: Mean, Median, Mode, Range, Variance, Standard Deviation, IQR
Generates plots and comprehensive PDF tutorial for each statistic.
"""

import csv
import json
import sys
from io import StringIO
from pathlib import Path
from collections import Counter
import statistics as stats_module

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

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('Agg')
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False


class AdvancedDataAnalyzer:
    """Advanced statistical analysis with comprehensive metrics."""
    
    def __init__(self, dataset_name="iris"):
        self.dataset_name = dataset_name
        self.data = []
        self.numeric_columns = {}
        self.stats_results = {}
        
    def download_from_github(self):
        """Download Iris dataset from GitHub."""
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
        """Identify numeric columns."""
        if not self.data:
            print("No data loaded")
            return False
        
        first_row = self.data[0]
        numeric_cols = {}
        
        for key in first_row.keys():
            try:
                float(first_row[key])
                numeric_cols[key] = []
                numeric_cols[key].append(float(first_row[key]))
            except (ValueError, TypeError):
                pass
        
        for row in self.data[1:]:
            for col in numeric_cols:
                try:
                    numeric_cols[col].append(float(row[col]))
                except (ValueError, TypeError):
                    pass
        
        self.numeric_columns = numeric_cols
        return len(numeric_cols) > 0
    
    def calculate_mode(self, values):
        """Calculate mode (most frequent value)."""
        try:
            return stats_module.mode(values)
        except:
            # If no mode, return None
            return None
    
    def calculate_range(self, values):
        """Calculate range (max - min)."""
        return max(values) - min(values)
    
    def calculate_variance(self, values):
        """Calculate variance."""
        mean = sum(values) / len(values)
        return sum((x - mean) ** 2 for x in values) / len(values)
    
    def calculate_iqr(self, values):
        """Calculate Interquartile Range."""
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        
        # Q1 (25th percentile)
        q1_index = n // 4
        q1 = sorted_vals[q1_index]
        
        # Q3 (75th percentile)
        q3_index = (3 * n) // 4
        q3 = sorted_vals[q3_index]
        
        return {'Q1': q1, 'Q3': q3, 'IQR': q3 - q1}
    
    def calculate_all_statistics(self):
        """Calculate all statistics."""
        all_stats = {}
        
        for column, values in self.numeric_columns.items():
            if not values:
                continue
            
            sorted_values = sorted(values)
            n = len(sorted_values)
            mean = sum(values) / n
            
            # Median
            if n % 2 == 1:
                median = sorted_values[n // 2]
            else:
                median = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2
            
            # Mode
            mode_val = self.calculate_mode(values)
            
            # Variance and Std Dev
            variance = self.calculate_variance(values)
            std_dev = variance ** 0.5
            
            # Range
            data_range = self.calculate_range(values)
            
            # IQR
            iqr_data = self.calculate_iqr(values)
            
            all_stats[column] = {
                'mean': round(mean, 4),
                'median': round(median, 4),
                'mode': mode_val,
                'range': round(data_range, 4),
                'variance': round(variance, 4),
                'std_dev': round(std_dev, 4),
                'min': round(min(values), 4),
                'max': round(max(values), 4),
                'q1': round(iqr_data['Q1'], 4),
                'q3': round(iqr_data['Q3'], 4),
                'iqr': round(iqr_data['IQR'], 4),
                'count': n
            }
        
        self.stats_results = all_stats
        return all_stats
    
    def display_results(self):
        """Display results in console."""
        print("\n" + "=" * 80)
        print(f"COMPREHENSIVE STATISTICAL ANALYSIS - {self.dataset_name.upper()}")
        print("=" * 80)
        print(f"Total records: {len(self.data)}\n")
        
        for column, stats in self.stats_results.items():
            print(f"\n{column.upper()}")
            print("-" * 80)
            print(f"  Mean:              {stats['mean']}")
            print(f"  Median:            {stats['median']}")
            print(f"  Mode:              {stats['mode']}")
            print(f"  Range:             {stats['range']}")
            print(f"  Variance:          {stats['variance']}")
            print(f"  Standard Dev:      {stats['std_dev']}")
            print(f"  Min:               {stats['min']}")
            print(f"  Max:               {stats['max']}")
            print(f"  Q1:                {stats['q1']}")
            print(f"  Q3:                {stats['q3']}")
            print(f"  IQR:               {stats['iqr']}")
            print(f"  Count:             {stats['count']}")
    
    def create_plots(self):
        """Create plots for each statistic."""
        if not HAS_MATPLOTLIB:
            print("⚠ Matplotlib not available - skipping plots")
            return False
        
        print("\nCreating visualization plots...")
        
        for column, values in self.numeric_columns.items():
            fig, axes = plt.subplots(2, 3, figsize=(15, 10))
            fig.suptitle(f'{column.upper()} - Statistical Visualizations', fontsize=16, fontweight='bold')
            
            # 1. Histogram with Mean/Median
            ax = axes[0, 0]
            ax.hist(values, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.axvline(self.stats_results[column]['mean'], color='red', linestyle='--', label=f"Mean: {self.stats_results[column]['mean']}")
            ax.axvline(self.stats_results[column]['median'], color='green', linestyle='--', label=f"Median: {self.stats_results[column]['median']}")
            ax.set_title('Histogram with Mean & Median')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # 2. Box Plot (for IQR visualization)
            ax = axes[0, 1]
            box = ax.boxplot(values, vert=True)
            ax.set_title('Box Plot (IQR Visualization)')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
            
            # 3. Density Plot
            ax = axes[0, 2]
            ax.hist(values, bins=20, alpha=0.5, density=True, color='skyblue', edgecolor='black')
            from scipy import stats as scipy_stats
            try:
                mu, sigma = self.stats_results[column]['mean'], self.stats_results[column]['std_dev']
                x = [i for i in sorted(values)]
                ax.plot(x, scipy_stats.norm.pdf(x, mu, sigma), 'r-', label='Normal Distribution')
                ax.legend()
            except:
                pass
            ax.set_title('Distribution Density')
            ax.set_xlabel('Value')
            ax.set_ylabel('Density')
            ax.grid(True, alpha=0.3)
            
            # 4. Q-Q Plot style (sorted values)
            ax = axes[1, 0]
            sorted_vals = sorted(values)
            ax.plot(range(len(sorted_vals)), sorted_vals, 'b-o', markersize=3)
            ax.set_title('Sorted Values (Distribution Shape)')
            ax.set_xlabel('Index')
            ax.set_ylabel('Value')
            ax.grid(True, alpha=0.3)
            
            # 5. Statistics Summary (Text)
            ax = axes[1, 1]
            ax.axis('off')
            stats_text = f"""
            STATISTICS SUMMARY
            
            Mean: {self.stats_results[column]['mean']}
            Median: {self.stats_results[column]['median']}
            Mode: {self.stats_results[column]['mode']}
            
            Min: {self.stats_results[column]['min']}
            Max: {self.stats_results[column]['max']}
            Range: {self.stats_results[column]['range']}
            
            Variance: {self.stats_results[column]['variance']}
            Std Dev: {self.stats_results[column]['std_dev']}
            
            Q1: {self.stats_results[column]['q1']}
            Q3: {self.stats_results[column]['q3']}
            IQR: {self.stats_results[column]['iqr']}
            """
            ax.text(0.1, 0.9, stats_text, transform=ax.transAxes, fontsize=11,
                   verticalalignment='top', fontfamily='monospace',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
            
            # 6. Range visualization
            ax = axes[1, 2]
            ax.barh(['Range'], [self.stats_results[column]['range']], color='orange')
            ax.set_xlim(0, self.stats_results[column]['max'])
            ax.set_title('Range Visualization')
            ax.grid(True, alpha=0.3, axis='x')
            
            plt.tight_layout()
            filename = f"{column}_statistics_plot.png"
            plt.savefig(filename, dpi=150, bbox_inches='tight')
            plt.close()
            print(f"  ✓ Created {filename}")
        
        return True
    
    def save_results_to_json(self):
        """Save results to JSON."""
        json_file = f"{self.dataset_name}_comprehensive_stats.json"
        with open(json_file, 'w') as f:
            json.dump(self.stats_results, f, indent=2)
        print(f"✓ Results saved to {json_file}")
    
    def generate_pdf_tutorial(self):
        """Generate comprehensive PDF tutorial."""
        if not HAS_REPORTLAB:
            print("⚠ ReportLab not installed - skipping PDF generation")
            return False
        
        print("Generating PDF tutorial...")
        
        filename = f"{self.dataset_name}_complete_statistical_tutorial.pdf"
        doc = SimpleDocTemplate(filename, pagesize=letter,
                               rightMargin=0.5*inch, leftMargin=0.5*inch,
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'],
                                    fontSize=22, textColor=colors.HexColor('#1f4788'),
                                    spaceAfter=20, alignment=TA_CENTER, fontName='Helvetica-Bold')
        
        heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'],
                                      fontSize=14, textColor=colors.HexColor('#2c5aa0'),
                                      spaceAfter=10, spaceBefore=10, fontName='Helvetica-Bold')
        
        body_style = ParagraphStyle('Body', parent=styles['BodyText'],
                                   fontSize=10, alignment=TA_JUSTIFY, spaceAfter=10, leading=14)
        
        code_style = ParagraphStyle('Code', parent=styles['Normal'],
                                   fontSize=8, fontName='Courier', textColor=colors.HexColor('#333333'),
                                   backColor=colors.HexColor('#f5f5f5'), leftIndent=15, spaceAfter=8)
        
        # Title Page
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("COMPREHENSIVE STATISTICAL ANALYSIS TUTORIAL", title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Mean • Median • Mode • Range • Variance • Standard Deviation • IQR",
                                 ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER)))
        elements.append(Spacer(1, 1*inch))
        elements.append(Paragraph(f"Dataset: {self.dataset_name.upper()} ({len(self.data)} records)",
                                 ParagraphStyle('dataset', parent=styles['Normal'], fontSize=11, alignment=TA_CENTER)))
        elements.append(PageBreak())
        
        # Table of Contents
        elements.append(Paragraph("Table of Contents", heading_style))
        toc_items = [
            "1. Mean (Average)",
            "2. Median (Middle Value)",
            "3. Mode (Most Frequent Value)",
            "4. Range (Spread)",
            "5. Variance (Variability)",
            "6. Standard Deviation (Spread from Mean)",
            "7. Interquartile Range (IQR)",
            "8. Real Data Analysis & Results"
        ]
        for item in toc_items:
            elements.append(Paragraph(item, body_style))
        elements.append(PageBreak())
        
        # 1. MEAN
        elements.append(Paragraph("1. Mean (Average)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("The mean is the sum of all values divided by the count. It's the most common measure of center.", body_style))
        elements.append(Paragraph("<b>Formula:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Mean = (Sum of all values) ÷ (Number of values)", code_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Values: 2, 4, 6, 8, 10<br/>Sum = 2+4+6+8+10 = 30<br/>Mean = 30 ÷ 5 = <b>6</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        mean_code = """
values = [2, 4, 6, 8, 10]
mean = sum(values) / len(values)
print(f"Mean: {mean}")  # Output: 6.0

# Using statistics module
import statistics
mean = statistics.mean(values)
"""
        elements.append(Preformatted(mean_code, code_style))
        elements.append(PageBreak())
        
        # 2. MEDIAN
        elements.append(Paragraph("2. Median (Middle Value)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("The median is the middle value when data is sorted. It divides data into two equal halves. Resistant to outliers.", body_style))
        
        elements.append(Paragraph("<b>Calculation Steps:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("1. Sort all values<br/>2. If odd count: middle value is median<br/>3. If even count: average of two middle values", body_style))
        
        elements.append(Paragraph("<b>Examples:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Odd count: [1, 3, 5, 7, 9] → Median = <b>5</b><br/>Even count: [1, 3, 5, 7] → Median = (3+5)÷2 = <b>4</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        median_code = """
values = [1, 3, 5, 7, 9]
sorted_vals = sorted(values)
n = len(sorted_vals)

if n % 2 == 1:
    median = sorted_vals[n // 2]
else:
    median = (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2

import statistics
median = statistics.median(values)
"""
        elements.append(Preformatted(median_code, code_style))
        elements.append(PageBreak())
        
        # 3. MODE
        elements.append(Paragraph("3. Mode (Most Frequent Value)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("The mode is the value that appears most frequently in the dataset. A dataset can have no mode, one mode, or multiple modes (bimodal/multimodal).", body_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Values: [1, 2, 2, 3, 3, 3, 4]<br/>Mode = <b>3</b> (appears 3 times, most frequent)", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        mode_code = """
from collections import Counter
values = [1, 2, 2, 3, 3, 3, 4]

# Method 1: Using statistics
import statistics
mode = statistics.mode(values)

# Method 2: Manual counting
counter = Counter(values)
mode = counter.most_common(1)[0][0]
"""
        elements.append(Preformatted(mode_code, code_style))
        elements.append(PageBreak())
        
        # 4. RANGE
        elements.append(Paragraph("4. Range (Spread)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("The range is the difference between the maximum and minimum values. It shows how spread out the data is.", body_style))
        
        elements.append(Paragraph("<b>Formula:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Range = Maximum - Minimum", code_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Values: [10, 15, 20, 25, 30]<br/>Min = 10, Max = 30<br/>Range = 30 - 10 = <b>20</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        range_code = """
values = [10, 15, 20, 25, 30]
data_range = max(values) - min(values)
print(f"Range: {data_range}")  # Output: 20
"""
        elements.append(Preformatted(range_code, code_style))
        elements.append(PageBreak())
        
        # 5. VARIANCE
        elements.append(Paragraph("5. Variance (Variability)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Variance measures how spread out values are from the mean. Higher variance = more spread out.", body_style))
        
        elements.append(Paragraph("<b>Formula:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Variance = Average of squared deviations from mean", code_style))
        
        elements.append(Paragraph("<b>Steps:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("1. Calculate mean<br/>2. Find deviation (value - mean) for each value<br/>3. Square each deviation<br/>4. Average the squared deviations", body_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Values: [2, 4, 6]<br/>Mean = 4<br/>Deviations²: (-2)²=4, (0)²=0, (2)²=4<br/>Variance = (4+0+4)÷3 = <b>2.67</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        variance_code = """
values = [2, 4, 6]
mean = sum(values) / len(values)
variance = sum((x - mean)**2 for x in values) / len(values)

import statistics
variance = statistics.variance(values)
"""
        elements.append(Preformatted(variance_code, code_style))
        elements.append(PageBreak())
        
        # 6. STANDARD DEVIATION
        elements.append(Paragraph("6. Standard Deviation", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Standard deviation is the square root of variance. It measures how far values typically are from the mean. Same units as original data.", body_style))
        
        elements.append(Paragraph("<b>Formula:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Std Dev = √Variance", code_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Variance = 2.67<br/>Std Dev = √2.67 = <b>1.63</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        std_code = """
values = [2, 4, 6]
mean = sum(values) / len(values)
variance = sum((x - mean)**2 for x in values) / len(values)
std_dev = variance ** 0.5

import statistics
std_dev = statistics.stdev(values)
"""
        elements.append(Preformatted(std_code, code_style))
        elements.append(PageBreak())
        
        # 7. IQR
        elements.append(Paragraph("7. Interquartile Range (IQR)", heading_style))
        elements.append(Paragraph("<b>Definition:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("IQR is the range of the middle 50% of the data. Q1 is 25th percentile, Q3 is 75th percentile. IQR = Q3 - Q1.", body_style))
        
        elements.append(Paragraph("<b>Interpretation:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("• Q1: 25% of data below this value<br/>• Q2 (Median): 50% below, 50% above<br/>• Q3: 75% of data below this value<br/>• IQR: Contains middle 50% of data", body_style))
        
        elements.append(Paragraph("<b>Example:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        elements.append(Paragraph("Sorted: [1, 2, 3, 4, 5, 6, 7, 8, 9]<br/>Q1 = 2, Q3 = 8<br/>IQR = 8 - 2 = <b>6</b>", body_style))
        
        elements.append(Paragraph("<b>Python Code:</b>", ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')))
        iqr_code = """
values = [1, 2, 3, 4, 5, 6, 7, 8, 9]
sorted_vals = sorted(values)
n = len(sorted_vals)

q1 = sorted_vals[n // 4]
q3 = sorted_vals[(3 * n) // 4]
iqr = q3 - q1

# Using numpy (easier)
import numpy as np
q1 = np.percentile(values, 25)
q3 = np.percentile(values, 75)
"""
        elements.append(Preformatted(iqr_code, code_style))
        elements.append(PageBreak())
        
        # 8. REAL DATA RESULTS
        elements.append(Paragraph("8. Real Data Analysis Results", heading_style))
        
        # Create results table
        table_data = [['Metric', 'Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']]
        
        metrics = ['mean', 'median', 'mode', 'range', 'variance', 'std_dev', 'min', 'max', 'q1', 'q3', 'iqr']
        
        for metric in metrics:
            row = [metric.upper()]
            for col in self.numeric_columns.keys():
                if col in self.stats_results:
                    row.append(str(self.stats_results[col].get(metric, 'N/A')))
            table_data.append(row)
        
        table = Table(table_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Add plot images
        elements.append(PageBreak())
        elements.append(Paragraph("Statistical Visualizations", heading_style))
        
        for column in self.numeric_columns.keys():
            plot_file = f"{column}_statistics_plot.png"
            if Path(plot_file).exists():
                elements.append(Paragraph(f"{column.upper()} Analysis", 
                                        ParagraphStyle('plotheading', parent=styles['Normal'], fontSize=12, fontName='Helvetica-Bold')))
                elements.append(Image(plot_file, width=7*inch, height=5*inch))
                elements.append(Spacer(1, 0.2*inch))
                elements.append(PageBreak())
        
        # Build PDF
        doc.build(elements)
        print(f"✓ PDF created: {filename}")
        return True


def main():
    """Main execution."""
    print("=" * 80)
    print("COMPREHENSIVE STATISTICAL ANALYSIS TOOL")
    print("=" * 80)
    
    analyzer = AdvancedDataAnalyzer("iris")
    
    # Load data
    data_loaded = False
    if HAS_REQUESTS:
        data_loaded = analyzer.download_from_github()
    
    if not data_loaded and Path('iris.csv').exists():
        data_loaded = analyzer.load_local_file('iris.csv')
    
    if not data_loaded:
        print("\n✗ Could not load data")
        sys.exit(1)
    
    # Identify numeric columns
    if not analyzer.identify_numeric_columns():
        print("✗ No numeric columns found")
        sys.exit(1)
    
    print(f"✓ Found {len(analyzer.numeric_columns)} numeric columns")
    
    # Calculate all statistics
    print("\nCalculating statistics...")
    analyzer.calculate_all_statistics()
    
    # Display results
    analyzer.display_results()
    
    # Save results
    analyzer.save_results_to_json()
    
    # Create plots
    analyzer.create_plots()
    
    # Generate PDF
    analyzer.generate_pdf_tutorial()
    
    print("\n" + "=" * 80)
    print("✓ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated Files:")
    print("  • iris_comprehensive_stats.json (Statistics in JSON)")
    print("  • iris_complete_statistical_tutorial.pdf (Full tutorial with plots)")
    print("  • *_statistics_plot.png (Visualization plots)")


if __name__ == "__main__":
    main()
