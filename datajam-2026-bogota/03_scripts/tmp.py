import pandas as pd 
df = pd.read_excel('../01_datos/processed/p_salud_consumo.xlsx') 
print(df['CURSO_DE_VIDA'].value_counts()) 
print() 
print(df['SEXO'].value_counts()) 
print() 
print(df.groupby('CURSO_DE_VIDA')['CASOS'].sum().sort_values(ascending=False)) 
