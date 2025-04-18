
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import io

st.title("📷 Cálculo de valor H (Hue) y relación con concentración")

# Inicializar listas en sesión
if 'concentraciones' not in st.session_state:
    st.session_state.concentraciones = []
if 'valores_H' not in st.session_state:
    st.session_state.valores_H = []

# Subida de imagen
imagen_cargada = st.file_uploader("Selecciona una imagen JPG", type=["jpg", "jpeg"])
concentracion = st.number_input("Introduce la concentración correspondiente (en M):", min_value=0.0, step=0.01)

if st.button("Agregar datos"):
    if imagen_cargada:
        # Convertir la imagen cargada a formato OpenCV
        image = Image.open(imagen_cargada).convert("RGB")
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        hsv = cv2.cvtColor(image_cv, cv2.COLOR_BGR2HSV)
        H = hsv[:, :, 0]
        H_promedio = np.mean(H)

        st.session_state.concentraciones.append(concentracion)
        st.session_state.valores_H.append(H_promedio)

        st.success(f"H promedio: {H_promedio:.2f} agregado con concentración {concentracion} M")

# Mostrar gráfico si hay datos
if len(st.session_state.concentraciones) > 1:
    st.subheader("📊 Gráfica H vs Concentración")
    fig, ax = plt.subplots()
    ax.plot(st.session_state.concentraciones, st.session_state.valores_H, 'o-', label="Datos")
    ax.set_xlabel("Concentración (M)")
    ax.set_ylabel("H (Hue promedio)")
    ax.grid(True)
    st.pyplot(fig)
