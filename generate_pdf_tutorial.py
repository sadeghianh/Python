#!/usr/bin/env python3
"""
Statistical Analysis Tutorial PDF Generator

Creates a comprehensive PDF guide explaining:
- Mean (Average)
- Median (Middle Value)
- Standard Deviation
- Minimum and Maximum Values

Includes explanations, examples, Python code, and real data from Iris dataset.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from datetime import datetime


def create_statistical_pdf():
    """Create comprehensive PDF with statistical explanations."""
    
    # Create PDF document
    filename = "Statistical_Analysis_Tutorial.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch,
                           leftMargin=0.75*inch,
                           topMargin=0.75*inch,
                           bottomMargin=0.75*inch)
    
    # Container for elements
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    code_style = ParagraphStyle(
        'Code',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=colors.HexColor('#333333'),
        backColor=colors.HexColor('#f5f5f5'),
        leftIndent=20,
        spaceAfter=10
    )
    
    # === TITLE PAGE ===
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("Statistical Analysis Tutorial", title_style))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Understanding Mean, Median, and Standard Deviation", 
                             ParagraphStyle('subtitle', parent=styles['Normal'], 
                                          fontSize=14, alignment=TA_CENTER, 
                                          textColor=colors.HexColor('#555555'))))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%B %d, %Y')}", 
                             ParagraphStyle('date', parent=styles['Normal'], 
                                          fontSize=11, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph("Dataset: Iris Flower Measurements (150 records)", 
                             ParagraphStyle('dataset', parent=styles['Normal'], 
                                          fontSize=11, alignment=TA_CENTER,
                                          textColor=colors.HexColor('#666666'))))
    elements.append(PageBreak())
    
    # === TABLE OF CONTENTS ===
    elements.append(Paragraph("Table of Contents", heading_style))
    toc_items = [
        "1. Introduction to Statistical Measures",
        "2. Mean (Average)",
        "3. Median (Middle Value)",
        "4. Standard Deviation",
        "5. Minimum and Maximum",
        "6. Real Data Example: Iris Dataset",
        "7. Python Code Examples"
    ]
    for item in toc_items:
        elements.append(Paragraph(item, body_style))
        elements.append(Spacer(1, 0.1*inch))
    elements.append(PageBreak())
    
    # === SECTION 1: INTRODUCTION ===
    elements.append(Paragraph("1. Introduction to Statistical Measures", heading_style))
    elements.append(Paragraph(
        "Statistical measures help us understand data by summarizing large datasets into meaningful numbers. "
        "In this tutorial, we will explore five key statistical measures that are essential for data analysis: "
        "<b>Mean, Median, Standard Deviation, Minimum, and Maximum</b>. Each measure tells us something different about our data.",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # === SECTION 2: MEAN ===
    elements.append(Paragraph("2. Mean (Average)", heading_style))
    
    elements.append(Paragraph(
        "<b>What is the Mean?</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor('#2c5aa0'), fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "The mean is the most common measure of central tendency. It is calculated by adding all values "
        "together and dividing by the number of values. Think of it as the 'average' you calculate in school.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Formula:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Mean = (Sum of all values) ÷ (Number of values)",
        code_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Example Calculation:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Let's say we have 5 test scores: <b>80, 85, 90, 78, 92</b><br/>"
        "Mean = (80 + 85 + 90 + 78 + 92) ÷ 5<br/>"
        "Mean = 425 ÷ 5<br/>"
        "Mean = <b>85</b>",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Python Code:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    
    mean_code = """
# Method 1: Using a loop
values = [80, 85, 90, 78, 92]
total = 0
for value in values:
    total = total + value
mean = total / len(values)
print(f"Mean: {mean}")  # Output: Mean: 85.0

# Method 2: Using built-in sum()
mean = sum(values) / len(values)
print(f"Mean: {mean}")  # Output: Mean: 85.0

