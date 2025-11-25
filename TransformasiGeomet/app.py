import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Fungsi Transformasi Geometri ---

def translate_point(x, y, tx, ty):
    """Menghitung translasi titik (x, y) sejauh (tx, ty)."""
    x_new = x + tx
    y_new = y + ty
    return x_new, y_new

def rotate_point(x, y, angle_deg, cx=0, cy=0):
    """Menghitung rotasi titik (x, y) sejauh angle_deg di sekitar pusat (cx, cy)."""
    angle_rad = np.radians(angle_deg)
    # Pindahkan ke pusat (0,0)
    x_shifted = x - cx
    y_shifted = y - cy
    # Terapkan rotasi
    x_new = x_shifted * np.cos(angle_rad) - y_shifted * np.sin(angle_rad)
    y_new = x_shifted * np.sin(angle_rad) + y_shifted * np.cos(angle_rad)
    # Pindahkan kembali
    x_new += cx
    y_new += cy
    return x_new, y_new

def dilate_point(x, y, k, cx=0, cy=0):
    """Menghitung dilatasi titik (x, y) dengan faktor skala k dan pusat (cx, cy)."""
    # Pindahkan ke pusat (0,0)
    x_shifted = x - cx
    y_shifted = y - cy
    # Terapkan dilatasi
    x_new = x_shifted * k
    y_new = y_shifted * k
    # Pindahkan kembali
    x_new += cx
    y_new += cy
    return x_new, y_new

def reflect_point(x, y, axis):
    """Menghitung refleksi titik (x, y) terhadap sumbu/garis tertentu."""
    if axis == "sumbu x":
        return x, -y
    elif axis == "sumbu y":
        return -x, y
    elif axis == "garis y = x":
        return y, x
    elif axis == "garis y = -x":
        return -y, -x
    return x, y # Default jika tidak ada yang dipilih

# --- 2. Komponen Plotting ---

def plot_transformation(original_points, transformed_points, title):
    """Membuat plot yang menampilkan titik asli dan titik hasil transformasi."""
    fig, ax = plt.subplots(figsize=(6, 6))

    # Ekstrak koordinat
    x_orig = [p[0] for p in original_points]
    y_orig = [p[1] for p in original_points]
    x_trans = [p[0] for p in transformed_points]
    y_trans = [p[1] for p in transformed_points]

    # Plot titik asli (biru)
    ax.plot(x_orig, y_orig, 'bo-', label='Asli')
    ax.plot(x_orig, y_orig, 'b.')

    # Plot titik hasil (merah)
    ax.plot(x_trans, y_trans, 'ro--', label='Transformasi')
    ax.plot(x_trans, y_trans, 'r.')

    # Menambahkan anotasi untuk titik (opsional)
    for i in range(len(original_points)):
        ax.annotate(f'A{i+1} ({x_orig[i]:.1f}, {y_orig[i]:.1f})', (x_orig[i], y_orig[i]), textcoords="offset points", xytext=(0,10), ha='center', color='blue')
        ax.annotate(f"A'{i+1} ({x_trans[i]:.1f}, {y_trans[i]:.1f})", (x_trans[i], y_trans[i]), textcoords="offset points", xytext=(0,-15), ha='center', color='red')

    # Konfigurasi plot
    max_coord = max(
        max(np.abs(x_orig)), max(np.abs(y_orig)),
        max(np.abs(x_trans)), max(np.abs(y_trans))
    ) * 1.2 + 1 # Batas sumbu
    ax.set_xlim(-max_coord, max_coord)
    ax.set_ylim(-max_coord, max_coord)
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('Sumbu X')
    ax.set_ylabel('Sumbu Y')
    ax.set_title(title)
    ax.legend()

    st.pyplot(fig)

# --- 3. Antarmuka Streamlit ---

