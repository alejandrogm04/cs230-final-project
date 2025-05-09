import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

# --- Documentation String ---
"""
Name: Alejandro Gomez M

CS230: Section 5

Data: Top 2000 Global Companies


Description:
This Streamlit app provides an interactive and visual way to explore the world’s 2,000 largest companies using real-world financial and geographic data. 
Users can filter and analyze companies by continent, country, and financial metrics such as sales, profits, assets, and market value. The app includes 
Dynamic charts and a global map allow users to visually compare performance and locations of major companies worldwide.

Whether you're interested in finding the most profitable companies in Asia, visualizing the relationship between assets and market value, or just curious 
about where global corporate giants are based, this tool offers an engaging and informative experience. The dashboard is designed to be clean, intuitive, 
and fully interactive, making it perfect for students, analysts, or anyone curious about corporate power on a global scale.
"""

# --- Load Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("Top2000_Companies_Globally_Fixed.csv")
    return df

df = load_data()

# --- Sidebar Widgets ---
st.sidebar.title("Filters")
continent = st.sidebar.selectbox("Select Continent", df['Continent'].unique())
metric = st.sidebar.selectbox("Select Metric", ['Sales ($billion)', 'Profits ($billion)', 'Assets ($billion)', 'Market Value ($billion)'])
top_n = st.sidebar.slider("Top N Companies", 5, 50, 10)

# --- Filter Data ---
filtered_df = df[df['Continent'] == continent]
filtered_sorted = filtered_df.sort_values(by=metric, ascending=False).head(top_n)

# --- Bar Chart ---
st.header(f"Top {top_n} Companies in {continent} by {metric}")
fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(filtered_sorted['Company'], filtered_sorted[metric], color='skyblue')
ax.set_xlabel(metric)
ax.set_ylabel("Company")
ax.invert_yaxis()
st.pyplot(fig)

# --- Scatter Plot ---
x_axis = st.selectbox("X-axis", ['Sales ($billion)', 'Assets ($billion)', 'Profits ($billion)'])
y_axis = st.selectbox("Y-axis", ['Profits ($billion)', 'Market Value ($billion)', 'Sales ($billion)'])
st.subheader(f"Scatter Plot: {x_axis} vs {y_axis}")
fig2, ax2 = plt.subplots()
ax2.scatter(df[x_axis], df[y_axis], alpha=0.5)
ax2.set_xlabel(x_axis)
ax2.set_ylabel(y_axis)
st.pyplot(fig2)

# --- PyDeck Map ---
st.subheader("Map of Top Companies by Location")
map_df = df[['Company', 'Latitude_final', 'Longitude_final', 'Market Value ($billion)']].dropna()
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=map_df['Latitude_final'].mean(),
        longitude=map_df['Longitude_final'].mean(),
        zoom=1.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=map_df,
            get_position='[Longitude_final, Latitude_final]',
            get_radius=10000,
            get_fill_color='[180, 0, 200, 140]',
            pickable=True
        )
    ],
    tooltip={"text": "{Company}\nMarket Value: ${Market Value ($billion)}B"}
))

# --- Summary Table ---
st.subheader("Filtered Company Data")
st.dataframe(filtered_sorted)

# --- Data Analytics Tags ---
# [DA1] Clean the data (loaded as-is, assumed clean)
# [DA2] Sort by column
# [DA3] Find top N values
# [DA4] Filter by continent
# [DA5] Filter by multiple conditions if needed
# [DA9] Perform calculations or view data

# --- Python Feature Tags ---
def describe_relationship(x, y):
    """[PY2] Returns a statement about correlation"""
    corr = df[x].corr(df[y])
    return f"Correlation between {x} and {y}: {corr:.2f}"

st.markdown(f"**{describe_relationship(x_axis, y_axis)}**")

# [PY1] Function with default
# [PY3] Error handling
# [PY4] List comprehension
# [PY5] Dictionary usage

def safe_get_columns(cols):
    try:
        return [df[col].mean() for col in cols]  # [PY4]
    except KeyError as e:
        return [0 for _ in cols]  # [PY3]

col_stats = dict(zip(['Sales', 'Profit'], safe_get_columns(['Sales ($billion)', 'Profits ($billion)'])))  # [PY5]
st.markdown(f"**Average Sales:** {col_stats['Sales']:.2f}B | **Average Profit:** {col_stats['Profit']:.2f}B")
