
import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

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
        image = Image.open(imagen_cargada).convert("RGB")
        image_np = np.array(image)

        # Convertir de RGB a HSV
        image_hsv = np.array(image.convert("HSV"))
        H = image_hsv[:, :, 0]
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
