import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import re
import datetime
import random

def fetch_top3():
    """
    Fetch y parsea el top 5 de Global Power Rankings desde LoL Esports.
    Devuelve al menos 5 para variaciones, usa fallback si falla.
    """
    url = 'https://lolesports.com/en-US/gpr'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        text = response.text
        
        # Regex para extraer ranks: e.g., "1. -. Gen.G Esports. GEN. LCK. 1627 pts"
        pattern = r'(\d+)\.\s*-\.\s*([A-Za-z0-9\s.&]+?)\.\s*[A-Z]{2,4}\.\s*[A-Z]{2,4}\.\s*\d+\s*pts'
        matches = re.findall(pattern, text, re.IGNORECASE)
        
        top5_full = [f"{match[0]}. {match[1].strip()}" for match in matches[:5]]
        
        if len(top5_full) >= 5:
            return top5_full, True, "Datos frescos de LoL Esports"
        else:
            raise Exception("No se encontraron suficientes equipos")
    except Exception as e:
        print(f"Error en fetch: {e}")
        # Fallback extendido a top 5 (realista al 01/10/2025)
        fallback = [
            "1. Gen.G Esports",
            "2. Hanwha Life Esports",
            "3. T1",
            "4. Bilibili Gaming",
            "5. Dplus KIA"
        ]
        return fallback, False, f"Fallback usado: Error en scraping ({str(e)})"

def generate_variations(base_top3):
    """
    Genera variaciones seguras basado en los equipos disponibles.
    Evita IndexError usando solo índices válidos.
    """
    teams = [team.split('. ', 1)[1] for team in base_top3]  # Extrae nombres
    max_idx = len(teams) - 1  # Índice máximo seguro
    variations = []
    
    # Escenario 1: Actual
    variations.append({
        'escenario': 'Actual (GPR)',
        'descripcion': 'Basado en rankings actuales de LoL Esports.',
        'top3': ', '.join([f"{i+1}. {team}" for i, team in enumerate(teams[:3])])
    })
    
    # Variación 2: Upset LCK
    if max_idx >= 2:
        temp = teams.copy()
        idx = random.randint(2, min(3, max_idx))  # Índice seguro
        temp[2], temp[idx] = temp[idx], temp[2]
        variations.append({
            'escenario': 'Upset en LCK',
            'descripcion': 'Si T1 pierde vs LPL en play-ins.',
            'top3': ', '.join([f"{i+1}. {team}" for i, team in enumerate(temp[:3])])
        })
    
    # Variación 3: Dominio LPL
    if max_idx >= 3:
        temp = teams.copy()
        temp[0], temp[3] = temp[3], temp[0]  # Swap con BLG (o similar)
        variations.append({
            'escenario': 'Dominio LPL',
            'descripcion': 'Si BLG/AL upsets a Gen.G en semis.',
            'top3': ', '.join([f"{i+1}. {team}" for i, team in enumerate(temp[:3])])
        })
    
    # Variación 4: Estabilidad
    variations.append({
        'escenario': 'Estabilidad',
        'descripcion': 'Sin grandes upsets, LCK domina.',
        'top3': ', '.join([f"{i+1}. {team}" for i, team in enumerate(teams[:3])])
    })
    
    return variations

def update_display():
    """Actualiza labels, tabla y status."""
    global last_update_time
    base_top5, connected, fetch_message = fetch_top3()
    last_update_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Actualiza labels principales
    label1.config(text=base_top5[0])
    label2.config(text=base_top5[1])
    label3.config(text=base_top5[2])
    
    # Genera y actualiza tabla
    variations = generate_variations(base_top5)
    for item in tree.get_children():
        tree.delete(item)
    for var in variations:
        tree.insert('', 'end', values=(var['escenario'], var['descripcion'], var['top3']))
    
    # Status con conexión y tiempo
    conn_status = "Éxito" if connected else "Fallback"
    status_label.config(text=f"Actualizado: {last_update_time} | Conexión: {conn_status} | {fetch_message}")

def auto_update():
    """Toggle auto-update cada 30s."""
    if auto_var.get():
        update_display()
        root.after(30000, auto_update)

# Configuración GUI
root = tk.Tk()
root.title("Predicción IA: Top 3 Worlds LoL 2025 - Versión Mejorada")
root.geometry("600x500")
root.configure(bg='black')

# Colores neón
neon_green = "#00FF41"
neon_purple = "#8A2BE2"

# Título
title = tk.Label(
    root, 
    text="Predicción IA Top 3\nCampeonato LoL Worlds 2025", 
    fg=neon_green, 
    bg='black', 
    font=('Arial', 16, 'bold')
)
title.pack(pady=10)

# Labels principales top 3
label1 = tk.Label(root, text="", fg=neon_purple, bg='black', font=('Arial', 14, 'bold'))
label1.pack(pady=2)

label2 = tk.Label(root, text="", fg=neon_purple, bg='black', font=('Arial', 14, 'bold'))
label2.pack(pady=2)

label3 = tk.Label(root, text="", fg=neon_purple, bg='black', font=('Arial', 14, 'bold'))
label3.pack(pady=10)

# Tabla de variaciones
frame_table = tk.Frame(root, bg='black')
frame_table.pack(pady=10, padx=20, fill='both', expand=True)

columns = ('Escenario', 'Descripción', 'Top 3 Predicho')
tree = ttk.Treeview(frame_table, columns=columns, show='headings', height=6)
tree.heading('Escenario', text='Escenario')
tree.heading('Descripción', text='Descripción')
tree.heading('Top 3 Predicho', text='Top 3 Predicho')

# Estilo neón para tabla
style = ttk.Style()
style.configure('Treeview', background='black', foreground=neon_purple, fieldbackground='black')
style.configure('Treeview.Heading', background='black', foreground=neon_green, font=('Arial', 10, 'bold'))

tree.column('Escenario', width=100)
tree.column('Descripción', width=200)
tree.column('Top 3 Predicho', width=250)

scrollbar = ttk.Scrollbar(frame_table, orient='vertical', command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

# Botón y auto-update
button_frame = tk.Frame(root, bg='black')
button_frame.pack(pady=10)

button = tk.Button(
    button_frame, 
    text="Actualizar Manual (Tiempo Real)", 
    command=update_display, 
    fg=neon_green, 
    bg='black', 
    activeforeground=neon_purple,
    activebackground='black',
    font=('Arial', 12, 'bold'),
    relief='flat',
    borderwidth=0
)
button.pack(side='left', padx=5)

auto_var = tk.BooleanVar()
auto_check = tk.Checkbutton(
    button_frame,
    text="Auto-actualizar cada 30s",
    variable=auto_var,
    command=auto_update,
    fg=neon_purple,
    bg='black',
    selectcolor='black',
    activeforeground=neon_green,
    activebackground='black',
    font=('Arial', 10)
)
auto_check.pack(side='left', padx=10)

# Status
last_update_time = ""
status_label = tk.Label(root, text="Cargando...", fg=neon_green, bg='black', font=('Arial', 10))
status_label.pack(pady=5)

# Carga inicial
update_display()

root.mainloop()