import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Global Food Security Dashboard",
    page_icon="🌾",
    layout="wide"
)

#data loading
@st.cache_data
def load_data():
    df = pd.read_csv("data/FAO_FS_clean.csv")
    df["Year"] = df["Year"].astype(int)

    name_map = {
        "Number of people undernourished (million) (3-year average)":
            "People Undernourished (millions)",
        "Prevalence of undernourishment (percent) (3-year average)":
            "Undernourishment Rate (%)",
        "Severely food insecure people (million) (3-year average)":
            "Severely Food Insecure (millions)",
        "Moderately or severely food insecure people (million) (3-year average)":
            "Moderately/Severely Food Insecure (millions)",
        "Prevalence of moderate or severe food insecurity in the total population (percent) (3-year average)":
            "Food Insecurity Rate - Mod/Severe (%)",
        "Prevalence of severe food insecurity in the total population (percent) (3-year average)":
            "Food Insecurity Rate - Severe (%)",
        "Average dietary energy supply adequacy (percent) (3-year average)":
            "Dietary Energy Supply Adequacy (%)",
        "Share of dietary energy supply derived from cereals, roots and tubers (percent) (3-year average)":
            "Cereal Dependency (%)",
        "Average protein supply (g/cap/day) (3-year average)":
            "Protein Supply (g/cap/day)",
        "Average supply of protein of animal origin (g/cap/day) (3-year average)":
            "Animal Protein Supply (g/cap/day)",
        "Gross domestic product per capita, PPP, (constant 2017 international $)":
            "GDP per Capita (PPP, 2017 USD)",
    }
    df["Short_Name"] = df["Indicator"].map(name_map).fillna(df["Indicator"])

    region_map = {
        "Afghanistan":"South Asia","Bangladesh":"South Asia","India":"South Asia",
        "Nepal":"South Asia","Pakistan":"South Asia","Sri Lanka":"South Asia",
        "Angola":"Sub-Saharan Africa","Benin":"Sub-Saharan Africa",
        "Burkina Faso":"Sub-Saharan Africa","Burundi":"Sub-Saharan Africa",
        "Cameroon":"Sub-Saharan Africa","Central African Republic":"Sub-Saharan Africa",
        "Chad":"Sub-Saharan Africa","Congo, Dem. Rep.":"Sub-Saharan Africa",
        "Congo, Rep.":"Sub-Saharan Africa","Eritrea":"Sub-Saharan Africa",
        "Ethiopia":"Sub-Saharan Africa","Gambia, The":"Sub-Saharan Africa",
        "Ghana":"Sub-Saharan Africa","Guinea":"Sub-Saharan Africa",
        "Kenya":"Sub-Saharan Africa","Lesotho":"Sub-Saharan Africa",
        "Liberia":"Sub-Saharan Africa","Madagascar":"Sub-Saharan Africa",
        "Malawi":"Sub-Saharan Africa","Mali":"Sub-Saharan Africa",
        "Mozambique":"Sub-Saharan Africa","Namibia":"Sub-Saharan Africa",
        "Niger":"Sub-Saharan Africa","Nigeria":"Sub-Saharan Africa",
        "Rwanda":"Sub-Saharan Africa","Senegal":"Sub-Saharan Africa",
        "Sierra Leone":"Sub-Saharan Africa","Somalia":"Sub-Saharan Africa",
        "South Africa":"Sub-Saharan Africa","South Sudan":"Sub-Saharan Africa",
        "Sudan":"Sub-Saharan Africa","Tanzania":"Sub-Saharan Africa",
        "Togo":"Sub-Saharan Africa","Uganda":"Sub-Saharan Africa",
        "Zambia":"Sub-Saharan Africa","Zimbabwe":"Sub-Saharan Africa",
        "Bolivia":"Latin America & Caribbean","Brazil":"Latin America & Caribbean",
        "Colombia":"Latin America & Caribbean","Ecuador":"Latin America & Caribbean",
        "Guatemala":"Latin America & Caribbean","Haiti":"Latin America & Caribbean",
        "Honduras":"Latin America & Caribbean","Mexico":"Latin America & Caribbean",
        "Nicaragua":"Latin America & Caribbean","Peru":"Latin America & Caribbean",
        "Venezuela, RB":"Latin America & Caribbean",
        "Cambodia":"East Asia & Pacific","China":"East Asia & Pacific",
        "Indonesia":"East Asia & Pacific","Mongolia":"East Asia & Pacific",
        "Myanmar":"East Asia & Pacific","Philippines":"East Asia & Pacific",
        "Thailand":"East Asia & Pacific","Viet Nam":"East Asia & Pacific",
        "Timor-Leste":"East Asia & Pacific",
        "Algeria":"Middle East & N. Africa","Egypt, Arab Rep.":"Middle East & N. Africa",
        "Jordan":"Middle East & N. Africa","Libya":"Middle East & N. Africa",
        "Morocco":"Middle East & N. Africa","Syrian Arab Republic":"Middle East & N. Africa",
        "Tunisia":"Middle East & N. Africa","Yemen, Rep.":"Middle East & N. Africa",
        "Djibouti":"Middle East & N. Africa",
    }
    df["Region"] = df["Country"].map(region_map).fillna("Other")
    return df

