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
