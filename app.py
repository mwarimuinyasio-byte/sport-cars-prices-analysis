import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------
st.set_page_config(
    page_title="Sports Cars Price Dashboard",
    layout="wide"
)

# ---------------------------------------------------
# Load Dataset
# ---------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("sports_car_prices.csv")


df = load_data()


# ---------------------------------------------------
# Dashboard Title
# ---------------------------------------------------
st.title("Sports Cars Price Analysis Dashboard")

st.markdown("""
This dashboard provides an interactive analysis of sports car prices,
including car manufacturers, models, production years, mileage,
horsepower, engine size, and other available features.
""")

st.divider()


# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------
st.sidebar.header("Dashboard Filters")

# Car Make Filter
if "Make" in df.columns:
    makes = st.sidebar.multiselect(
        "Select Car Make",
        options=df["Make"].unique(),
        default=df["Make"].unique()
    )
else:
    makes = None


# Price Filter
if "Price" in df.columns:

    min_price = float(df["Price"].min())
    max_price = float(df["Price"].max())

    price_range = st.sidebar.slider(
        "Select Price Range",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price)
    )


# ---------------------------------------------------
# Filter Dataset
# ---------------------------------------------------
filtered_df = df.copy()

if "Make" in df.columns and makes is not None:
    filtered_df = filtered_df[
        filtered_df["Make"].isin(makes)
    ]

if "Price" in df.columns:
    filtered_df = filtered_df[
        filtered_df["Price"].between(
            price_range[0],
            price_range[1]
        )
    ]


# ---------------------------------------------------
# Key Metrics
# ---------------------------------------------------
st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cars",
        f"{len(filtered_df):,}"
    )

with col2:
    if "Price" in filtered_df.columns:
        st.metric(
            "Average Price",
            f"${filtered_df['Price'].mean():,.2f}"
        )

with col3:
    if "Price" in filtered_df.columns:
        st.metric(
            "Highest Price",
            f"${filtered_df['Price'].max():,.2f}"
        )

with col4:
    if "Make" in filtered_df.columns:
        st.metric(
            "Car Manufacturers",
            filtered_df["Make"].nunique()
        )


st.divider()


# ---------------------------------------------------
# Dataset Overview
# ---------------------------------------------------
st.header("Dataset Overview")

tab1, tab2, tab3, tab4 = st.tabs([
    "Full Dataset",
    "Dataset Information",
    "Missing Values",
    "Statistics"
])


# ---------------------------------------------------
# Full Dataset
# ---------------------------------------------------
with tab1:

    st.subheader("Sports Cars Dataset")

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("First Five Rows")
        st.dataframe(filtered_df.head())

    with col2:
        st.subheader("Last Five Rows")
        st.dataframe(filtered_df.tail())


# ---------------------------------------------------
# Dataset Information
# ---------------------------------------------------
with tab2:

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
        st.metric("Number of Rows", rows)

    with col2:
        st.metric("Number of Columns", columns)


# ---------------------------------------------------
# Missing Values
# ---------------------------------------------------
with tab3:

    missing_values = (
        filtered_df
        .isnull()
        .sum()
        .reset_index()
    )

    missing_values.columns = [
        "Column",
        "Missing Values"
    ]

    st.dataframe(
        missing_values,
        use_container_width=True
    )


# ---------------------------------------------------
# Descriptive Statistics
# ---------------------------------------------------
with tab4:

    st.dataframe(
        filtered_df.describe(),
        use_container_width=True
    )


st.divider()


# ---------------------------------------------------
# Visualizations
# ---------------------------------------------------
st.header("Sports Car Price Visualizations")


# ---------------------------------------------------
# Cars by Manufacturer
# ---------------------------------------------------
if "Make" in filtered_df.columns:

    car_counts = (
        filtered_df["Make"]
        .value_counts()
        .reset_index()
    )

    car_counts.columns = [
        "Make",
        "Number of Cars"
    ]

    fig_make = px.bar(
        car_counts,
        x="Make",
        y="Number of Cars",
        title="Number of Sports Cars by Manufacturer",
        text="Number of Cars"
    )

    fig_make.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_make,
        use_container_width=True
    )


# ---------------------------------------------------
# Price Distribution
# ---------------------------------------------------
if "Price" in filtered_df.columns:

    fig_price = px.histogram(
        filtered_df,
        x="Price",
        nbins=30,
        title="Sports Car Price Distribution"
    )

    fig_price.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True
    )


# ---------------------------------------------------
# Two Column Charts
# ---------------------------------------------------
col1, col2 = st.columns(2)


# Price by Manufacturer
with col1:

    if "Make" in filtered_df.columns and "Price" in filtered_df.columns:

        fig_price_make = px.box(
            filtered_df,
            x="Make",
            y="Price",
            title="Sports Car Prices by Manufacturer",
            points=False
        )

        fig_price_make.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_price_make,
            use_container_width=True
        )


# Horsepower Distribution
with col2:

    if "Horsepower" in filtered_df.columns:

        fig_hp = px.histogram(
            filtered_df,
            x="Horsepower",
            nbins=30,
            title="Horsepower Distribution"
        )

        fig_hp.update_layout(
            template="plotly_white"
        )

        st.plotly_chart(
            fig_hp,
            use_container_width=True
        )


# ---------------------------------------------------
# Price vs Horsepower
# ---------------------------------------------------
if (
    "Horsepower" in filtered_df.columns
    and "Price" in filtered_df.columns
):

    fig_scatter = px.scatter(
        filtered_df,
        x="Horsepower",
        y="Price",
        color="Make" if "Make" in filtered_df.columns else None,
        hover_data=filtered_df.columns.tolist(),
        title="Horsepower vs Sports Car Price"
    )

    fig_scatter.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_scatter,
        use_container_width=True
    )


# ---------------------------------------------------
# Price vs Year
# ---------------------------------------------------
if (
    "Year" in filtered_df.columns
    and "Price" in filtered_df.columns
):

    fig_year_price = px.scatter(
        filtered_df,
        x="Year",
        y="Price",
        color="Make" if "Make" in filtered_df.columns else None,
        title="Car Year vs Price"
    )

    fig_year_price.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_year_price,
        use_container_width=True
    )


# ---------------------------------------------------
# Average Price by Manufacturer
# ---------------------------------------------------
if (
    "Make" in filtered_df.columns
    and "Price" in filtered_df.columns
):

    st.header("Manufacturer Price Analysis")

    manufacturer_summary = (
        filtered_df
        .groupby("Make")
        .agg(
            Average_Price=("Price", "mean"),
            Minimum_Price=("Price", "min"),
            Maximum_Price=("Price", "max"),
            Number_of_Cars=("Price", "count")
        )
        .reset_index()
    )

    st.dataframe(
        manufacturer_summary,
        use_container_width=True
    )


    fig_average_price = px.bar(
        manufacturer_summary,
        x="Make",
        y="Average_Price",
        title="Average Sports Car Price by Manufacturer",
        text_auto=".2f"
    )

    fig_average_price.update_layout(
        template="plotly_white"
    )

    st.plotly_chart(
        fig_average_price,
        use_container_width=True
    )


# ---------------------------------------------------
# Download Dataset
# ---------------------------------------------------
st.divider()

st.header("Download Data")

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset as CSV",
    data=csv,
    file_name="filtered_sports_car_prices.csv",
    mime="text/csv"
)