import streamlit as st
import pandas as pd

# Import functions from our modules
from src.data_processing import load_star_data
from src.visualization import (
    create_star_type_bar_chart,
    create_star_color_bar_chart,
    create_boxplots,
    create_hr_diagram
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
    ["📊 Star Types", "🎨 Star Colors", "📏 Physical Properties", "🌠 HR Diagram"]
)

# Display different pages based on selection
if page == "📊 Star Types":
    st.header("Star Types Distribution")
    st.markdown("""
    This visualization shows the distribution of different star types in our dataset.
    Each bar represents the count of stars belonging to a specific star type.
    """)

    fig = create_star_type_bar_chart(df)
    st.plotly_chart(fig, use_container_width=True)

    # Additional information
    st.subheader("About Star Types")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Main Sequence Stars**: The majority of stars, including our Sun, are main sequence stars. 
        They fuse hydrogen into helium in their cores.
        
        **Red Dwarfs**: These are the most common type of star in the Milky Way. They're small, cool, and have long lifespans.
        
        **White Dwarfs**: These are remnants of stars that have exhausted their nuclear fuel.
        """)

    with col2:
        st.markdown("""
        **Brown Dwarfs**: Objects too large to be classified as planets but too small to sustain hydrogen fusion.
        
        **Supergiants**: These are massive stars that have evolved away from the main sequence.
        
        **Hypergiants**: These are extremely massive and luminous stars, among the most massive and luminous known.
        """)

elif page == "🎨 Star Colors":
    st.header("Star Colors Distribution")
    st.markdown("""
    This visualization shows the distribution of different star colors in our dataset.
    The color of a star is primarily determined by its surface temperature.
    """)

    fig = create_star_color_bar_chart(df)
    st.plotly_chart(fig, use_container_width=True)

    # Additional information about star colors
    st.subheader("What Determines a Star's Color?")
    st.markdown("""
    The color of a star is primarily determined by its surface temperature:
    
    - **Blue/Blue-White stars** (>10,000K): The hottest stars appear blue or blue-white.
    - **White stars** (~8,000K): Stars like Sirius appear white.
    - **Yellow/Yellow-White stars** (~6,000K): Stars like our Sun appear yellow or yellow-white.
    - **Orange stars** (~4,000K): Cooler stars appear orange.
    - **Red stars** (<3,500K): The coolest stars appear red.
    """)

elif page == "📏 Physical Properties":
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

    fig = create_hr_diagram(df)
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

# Footer
st.markdown("---")
st.markdown("Created with ❤️ using Streamlit | Data source: Stellar dataset")
