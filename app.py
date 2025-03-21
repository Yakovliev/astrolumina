import streamlit as st
import pandas as pd

# Import functions from our modules
from src.data_processing import load_star_data
from src.visualization import (
    create_boxplots,
    create_hr_diagram_improved,
    create_scatter_matrix
)

# Page configuration
st.set_page_config(
    page_title="AstroLumina - Star Data Explorer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("✨ AstroLumina: Star Data Explorer")
st.markdown("""
This interactive dashboard allows you to explore various properties of stars 
in our catalog. Select different visualizations from the sidebar to learn more about star types, 
colors, and their physical properties.
""")

# Load data


@st.cache_data
def get_data():
    return load_star_data()


try:
    df = get_data()
    st.success(f"Successfully loaded data with {len(df)} stars!")
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select a visualization:",
    ["📏 Physical Properties", "🌠 HR Diagram",
        "📊 Feature Correlations"]
)

# Display different pages based on selection
if page == "📏 Physical Properties":
    st.header("Physical Properties by Star Type")
    st.markdown("""
    These box plots show the distribution of key physical properties across different star types.
    You can observe how properties like temperature, luminosity, radius, and absolute magnitude
    vary between different categories of stars.
    """)

    fig = create_boxplots(df)
    st.plotly_chart(fig, use_container_width=True)

    # Explanation of each property
    st.subheader("Understanding Star Properties")
    st.markdown("""
    - **Temperature (K)**: Surface temperature in Kelvin.
    - **Luminosity (L/Lo)**: Brightness relative to our Sun (Lo = Solar luminosity).
    - **Radius (R/Ro)**: Size relative to our Sun (Ro = Solar radius).
    - **Absolute Magnitude (Mv)**: Intrinsic brightness (lower values indicate brighter stars).
    """)

elif page == "🌠 HR Diagram":
    st.header("Hertzsprung-Russell Diagram")
    st.markdown("""
    The Hertzsprung-Russell (H-R) diagram is one of the most important tools in astronomy.
    It plots stars based on their temperature (x-axis) and absolute magnitude/luminosity (y-axis).
    
    This diagram helps astronomers classify stars and understand stellar evolution.
    """)

    fig = create_hr_diagram_improved(df)
    st.plotly_chart(fig, use_container_width=True)

    # HR Diagram explanation
    st.subheader("Understanding the H-R Diagram")
    st.markdown("""
    The H-R diagram reveals several distinct regions:
    
    - **Main Sequence**: A diagonal band where most stars (including our Sun) spend the majority of their lives.
    - **Red Giants**: Cooler but very luminous stars in the upper right.
    - **White Dwarfs**: Hot but dim stars in the lower left.
    - **Supergiants**: Extremely bright stars at the top of the diagram.
    
    A star's position on this diagram tells us about its age, mass, and evolutionary stage.
    """)

elif page == "📊 Feature Correlations":
    st.header("Star Feature Correlations")
    st.markdown("""
    This scatter matrix shows the relationships between key stellar properties.
    Each plot shows the correlation between two properties, allowing you to see
    patterns and relationships in the data.
    
    Points are colored by spectral class to highlight how different types of stars
    cluster in different regions of the feature space.
    """)

    fig = create_scatter_matrix(df)
    st.plotly_chart(fig, use_container_width=True)

    # Scatter matrix explanation
    st.subheader("Interpreting the Scatter Matrix")
    st.markdown("""
    A scatter matrix is a powerful way to visualize multiple relationships at once:
    
    - The **diagonal** shows the distribution of each feature
    - Each **off-diagonal plot** shows the relationship between two features
    - **Clusters** of similarly colored points indicate stars of the same spectral class sharing similar properties
    - **Trends** (like diagonal patterns) show correlated features
    
    For example, you can observe how temperature and luminosity are related, or how radius correlates with absolute magnitude.
    """)

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | Data source: Stellar dataset")
