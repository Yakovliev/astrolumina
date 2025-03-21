import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set a default template for all plots
template = "plotly_white"

# Map numeric Star type to category names if needed
star_type_mapping = {
    0: 'Brown Dwarf',
    1: 'Red Dwarf',
    2: 'White Dwarf',
    3: 'Main Sequence',
    4: 'Supergiants',
    5: 'Hypergiants'
}


def create_star_type_bar_chart(star_df):
    """Create a bar chart showing the count of each star type."""
    # Add star type labels if not already present
    if 'Star type label' not in star_df.columns and pd.api.types.is_numeric_dtype(star_df['Star type']):
        star_df['Star type label'] = star_df['Star type'].map(
            star_type_mapping)
        count_column = 'Star type label'
    else:
        count_column = 'Star type'

    # Count values by star type
    star_type_counts = star_df[count_column].value_counts().reset_index()
    star_type_counts.columns = ['Star type', 'Count']

    # Calculate percentage
    star_type_counts['percentage'] = (
        star_type_counts['Count'] / star_type_counts['Count'].sum() * 100)

    # Create bar chart using Plotly
    fig = px.bar(
        star_type_counts,
        x='Star type',
        y='Count',
        color='Star type',  # Color bars by star type
        text='Count',       # Show count on bars
        title='Star Count by Type'
    )

    # Add hover template with percentage
    fig.update_traces(
        hovertemplate='Star Type: %{x}<br>Count: %{y}<br>Percentage: %{customdata:.2f}%',
        customdata=star_type_counts['percentage']
    )

    # Update layout
    fig.update_layout(
        template=template,
        height=500,
        width=700,
        title_x=0.5,
        showlegend=False
    )

    return fig


def create_star_color_bar_chart(star_df):
    """Create a bar chart showing the count of each star color."""
    # Calculating value counts for 'Star color'
    star_color_counts = star_df['Star color'].value_counts().reset_index()
    star_color_counts.columns = ['Star color', 'Count']

    # Adding percentage calculation
    star_color_counts['percentage'] = (
        star_color_counts['Count'] / star_color_counts['Count'].sum() * 100).round(2)

    # Color mapping that matches actual star colors
    color_map = {
        'Red': 'OrangeRed',
        'Blue': 'blue',
        'Blue-White': 'lightblue',
        'White': 'azure',
        'Yellow-White': 'yellow',
        'Yellowish': 'gold',
        'Orange': 'orange',
        'Orange-Red': 'tomato',
        # Add any other colors that might be in your dataset
    }

    # Creating the bar plot
    fig = px.bar(
        star_color_counts,
        x='Star color',
        y='Count',
        title='Count of Stars by Color',
        text='Count',
        color='Star color',
        color_discrete_map=color_map
    )

    # Add hover template with percentage
    fig.update_traces(
        hovertemplate='Star Color: %{x}<br>Count: %{y}<br>Percentage: %{customdata:.2f}%',
        customdata=star_color_counts['percentage']
    )

    # Update layout
    fig.update_layout(
        template=template,
        height=500,
        width=700,
        title_x=0.5,
        xaxis_title='Star Color',
        yaxis_title='Count',
        showlegend=False
    )

    return fig


def create_boxplots(star_df):
    """Create box plots for numeric features grouped by star type."""
    numeric_features = [
        'Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']

    # Create 2x2 grid
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=numeric_features,
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )

    # Define colors for different star types for consistency
    colors = {
        'Brown Dwarf': 'brown',
        'Red Dwarf': 'red',
        'White Dwarf': 'lightskyblue',
        'Main Sequence': 'yellow',
        'Supergiants': 'blue',
        'Hypergiants': 'orange'
    }

    # Position mapping for 2x2 grid
    positions = [(1, 1), (1, 2), (2, 1), (2, 2)]

    # Add box plots for each numeric feature grouped by star type
    for i, feature in enumerate(numeric_features):
        row, col = positions[i]

        for star_type in star_df['Star type'].unique():
            # Filter data for this star type
            subset = star_df[star_df['Star type'] == star_type]

            # Skip if there are no data points for this star type
            if len(subset) == 0:
                continue

            # Get color from mapping or use a default
            color = colors.get(star_type, 'gray')

            fig.add_trace(
                go.Box(
                    y=subset[feature],
                    name=star_type,
                    marker_color=color,
                    boxmean=True,
                    boxpoints='outliers',
                    jitter=0,
                    pointpos=0,
                    line_width=2,
                    fillcolor=color,
                    opacity=0.7,
                    showlegend=i == 0,
                    quartilemethod="linear",
                    width=0.4
                ),
                row=row,
                col=col
            )

    fig.update_layout(
        template=template,
        title='Feature Distribution by Star Type',
        title_x=0.5,
        height=700,
        width=850,
        boxmode='group',
        boxgroupgap=0.2,
        boxgap=0.1,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )

    # Add feature names as y-axis titles
    for i, feature in enumerate(numeric_features):
        row, col = positions[i]
        fig.update_yaxes(title_text=feature, row=row, col=col)

    return fig


