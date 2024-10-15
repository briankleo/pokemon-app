import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from PIL import Image
from io import BytesIO

# App title
st.title("Pokémon Explorer with Stat Comparison")
st.write("Compare the stats of two Pokémon visually using a radar chart!")

# Function to get Pokémon data from the API
def get_pokemon_data(pokemon_name_or_id):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id.lower()}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Pokémon {pokemon_name_or_id} not found.")
        return None

# Sidebar for input
pokemon_1 = st.sidebar.text_input("First Pokémon", "pikachu")
pokemon_2 = st.sidebar.text_input("Second Pokémon", "charizard")

# Fetch Pokémon data
pokemon_1_data = get_pokemon_data(pokemon_1)
pokemon_2_data = get_pokemon_data(pokemon_2)

def plot_radar_chart(pokemon_1_data, pokemon_2_data):
    # Extract base stats for both Pokémon
    stats_1 = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_1_data['stats']}
    stats_2 = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_2_data['stats']}
    
    labels = list(stats_1.keys())
    stats_1_values = list(stats_1.values())
    stats_2_values = list(stats_2.values())

    # Number of variables we're plotting
    num_vars = len(labels)

    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Closing the loop

    # Radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # First Pokémon
    stats_1_values += stats_1_values[:1]  # Closing the loop for radar chart
    ax.fill(angles, stats_1_values, color='blue', alpha=0.25)
    ax.plot(angles, stats_1_values, color='blue', linewidth=2, label=pokemon_1_data['name'].capitalize())

    # Second Pokémon
    stats_2_values += stats_2_values[:1]  # Closing the loop for radar chart
    ax.fill(angles, stats_2_values, color='red', alpha=0.25)
    ax.plot(angles, stats_2_values, color='red', linewidth=2, label=pokemon_2_data['name'].capitalize())

    # Add labels
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='grey', size=12)

    # Move legend and increase font size
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12, fancybox=True, framealpha=1, shadow=True, borderpad=1)

    # Display the chart
    st.pyplot(fig)

# Display Pokémon images and stats
if pokemon_1_data and pokemon_2_data:
    st.subheader(f"Comparing {pokemon_1_data['name'].capitalize()} and {pokemon_2_data['name'].capitalize()}")
    
    col1, col2 = st.columns(2)

    with col1:
        st.image(pokemon_1_data['sprites']['front_default'], caption=pokemon_1_data['name'].capitalize())
        st.write("Stats:")
        for stat in pokemon_1_data['stats']:
            st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")

    with col2:
        st.image(pokemon_2_data['sprites']['front_default'], caption=pokemon_2_data['name'].capitalize())
        st.write("Stats:")
        for stat in pokemon_2_data['stats']:
            st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")

    # Plot radar chart for stat comparison
    plot_radar_chart(pokemon_1_data, pokemon_2_data)

else:
    st.write("Please enter valid Pokémon names or IDs in the sidebar.")
