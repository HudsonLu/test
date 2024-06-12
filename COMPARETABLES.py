import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 20)
pd.set_option('display.width', None)

filepath = 'C:\\Users\\hlu\\OneDrive - IC IC\\POWER BI\\\lasttest\\2024-04-22_PIMS_GEOTABLE_UPDATED.xlsx'
#filepath = 'C:\\Users\\hlu\\OneDrive - IC IC\\POWER BI\\\2024-03-15_UDP_pims.PROJECT.xlsx'
#comparedfile = 'C:\\Users\\hlu\\OneDrive - IC IC\\POWER BI\\2024-04-17 - 2016 - Project List.xlsx'
comparedfile = 'C:\\Users\\hlu\\OneDrive - IC IC\\POWER BI\\\lasttest\\DMAF_KML_FILES.xlsx'

df = pd.read_excel(filepath)
df1 = pd.read_excel(comparedfile)
matched_projects = df[df['PROJECT_ID'].isin(df1['Project #'])]
matched_projects_count = len(matched_projects)
total_projects_count = len(df)

unmatched_projects_count = total_projects_count - matched_projects_count

print("Number of matched projects:", matched_projects_count)
print("Number of unmatched projects:", unmatched_projects_count)
