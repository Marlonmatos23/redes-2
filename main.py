import psutil
import time
import matplotlib.pyplot as plt

# Função para monitorar tráfego de rede real usando psutil
def monitor_network_traffic(interface="eth0", duration=30, interval=1):
    """
    Monitora o tráfego de rede em tempo real e gera um gráfico.
    
    :param interface: Interface de rede a ser monitorada (ex: "eth0" ou "wlan0").
    :param duration: Tempo total de monitoramento (em segundos).
    :param interval: Intervalo entre as medições (em segundos).
    :return: Listas de tempos e largura de banda (em Mbits/sec).
    """
    time_values = []
    bw_values = []

    # Pegando o tráfego de rede no início
    initial_stats = psutil.net_io_counters(pernic=True).get(interface, None)
    if initial_stats is None:
        print(f"Interface {interface} não encontrada.")
        return [], []

    initial_bytes_sent = initial_stats.bytes_sent
    initial_bytes_recv = initial_stats.bytes_recv

    # Monitorando o tráfego por 'duration' segundos
    for t in range(0, duration, interval):
        time_values.append(t)

        # Pegando as estatísticas de tráfego da interface
        current_stats = psutil.net_io_counters(pernic=True).get(interface, None)
        if current_stats is None:
            print(f"Interface {interface} não encontrada durante a execução.")
            break

        current_bytes_sent = current_stats.bytes_sent
        current_bytes_recv = current_stats.bytes_recv

        # Calculando a largura de banda em Mbits/sec (transmissão + recebimento)
        sent_bw = (current_bytes_sent - initial_bytes_sent) / (interval * 1024 * 1024)
        recv_bw = (current_bytes_recv - initial_bytes_recv) / (interval * 1024 * 1024)
        total_bw = sent_bw + recv_bw

        bw_values.append(total_bw)

        # Atualizando os valores anteriores
        initial_bytes_sent = current_bytes_sent
        initial_bytes_recv = current_bytes_recv

        time.sleep(interval)  # Espera o intervalo antes da próxima medição

    return time_values, bw_values

# Função para gerar o gráfico
def plot_network_traffic(time_values, bw_values):
    """
    Gera um gráfico da largura de banda de rede ao longo do tempo.
    
    :param time_values: Lista de tempos em que a largura de banda foi medida.
    :param bw_values: Lista de valores de largura de banda (em Mbits/sec).
    """
    plt.plot(time_values, bw_values, marker='o', linestyle='-')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Largura de Banda (Mbits/sec)")
    plt.title("Monitoramento de Tráfego de Rede")
    plt.grid()
    plt.show()

# Executar a monitorização do tráfego na interface de rede "eth0" durante 30 segundos com intervalos de 1 segundo
time_values, bw_values = monitor_network_traffic(interface="eth0", duration=30, interval=1)

# Gerar o gráfico
if time_values and bw_values:
    plot_network_traffic(time_values, bw_values)
else:
    print("Erro ao capturar dados de tráfego de rede.")