# Method 3: Using NumPy (for large datasets)
import numpy as np
mean = np.mean(values)
print(f"Mean: {mean}")  # Output: Mean: 85.0
"""
    elements.append(Preformatted(mean_code, code_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Real Data Example (Iris Dataset):</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Sepal Length measurements: 5.1, 7.0, 6.3, 6.4, 7.1, ... (150 values total)<br/>"
        "Mean Sepal Length = <b>5.8433 cm</b><br/>"
        "This tells us that the average sepal length in the Iris dataset is about 5.84 centimeters.",
        body_style
    ))
    elements.append(PageBreak())
    
    # === SECTION 3: MEDIAN ===
    elements.append(Paragraph("3. Median (Middle Value)", heading_style))
    
    elements.append(Paragraph(
        "<b>What is the Median?</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor('#2c5aa0'), fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "The median is the middle value when all data points are arranged in order from smallest to largest. "
        "If there's an even number of values, the median is the average of the two middle values. "
        "The median is useful because it's not affected by extreme values (outliers).",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Steps to Find Median:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "1. Sort all values from smallest to largest<br/>"
        "2. If odd number of values: median is the middle value<br/>"
        "3. If even number of values: median = (middle value 1 + middle value 2) ÷ 2",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Example Calculation (Odd number of values):</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Values: 80, 92, 78, 85, 90<br/>"
        "Sorted: 78, 80, 85, 90, 92<br/>"
        "Median = <b>85</b> (the middle value)<br/><br/>"
        "<b>Example Calculation (Even number of values):</b><br/>"
        "Values: 80, 92, 78, 85<br/>"
        "Sorted: 78, 80, 85, 92<br/>"
        "Median = (80 + 85) ÷ 2 = <b>82.5</b>",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Python Code:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    
    median_code = """
# Method 1: Manual calculation
values = [80, 92, 78, 85, 90]
sorted_values = sorted(values)
n = len(sorted_values)

