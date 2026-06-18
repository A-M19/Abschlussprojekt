import pandas as pd
import numpy as np

# 1. Gesamten Datensatz einlesen
df = pd.read_csv("athlete_physiological_dataset.csv")

# Alle Sportarten auf Deutsch übersetzen, passend zu deinem Mockup
df['Sport'] = df['Sport'].replace({
    'Swimming': 'Schwimmen',
    'Track': 'Leichtathletik',
    'Soccer': 'Fußball',
    'Tennis': 'Tennis',
    'Basketball': 'Basketball'
})

# 2. Jede Sportart einzeln durchgehen und rollierend auf die 10 IDs verteilen
df_list = []
for sportart, gruppe in df.groupby('Sport'):
    # Hol dir alle einzigartigen alten Athleten-IDs in dieser spezifischen Sportart
    alte_ids = gruppe['Athlete_ID'].unique()
    
    # Jeder alten ID wird eine neue ID von 1 bis 10 zugewiesen (rollierend)
    id_mapping = {alte_id: (i % 10) + 1 for i, alte_id in enumerate(alte_ids)}
    
    gruppe_kopie = gruppe.copy()
    gruppe_kopie['Neue_ID'] = gruppe_kopie['Athlete_ID'].map(id_mapping)
    df_list.append(gruppe_kopie)

# Alle sauberen Sportarten-Stapel wieder zusammenfügen
df_clean = pd.concat(df_list).reset_index(drop=True)

# 3. Profile für deine 10 Accounts festlegen
kombi_profile = {
    1:  {"Age": 22, "Gender": "Male"},
    2:  {"Age": 25, "Gender": "Female"},
    3:  {"Age": 24, "Gender": "Male"},
    4:  {"Age": 28, "Gender": "Female"},
    5:  {"Age": 21, "Gender": "Male"},
    6:  {"Age": 26, "Gender": "Female"},
    7:  {"Age": 23, "Gender": "Male"}, # Perfekt passend für dein PDF-Beispiel!
    8:  {"Age": 29, "Gender": "Female"},
    9:  {"Age": 27, "Gender": "Male"},
    10: {"Age": 24, "Gender": "Female"}
}

for neue_id, profile in kombi_profile.items():
    df_clean.loc[df_clean['Neue_ID'] == neue_id, 'Age'] = profile['Age']
    df_clean.loc[df_clean['Neue_ID'] == neue_id, 'Gender'] = profile['Gender']

# 4. Chronologisches Datum für Mai, Juni, Juli hinzufügen
df_clean = df_clean.sort_values(by=['Neue_ID', 'Sport']).reset_index(drop=True)

start_datum = pd.to_datetime("2026-05-01")
# Zeitstempel hochzählen, damit die Einträge schön über die 3 Monate verteilt werden
df_clean['Datum'] = start_datum + pd.to_timedelta(df_clean.groupby('Neue_ID').cumcount() * 45, unit='m')
df_clean['Datum'] = df_clean['Datum'].dt.strftime('%Y-%m-%d')

# 5. Spalten aufräumen
df_clean['Athlete_ID'] = "Nutzer_" + df_clean['Neue_ID'].astype(str)
df_clean = df_clean.drop(columns=['Neue_ID'])

# 6. Speichern
df_clean.to_csv("athlete_physiological_dataset_clean.csv", index=False)

print("Verteilung pro neuem Nutzer überprüft:\n")
print(pd.crosstab(df_clean['Athlete_ID'], df_clean['Sport']))