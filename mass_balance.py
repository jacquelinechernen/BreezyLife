import pandas as pd

# Constant Parameters for all Scenarios
P = 0.8         # Penetration [-]
S = 1e12        # Indoor particle generation rate [particles/hour]
V = 450         # Indoor volume [m³] - 180 m² × 2.5 m ceiling height
C_OA = 4e9      # Outdoor particle concentration (particles/m³);

# File paths
input_file = 'scenario_params.csv'
output_file = 'scenario_concentrations.csv'

# Read the scenario parameters
df = pd.read_csv(input_file)

# Just renaming params for varibles
df = df.rename(columns={
    'Q_OA (m³/h)': 'Q_OA',
    'Q_I (m³/h)':  'Q_I',
    'Q_R (m³/h)':  'Q_R',
    'ε_S (combined)': 'epsilon_S',
    'β_total (h⁻¹)':  'beta'
})

# Steady-state mass balance calc
df['C_i [particles/m³]'] = (
    S
    + (P * df['Q_I'] + df['Q_OA']) * C_OA
) / (
    df['Q_OA']
    + df['Q_I']
    + df['epsilon_S'] * df['Q_R']
    + df['beta'] * V
)

# Output .csv :P
df[['Scenario', 'C_i [particles/m³]']].to_csv(output_file, index=False)
print(f"Steady-state concentrations saved to: {output_file}")
