import pandas as pd
import streamlit as st
import plotly.express as px


# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------
st.set_page_config(
    page_title="Sports Car Price Dashboard",
    layout="wide"
)


# ---------------------------------------------------
# LOAD AND CLEAN DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    df = pd.read_csv("sports_car_prices.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Numeric columns
    numeric_columns = [
        "Year",
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)",
        "0-60 MPH Time (seconds)",
        "Price (in USD)"
    ]

    # Convert numeric columns safely
    for column in numeric_columns:

        if column in df.columns:

            df[column] = (
                df[column]
                .astype(str)
                .str.replace(",", "", regex=False)
                .str.replace("$", "", regex=False)
                .str.strip()
            )

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    return df


df = load_data()


# ---------------------------------------------------
# DASHBOARD TITLE
# ---------------------------------------------------
st.title("Sports Car Price Analysis Dashboard")

st.write(
    """
    This interactive dashboard provides an analysis of sports car prices
    and performance. Explore manufacturers, models, production years,
    engine sizes, horsepower, torque, acceleration, and prices.
    """
)

st.divider()


# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")


# Car Make Filter
car_makes = sorted(
    df["Car Make"]
    .dropna()
    .unique()
)

selected_makes = st.sidebar.multiselect(
    "Select Car Make",
    options=car_makes,
    default=car_makes
)


# Year Filter
min_year = int(df["Year"].min())
max_year = int(df["Year"].max())

selected_years = st.sidebar.slider(
    "Select Year Range",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)
)


# Price Filter
price_data = df["Price (in USD)"].dropna()

min_price = float(price_data.min())
max_price = float(price_data.max())

selected_price = st.sidebar.slider(
    "Select Price Range (USD)",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)
)


# ---------------------------------------------------
# FILTER DATA
# ---------------------------------------------------
filtered_df = df.copy()

filtered_df = filtered_df[
    filtered_df["Car Make"].isin(selected_makes)
]

filtered_df = filtered_df[
    filtered_df["Year"].between(
        selected_years[0],
        selected_years[1]
    )
]

filtered_df = filtered_df[
    filtered_df["Price (in USD)"].between(
        selected_price[0],
        selected_price[1]
    )
]


# ---------------------------------------------------
# HANDLE EMPTY FILTER RESULTS
# ---------------------------------------------------
if filtered_df.empty:

    st.warning(
        "No cars match the selected filters. Please adjust your filters."
    )

    st.stop()


# ---------------------------------------------------
# KEY METRICS
# ---------------------------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Cars",
        f"{len(filtered_df):,}"
    )


with col2:

    st.metric(
        "Average Price",
        f"${filtered_df['Price (in USD)'].mean():,.0f}"
    )


with col3:

    st.metric(
        "Highest Price",
        f"${filtered_df['Price (in USD)'].max():,.0f}"
    )


with col4:

    st.metric(
        "Car Manufacturers",
        filtered_df["Car Make"].nunique()
    )


col5, col6, col7 = st.columns(3)


with col5:

    st.metric(
        "Average Horsepower",
        f"{filtered_df['Horsepower'].mean():,.0f} HP"
    )


with col6:

    st.metric(
        "Average Engine Size",
        f"{filtered_df['Engine Size (L)'].mean():.1f} L"
    )


with col7:

    st.metric(
        "Average 0-60 Time",
        f"{filtered_df['0-60 MPH Time (seconds)'].mean():.2f} sec"
    )


st.divider()


# ---------------------------------------------------
# DATASET OVERVIEW
# ---------------------------------------------------
st.header("Dataset Overview")


tab1, tab2, tab3, tab4 = st.tabs([
    "Full Dataset",
    "Dataset Information",
    "Missing Values",
    "Statistical Summary"
])


# ---------------------------------------------------
# FULL DATASET
# ---------------------------------------------------
with tab1:

    st.subheader("Filtered Sports Car Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("First Five Rows")

        st.dataframe(
            filtered_df.head()
        )

    with col2:

        st.subheader("Last Five Rows")

        st.dataframe(
            filtered_df.tail()
        )


# ---------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------
with tab2:

    st.subheader("Dataset Columns and Data Types")

    column_info = pd.DataFrame({
        "Column Name": filtered_df.columns,
        "Data Type": filtered_df.dtypes.astype(str)
    })

    st.dataframe(
        column_info,
        use_container_width=True
    )


    rows, columns = filtered_df.shape

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Number of Rows",
            rows
        )

    with col2:

        st.metric(
            "Number of Columns",
            columns
        )


# ---------------------------------------------------
# MISSING VALUES
# ---------------------------------------------------
with tab3:

    st.subheader("Missing Values Analysis")

    missing_values = pd.DataFrame({
        "Column": filtered_df.columns,
        "Missing Values": filtered_df.isnull().sum().values
    })

    st.dataframe(
        missing_values,
        use_container_width=True
    )


# ---------------------------------------------------
# DESCRIPTIVE STATISTICS
# ---------------------------------------------------
with tab4:

    st.subheader("Descriptive Statistics")

    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------
# VISUALIZATIONS
# ---------------------------------------------------
st.header("Sports Car Price and Performance Analysis")