def create_hr_diagram(star_df):
    """Create a Hertzsprung-Russell diagram."""
    # Create base scatter plot
    fig = px.scatter(
        star_df,
        x='Temperature (K)',
        y='Absolute magnitude(Mv)',
        color='Star type',
        title='Hertzsprung-Russell Diagram',
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Bold
    )

    # Add the Sun
    fig.add_trace(go.Scatter(
        x=[5778],
        y=[4.83],
        mode='markers+text',
        name='Sun',
        text=['Sun'],
        textposition='top center',
        marker=dict(
            size=12,
            color='gold',
            line=dict(width=2, color='orange'),
            symbol='star'
        )
    ))

    # Improve layout
    fig.update_layout(
        template='plotly_dark',
        title={
            'text': 'Hertzsprung-Russell Diagram',
            'font': {'size': 24}
        },
        title_x=0.5,
        xaxis=dict(
            title='Temperature (K)',
            autorange='reversed',
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        yaxis=dict(
            title='Absolute Magnitude (Mv)',
            autorange='reversed',
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        legend=dict(
            title='Star Type',
            bordercolor='rgba(255, 255, 255, 0.3)',
            borderwidth=1
        ),
        plot_bgcolor='rgba(15, 15, 35, 1)',
        paper_bgcolor='rgba(10, 10, 30, 1)',
        height=600,
        width=800
    )

    # Add star classification regions
    regions = [
        dict(x=30000, y=0, text="Hot Blue Stars", color="lightblue"),
        dict(x=6000, y=15, text="Red Giants", color="lightcoral"),
        dict(x=6000, y=0, text="Main Sequence", color="white")
    ]

    for region in regions:
        fig.add_annotation(
            x=region['x'],
            y=region['y'],
            text=region['text'],
            showarrow=False,
            font=dict(size=14, color=region['color'])
        )

    return fig


def create_scatter_matrix(star_df):
    numeric_features = [
        'Temperature (K)', 'Luminosity(L/Lo)', 'Radius(R/Ro)', 'Absolute magnitude(Mv)']

    # Create the scatter matrix with improved parameters
    fig = px.scatter_matrix(
        star_df,
        dimensions=numeric_features,
        color='Spectral Class',
        title='Scatter Matrix of Star Features',
        opacity=0.7,  # Slightly higher opacity for better visibility
        height=900,   # Increased height for better clarity
        width=1000,   # Width to maintain proportion
        color_discrete_sequence=px.colors.qualitative.Bold,  # Better color scheme
        labels={col: col.split('(')[0].strip()
                for col in numeric_features}  # Shorter axis labels
    )

    fig.update_layout(
        template=template,
        title_x=0.5,
        title_font=dict(size=20),  # Larger title font
        font=dict(size=12),        # Larger overall font size
        dragmode='select',         # Enable box select mode
        margin=dict(l=50, r=50, t=80, b=50)  # Adjust margins for better layout
    )

    # Improve marker appearance
    fig.update_traces(
        marker=dict(
            size=6,                # Slightly larger points
            # Add thin line around markers for definition
            line=dict(width=0.5),
            symbol='circle'        # Consistent symbol
        ),
        diagonal_visible=True      # Ensure diagonals are visible
    )

    # Improve readability of axis titles
    for axis in fig.layout:
        if axis.startswith('xaxis') or axis.startswith('yaxis'):
            fig.layout[axis].title.font.size = 14

    # Add grid lines for better readability
    fig.update_xaxes(showgrid=True, gridwidth=0.5,
                     gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=0.5,
                     gridcolor='rgba(128,128,128,0.2)')

    return fig


def create_hr_diagram_improved(star_df):
    # Create base scatter plot
    fig = px.scatter(
        star_df,
        x='Temperature (K)',
        y='Absolute magnitude(Mv)',
        color='Star type',
        title='Hertzsprung-Russell Diagram',
        opacity=0.8,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    # Add the Sun with improved marker
    fig.add_trace(go.Scatter(
        x=[5778],
        y=[4.83],
        mode='markers+text',
        name='Sun',
        text=['Sun'],
        textposition='top center',
        marker=dict(
            size=12,
            color='gold',
            line=dict(width=2, color='orange'),
            symbol='star'
        ),
        textfont=dict(color='gold')  # Make Sun text visible
    ))

    # Add famous stars with their properties
    famous_stars = {
        'Sirius': {'temp': 9940, 'mag': 1.42, 'color': 'rgb(170, 170, 255)'},
        'Betelgeuse': {'temp': 3600, 'mag': -5.85, 'color': 'rgb(255, 100, 50)'},
        'Vega': {'temp': 9602, 'mag': 0.58, 'color': 'rgb(200, 200, 255)'},
        'Proxima Centauri': {'temp': 3042, 'mag': 15.6, 'color': 'rgb(255, 120, 100)'},
    }

    for star, props in famous_stars.items():
        fig.add_trace(go.Scatter(
            x=[props['temp']],
            y=[props['mag']],
            mode='markers+text',
            name=star,
            text=[star],
            textposition='top right',
            marker=dict(
                size=10,
                color=props['color'],
                symbol='star'
            ),
            textfont=dict(color=props['color'])  # Use matching color for text
        ))

    # Improve layout
    fig.update_layout(
        template='plotly_dark',
        title={
            'text': 'Interactive Hertzsprung-Russell Diagram',
            'font': {'size': 24, 'color': 'white'}  # Ensure title is visible
        },
        title_x=0.5,
        xaxis=dict(
            title='Temperature (K)',
            autorange='reversed',
            gridcolor='rgba(128, 128, 128, 0.2)',
            title_font=dict(color='white'),  # Make axis title visible
            tickfont=dict(color='white')  # Make tick labels visible
        ),
        yaxis=dict(
            title='Absolute Magnitude (Mv)',
            autorange='reversed',
            gridcolor='rgba(128, 128, 128, 0.2)',
            title_font=dict(color='white'),  # Make axis title visible
            tickfont=dict(color='white'),  # Make tick labels visible
            # Make zero line less prominent
            zerolinecolor='rgba(100, 100, 100, 0.4)',
            zerolinewidth=1
        ),
        legend=dict(
            title='Star Type',
            bordercolor='rgba(255, 255, 255, 0.3)',
            borderwidth=1,
            font=dict(color='white'),  # Make legend text visible
            title_font=dict(color='white')  # Make legend title visible
        ),
        plot_bgcolor='rgb(10, 10, 35)',
        paper_bgcolor='rgb(5, 5, 25)',
        height=600,  # Reduced height
        width=750,   # Reduced width for better proportions
    )

    # Add main sequence line (simplified)
    main_sequence_temps = [30000, 20000, 10000, 7500, 6000, 5000, 3500]
    main_sequence_mags = [-5, -2.5, 0, 2, 4, 6, 9]

    fig.add_trace(go.Scatter(
        x=main_sequence_temps,
        y=main_sequence_mags,
        mode='lines',
        line=dict(dash='solid', width=2, color='white'),
        name='Main Sequence'
    ))

    # Add simple annotations for star types - ensure all text is visible with appropriate colors
    annotations = [
        dict(x=25000, y=-3, text="Blue Giants",
             showarrow=False, font=dict(color="lightblue", size=12)),
        dict(x=4000, y=-3, text="Red Giants",
             showarrow=False, font=dict(color="lightcoral", size=12)),
        dict(x=15000, y=2, text="Main Sequence",
             showarrow=False, font=dict(color="white", size=12)),
        dict(x=10000, y=12, text="White Dwarfs",
             showarrow=False, font=dict(color="white", size=12))
    ]

    for annotation in annotations:
        fig.add_annotation(annotation)

    return fig
