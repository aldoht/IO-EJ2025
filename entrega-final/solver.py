from math import factorial, log, exp, lgamma
from typing import Tuple, Literal
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np
from graficas import calculate_l, calculate_p0, calculate_rho, calculate_queue_values

def calculate_lq(p0: float, rho: float, s: int) -> float:
    return (p0 * pow(rho * s, s) * rho) / (factorial(s) * pow(1-rho, 2))

def get_lambda_mu() -> Tuple[float, float]:
    while True:
        try:
            l = float(input('El valor de lambda para la cola: '))
        except OverflowError:
            print('Error: Es un número demasiado grande. Favor de intentar de nuevo.')
            continue
        except ValueError:
            print('Error: No se introdujo ningún número. Favor de intentar de nuevo.')
            continue
        break
    while True:
        try:
            m = float(input('El valor de mu para la cola: '))
        except OverflowError:
            print('Error: Es un número demasiado grande. Favor de intentar de nuevo.')
            continue
        except ValueError:
            print('Error: No se introdujo ningún número. Favor de intentar de nuevo.')
            continue
        break
    return l, m

def get_min_server(l: float, m: float) -> int | None:
    if l / m <= 1:
        return 1
    s = 2
    while l / (s*m) >= 1:
        s += 1
    return s

def get_queue_params(l: float, m: float, s: int) -> {}:
    rho = calculate_rho(l, m, s)
    p0 = calculate_p0(rho, s)
    l_q = calculate_lq(p0, rho, s)
    w_q = l_q / l
    return {
        'inv_lambda': 1 / l,
        'lambda': l,
        'inv_mu': 1 / m,
        'mu': m,
        's': s,
        'rho': rho,
        'p0': p0,
        'W_q': w_q,
        'W': w_q + 1 / m,
        'L': calculate_l(rho, s),
        'L_q': l_q,
    }

def display_queue_params(params: dict, fmt: str) -> None:
    rows = [[key, params[key]] for key in params]
    headers = ['Parámetro', 'Valor']
    print(tabulate(rows, headers=headers, tablefmt=fmt))

def calculate_pn(n: int, rho: float, s: int, p0: float):
    if n == 0:
        return p0
    log_p0 = log(p0)
    if n <= s:
        log_num = n * log(rho * s)
        log_den = lgamma(n + 1)  # log(n!) = lgamma(n + 1)
        return exp(log_num - log_den + log_p0)
    else:
        log_num = n * log(rho * s)
        log_den = lgamma(s + 1) + (n - s) * log(s)
        return exp(log_num - log_den + log_p0)

def get_p_values(discrete_domain: list, rho: float, s: int, p0: float):
    return [calculate_pn(n, rho, s, p0) for n in discrete_domain]

def get_domain(limit: int):
    return np.arange(0, limit+2, 1)

def get_mean_from_dataset(level: int):
    match level:
        case 1:
            df = pd.read_csv('../datasets/ensat-1-septiembre-2017.csv', encoding='latin-1')
            df = df[df['Unidad'].astype(str).str.contains('UMF 28 Monterrey')]
            return df['Promedio_Diario2016'].mean() / (12*60)
        case 3:
            df = pd.read_csv('../datasets/ensat-3-septiembre-2017.csv', encoding='latin-1')
            df = df[df['Unidad'].astype(str).str.contains('HES 25 MONTERREY')]
            return df['Promedio_Diario2016'].mean() / (12*60)
        case _:
            raise Exception('Error: Ese nivel no existe en los archivos del problema.')

def show_pvalues_graph(limit: int, q_info: dict):
    plt.style.use('seaborn-v0_8-darkgrid')
    xvalues = get_domain(limit)
    yvalues = get_p_values(xvalues, q_info['rho'], q_info['s'], q_info['p0'])
    max_n_value = yvalues.index(max(yvalues))
    plt.figure(figsize=(10, 6))
    plt.plot(xvalues, yvalues, label='P(n)', color='steelblue', linewidth=2, marker='o', markersize=4)
    plt.axvline(x=max_n_value, color='crimson', linestyle='--', linewidth=2, label=f'Máx. en n={max_n_value}')
    plt.title('Probabilidades de tener x pacientes en el sistema\nen algún tiempo dado t', fontsize=14, pad=15)
    plt.xlabel('Número de pacientes', fontsize=12)
    plt.ylabel('Probabilidad', fontsize=12)
    plt.legend(frameon=True, shadow=True, fontsize=10)
    plt.grid(True, linestyle=':', linewidth=1)
    plt.tight_layout()
    plt.show()

def display_l_values(q_info: dict, fmt: str):
    rows = [[calculate_l(q_info['lambda']/(q_info['mu']*s), s), s] for s in range(q_info['s'], q_info['s']+9)]
    headers = ['Pacientes promedio en sistema', 'Servidores']
    print(tabulate(rows, headers=headers, tablefmt=fmt))

def display_queue(l: float, m: float, queues: Literal['Unknown'] | Literal[1], limit: Literal['Unknown'] | int):
    servers = get_min_server(l, m)

    if queues == 'Unknown':
        queue_params = get_queue_params(l, m, servers)
    else:
        queue_params = get_queue_params(l, m, 1)

    display_queue_params(queue_params, 'heavy_grid')
    display_l_values(queue_params, 'heavy_grid')

    if limit == 'Unknown':
        show_pvalues_graph(queue_params['L']*4, queue_params)
    else:
        show_pvalues_graph(limit, queue_params)

if __name__ == '__main__':
    print('Bienvenido al programa, ¿desea resolver los datos del IMSS o tiene otro problema?',
          '1. IMSS',
          '2. Otro',
          sep='\n')
    try:
        option = int(input('Respuesta: '))
        if option != 1 and option != 2:
            raise ValueError()
    except (OverflowError, ValueError):
        raise SystemExit('Error: Opciones no válidas. Cerrando el programa...')

    match option:
        case 1:
            print('Para la primera cola se asumen 15 minutos en promedio de servicio.')
            display_queue(get_mean_from_dataset(1), 1/15, 'Unknown', 300)
            print('Para la tercera cola se asumen 30 minutos en promedio de servicio.')
            display_queue(get_mean_from_dataset(3), 1/30, 'Unknown', 300)
        case 2:
            print('Por favor ingrese los siguientes datos:')
            lambda_1, mu_1 = get_lambda_mu()
            display_queue(lambda_1, mu_1, 'Unknown', 'Unknown')
    print('Saliendo del programa...')