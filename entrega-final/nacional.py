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

# Filtro de información
primer_nivel = pd.read_csv('../datasets/ensat-1-septiembre-2017.csv', encoding='latin-1')
cols = ['Folio', 'Servatn', 'Sat1', 'Citapre', 'Diascita', 'Satiemhoci', 'Filtrounifila', 'Comptmpunif', 'Limp2']
primer_nivel = primer_nivel[cols]
primer_nivel = primer_nivel[primer_nivel['Servatn'] == 1]

satisfecho_imss = primer_nivel['Sat1'].dropna()
satisfecho_imss = satisfecho_imss[satisfecho_imss != 99]

previa_cita = primer_nivel[primer_nivel['Citapre'] == 1]
dias_cita = previa_cita['Diascita'].dropna()
dias_cita = dias_cita[dias_cita != 99]
previa_cita = primer_nivel['Citapre'].dropna()
previa_cita = previa_cita[previa_cita != 99]

usado_unifila = primer_nivel['Filtrounifila'].dropna()
usado_unifila = usado_unifila[usado_unifila != 99]

tiempo_unifila = primer_nivel['Comptmpunif'].dropna()
tiempo_unifila = tiempo_unifila[tiempo_unifila != 97]
tiempo_unifila = tiempo_unifila[tiempo_unifila != 99]

material_sanitario = primer_nivel['Limp2'].dropna()
material_sanitario = material_sanitario[material_sanitario != 99]

# Convirtiendo a variables categóricas
def num_a_texto(s: pd.Series, l: list) -> dict:
    d = {}
    for item in l:
        d[item] = 0
    for index, value in s.items():
        s[index] = l[int(value-1)]
        d[l[int(value-1)]] += 1
    return d

imss_freq = num_a_texto(satisfecho_imss, ['Muy satisfecho', 'Satisfecho', 'Ni satisfecho ni insatisfecho', 'Insatisfecho', 'Muy insatisfecho'])
previa_freq = num_a_texto(previa_cita, ['Sí', 'No'])
dias_freq = num_a_texto(dias_cita, ['Mismo día', '1-3 días', '4-10 días', '11-30 días', '31-90 días', '+90 días'])
unifila_freq = num_a_texto(usado_unifila, ['Sí', 'Sí', 'No'])
tiempo_freq = num_a_texto(tiempo_unifila, ['Menor', 'Igual', 'Mayor'])
sanitario_freq = num_a_texto(material_sanitario, ['Sí', 'No'])

# Gráficas
def mostrar_grafica(d: dict, t: str, x: str, y: str) -> None:
    s = pd.Series(d)
    ax = s.plot(kind='bar', color='#1A5276')
    plt.xticks(rotation=0)
    plt.title(t)
    plt.ylabel(y)
    plt.xlabel(x)
    for i, count in enumerate(s):
        ax.text(i, count + 0.1, str(count), ha='center')
    plt.tight_layout()
    plt.show()

mostrar_grafica(imss_freq, '¿Está satisfecho con la atención médica que recibe en el IMSS?', 'Nivel de satisfacción', 'Frecuencia')
mostrar_grafica(previa_freq, '¿Hizo cita previa?', 'Valor', 'Frecuencia')
mostrar_grafica(dias_freq, '¿Cuánto tardaron en asignarle cita?', 'Rango', 'Frecuencia')
mostrar_grafica(unifila_freq, '¿Ha usado UNIFILA?', 'Respuesta', 'Frecuencia')
mostrar_grafica(tiempo_freq, '¿Cómo fue el tiempo de espera al usar UNIFILA en comparación a cuando no existía?', 'Tiempo', 'Frecuencia')
mostrar_grafica(sanitario_freq, '¿Había material sanitario en los baños de la clínica?', 'Valor', 'Frecuencia')