df = load_data()
all_countries  = sorted(df["Country"].unique())
all_indicators = sorted(df["Short_Name"].unique())
all_years      = sorted(df["Year"].unique())

# Sidebar
st.sidebar.title("🌾 Dashboard Controls")
st.sidebar.markdown("---")

selected_indicator_name = st.sidebar.selectbox(
    "📊 Select Indicator",
    options=[
        "Undernourishment Rate (%)",
        "Food Insecurity Rate - Mod/Severe (%)",
        "Food Insecurity Rate - Severe (%)",
        "People Undernourished (millions)",
        "Protein Supply (g/cap/day)",
        "Animal Protein Supply (g/cap/day)",
        "Dietary Energy Supply Adequacy (%)",
        "Cereal Dependency (%)",
        "GDP per Capita (PPP, 2017 USD)",
    ]
)

selected_countries = st.sidebar.multiselect(
    "🌍 Compare Countries",
    options=all_countries,
    default=["Haiti","Somalia","India","Brazil","United Kingdom","China"]
)

year_range = st.sidebar.slider(
    "📅 Year Range",
    min_value=2000, max_value=2024,
    value=(2000, 2024)
)

selected_year = st.sidebar.slider(
    "📅 Single Year (Map & Rankings)",
    min_value=2000, max_value=2022,
    value=2022
)

top_n = st.sidebar.slider(
    "🔢 Top / Bottom N Countries",
    min_value=5, max_value=25, value=15
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Source:** FAO / World Bank Data360  \n"
    "**Dataset:** Suite of Food Security Indicators  \n"
    "**Coverage:** 198 countries · 2000–2024"
)

# Header
st.title("🌾 Global Food Security Dashboard")
st.markdown(
    """
    **616 million people**, 7.6% of humanity are still undernourished in 2024.
    After decades of progress, global hunger has been rising again since 2019,
    driven by conflict, climate shocks and the COVID-19 pandemic.
    This dashboard uses the World Bank's FAO Food Security dataset to explore
    where hunger is worst, what is driving it, and whether progress is being made.
    """
)
st.markdown("---")

# KPI tiles
ind_pct  = df[df["Short_Name"] == "Undernourishment Rate (%)"]
ind_fi   = df[df["Short_Name"] == "Food Insecurity Rate - Mod/Severe (%)"]
ind_num  = df[df["Short_Name"] == "People Undernourished (millions)"]
ind_prot = df[df["Short_Name"] == "Protein Supply (g/cap/day)"]

val_2024_pct  = ind_pct[ind_pct["Year"]==2024]["Value"].mean()
val_2019_pct  = ind_pct[ind_pct["Year"]==2019]["Value"].mean()
val_fi_2024   = ind_fi[ind_fi["Year"]==2024]["Value"].mean()
val_fi_2019   = ind_fi[ind_fi["Year"]==2019]["Value"].mean()
val_num_2024  = ind_num[ind_num["Year"]==2024]["Value"].sum()
val_prot_2022 = ind_prot[ind_prot["Year"]==2022]["Value"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric(
    "🌍 People Undernourished",
    f"{val_num_2024:.0f}M",
    "2024 total",
    delta_color="off"
)
c2.metric(
    "📉 Global Undernourishment Rate",
    f"{val_2024_pct:.1f}%",
    f"{val_2024_pct - val_2019_pct:+.1f}pp since 2019",
    delta_color="inverse"
)
c3.metric(
    "⚠️ Food Insecurity Rate",
    f"{val_fi_2024:.1f}%",
    f"{val_fi_2024 - val_fi_2019:+.1f}pp since 2019",
    delta_color="inverse"
)
c4.metric(
    "🍗 Avg Protein Supply",
    f"{val_prot_2022:.0f} g/day",
    "global average (2022)"
)
c5.metric(
    "🌍 Countries Tracked",
    "198",
    "across 25 years"
)
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️  World Map",
    "📈  Trends Over Time",
    "🏆  Country Rankings",
    "🍽️  Nutrition Profile",
    "💰  Hunger vs Wealth"
])

