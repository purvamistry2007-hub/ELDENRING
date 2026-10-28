import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page Configuration
st.set_page_config(
    page_title="Elden Ring Professional Analytics Dashboard",
    page_icon="⚔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & Theme (Dark Fantasy Mode)
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
            color: #ffffff;
        }
        .stMetric {
            background-color: #1a1d24;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #30363d;
        }
        .stMetric label {
            color: #8b949e !important;
        }
        .stMetric value {
            color: #f0f6fc !important;
        }
        h1, h2, h3 {
            font-family: 'Cinzel', serif, sans-serif;
            color: #e6edf3;
        }
    </style>
""", unsafe_allow_html=True)

# Load and Cache Data
@st.cache_data
def load_data():
    file_path = 'Elden_Ring_PowerBI_Dataset_20_Columns.xlsx'
    df = pd.read_excel(file_path, sheet_name='EldenRing_Master')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.image("https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=500&auto=format&fit=crop&q=60", use_column_width=True)
st.sidebar.title("⚔️ Filter Options")

# Weapon Type Filter
weapon_types = ['All'] + sorted(df['Weapon_Type'].unique().tolist())
selected_weapon_type = st.sidebar.selectbox("Select Weapon Type", weapon_types)

# Rarity Filter
rarities = ['All'] + sorted(df['Rarity'].unique().tolist())
selected_rarity = st.sidebar.selectbox("Select Rarity", rarities)

# Region Filter
regions = ['All'] + sorted(df['Region_Found'].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region Found", regions)

# Boss Loot Filter
boss_loot_options = ['All'] + sorted(df['Is_Boss_Loot'].unique().tolist())
selected_boss_loot = st.sidebar.selectbox("Is Boss Loot?", boss_loot_options)

# Apply Filters
filtered_df = df.copy()
if selected_weapon_type != 'All':
    filtered_df = filtered_df[filtered_df['Weapon_Type'] == selected_weapon_type]
if selected_rarity != 'All':
    filtered_df = filtered_df[filtered_df['Rarity'] == selected_rarity]
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region_Found'] == selected_region]
if selected_boss_loot != 'All':
    filtered_df = filtered_df[filtered_df['Is_Boss_Loot'] == selected_boss_loot]

# --- MAIN DASHBOARD CONTENT ---
st.title("🛡️ Elden Ring Weapon & Equipment Intelligence Dashboard")
st.markdown("Explore comprehensive analytics across attributes, damage types, weapon tiers, and regions in the Lands Between.")

if filtered_df.empty:
    st.warning("No data available for the selected filters. Please adjust your criteria.")
else:
    # --- TOP METRICS / KPI CARDS ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_items = len(filtered_df)
    avg_base_damage = filtered_df['Base_Damage'].mean()
    max_base_damage = filtered_df['Base_Damage'].max()
    avg_weight = filtered_df['Weight_Kg'].mean()
    boss_loot_count = len(filtered_df[filtered_df['Is_Boss_Loot'] == 'Yes'])
    
    col1.metric("Total Records", f"{total_items:,}")
    col2.metric("Avg Base Damage", f"{avg_base_damage:.1f}")
    col3.metric("Max Base Damage", f"{max_base_damage}")
    col4.metric("Avg Weight (Kg)", f"{avg_weight:.2f}")
    col5.metric("Boss Loot Items", f"{boss_loot_count:,}")

    st.markdown("---")

    # --- ROW 1: CHARTS ---
    r1_col1, r1_col2 = st.columns(2)

    with r1_col1:
        st.subheader("📊 Average Base Damage by Weapon Type")
        damage_by_type = filtered_df.groupby('Weapon_Type')['Base_Damage'].mean().reset_index().sort_values(by='Base_Damage', ascending=True)
        fig_dmg = px.bar(
            damage_by_type, 
            x='Base_Damage', 
            y='Weapon_Type', 
            orientation='h',
            text_auto='.1f',
            color='Base_Damage',
            color_continuousScale='Viridis'
        )
        fig_dmg.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=400)
        st.plotly_chart(fig_dmg, use_container_width=True)

    with r1_col2:
        st.subheader("🎯 Distribution of Rarity Types")
        rarity_counts = filtered_df['Rarity'].value_counts().reset_index()
        rarity_counts.columns = ['Rarity', 'Count']
        fig_rarity = px.pie(
            rarity_counts, 
            names='Rarity', 
            values='Count', 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_rarity.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=400)
        st.plotly_chart(fig_rarity, use_container_width=True)

    # --- ROW 2: CHARTS ---
    r2_col1, r2_col2 = st.columns(2)

    with r2_col1:
        st.subheader("🗺️ Equipment Count Across Regions")
        region_counts = filtered_df['Region_Found'].value_counts().reset_index()
        region_counts.columns = ['Region_Found', 'Count']
        fig_region = px.bar(
            region_counts,
            x='Region_Found',
            y='Count',
            color='Count',
            color_continuousScale='Teal'
        )
        fig_region.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=400)
        st.plotly_chart(fig_region, use_container_width=True)

    with r2_col2:
        st.subheader("⚖️ Weight vs Base Damage Analysis")
        fig_scatter = px.scatter(
            filtered_df,
            x='Weight_Kg',
            y='Base_Damage',
            color='Primary_Damage_Type',
            size='Upgrade_Level',
            hover_data=['Item_Name', 'Weapon_Type', 'Affinity'],
            opacity=0.8
        )
        fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- ROW 3: ADDITIONAL BREAKDOWN ---
    st.markdown("---")
    r3_col1, r3_col2 = st.columns(2)

    with r3_col1:
        st.subheader("⚡ Primary Damage Type Breakdown")
        damage_type_counts = filtered_df['Primary_Damage_Type'].value_counts().reset_index()
        damage_type_counts.columns = ['Primary_Damage_Type', 'Count']
        fig_dt = px.bar(
            damage_type_counts,
            x='Primary_Damage_Type',
            y='Count',
            color='Primary_Damage_Type'
        )
        fig_dt.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white', height=350, showlegend=False)
        st.plotly_chart(fig_dt, use_container_width=True)

    with r3_col2:
        st.subheader("🛡️ Hand Requirement Distribution")
        hand_counts = filtered_df['Hand_Requirement'].value_counts().reset_index()
        hand_counts.columns = ['Hand_Requirement', 'Count']
        fig_hand = px.pie(
            hand_counts,
            names='Hand_Requirement',
            values='Count',
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        fig_hand.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white', height=350)
        st.plotly_chart(fig_hand, use_container_width=True)

    # --- DATA TABLE VIEW ---
    st.markdown("---")
    st.subheader("📋 Filtered Dataset Records")
    st.dataframe(filtered_df, use_container_width=True)