if n % 2 == 1:  # Odd number of values
    median = sorted_values[n // 2]
else:  # Even number of values
    median = (sorted_values[n//2 - 1] + sorted_values[n//2]) / 2

print(f"Median: {median}")  # Output: Median: 85

# Method 2: Using statistics module
import statistics
median = statistics.median(values)
print(f"Median: {median}")  # Output: Median: 85

# Method 3: Using NumPy
import numpy as np
median = np.median(values)
print(f"Median: {median}")  # Output: Median: 85.0
"""
    elements.append(Preformatted(median_code, code_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Real Data Example (Iris Dataset):</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Sepal Length sorted: 4.3, 4.4, 4.4, 4.5, ... 7.9 (150 values)<br/>"
        "Median Sepal Length = <b>5.8 cm</b> (the 75th and 76th values average)<br/>"
        "Notice that median (5.8) is very close to mean (5.8433), showing the data is fairly symmetric.",
        body_style
    ))
    elements.append(PageBreak())
    
    # === SECTION 4: STANDARD DEVIATION ===
    elements.append(Paragraph("4. Standard Deviation", heading_style))
    
    elements.append(Paragraph(
        "<b>What is Standard Deviation?</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor('#2c5aa0'), fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Standard deviation measures how spread out the data is from the mean. "
        "A small standard deviation means values are close to the mean. "
        "A large standard deviation means values are spread far apart. "
        "It's a crucial measure for understanding data variability.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Steps to Calculate Standard Deviation:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "1. Calculate the mean<br/>"
        "2. Find the difference between each value and the mean (deviation)<br/>"
        "3. Square each deviation<br/>"
        "4. Calculate the average of squared deviations (variance)<br/>"
        "5. Take the square root of variance",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Example Calculation:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Values: 80, 85, 90, 78, 92<br/>"
        "Step 1: Mean = 85<br/>"
        "Step 2 & 3: Deviations² = (-5)²=25, (0)²=0, (5)²=25, (-7)²=49, (7)²=49<br/>"
        "Step 4: Variance = (25+0+25+49+49) ÷ 5 = 29.6<br/>"
        "Step 5: Std Dev = √29.6 = <b>5.44</b>",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Python Code:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    
    std_code = """
# Method 1: Manual calculation
values = [80, 85, 90, 78, 92]
mean = sum(values) / len(values)  # mean = 85

# Calculate variance
squared_deviations = [(x - mean) ** 2 for x in values]
variance = sum(squared_deviations) / len(values)

# Calculate standard deviation
std_dev = variance ** 0.5
print(f"Std Dev: {std_dev}")  # Output: Std Dev: 5.44

# Method 2: Using statistics module
import statistics
std_dev = statistics.stdev(values)
print(f"Std Dev: {std_dev}")  # Output: Std Dev: 6.08 (sample std dev)

# Method 3: Using NumPy
import numpy as np
std_dev = np.std(values)
print(f"Std Dev: {std_dev}")  # Output: Std Dev: 5.44
"""
    elements.append(Preformatted(std_code, code_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Real Data Example (Iris Dataset):</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Sepal Length - Std Dev = <b>0.8253</b><br/>"
        "Sepal Width - Std Dev = <b>0.4344</b><br/>"
        "Sepal width is less variable (smaller std dev) than sepal length. "
        "Petal measurements have much higher std dev, meaning they vary more by species.",
        body_style
    ))
    elements.append(PageBreak())
    
    # === SECTION 5: MIN AND MAX ===
    elements.append(Paragraph("5. Minimum and Maximum Values", heading_style))
    
    elements.append(Paragraph(
        "<b>What are Min and Max?</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor('#2c5aa0'), fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "<b>Minimum (Min)</b> is the smallest value in the dataset.<br/>"
        "<b>Maximum (Max)</b> is the largest value in the dataset.<br/>"
        "These values help us understand the range of our data and identify outliers.",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Example:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Values: 80, 85, 90, 78, 92<br/>"
        "Minimum = <b>78</b><br/>"
        "Maximum = <b>92</b><br/>"
        "Range = Max - Min = 92 - 78 = <b>14</b>",
        body_style
    ))
    elements.append(Spacer(1, 0.15*inch))
    
    elements.append(Paragraph(
        "<b>Python Code:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    
    minmax_code = """
values = [80, 85, 90, 78, 92]

# Method 1: Using built-in functions
minimum = min(values)
maximum = max(values)
print(f"Min: {minimum}, Max: {maximum}")  # Output: Min: 78, Max: 92

# Method 2: Manual search
minimum = values[0]
maximum = values[0]
for value in values:
    if value < minimum:
        minimum = value
    if value > maximum:
        maximum = value
print(f"Min: {minimum}, Max: {maximum}")  # Output: Min: 78, Max: 92

# Method 3: Using NumPy
import numpy as np
minimum = np.min(values)
maximum = np.max(values)
print(f"Min: {minimum}, Max: {maximum}")  # Output: Min: 78, Max: 92

# Calculate range
data_range = maximum - minimum
print(f"Range: {data_range}")  # Output: Range: 14
"""
    elements.append(Preformatted(minmax_code, code_style))
    elements.append(Spacer(1, 0.1*inch))
    
    elements.append(Paragraph(
        "<b>Real Data Example (Iris Dataset):</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "Sepal Length: Min = 4.3 cm, Max = 7.9 cm (Range: 3.6 cm)<br/>"
        "Petal Length: Min = 1.0 cm, Max = 6.9 cm (Range: 5.9 cm)<br/>"
        "The wider range in petal length shows that this measurement varies more across iris species.",
        body_style
    ))
    elements.append(PageBreak())
    
    # === SECTION 6: REAL DATA SUMMARY ===
    elements.append(Paragraph("6. Real Data Example: Iris Dataset Summary", heading_style))
    
    elements.append(Paragraph(
        "The Iris dataset contains measurements of 150 iris flowers from three different species. "
        "Here's a summary of all our statistical measures applied to real data:",
        body_style
    ))
    elements.append(Spacer(1, 0.2*inch))
    
    # Create summary table
    table_data = [
        ['Measurement', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Count'],
        ['Sepal Length', '5.8433', '5.8', '0.8253', '4.3', '7.9', '150'],
        ['Sepal Width', '3.0573', '3.0', '0.4344', '2.0', '4.4', '150'],
        ['Petal Length', '3.758', '4.35', '1.7594', '1.0', '6.9', '150'],
        ['Petal Width', '1.1993', '1.3', '0.7597', '0.1', '2.5', '150'],
    ]
    
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
    ])
    
    table = Table(table_data, colWidths=[1.2*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.7*inch, 0.7*inch, 0.7*inch])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    elements.append(Paragraph(
        "<b>Interpretation:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "• Sepal measurements are fairly consistent across flowers (low std dev)<br/>"
        "• Petal length varies greatly (std dev: 1.76), suggesting different species have very different petal sizes<br/>"
        "• The range of values is different for each measurement<br/>"
        "• Mean and median are very similar, indicating normally distributed data",
        body_style
    ))
    elements.append(PageBreak())
    
    # === SECTION 7: PYTHON CODE ===
    elements.append(Paragraph("7. Complete Python Code Example", heading_style))
    
    complete_code = """
# Complete example: Calculate all statistics for a dataset

import statistics
import numpy as np

# Sample data: Iris sepal lengths
sepal_lengths = [5.1, 7.0, 6.3, 6.4, 7.1, 5.8, 6.3, 4.7, 6.4, 4.9, 
                 5.5, 4.9, 5.8, 5.7, 5.2, 5.2, 4.7, 5.4, 5.2, 5.5]

# Calculate statistics
mean_val = sum(sepal_lengths) / len(sepal_lengths)
median_val = statistics.median(sepal_lengths)
std_dev_val = statistics.stdev(sepal_lengths)
min_val = min(sepal_lengths)
max_val = max(sepal_lengths)
count = len(sepal_lengths)

# Display results
print("=" * 50)
print("STATISTICAL ANALYSIS RESULTS")
print("=" * 50)
print(f"Mean:          {mean_val:.4f} cm")
print(f"Median:        {median_val:.4f} cm")
print(f"Std Dev:       {std_dev_val:.4f} cm")
print(f"Minimum:       {min_val:.4f} cm")
print(f"Maximum:       {max_val:.4f} cm")
print(f"Count:         {count}")
print(f"Range:         {max_val - min_val:.4f} cm")
print("=" * 50)

# Create a complete class for analysis
class DataAnalyzer:
    def __init__(self, data):
        self.data = data
    
    def analyze(self):
        return {
            'mean': sum(self.data) / len(self.data),
            'median': statistics.median(self.data),
            'std_dev': statistics.stdev(self.data),
            'min': min(self.data),
            'max': max(self.data),
            'count': len(self.data)
        }

# Usage
analyzer = DataAnalyzer(sepal_lengths)
results = analyzer.analyze()
print("\\nAnalysis Results:", results)
"""
    
    elements.append(Preformatted(complete_code, code_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # === FOOTER ===
    elements.append(Spacer(1, 0.3*inch))
    elements.append(Paragraph(
        "_______________________________________________",
        ParagraphStyle('line', parent=styles['Normal'], alignment=TA_CENTER)
    ))
    elements.append(Paragraph(
        "<b>Key Takeaways:</b>",
        ParagraphStyle('subheading', parent=styles['Normal'], fontSize=12, 
                      textColor=colors.HexColor('#2c5aa0'), fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "✓ Mean gives us the average value of the dataset<br/>"
        "✓ Median shows us the middle value and is resistant to outliers<br/>"
        "✓ Standard Deviation tells us how spread out the data is<br/>"
        "✓ Min and Max give us the range of our data<br/>"
        "✓ Together, these statistics paint a complete picture of any dataset",
        ParagraphStyle('body', parent=styles['Normal'], fontSize=11, leading=16)
    ))
    
    # Build PDF
    doc.build(elements)
    print(f"✓ PDF created successfully: {filename}")
    return filename


if __name__ == "__main__":
    print("Generating Statistical Analysis Tutorial PDF...")
    print("=" * 60)
    pdf_file = create_statistical_pdf()
    print("=" * 60)
    print(f"✓ Location: d:\\vs code\\Data Analysis\\Mean\\{pdf_file}")
