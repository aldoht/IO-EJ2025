import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['font.size'] = 11
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['figure.figsize'] = (16, 9)

# Tercer nivel
tercer_nivel = pd.read_csv('../datasets/ensat-3-septiembre-2017.csv', encoding='latin-1')

## Hospital de Especialidades No. 25 Monterrey
tercer_nivel = tercer_nivel[tercer_nivel['Unidad'].astype(str).str.contains('HES 25 MONTERREY')]
columnas_interes_3 = ['Folio', 'Tipopac', 'Filtroch', 'Probsal', 'Especialid', 'Tmedreg3', 'Nivel', 'Unidad', 'Promedio_Diario2016']
tercer_nivel = tercer_nivel[columnas_interes_3]
tercer_nivel = tercer_nivel[tercer_nivel['Filtroch'] == 1]
print(tercer_nivel.head())

## Gráfica de tiempos de espera
waiting_times_count_3 = {}
rango = ''
for index, value in tercer_nivel['Tmedreg3'].items():
    match value:
        case 1:
            rango = '0-15 minutos'
        case 2:
            rango = '16-30 minutos'
        case 3:
            rango = '31-60 minutos'
        case 4:
            rango = '61-120 minutos'
        case _:
            rango = '+121 minutos'
    if rango in waiting_times_count_3:
        waiting_times_count_3[rango] += 1
    else:
        waiting_times_count_3[rango] = 1
waiting_frequencies_3 = pd.Series(waiting_times_count_3)
sorted_waiting_frequencies_3 = waiting_frequencies_3.sort_values(ascending=False)
ax4 = sorted_waiting_frequencies_3.plot(kind='bar', color='orange')
waiting_frequencies_3.sort_values(ascending=False).plot(kind='bar', color='#1A5276')
plt.xticks(rotation=0)
plt.title('Rangos de tiempo en la sala de espera (HES 25 Monterrey)')
plt.ylabel('Frecuencia')
plt.xlabel('Rango de tiempo')
for i, count in enumerate(sorted_waiting_frequencies_3):
    ax4.text(i, count + 0.1, str(count), ha='center')
plt.tight_layout()
plt.show()