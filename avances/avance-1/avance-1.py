import pandas as pd

primer_nivel = pd.read_csv('../../datasets/ensat-1-septiembre-2017.csv', encoding='latin-1')
tercer_nivel = pd.read_csv('../../datasets/ensat-3-septiembre-2017.csv', encoding='latin-1')

#
primer_nivel = primer_nivel[primer_nivel['Unidmed'].astype(str).str.contains('UMF 28 Monterrey')]
columnas_interes = ['Folio', 'Deleg', 'Unidmed', 'Id_Unid', 'Fecha_D', 'Fecha_M', 'Fecha_A', 'Hr_Ini_H', 'Hr_Ini_M', 'Hr_Fin_H', 'Hr_Fin_M', 'Servatn', 'Tipopac', 'Probsal', 'Citapre', 'Comocita', 'Diascita', 'Tmedreg2', 'Tratocomf', 'Totorpase1', 'Tiem_Esp1', 'Fecha', 'Entidad', 'DelegacióN', 'Nivel', 'Unidad', 'Promedio_Diario2016']
primer_nivel = primer_nivel[columnas_interes]

fechas_horas = ['Hr_Ini_M', 'Hr_Fin_M', 'Hr_Ini_H', 'Hr_Fin_H']
for columna in fechas_horas:
    primer_nivel[columna] = primer_nivel[columna].astype(str).apply(lambda s: s if len(s) == 2 else '0' + s)

primer_nivel['FechaEntrada'] = (primer_nivel['Fecha'].astype(str) + ' '
                                + primer_nivel['Hr_Ini_H'].astype(str) + ':'
                                + primer_nivel['Hr_Ini_M'].astype(str))
primer_nivel['FechaSalida'] = (primer_nivel['Fecha'].astype(str) + ' '
                                + primer_nivel['Hr_Fin_H'].astype(str) + ':'
                                + primer_nivel['Hr_Fin_M'].astype(str))
pd.to_datetime(primer_nivel['FechaEntrada'], format='%Y-%m-%d %H:%M')
pd.to_datetime(primer_nivel['FechaSalida'], format='%Y-%m-%d %H:%M')

primer_nivel = primer_nivel.drop(['Fecha_D', 'Fecha_M', 'Fecha_A', 'Hr_Ini_H', 'Hr_Ini_M', 'Hr_Fin_H', 'Hr_Fin_M', 'Fecha'], axis=1)

print(list(primer_nivel.columns), primer_nivel.shape, primer_nivel.head(), sep='\n')