# Tab 1: world map
with tab1:
    st.subheader(f"Global Map — {selected_indicator_name} ({selected_year})")
    st.markdown(
        "Use the **Select Indicator** and **Single Year** controls in the sidebar "
        "to explore food security across the world."
    )

    map_df = df[
        (df["Short_Name"] == selected_indicator_name) &
        (df["Year"] == selected_year)
    ].copy()

    if map_df.empty:
        st.warning(
            "No data available for this indicator and year combination. "
            "Try selecting a different year — some indicators only have data from 2015 onwards."
        )
    else:
        # Pick colour scale: red = bad for hunger indicators, green = bad for protein
        hunger_indicators = [
            "Undernourishment Rate (%)",
            "Food Insecurity Rate - Mod/Severe (%)",
            "Food Insecurity Rate - Severe (%)",
            "People Undernourished (millions)",
            "Severely Food Insecure (millions)",
            "Cereal Dependency (%)",
        ]
        colour_scale = "Reds" if selected_indicator_name in hunger_indicators else "Greens"

        fig_map = px.choropleth(
            map_df,
            locations="Country",
            locationmode="country names",
            color="Value",
            hover_name="Country",
            hover_data={"Value":":.1f","Country":False},
            color_continuous_scale=colour_scale,
            labels={"Value": selected_indicator_name},
            title=f"{selected_indicator_name} — {selected_year}"
        )
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True,
                     projection_type="natural earth"),
            coloraxis_colorbar=dict(title="Value"),
            margin=dict(l=0, r=0, t=50, b=0),
            height=520
        )
        st.plotly_chart(fig_map, use_container_width=True)

    direction = "Darker red = more hunger" if selected_indicator_name in [
        "Undernourishment Rate (%)","Food Insecurity Rate - Mod/Severe (%)"
    ] else "Darker = higher value"
    st.caption(
        f"**How to read:** {direction}. Grey = no data for this year. "
        f"Hover over any country for the exact value."
    )

# Tab 2: trends over time
with tab2:
    st.subheader("How Has Food Security Changed Over Time?")
    st.markdown(
        "Select countries in the sidebar to compare their trajectories. "
        "The **dashed global average line** shows the worldwide benchmark."
    )

    if not selected_countries:
        st.warning("Please select at least one country from the sidebar.")
    else:
        trend_df = df[
            (df["Short_Name"] == selected_indicator_name) &
            (df["Country"].isin(selected_countries)) &
            (df["Year"] >= year_range[0]) &
            (df["Year"] <= year_range[1])
        ].copy()

        global_avg = df[
            (df["Short_Name"] == selected_indicator_name) &
            (df["Year"] >= year_range[0]) &
            (df["Year"] <= year_range[1])
        ].groupby("Year")["Value"].mean().reset_index()
        global_avg["Country"] = "🌐 Global Average"

        combined = pd.concat([trend_df, global_avg], ignore_index=True)

        fig_line = px.line(
            combined,
            x="Year", y="Value", color="Country",
            markers=True,
            line_dash_map={"🌐 Global Average": "dash"},
            labels={"Value": selected_indicator_name, "Year": "Year"},
            title=f"{selected_indicator_name} — {year_range[0]} to {year_range[1]}"
        )
        fig_line.update_layout(height=480, hovermode="x unified")
        st.plotly_chart(fig_line, use_container_width=True)

    # COVID impact callout
    st.markdown("---")
    st.markdown("##### 🔍 The COVID-19 Impact on Global Food Security")
    covid_df = df[
        (df["Short_Name"] == "Food Insecurity Rate - Mod/Severe (%)") &
        (df["Year"].between(2015, 2024))
    ].groupby("Year")["Value"].mean().reset_index()
    covid_df.columns = ["Year","Food Insecurity Rate (%)"]

    fig_covid = px.bar(
        covid_df,
        x="Year", y="Food Insecurity Rate (%)",
        color="Food Insecurity Rate (%)",
        color_continuous_scale="Reds",
        title="Global Average Food Insecurity Rate (%) — 2015 to 2024",
        labels={"Food Insecurity Rate (%)":"Population (%)"}
    )
    fig_covid.add_vline(x=2020, line_dash="dash", line_color="black",
                        annotation_text="COVID-19", annotation_position="top right")
    fig_covid.update_layout(height=380, coloraxis_showscale=False)
    st.plotly_chart(fig_covid, use_container_width=True)
    st.caption(
        "Food insecurity jumped from 26.8% in 2019 to 30.4% in 2021 — "
        "a rise of 3.6 percentage points, equivalent to hundreds of millions of additional people."
    )

