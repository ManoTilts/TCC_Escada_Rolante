import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_heatmap(data):
    # Extrair apenas os arrays completos de mouse_tracking
    mouse_data = []
    for entry in data['mouse_tracking']:
        if 'x' in entry and 'y' in entry:
            mouse_data.append({
                'x': entry['x'],
                'y': entry['y'],
                'game_state': entry['game_state']
            })
    
    # Converte para DataFrame
    heatmap_data = pd.DataFrame(mouse_data)
    
    # Cria o Heatmap usando seaborn
    plt.figure(figsize=(12, 8))
    
    # Gera heatmap com coordenadas x e y
    sns.kdeplot(
        data=heatmap_data,
        x='x',
        y='y',
        cmap='hot',
        fill=True
    )
    
    plt.title('Mouse Movement Heatmap')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    
    # Mostra o gráfico
    plt.show()