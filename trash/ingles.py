import matplotlib.pyplot as plt

# Aplicar tema escuro
plt.style.use('dark_background')

# Dados fictícios
anos = list(range(2015, 2025))
receita = [3.2, 3.5, 3.7, 4.0, 4.2, 5.8, 7.1, 8.6, 10.2, 11.9]
reducao_custos = [None, 2.1, 2.4, 2.6, 3.0, 4.5, 5.0, 6.2, 6.8, 7.4]
tempo_upload = [15, 14, 13, 12, 10, 7, 6, 5, 4.5, 4.2]
indies_ativos = [2000, 2400, 2800, 3300, 4000, 6500, 8300, 9700, 11000, 12400]
premios = [1, 1, 2, 2, 3, 6, 7, 9, 10, 12]

# Criar subplots
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Steam/Valve Analysis (2015–2024)', fontsize=16)

# Receita
axs[0, 0].plot(anos, receita, marker='o', color='lime')
axs[0, 0].set_title('Annual Revenue (in billion USD)')
axs[0, 0].set_ylabel('Revenue (B USD)')
axs[0, 0].grid(True)

# Redução de Custos
axs[0, 1].plot(anos[1:], reducao_custos[1:], marker='o', color='deepskyblue')
axs[0, 1].set_title('Cost Reduction (%)')
axs[0, 1].set_ylabel('% Reduction')
axs[0, 1].grid(True)

# Tempo de Upload
axs[1, 0].plot(anos, tempo_upload, marker='o', color='orange')
axs[1, 0].set_title('Average Game Upload Time (days)')
axs[1, 0].set_ylabel('Days')
axs[1, 0].grid(True)

# Prêmios
axs[1, 1].bar(anos, premios, color='magenta')
axs[1, 1].set_title('Awards and Recognitions per Year')
axs[1, 1].set_ylabel('Count')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
