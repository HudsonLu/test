import pandas as pd

# Read the CSV into a DataFrame

filepath = 'C:\\Users\hlu\\OneDrive - IC IC\\POWER BI\\lasttest\\updated_data.xlsx'
comparedfilepath = 'C:\\Users\hlu\\OneDrive - IC IC\\POWER BI\\lasttest\\2024-04-22_KML_GEOTABLE_V2_.xlsx'
newfilepath = 'C:\\Users\hlu\\OneDrive - IC IC\\POWER BI\\lasttest\\final_test.xlsx'

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('display.width', None)

df = pd.read_excel(filepath, usecols=["PROJECT_ID", "KML_SUBMISSION_ID", "FINAL LONGITUDE", "FINAL LATITUDE", "Coordinates_Data_Sources"])
df_geotable = pd.read_excel(comparedfilepath, usecols=["IRIS ID", "Longitude KML", "Latitude KML"])

# Merge the two DataFrames
merged_columns = pd.merge(df, df_geotable, left_on="KML_SUBMISSION_ID", right_on="IRIS ID", how="left")

# Apply the logic
for index, row in merged_columns.iterrows():
    if row['Coordinates_Data_Sources'] == 'KML' and pd.isnull(row['FINAL LONGITUDE']) and pd.isnull(row['FINAL LATITUDE']):
        merged_columns.at[index, 'FINAL LONGITUDE'] = row['Longitude KML']
        merged_columns.at[index, 'FINAL LATITUDE'] = row['Latitude KML']

# Save the modified DataFrame to a new Excel file
merged_columns.to_excel(newfilepath, index=False)
print(merged_columns)
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
