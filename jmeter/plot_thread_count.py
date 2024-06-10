import pandas as pd
import matplotlib.pyplot as plt

# Caminho para o arquivo CSV
arquivo_csv = 'thread_count.csv'

# Leitura do arquivo CSV em um DataFrame
df = pd.read_csv(arquivo_csv)

# Visualização rápida dos dados
print(df.head())

# Gerando um gráfico de linha
plt.figure(figsize=(10, 6))
plt.plot(df['thread_count'], df['latency'], marker='o', linestyle='-')

plt.title('Gráfico de Linha de Latência vs. Quantidade de Threads')
plt.xlabel('Quantidade de Threads')
plt.ylabel('Latência')

plt.grid(True)
plt.tight_layout()
plt.show()
