import pandas as pd

# Load the data
edges = pd.read_csv('edges_hc.csv')

# Set display options to avoid scientific notation
pd.set_option('display.float_format', '{:.2f}'.format)

# Display some summary statistics to understand the distribution
print(edges[['fee_base(millisat)', 'fee_proportional', 'min_htlc(millisat)']].describe())

# Calculate the median
median_fee_base = edges['fee_base(millisat)'].median()
median_fee_proportional = edges['fee_proportional'].median()
median_min_htlc = edges['min_htlc(millisat)'].median()

# Calculate the means
mean_fee_base = edges['fee_base(millisat)'].mean()
mean_fee_proportional = edges['fee_proportional'].mean()
mean_min_htlc = edges['min_htlc(millisat)'].mean()

# Fill missing values using the median since the data is heavily skewed
edges.fillna({
    'fee_base(millisat)': median_fee_base,
    'fee_proportional': median_fee_proportional,
    'min_htlc(millisat)': median_min_htlc
}, inplace=True)


# Ensure all columns are integers after filling
edges['fee_base(millisat)'] = edges['fee_base(millisat)'].astype(int)
edges['fee_proportional'] = edges['fee_proportional'].astype(int)
edges['min_htlc(millisat)'] = edges['min_htlc(millisat)'].astype(int)
edges['timelock'] = edges['timelock'].astype(int)

# Save the cleaned data back to a CSV
edges.to_csv('edges_hc.csv', index=False)
