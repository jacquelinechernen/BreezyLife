import streamlit as st
import pandas as pd

def main():
    st.set_page_config(
        page_title="BreezyLiving: PM₂.₅ Combo Recommender",
        page_icon="🌙",
        layout="centered"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu+Mono&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Ubuntu Mono', monospace;
        background-color: #303030;
        color: #fafafa;
    }
    h1, h2, h3, .st-title {
        color: #80cbc4 !important;
    }
    [data-baseweb="select"] div[class^="css-1wa3eu0-placeholder"] {
        color: #80cbc4 !important;
        opacity: 0.8;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background: #606060 !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div {
        background: #80cbc4 !important;
    }
    .stDataFrame, .css-1kxckz2 { 
        background-color: #424242 !important; 
        color: #fafafa !important;
    }
    .recommended-box {
        background-color: #424242;
        border-radius: 10px;
        padding: 15px;
        margin-top: 10px;
        border: 2px solid #80cbc4;
    }
    .recommended-box p, .recommended-box b {
        color: #fafafa;
        margin: 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("BreezyLiving: PM₂.₅ Intervention Recommender")

    # Load  BCA data 
    df = pd.read_csv('BCA.csv')

    # Budget range slider
    budget = st.slider(
        "Choose your annual budget (CAD):",
        min_value=140,
        max_value=int(df['Total Cost'].max()),
        value=int(df['Total Cost'].median()),
        step=50
    )

    # Already installed items
    st.write("Select the interventions you already have, so we skip them:")
    existing_opts = [
        "MERV 13+ Filter",
        "HRV/ERV Unit",
    ]
    existing = st.multiselect("Already Installed Interventions:", existing_opts)

    # Filter by budget
    eligible = df[df['Total Cost'] <= budget].copy()

    # Filter out existing interventions
    if "MERV 13+ Filter" in existing:
        eligible = eligible[~eligible['Scenario'].str.contains('MERV', case=False, na=False)]
    if "HRV/ERV Unit" in existing:
        eligible = eligible[~eligible['Scenario'].str.contains('HRV', case=False, na=False)]

    # Sort by net benefit
    eligible = eligible.sort_values(by='Benefit - Cost', ascending=False)

    # Display top 5 scenarios
    st.subheader("Top 5 Scenarios")
    top3 = eligible.head(3).reset_index(drop=True)
    st.dataframe(top3[[
        'Scenario',
        'Total Cost',
        'Benefit',
        'Benefit - Cost'
    ]])

    # Show best combo details
    if not top3.empty:
        best = top3.iloc[0]
        st.subheader("Recommended Best Combo")
        st.markdown(f"""
        <div class='recommended-box'>
            <p><b>Scenario:</b> {best['Scenario']}</p>
            <p><b>Benefit:</b> {best['Benefit']}</p>
            <p><b>Cost:</b> ${int(best['Total Cost'])}</p>
            <p><b>Net Benefit:</b> {best['Benefit - Cost']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No scenarios match your budget and existing installations.")

if __name__ == "__main__":
    main()
