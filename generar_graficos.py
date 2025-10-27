import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import zipfile

# Simulación de datos de encuesta (reemplaza con tus datos reales si los tienes)
df = pd.DataFrame({
    "intencion_1v": np.random.choice(["A", "B", "Blanco", "Nulo", "Indeciso"], 1000),
    "medio_info": np.random.choice(["TikTok", "Facebook", "Instagram", "Televisión tradicional", "Prensa en línea"], 1000),
    "frecuencia_participacion": np.random.choice(["Nunca", "Rara vez", "A veces", "Frecuentemente", "Siempre"], 1000),
    "genero": np.random.choice(["Masculino", "Femenino", "No Binario"], 1000),
    "ideologia": np.random.choice(["Izquierda", "Centro-Izquierda", "Centro", "Centro-Derecha", "Derecha"], 1000),
    "voto_ultimas": np.random.choice([0, 1], 1000)
})

# 1. Gráfico de barras para la "Intención de Voto"
intencion_counts = df['intencion_1v'].value_counts()
plt.figure(figsize=(8,5))
intencion_counts.plot(kind="bar", color=["blue", "red", "gray", "green", "yellow"])
plt.title("Distribución de Intención de Voto (1ra vuelta)")
plt.xlabel("Intención de Voto")
plt.ylabel("Número de Votos")
plt.xticks(rotation=45)
intencion_plot_path = "intencion_voto.png"
plt.tight_layout()
plt.savefig(intencion_plot_path, dpi=140)
plt.close()

# 2. Gráfico de torta (pie chart) para "Medios de Información"
medio_info_counts = df['medio_info'].value_counts()
plt.figure(figsize=(8,5))
medio_info_counts.plot(kind="pie", autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
plt.title("Distribución de Medios de Información")
plt.ylabel("")
medio_info_plot_path = "medio_info.png"
plt.tight_layout()
plt.savefig(medio_info_plot_path, dpi=140)
plt.close()

# 3. Gráfico de barras para "Frecuencia de Participación Cívica"
participacion_counts = df['frecuencia_participacion'].value_counts()
plt.figure(figsize=(8,5))
participacion_counts.plot(kind="bar", color=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#c2c2f0"])
plt.title("Frecuencia de Participación Cívica y Política")
plt.xlabel("Frecuencia")
plt.ylabel("Número de Votos")
plt.xticks(rotation=45)
participacion_plot_path = "participacion_civica.png"
plt.tight_layout()
plt.savefig(participacion_plot_path, dpi=140)
plt.close()

# 4. Generar simulación de balotaje (histograma de votos A y B)
share_A = np.random.beta(2, 5, 10000)
share_B = np.random.beta(5, 2, 10000)

plt.figure(figsize=(8,5))
plt.hist(share_A, bins=60, alpha=0.6, label="Candidato A (Balotaje)", density=True)
plt.hist(share_B, bins=60, alpha=0.6, label="Candidato B (Balotaje)", density=True)
plt.axvline(0.5, linestyle="--")
plt.title("Distribución de votos en Balotaje (Excluye Votos Blancos/Nulos)")
plt.xlabel("Porcentaje de Votos")
plt.ylabel("Densidad")
plt.legend()
balotaje_hist_path = "balotaje_histograma.png"
plt.tight_layout()
plt.savefig(balotaje_hist_path, dpi=140)
plt.close()

# Crear un archivo zip con los gráficos generados
zip_path = "graficos_simulacion.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(intencion_plot_path)
    zipf.write(medio_info_plot_path)
    zipf.write(participacion_plot_path)
    zipf.write(balotaje_hist_path)

print(f"Gráficos generados y guardados en {zip_path}")