# ─Tab 3; country rankings
with tab3:
    st.subheader(f"Which Countries Are Best and Worst? ({selected_year})")

    rank_df = df[
        (df["Short_Name"] == selected_indicator_name) &
        (df["Year"] == selected_year)
    ].dropna(subset=["Value"]).sort_values("Value", ascending=False)

    if rank_df.empty:
        st.warning("No ranking data available for this indicator and year.")
    else:
        # Decide which direction is bad for colour
        hunger_indicators = [
            "Undernourishment Rate (%)","Food Insecurity Rate - Mod/Severe (%)",
            "Food Insecurity Rate - Severe (%)","People Undernourished (millions)",
            "Cereal Dependency (%)"
        ]
        if selected_indicator_name in hunger_indicators:
            top_label = f"Worst {top_n} (Highest)"
            bot_label = f"Best {top_n} (Lowest)"
            top_scale = "Reds"
            bot_scale = "Greens"
        else:
            top_label = f"Best {top_n} (Highest)"
            bot_label = f"Worst {top_n} (Lowest)"
            top_scale = "Greens"
            bot_scale = "Reds"

        col_top, col_bot = st.columns(2)
        with col_top:
            top_df = rank_df.head(top_n).sort_values("Value")
            fig_top = px.bar(
                top_df, x="Value", y="Country",
                orientation="h",
                color="Value",
                color_continuous_scale=top_scale,
                labels={"Value": selected_indicator_name},
                title=top_label
            )
            fig_top.update_layout(
                height=max(380, top_n*28),
                coloraxis_showscale=False,
                yaxis_title=""
            )
            st.plotly_chart(fig_top, use_container_width=True)

        with col_bot:
            bot_df = rank_df.tail(top_n).sort_values("Value")
            fig_bot = px.bar(
                bot_df, x="Value", y="Country",
                orientation="h",
                color="Value",
                color_continuous_scale=bot_scale,
                labels={"Value": selected_indicator_name},
                title=bot_label
            )
            fig_bot.update_layout(
                height=max(380, top_n*28),
                coloraxis_showscale=False,
                yaxis_title=""
            )
            st.plotly_chart(fig_bot, use_container_width=True)

    # Progress chart: biggest improvements
    st.markdown("---")
    st.subheader("Which Countries Have Made the Most Progress? (2002 → 2024)")
    prog_ind = df[df["Short_Name"] == "Undernourishment Rate (%)"]
    start_df = prog_ind[prog_ind["Year"]==2002][["Country","Value"]].rename(columns={"Value":"v2002"})
    end_df   = prog_ind[prog_ind["Year"]==2024][["Country","Value"]].rename(columns={"Value":"v2024"})
    prog_df  = start_df.merge(end_df, on="Country").dropna()
    prog_df["Change"] = prog_df["v2024"] - prog_df["v2002"]
    prog_df["Direction"] = prog_df["Change"].apply(lambda x: "Improved" if x < 0 else "Worsened")

    gainers = prog_df.nsmallest(10,"Change")
    losers  = prog_df.nlargest(8,"Change")
    both    = pd.concat([gainers, losers]).sort_values("Change")

    fig_prog = px.bar(
        both,
        x="Change", y="Country",
        orientation="h",
        color="Direction",
        color_discrete_map={"Improved":"#4CAF50","Worsened":"#F44336"},
        labels={"Change":"Change in Undernourishment Rate (pp)", "Country":""},
        title="Change in Undernourishment Rate 2002–2024 (percentage points)"
    )
    fig_prog.update_layout(height=550)
    st.plotly_chart(fig_prog, use_container_width=True)
    st.caption(
        "Angola improved by 45 percentage points. Syria worsened by 32 points — "
        "the largest deterioration, driven by conflict."
    )

