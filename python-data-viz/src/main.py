from tkinter import filedialog
import tkinter as tk
from utils.json_reader import read_json
from visualization.heatmap import generate_heatmap

def main():
    # Cria uma janela oculta do Tkinter
    root = tk.Tk()
    root.withdraw()

    # Abre filedialog para selecionar o arquivo JSON
    json_file_path = filedialog.askopenfilename(
        title="Select JSON file",
        filetypes=[("JSON files", "*.json")]
    )

    if not json_file_path:
        print("No file selected. Exiting...")
        return

    # Lê o arquivo JSON selecionado	
    data = read_json(json_file_path)

    # Gera o heatmap usando os dados lidos
    generate_heatmap(data)

if __name__ == "__main__":
    main()