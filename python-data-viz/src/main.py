from tkinter import filedialog, simpledialog
import tkinter as tk
from utils.json_reader import read_json
from visualization.heatmap import generate_heatmap

def display_data_table(data, on_heatmap_request=None):
    """
    Exibe os dados do jogo em formato tabular incluindo ID do jogador, tempo médio de reação, etc.
    Para cada modo de jogo jogado em uma sessão, mostrando entradas separadas para cada "novo jogo".
    
    Args:
        data: Os dados JSON carregados contendo as sessões de jogo
        on_heatmap_request: Função de callback para gerar mapa de calor para a sessão selecionada
    """
    try:
        import pandas as pd
        from tkinter import Toplevel, ttk
        
        # Obtém todas as sessões dos dados
        sessions = data.get('sessions', [])
        
        # Se os dados não estiverem no novo formato (com sessões), tenta tratar como uma única sessão
        if not sessions and isinstance(data, dict):
            sessions = [data]
            
        if not sessions:
            tk.messagebox.showerror("Erro de Dados", "Nenhuma sessão de jogo válida encontrada no arquivo selecionado.")
            return
            
        # Prepara os dados da tabela
        table_data = []
        session_index_map = {}  # Mapeia linhas da tabela para índices de sessão
        
        # Processa cada sessão
        for session_idx, session in enumerate(sessions):
            username = session.get('username', 'Unknown')
            session_id = session.get('session_id', f'Session {session_idx+1}')
            
            # Obtém todas as tentativas para esta sessão
            all_trials = session.get('trials', [])
            
            # Analisa tentativas em jogos - cada mudança de "modo de jogo" ou quebra de sequência indica um novo jogo
            games = []
            current_game = {"trials": [], "game_mode": None}
            
            for i, trial in enumerate(all_trials):
                trial_game_mode = trial.get('game_mode', None)
                trial_start_time = trial.get('trial_start_time', None)
                
                # Verifica se este é um novo jogo (mudança de modo ou primeira tentativa)
                if current_game["game_mode"] is None:
                    current_game["game_mode"] = trial_game_mode
                    current_game["start_time"] = trial_start_time
                    
                # Se o modo de jogo mudar ou houver uma lacuna significativa de tempo, este é um novo jogo
                elif trial_game_mode != current_game["game_mode"]:
                    # Salva o jogo anterior
                    if current_game["trials"]:
                        games.append(current_game)
                    # Inicia um novo jogo
                    current_game = {
                        "trials": [],
                        "game_mode": trial_game_mode,
                        "start_time": trial_start_time
                    }
                
                # Adiciona a tentativa ao jogo atual
                current_game["trials"].append(trial)
            
            # Não esqueça de adicionar o último jogo
            if current_game["trials"]:
                games.append(current_game)
            
            # Processa cada jogo dentro desta sessão
            for i, game in enumerate(games):
                game_mode = game["game_mode"]
                trials = game["trials"]
                
                # Torna o modo de jogo mais amigável para o usuário
                game_mode_display = game_mode
                if game_mode == 0 or game_mode == "0":
                    game_mode_display = "Modo de Aparição Única"
                elif game_mode == 1 or game_mode == "1":
                    game_mode_display = "Modo de Múltiplas Aparições"
                elif game_mode == 2 or game_mode == "2":
                    game_mode_display = "Modo Infinito"
                    
                # Calcula pontuação e taxa de sucesso
                successful_trials = sum(1 for trial in trials if trial.get('success', False))
                total_trials = len(trials)
                score = successful_trials
                success_rate = f"{(successful_trials / total_trials * 100):.1f}%" if total_trials > 0 else "N/A"
                
                # Calcula tempo médio de reação
                reaction_times = []
                for trial in trials:
                    if trial.get('reaction_time') is not None:
                        reaction_times.append(trial.get('reaction_time'))
                
                avg_reaction_time = sum(reaction_times) / len(reaction_times) if reaction_times else 'N/A'
                if avg_reaction_time != 'N/A':
                    avg_reaction_time = f"{avg_reaction_time:.2f} seg"
                
                # Formata a hora de início do jogo, se disponível
                game_start = game.get("start_time", "Unknown")
                if game_start != "Unknown" and isinstance(game_start, (int, float)):
                    try:
                        from datetime import datetime
                        dt = datetime.fromtimestamp(game_start) 
                        game_start_time = dt.strftime("%d/%m/%Y %H:%M:%S")
                    except Exception:
                        game_start_time = str(game_start)
                else:
                    # Tenta analisar o session_id como um timestamp se parecer um
                    if isinstance(session_id, str) and '_' in session_id:
                        try:
                            from datetime import datetime
                            date_part = session_id.split('_')[0]
                            if len(date_part) == 8:  # Formato AAAAMMDD
                                dt = datetime.strptime(date_part, "%Y%m%d")
                                game_start_time = dt.strftime("%d/%m/%Y")
                            else:
                                game_start_time = "Desconhecido"
                        except Exception:
                            game_start_time = "Desconhecido"
                    else:
                        game_start_time = "Desconhecido"
                    
                # Adiciona os dados deste jogo à tabela
                row_index = len(table_data)
                table_data.append({
                    'ID da Sessão': session_id,
                    'Nome do Usuário': username,
                    'Jogo #': i+1,
                    'Modo de Jogo': game_mode_display,
                    'Pontuação': score,
                    'Taxa de Sucesso': success_rate,
                    'Hora de Início': game_start_time,
                    'Tempo Médio de Reação': avg_reaction_time
                })
                
                # Armazena o mapeamento da linha da tabela para o índice da sessão
                session_index_map[row_index] = session_idx
        
        if not table_data:
            tk.messagebox.showerror("Erro de Dados", "Nenhum jogo válido encontrado nas sessões.")
            return
            
        # Create DataFrame
        df = pd.DataFrame(table_data)
        
        # Cria uma nova janela para a tabela
        table_window = Toplevel()
        table_window.title("Resumo de Dados do Jogo")
        table_window.geometry("1000x600")
        
        # Adiciona um título
        title_frame = tk.Frame(table_window, pady=10)
        title_frame.pack(fill='x')
        title_label = tk.Label(title_frame, text="Tabela de Dados das Sessões de Jogo", font=("Arial", 16, "bold"))
        title_label.pack()
        
        # Adiciona descrição
        desc_label = tk.Label(title_frame, text="Selecione uma sessão e clique em 'Gerar Mapa de Calor' para visualizar o movimento de mouse", font=("Arial", 10))
        desc_label.pack()
        
        # Cria o frame principal
        main_frame = tk.Frame(table_window)
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Cria o widget Treeview com barra de rolagem
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True)
        
        # Adiciona barra de rolagem vertical
        tree_scroll_y = ttk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Adiciona barra de rolagem horizontal
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal")
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Cria o Treeview
        tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set, selectmode="browse")
        tree_scroll_y.config(command=tree.yview)
        tree_scroll_x.config(command=tree.xview)
        
        tree["columns"] = list(df.columns)
        tree["show"] = "headings"
        
        # Set column headings
        for column in df.columns:
            tree.heading(column, text=column)
            # Adjust column width based on content
            if column in ["Hora de Início", "ID da Sessão"]:
                tree.column(column, width=150)
            elif column == "Modo de Jogo":
                tree.column(column, width=180)
            elif column == "Nome do Usuário":
                tree.column(column, width=120)
            else:
                tree.column(column, width=100)
        
        # Adiciona linhas de dados
        for i, row in df.iterrows():
            tree.insert("", "end", iid=str(i), values=list(row))
        
        tree.pack(expand=True, fill='both')
        
        # Frame para botões
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill='x', pady=10)
        
        # Adiciona botão para gerar mapa de calor para a sessão selecionada
        def on_generate_heatmap():
            selected_items = tree.selection()
            if not selected_items:
                tk.messagebox.showinfo("Seleção Necessária", "Por favor, selecione uma sessão da tabela primeiro.")
                return
            
            selected_row = int(selected_items[0])
            session_idx = session_index_map.get(selected_row)
            
            if session_idx is not None and on_heatmap_request is not None:
                selected_session = sessions[session_idx]
                on_heatmap_request(selected_session)
            else:
                tk.messagebox.showerror("Erro", "Não foi possível recuperar os dados da sessão para a linha selecionada.")
        
        if on_heatmap_request:
            heatmap_button = tk.Button(button_frame, text="Gerar Mapa de Calor para Sessão Selecionada", command=on_generate_heatmap)
            heatmap_button.pack(side=tk.LEFT, padx=5)
        
        # Adiciona botão de exportação
        def export_data():
            export_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("Arquivos CSV", "*.csv"), ("Arquivos Excel", "*.xlsx")]
            )
            if export_path:
                if export_path.endswith('.csv'):
                    df.to_csv(export_path, index=False)
                else:
                    df.to_excel(export_path, index=False)
                tk.messagebox.showinfo("Exportação Bem-Sucedida", f"Dados exportados para {export_path}")
        
        export_button = tk.Button(button_frame, text="Exportar Dados", command=export_data)
        export_button.pack(side=tk.RIGHT, padx=5)
        
        # Variáveis para armazenar dados da sessão selecionada
        selected_session_data = {'session': None}
        
        # Adiciona uma visualização detalhada da sessão selecionada
        detail_label = tk.Label(main_frame, text="Detalhes da Sessão:", anchor='w')
        detail_label.pack(fill='x', pady=(10, 0))
        
        # Widget de texto para dados JSON
        import json
        text_frame = tk.Frame(main_frame)
        text_frame.pack(expand=True, fill='both')
        
        text_widget = tk.Text(text_frame, height=8, wrap=tk.NONE)
        text_widget.pack(expand=True, fill='both')
        
        # Barras de rolagem para o widget de texto
        text_scroll_y = tk.Scrollbar(text_widget)
        text_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=text_scroll_y.set)
        text_scroll_y.config(command=text_widget.yview)
        
        text_scroll_x = tk.Scrollbar(text_frame, orient='horizontal')
        text_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        text_widget.config(xscrollcommand=text_scroll_x.set)
        text_scroll_x.config(command=text_widget.xview)
        
        # Função para atualizar a visualização de detalhes quando uma linha é selecionada
        def on_tree_select(event):
            selected_items = tree.selection()
            if not selected_items:
                return
                
            selected_row = int(selected_items[0])
            session_idx = session_index_map.get(selected_row)
            
            if session_idx is not None:
                selected_session = sessions[session_idx]
                selected_session_data['session'] = selected_session
                
                # Atualiza o widget de texto com os dados JSON
                text_widget.config(state='normal')
                text_widget.delete(1.0, tk.END)
                text_widget.insert(tk.END, json.dumps(selected_session, indent=2))
                text_widget.config(state='disabled')
        
        # Vincula o evento de seleção
        tree.bind("<<TreeviewSelect>>", on_tree_select)
        
        return table_window
        
    except ImportError as e:
        print(f"Erro: {e}")
        print("pandas é necessário para visualização de tabela de dados. Por favor, instale pandas usando 'pip install pandas'")
    except Exception as e:
        import traceback
        print(f"Erro ao exibir a tabela de dados: {e}")
        traceback.print_exc()
        