#tab 4: nutrition profile
with tab4:
    st.subheader("Nutrition Deep-Dive — 4 Dimensions of Food Security")
    st.markdown(
        "The FAO defines food security across **4 dimensions**: Availability, Access, "
        "Utilisation, and Stability. This tab lets you explore them for any country."
    )

    col_a, col_b = st.columns([1, 2])
    with col_a:
        profile_country = st.selectbox(
            "Select a country",
            options=all_countries,
            index=all_countries.index("India") if "India" in all_countries else 0,
            key="profile_country"
        )

    # Pull all 4 key indicators for this country
    four_dims = {
        "Availability": "Dietary Energy Supply Adequacy (%)",
        "Access (Wealth)": "GDP per Capita (PPP, 2017 USD)",
        "Utilisation (Protein)": "Protein Supply (g/cap/day)",
        "Stability": "Undernourishment Rate (%)",
    }

    country_df = df[
        (df["Country"] == profile_country) &
        (df["Short_Name"].isin(list(four_dims.values()))) &
        (df["Year"] >= year_range[0]) &
        (df["Year"] <= year_range[1])
    ].copy()

    if country_df.empty:
        st.warning("No data for this country in the selected year range.")
    else:
        fig_profile = px.line(
            country_df,
            x="Year", y="Value",
            color="Short_Name",
            facet_col="Short_Name",
            facet_col_wrap=2,
            markers=True,
            labels={"Value":"Value","Short_Name":"Indicator"},
            title=f"Food Security Profile — {profile_country}"
        )
        fig_profile.update_yaxes(matches=None)
        fig_profile.for_each_annotation(
            lambda a: a.update(text=a.text.split("=")[-1])
        )
        fig_profile.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig_profile, use_container_width=True)

    # Cereal dependency — global comparison
    st.markdown("---")
    st.markdown("##### 🌾 Cereal Dependency — Fragile Diets")
    cer_df = df[
        (df["Short_Name"] == "Cereal Dependency (%)") &
        (df["Year"] == selected_year)
    ].dropna(subset=["Value"]).nlargest(20,"Value")

    fig_cer = px.bar(
        cer_df.sort_values("Value"),
        x="Value", y="Country",
        orientation="h",
        color="Value",
        color_continuous_scale="Oranges",
        labels={"Value":"% of energy from cereals/roots/tubers"},
        title=f"Top 20 Countries by Cereal/Root Dependency — {selected_year}"
    )
    fig_cer.update_layout(height=500, coloraxis_showscale=False)
    st.plotly_chart(fig_cer, use_container_width=True)
    st.caption(
        "Countries where over 70% of calories come from cereals, roots and tubers "
        "have fragile diets with little nutritional diversity. "
        "DRC (82%), Madagascar (79%) and Cambodia (76%) are most vulnerable."
    )

# Tab 5: hunger vs wealth
with tab5:
    st.subheader("Does Money Buy Food Security?")
    st.markdown(
        "This scatter plot explores the relationship between **GDP per capita** and "
        "**undernourishment rate**. Richer countries generally have less hunger — "
        "but there are important exceptions that reveal the limits of wealth alone."
    )

    scatter_year = st.slider(
        "Year for scatter plot",
        min_value=2000, max_value=2024, value=2022,
        key="scatter_year"
    )

    gdp_df  = df[(df["Short_Name"]=="GDP per Capita (PPP, 2017 USD)")&
                 (df["Year"]==scatter_year)][["Country","Value","Region"]].rename(
                 columns={"Value":"GDP"})
    und_df  = df[(df["Short_Name"]=="Undernourishment Rate (%)")&
                 (df["Year"]==scatter_year)][["Country","Value"]].rename(
                 columns={"Value":"Undernourishment"})
    prot_df = df[(df["Short_Name"]=="Protein Supply (g/cap/day)")&
                 (df["Year"].between(scatter_year-1, scatter_year+1))]\
                 .groupby("Country")["Value"].mean().reset_index().rename(
                 columns={"Value":"Protein"})

    scatter_df = gdp_df.merge(und_df, on="Country").merge(prot_df, on="Country", how="left")

    if scatter_df.empty:
        st.warning("Insufficient data for this year combination. Try 2020–2022.")
    else:
        fig_scatter = px.scatter(
            scatter_df,
            x="GDP",
            y="Undernourishment",
            size="Protein",
            color="Region",
            hover_name="Country",
            log_x=True,
            labels={
                "GDP":"GDP per Capita (PPP, 2017 USD) — log scale",
                "Undernourishment":"Undernourishment Rate (%)",
                "Protein":"Protein Supply (g/cap/day)"
            },
            title=f"GDP per Capita vs Undernourishment Rate ({scatter_year}) — bubble = protein supply"
        )
        fig_scatter.update_layout(height=560)
        st.plotly_chart(fig_scatter, use_container_width=True)
        st.caption(
            "**Trend:** As GDP rises, undernourishment generally falls — "
            "but some middle-income countries still have high hunger, "
            "showing that inequality and conflict matter as much as wealth. "
            "Bubble size = protein supply per person per day."
        )

# footer
st.markdown("---")
st.markdown(
    "**Data Source:** FAO Suite of Food Security Indicators — World Bank Data360 | "
    "data360.worldbank.org | 198 countries · 2000–2024 | "
    "Module: 5DATA004C Data Science Project Lifecycle | University of Westminster"
)
