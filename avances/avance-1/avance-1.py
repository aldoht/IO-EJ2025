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

# Primer nivel
primer_nivel = pd.read_csv('../../datasets/ensat-1-septiembre-2017.csv', encoding='latin-1')

## UMF 28 Monterrey
primer_nivel = primer_nivel[primer_nivel['Unidad'].astype(str).str.contains('UMF 28 Monterrey')]
columnas_interes_1 = ['Folio', 'Servatn', 'Tipopac', 'Probsal', 'Citapre', 'Comocita', 'Diascita', 'Tmedreg2', 'Tratocomf', 'Totorpase1', 'Tiem_Esp1', 'Nivel', 'Unidad', 'Promedio_Diario2016']
primer_nivel = primer_nivel[columnas_interes_1]
primer_nivel = primer_nivel[primer_nivel['Servatn'] == 1]

## Gráfica de tiempos de espera
waiting_times_count = {}
rango = ''
for index, value in primer_nivel['Tmedreg2'].items():
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
    if rango in waiting_times_count:
        waiting_times_count[rango] += 1
    else:
        waiting_times_count[rango] = 1
waiting_frequencies = pd.Series(waiting_times_count)
sorted_waiting_frequencies = waiting_frequencies.sort_values(ascending=False)
ax1 = sorted_waiting_frequencies.plot(kind='bar', color='orange')
waiting_frequencies.sort_values(ascending=False).plot(kind='bar', color='#1A5276')
plt.xticks(rotation=0)
plt.title('Rangos de tiempo en la sala de espera (UMF 28 Monterrey)')
plt.ylabel('Frecuencia')
plt.xlabel('Rango de tiempo')
for i, count in enumerate(sorted_waiting_frequencies):
    ax1.text(i, count + 0.1, str(count), ha='center')
plt.tight_layout()
plt.show()

## Gráfica de días para cita en 3er nivel
primer_nivel = primer_nivel.dropna(subset=['Tiem_Esp1'])
specialist_checkup_times = {}
rango = ''
for index, value in primer_nivel['Tiem_Esp1'].items():
    match value:
        case 1:
            rango = '0-5 días'
        case 2:
            rango = '6-10 días'
        case 3:
            rango = '11-15 días'
        case 4:
            rango = '16-20 días'
        case 5:
            rango = '21-60 días'
        case 6:
            rango = '61-90 días'
        case _:
            rango = '+90 días'
    if rango in specialist_checkup_times:
        specialist_checkup_times[rango] += 1
    else:
        specialist_checkup_times[rango] = 1
specialist_frequencies = pd.Series(specialist_checkup_times)
sorted_specialist_frequencies = specialist_frequencies.sort_values(ascending=False)
ax2 = sorted_specialist_frequencies.plot(kind='bar', color='#1A5276')
plt.xticks(rotation=0)
plt.title('Rangos de tiempo para cita en 3er nivel (UMF 28 Monterrey)')
plt.ylabel('Frecuencia')
plt.xlabel('Rango de tiempo')
for i, count in enumerate(sorted_specialist_frequencies):
    ax2.text(i, count + 0.1, str(count), ha='center')
plt.tight_layout()
plt.show()

# Tercer nivel
tercer_nivel = pd.read_csv('../../datasets/ensat-3-septiembre-2017.csv', encoding='latin-1')

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