# ---------------------------------------------------
# ROW 1
# ---------------------------------------------------
col1, col2 = st.columns(2)


# Cars by Manufacturer
with col1:

    car_make_counts = (
        filtered_df["Car Make"]
        .value_counts()
        .reset_index()
    )

    car_make_counts.columns = [
        "Car Make",
        "Number of Cars"
    ]

    fig_make = px.bar(
        car_make_counts,
        x="Car Make",
        y="Number of Cars",
        title="Number of Sports Cars by Manufacturer",
        text="Number of Cars"
    )

    fig_make.update_layout(
        template="plotly_white",
        xaxis_title="Car Manufacturer",
        yaxis_title="Number of Cars"
    )

    st.plotly_chart(
        fig_make,
        use_container_width=True
    )


# Price Distribution
with col2:

    price_chart_df = filtered_df.dropna(
        subset=["Price (in USD)"]
    )

    fig_price_distribution = px.histogram(
        price_chart_df,
        x="Price (in USD)",
        nbins=30,
        title="Sports Car Price Distribution"
    )

    fig_price_distribution.update_layout(
        template="plotly_white",
        xaxis_title="Price (USD)",
        yaxis_title="Number of Cars"
    )

    st.plotly_chart(
        fig_price_distribution,
        use_container_width=True
    )


# ---------------------------------------------------
# ROW 2
# ---------------------------------------------------
col1, col2 = st.columns(2)


# Price by Manufacturer
with col1:

    price_make_df = filtered_df.dropna(
        subset=[
            "Car Make",
            "Price (in USD)"
        ]
    )

    fig_price_make = px.box(
        price_make_df,
        x="Car Make",
        y="Price (in USD)",
        title="Sports Car Prices by Manufacturer",
        points=False
    )

    fig_price_make.update_layout(
        template="plotly_white",
        xaxis_title="Car Manufacturer",
        yaxis_title="Price (USD)"
    )

    st.plotly_chart(
        fig_price_make,
        use_container_width=True
    )


# Horsepower Distribution
with col2:

    horsepower_df = filtered_df.dropna(
        subset=["Horsepower"]
    )

    fig_horsepower = px.histogram(
        horsepower_df,
        x="Horsepower",
        nbins=30,
        title="Horsepower Distribution"
    )

    fig_horsepower.update_layout(
        template="plotly_white",
        xaxis_title="Horsepower",
        yaxis_title="Number of Cars"
    )

    st.plotly_chart(
        fig_horsepower,
        use_container_width=True
    )


# ---------------------------------------------------
# ROW 3
# ---------------------------------------------------
col1, col2 = st.columns(2)


# Price vs Horsepower
with col1:

    horsepower_price_df = filtered_df.dropna(
        subset=[
            "Horsepower",
            "Price (in USD)",
            "Car Make"
        ]
    )

    fig_price_hp = px.scatter(
        horsepower_price_df,
        x="Horsepower",
        y="Price (in USD)",
        color="Car Make",
        hover_name="Car Model",
        hover_data=[
            "Year",
            "Engine Size (L)",
            "Torque (lb-ft)",
            "0-60 MPH Time (seconds)"
        ],
        title="Horsepower vs Sports Car Price"
    )

    fig_price_hp.update_layout(
        template="plotly_white",
        xaxis_title="Horsepower",
        yaxis_title="Price (USD)"
    )

    st.plotly_chart(
        fig_price_hp,
        use_container_width=True
    )


# Engine Size vs Price
with col2:

    engine_price_df = filtered_df.dropna(
        subset=[
            "Engine Size (L)",
            "Price (in USD)",
            "Car Make"
        ]
    )

    fig_engine_price = px.scatter(
        engine_price_df,
        x="Engine Size (L)",
        y="Price (in USD)",
        color="Car Make",
        hover_name="Car Model",
        hover_data=[
            "Year",
            "Horsepower",
            "Torque (lb-ft)"
        ],
        title="Engine Size vs Sports Car Price"
    )

    fig_engine_price.update_layout(
        template="plotly_white",
        xaxis_title="Engine Size (L)",
        yaxis_title="Price (USD)"
    )

    st.plotly_chart(
        fig_engine_price,
        use_container_width=True
    )


# ---------------------------------------------------
# ROW 4
# ---------------------------------------------------
col1, col2 = st.columns(2)


# Production Year vs Price
with col1:

    year_price_df = filtered_df.dropna(
        subset=[
            "Year",
            "Price (in USD)",
            "Car Make"
        ]
    )

    fig_year_price = px.scatter(
        year_price_df,
        x="Year",
        y="Price (in USD)",
        color="Car Make",
        hover_name="Car Model",
        hover_data=[
            "Horsepower",
            "Engine Size (L)"
        ],
        title="Production Year vs Sports Car Price"
    )

    fig_year_price.update_layout(
        template="plotly_white",
        xaxis_title="Production Year",
        yaxis_title="Price (USD)"
    )

    st.plotly_chart(
        fig_year_price,
        use_container_width=True
    )


