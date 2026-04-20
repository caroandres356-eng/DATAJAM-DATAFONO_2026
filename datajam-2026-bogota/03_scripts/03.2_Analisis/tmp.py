import pandas as pd 
df = pd.read_excel('../../01_datos/processed/p_salud_ideacion.xlsx') 
print(df['ano_notificacion'].value_counts().sort_index()) 
