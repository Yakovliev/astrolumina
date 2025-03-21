# AstroLumina: Star Data Explorer

A Streamlit application for visualizing and exploring star data. The application provides interactive visualizations of star types, colors, physical properties, and the Hertzsprung-Russell diagram.

## Features

- 📊 Visualize the distribution of star types
- 🎨 Explore the colors of stars
- 📏 Analyze physical properties of stars
- 🌠 Interactive Hertzsprung-Russell diagram

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/AstroLumina.git
   cd AstroLumina
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit application:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## Project Structure

```
AstroLumina/              # Root directory
├── data/                 # Data directory
│   └── cleaned_star_data.csv
├── notebooks/            # Jupyter notebooks
│   └── visualization.ipynb
├── src/                  # Source code
│   ├── __init__.py
│   ├── data_processing.py  # Data loading functions
│   └── visualization.py    # Visualization functions
├── app.py                # Main Streamlit application
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Data Source

The star data used in this application comes from [insert source information here].

## License

[Insert your license information here]