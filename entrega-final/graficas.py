import numpy as np
import matplotlib.pyplot as plt
from scipy.special import factorial

def calculate_rho(l: float, m: float, s: int):
    return l/(m*s)

def calculate_p0(rho: float, s: int):
    sum_term = 0
    for n in range(s):
        sum_term += (s * rho) ** n / factorial(n)
    sum_term += (s * rho) ** s / (factorial(s) * (1 - rho))
    return 1 / sum_term

def calculate_l(rho: float, s: int):
    p0 = calculate_p0(rho, s)
    lq = p0 * (rho * (s * rho) ** s) / (factorial(s) * (1 - rho) ** 2)
    return lq + s * rho

def create_graph(server_values: list, queue_model: int):
    # Iniciar la gráfica
    plt.figure(figsize=(10, 8))
    plt.grid(True)
    plt.yscale('log')
    plt.xticks(np.arange(0, 1.1, 0.1))

    # Definimos el dominio (valores de rho) y valores de s
    rho_values = np.linspace(0.01, 0.999, 100)
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(server_values)))

    # Generamos los valores de L (rango)
    lines = []
    labels = []
    for i, s in enumerate(server_values):
        l_values = [calculate_l(rho, s) for rho in rho_values]
        line, = plt.plot(rho_values, l_values, '-', linewidth=2.5, color=colors[i])
        lines.append(line)
        labels.append(f's = {s}')

        if s <= 5:
            pos_rho = 0.27
        elif s <= 10:
            pos_rho = 0.25
        elif s <= 20:
            pos_rho = 0.23
        else:
            pos_rho = 0.21

        idx = np.abs(rho_values - pos_rho).argmin()
        bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
        plt.annotate(f's = {s}',
                     xy=(rho_values[idx], l_values[idx]),
                     xytext=(rho_values[idx] + 0.01, l_values[idx] * 1.1),
                     fontsize=12,
                     bbox=bbox_props,
                     fontweight='bold')

    # Límites de la gráfica
    plt.xlim(0, 1.0)
    plt.ylim(0.1, 1000)
    plt.xlabel(r'Factor de utilización $\rho = \frac{\lambda}{s\mu}$', fontsize=12)
    plt.ylabel('Estado estable esperado del número de clientes en el sistema de colas (L)', fontsize=10)

    plt.title(f'Valores de L del modelo M/M/$s_{queue_model}$', fontsize=14)
    plt.tight_layout()
    plt.show()

def calculate_queue_values(l: float, m: float, server_values: list):
    for server in server_values:
        r = calculate_rho(l, m, server)
        print(server,
              r,
              calculate_l(r, server))

if __name__ == '__main__':
    create_graph([34, 50, 70, 100, 140], 1)
    print('Valores de s1 para la tabla')
    calculate_queue_values(2.22, 0.066, [34, 35, 36, 37, 40, 45, 50, 70, 100, 140])

    create_graph([31, 45, 65, 90], 2)
    print('Valores de s2 para la tabla')
    calculate_queue_values(0.99, 0.033, [31, 32, 33, 34, 35, 45, 65, 90, 140])