def main():
    st.set_page_config(layout="wide", page_title="Virtual Lab Transformasi Geometri")

    st.title("🔬 Virtual Lab Transformasi Geometri")
    st.markdown("Interaktif untuk memahami **Rotasi, Dilatasi, Refleksi, dan Translasi**.")

    st.sidebar.header("⚙️ Konfigurasi Titik Awal")

    # Input untuk titik awal
    st.sidebar.markdown("**Input Koordinat Titik Asli**")
    try:
        # Mengizinkan input banyak titik untuk membentuk bentuk
        points_str = st.sidebar.text_area(
            "Masukkan koordinat titik (pisahkan dengan koma dan spasi, contoh: 1,2; 3,4; 5,1)",
            value="1,2; 3,4; 5,1"
        )
        original_points = []
        for p_str in points_str.split(';'):
            x, y = map(float, p_str.strip().split(','))
            original_points.append((x, y))
    except:
        st.sidebar.error("Format koordinat tidak valid. Gunakan format X,Y; X2,Y2; ...")
        return

    # Menambahkan titik pertama ke akhir untuk menutup bentuk (jika lebih dari 1 titik)
    if len(original_points) > 1:
        original_points.append(original_points[0])

    st.header("Pilih Transformasi")
    # Pilihan transformasi
    transformation_type = st.selectbox(
        "Pilih jenis Transformasi:",
        ["Translasi", "Rotasi", "Dilatasi", "Refleksi"]
    )

    st.subheader(f"✨ Transformasi: {transformation_type}")
    transformed_points = []
    title = f"Visualisasi {transformation_type}"

    # --- Pengaturan Parameter Berdasarkan Jenis Transformasi ---

    if transformation_type == "Translasi":
        col1, col2 = st.columns(2)
        with col1:
            tx = st.slider("Pergeseran pada Sumbu X ($T_x$)", -5.0, 5.0, 2.0, 0.1)
        with col2:
            ty = st.slider("Pergeseran pada Sumbu Y ($T_y$)", -5.0, 5.0, 1.0, 0.1)

        # Hitung Transformasi
        transformed_points = [translate_point(x, y, tx, ty) for x, y in original_points]

        st.markdown(f"Rumus: $P'(x', y') = P(x, y) + T(T_x, T_y) \implies (x+T_x, y+T_y)$")
        st.info(f"Titik akan digeser **{tx}** satuan secara horizontal dan **{ty}** satuan secara vertikal.")

    elif transformation_type == "Rotasi":
        col1, col2, col3 = st.columns(3)
        with col1:
            angle = st.slider("Sudut Rotasi (derajat)", -360.0, 360.0, 90.0, 5.0)
        with col2:
            cx = st.number_input("Pusat Rotasi X ($C_x$)", value=0.0, step=1.0)
        with col3:
            cy = st.number_input("Pusat Rotasi Y ($C_y$)", value=0.0, step=1.0)

        # Hitung Transformasi
        transformed_points = [rotate_point(x, y, angle, cx, cy) for x, y in original_points]

        st.markdown(f"Rotasi $[(C_x, C_y), \\theta]$")
        st.info(f"Titik dirotasi **{angle}°** berlawanan arah jarum jam (jika positif) mengelilingi pusat **({cx}, {cy})**.")

    elif transformation_type == "Dilatasi":
        col1, col2, col3 = st.columns(3)
        with col1:
            k = st.slider("Faktor Skala ($k$)", 0.1, 5.0, 2.0, 0.1)
        with col2:
            cx = st.number_input("Pusat Dilatasi X ($C_x$)", value=0.0, step=1.0)
        with col3:
            cy = st.number_input("Pusat Dilatasi Y ($C_y$)", value=0.0, step=1.0)

        # Hitung Transformasi
        transformed_points = [dilate_point(x, y, k, cx, cy) for x, y in original_points]

        st.markdown(f"Rumus: $P'(x', y') = C + k(P - C)$")
        st.info(f"Titik diperbesar/diperkecil dengan faktor skala **{k}** dari pusat **({cx}, {cy})**.")

    elif transformation_type == "Refleksi":
        axis = st.selectbox(
            "Pilih Sumbu/Garis Refleksi:",
            ["sumbu x", "sumbu y", "garis y = x", "garis y = -x"]
        )

        # Hitung Transformasi
        transformed_points = [reflect_point(x, y, axis) for x, y in original_points]

        rumus = {
            "sumbu x": "$(x, y) \implies (x, -y)$",
            "sumbu y": "$(x, y) \implies (-x, y)$",
            "garis y = x": "$(x, y) \implies (y, x)$",
            "garis y = -x": "$(x, y) \implies (-y, -x)$"
        }
        st.markdown(f"Rumus: $P'(x', y') = {rumus[axis]}$")
        st.info(f"Titik dicerminkan terhadap **{axis}**.")

    # --- Plotting Hasil ---
    if original_points and transformed_points:
        st.markdown("---")
        st.subheader("🖼️ Visualisasi Hasil Transformasi")
        plot_transformation(original_points, transformed_points, title)
        

        st.markdown("---")
        st.subheader("📋 Hasil Koordinat")
        results = []
        # Tampilkan koordinat asli dan hasil
        for i, (orig, trans) in enumerate(zip(original_points, transformed_points)):
            if i < len(original_points) - 1 or len(original_points) == 1: # Hindari menampilkan duplikat titik penutup
                results.append({
                    "Titik Asli": f"A{i+1} ({orig[0]:.1f}, {orig[1]:.1f})",
                    "Titik Hasil": f"A'{i+1} ({trans[0]:.1f}, {trans[1]:.1f})"
                })

        st.dataframe(results, hide_index=True)


if __name__ == "__main__":
    main()