# 0-60 Time Distribution
with col2:

    acceleration_distribution_df = filtered_df.dropna(
        subset=["0-60 MPH Time (seconds)"]
    )

    fig_acceleration = px.histogram(
        acceleration_distribution_df,
        x="0-60 MPH Time (seconds)",
        nbins=20,
        title="0-60 MPH Acceleration Distribution"
    )

    fig_acceleration.update_layout(
        template="plotly_white",
        xaxis_title="0-60 MPH Time (Seconds)",
        yaxis_title="Number of Cars"
    )

    st.plotly_chart(
        fig_acceleration,
        use_container_width=True
    )


# ---------------------------------------------------
# PRICE VS ACCELERATION
# ---------------------------------------------------
st.divider()

st.subheader("Price vs Acceleration")

acceleration_df = filtered_df.dropna(
    subset=[
        "0-60 MPH Time (seconds)",
        "Price (in USD)",
        "Car Make",
        "Car Model"
    ]
)

# No size parameter is used here.
# This prevents Plotly bubble size validation errors.

fig_price_acceleration = px.scatter(
    acceleration_df,
    x="0-60 MPH Time (seconds)",
    y="Price (in USD)",
    color="Car Make",
    hover_name="Car Model",
    hover_data=[
        "Year",
        "Engine Size (L)",
        "Horsepower",
        "Torque (lb-ft)"
    ],
    title="Sports Car Price vs 0-60 MPH Time"
)

fig_price_acceleration.update_layout(
    template="plotly_white",
    xaxis_title="0-60 MPH Time (Seconds)",
    yaxis_title="Price (USD)"
)

st.plotly_chart(
    fig_price_acceleration,
    use_container_width=True
)


# ---------------------------------------------------
# MANUFACTURER PERFORMANCE ANALYSIS
# ---------------------------------------------------
st.divider()

st.header("Manufacturer Performance Analysis")


manufacturer_summary = (
    filtered_df
    .groupby("Car Make")
    .agg(
        Number_of_Cars=(
            "Car Model",
            "count"
        ),

        Average_Price=(
            "Price (in USD)",
            "mean"
        ),

        Average_Horsepower=(
            "Horsepower",
            "mean"
        ),

        Average_Engine_Size=(
            "Engine Size (L)",
            "mean"
        ),

        Average_0_60_Time=(
            "0-60 MPH Time (seconds)",
            "mean"
        )
    )
    .reset_index()
)


# Round numeric values
manufacturer_summary = manufacturer_summary.round(2)


st.dataframe(
    manufacturer_summary,
    use_container_width=True
)


# ---------------------------------------------------
# AVERAGE PRICE BY MANUFACTURER
# ---------------------------------------------------
average_price_df = manufacturer_summary.dropna(
    subset=["Average_Price"]
)

fig_average_price = px.bar(
    average_price_df,
    x="Car Make",
    y="Average_Price",
    title="Average Sports Car Price by Manufacturer",
    text_auto=".0f"
)

fig_average_price.update_layout(
    template="plotly_white",
    xaxis_title="Car Manufacturer",
    yaxis_title="Average Price (USD)"
)

st.plotly_chart(
    fig_average_price,
    use_container_width=True
)


# ---------------------------------------------------
# AVERAGE HORSEPOWER BY MANUFACTURER
# ---------------------------------------------------
average_hp_df = manufacturer_summary.dropna(
    subset=["Average_Horsepower"]
)

fig_average_hp = px.bar(
    average_hp_df,
    x="Car Make",
    y="Average_Horsepower",
    title="Average Horsepower by Manufacturer",
    text_auto=".0f"
)

fig_average_hp.update_layout(
    template="plotly_white",
    xaxis_title="Car Manufacturer",
    yaxis_title="Average Horsepower"
)

st.plotly_chart(
    fig_average_hp,
    use_container_width=True
)


# ---------------------------------------------------
# TOP 10 MOST EXPENSIVE SPORTS CARS
# ---------------------------------------------------
st.divider()

st.header("Top 10 Most Expensive Sports Cars")


top_expensive_cars = (
    filtered_df
    .dropna(subset=["Price (in USD)"])
    .sort_values(
        by="Price (in USD)",
        ascending=False
    )
    .head(10)
)


st.dataframe(
    top_expensive_cars,
    use_container_width=True
)


fig_top_expensive = px.bar(
    top_expensive_cars,
    x="Car Model",
    y="Price (in USD)",
    color="Car Make",
    hover_data=[
        "Year",
        "Horsepower",
        "Engine Size (L)"
    ],
    title="Top 10 Most Expensive Sports Cars"
)

fig_top_expensive.update_layout(
    template="plotly_white",
    xaxis_title="Car Model",
    yaxis_title="Price (USD)"
)

st.plotly_chart(
    fig_top_expensive,
    use_container_width=True
)


# ---------------------------------------------------
# DOWNLOAD FILTERED DATA
# ---------------------------------------------------
st.divider()

st.header("Download Filtered Data")


csv = (
    filtered_df
    .to_csv(index=False)
    .encode("utf-8")
)


st.download_button(
    label="Download Filtered Dataset as CSV",
    data=csv,
    file_name="filtered_sports_car_prices.csv",
    mime="text/csv"
)