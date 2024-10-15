import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from math import pi
from PIL import Image
from io import BytesIO

# App title
st.title("Pokémon Explorer with Stat Comparison")
st.write("Compare the stats of up to four Pokémon visually using a radar chart!")

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
pokemon_3 = st.sidebar.text_input("Third Pokémon (optional)", "")
pokemon_4 = st.sidebar.text_input("Fourth Pokémon (optional)", "")

# Fetch Pokémon data
pokemons = []
for pokemon in [pokemon_1, pokemon_2, pokemon_3, pokemon_4]:
    if pokemon:  # Only fetch data if a Pokémon name or ID is provided
        pokemons.append(get_pokemon_data(pokemon))

# Radar chart function for up to 4 Pokémon
def plot_radar_chart(pokemons):
    # Define colors for up to 4 Pokémon
    colors = ['blue', 'red', 'green', 'orange']
    
    labels = []
    stats_list = []
    names = []
    
    # Extract stats from Pokémon data
    for pokemon_data in pokemons:
        if pokemon_data:
            stats = {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
            labels = list(stats.keys())  # All Pokémon should have the same labels
            stats_values = list(stats.values())
            stats_list.append(stats_values)
            names.append(pokemon_data['name'].capitalize())

    num_vars = len(labels)

    # Compute angle for each axis
    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]  # Closing the loop

    # Radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    for i, stats_values in enumerate(stats_list):
        stats_values += stats_values[:1]  # Closing the loop for radar chart
        ax.fill(angles, stats_values, color=colors[i], alpha=0.25)
        ax.plot(angles, stats_values, color=colors[i], linewidth=2, label=names[i])

    # Add labels and formatting
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='grey', size=12)

    # Move legend and increase font size
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12, fancybox=True, framealpha=1, shadow=True, borderpad=1)

    # Display the chart
    st.pyplot(fig)

# Display Pokémon images and stats
if len(pokemons) >= 2:
    st.subheader(f"Comparing Pokémon: {', '.join([pokemon['name'].capitalize() for pokemon in pokemons if pokemon])}")
    
    # Create columns for up to 4 Pokémon
    cols = st.columns(len(pokemons))

    for i, pokemon_data in enumerate(pokemons):
        if pokemon_data:
            with cols[i]:
                st.image(pokemon_data['sprites']['front_default'], caption=pokemon_data['name'].capitalize())
                st.write("Stats:")
                for stat in pokemon_data['stats']:
                    st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
    
    # Plot radar chart for stat comparison
    plot_radar_chart(pokemons)
else:
    st.write("Please enter at least two Pokémon names or IDs in the sidebar.")