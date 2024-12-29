import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = 'D:\\c4gt\\CombinedVMDR.xlsx'  # Adjust the file path accordingly
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Display basic information
print("Basic Info:")
print(df.info())

# Check for missing values
print("\nMissing Values:")
missing_values = df.isnull().sum()
print(missing_values)

# Descriptive statistics for numerical columns
numeric_columns = df.select_dtypes(include=np.number).columns
print("\nDescriptive Statistics:")
print(df[numeric_columns].describe())

# Unique values for categorical columns
categorical_columns = df.select_dtypes(exclude=np.number).columns
print("\nUnique Values per Categorical Column:")
for col in categorical_columns:
    print(f"{col}: {df[col].nunique()} unique values")

# Correlation matrix for numerical columns
print("\nCorrelation Matrix:")
correlation_matrix = df[numeric_columns].corr()
print(correlation_matrix)

# Heatmap of the correlation matrix
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix Heatmap')
plt.show()

# Pairplot for visualizing relationships between numeric columns
sns.pairplot(df[numeric_columns])
plt.show()

# Group by 'Class' (if exists) and plot aggregated values
if 'Class' in df.columns:
    grouped = df.groupby('Class')[numeric_columns].mean()
    print("\nGrouped by 'Class' and Mean Aggregation:")
    print(grouped)
    
    # Bar plot for the grouped data
    grouped.plot(kind='bar', figsize=(12, 6))
    plt.title('Mean of Numeric Columns Grouped by Class')
    plt.xlabel('Class')
    plt.ylabel('Mean Value')
    plt.xticks(rotation=45)
    plt.show()

# Handling missing values (forward fill)
df_filled = df.fillna(method='ffill')

# Visualize missing data with heatmap
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
plt.title('Missing Data Heatmap')
plt.show()

# Histogram for numerical columns
df[numeric_columns].hist(bins=15, figsize=(15, 10), layout=(5, 2))
plt.suptitle('Distribution of Numeric Columns')
plt.show()

# Boxplot for outliers in numeric columns
plt.figure(figsize=(12, 8))
sns.boxplot(data=df[numeric_columns])
plt.title('Boxplot of Numeric Columns')
plt.xticks(rotation=90)
plt.show()

# Save the cleaned data to a new Excel file
output_path = 'D:\\sasi_learn\\sasi_intv\\interviewTracker\\cleaned_data_with_analysis.xlsx'
df_filled.to_excel(output_path, index=False)

print("\nData cleaning and analysis complete. Cleaned data saved to:", output_path)
