# Kaggle Dataset Analysis Project

A Python project for downloading datasets from Kaggle and calculating statistical measures (mean, median, standard deviation, min, max).

## Features

- Download datasets from Kaggle API or public sources
- Load data from local CSV files
- Calculate comprehensive statistics (mean, median, std dev, min, max)
- Export results to JSON and CSV formats
- Support for multiple data analysis workflows

## Files

- `kaggle_dataset_analyzer.py` - Main analysis script
- `download_and_chart.py` - Data download and charting tool
- `create_chart_png.py` - Generate PNG visualizations
- `kaggle_iris_analysis.py` - Complete Kaggle analysis pipeline

## Installation

```bash
pip install requests kaggle pillow matplotlib
```

## Usage

### Basic Usage
```python
python kaggle_dataset_analyzer.py
```

### Using Kaggle API
1. Get your Kaggle API credentials from https://www.kaggle.com/settings/account
2. Place credentials at `~/.kaggle/kaggle.json`
3. Run the script

## Output

The script generates:
- `iris_statistics.json` - Statistics in JSON format
- `iris_statistics.csv` - Statistics in CSV format
- `iris_chart.png` - Visual bar chart of measurements

## Dataset

Default: Iris Flower Dataset
- 150 records
- 4 numeric features (sepal length, sepal width, petal length, petal width)
- 3 species classes

## Statistics Calculated

- Mean (Average)
- Median (Middle value)
- Standard Deviation
- Minimum value
- Maximum value
- Count of records

## Author

Hossein Sadeghian

## License

MIT