def main():
    # Cria uma janela oculta do Tkinter
    root = tk.Tk()
    root.withdraw()

    # Abre filedialog para selecionar o arquivo JSON
    json_file_path = filedialog.askopenfilename(
        title="Selecionar arquivo JSON",
        filetypes=[("Arquivos JSON", "*.json")]
    )

    if not json_file_path:
        print("Nenhum arquivo selecionado. Saindo...")
        return

    # Lê o arquivo JSON selecionado	
    data = read_json(json_file_path)
    
    if not data:
        tk.messagebox.showerror("Erro", "Não foi possível ler os dados JSON ou o arquivo está vazio.")
        return
    
    # Define a função de callback para gerar mapa de calor para a sessão selecionada
    def on_heatmap_request(session_data):
        if session_data:
            # Gera mapa de calor para a sessão selecionada
            try:
                generate_heatmap(session_data)
            except Exception as e:
                import traceback
                traceback.print_exc()
                tk.messagebox.showerror("Erro no Mapa de Calor", f"Erro ao gerar mapa de calor: {str(e)}")
    
    # Sempre exibe a tabela de dados primeiro com capacidade de geração de mapa de calor
    table_window = display_data_table(data, on_heatmap_request=on_heatmap_request)
    
    # Trata corretamente o fechamento da janela
    if table_window:
        # Adiciona protocolo para tratar o evento de fechamento da janela
        table_window.protocol("WM_DELETE_WINDOW", root.destroy)
        root.mainloop()
    else:
        tk.messagebox.showerror("Erro", "Não foi possível criar a tabela de dados.")
        return

if __name__ == "__main__":
    main()