"""
Sistema de highscores (pontuações máximas)
"""
import os
import json
from datetime import datetime


class HighscoreManager:
    """Gerencia as melhores pontuações dos jogadores"""
    def __init__(self):
        self.highscores = self.load_highscores()
    
    def load_highscores(self):
        """Carrega os highscores do arquivo"""
        try:
            highscore_path = os.path.join("playerdata", "highscore", "highscores.json")
            if os.path.exists(highscore_path):
                with open(highscore_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {"single": [], "alternating": [], "infinite": [], "arrow": []}
        except:
            return {"single": [], "alternating": [], "infinite": [], "arrow": []}
    
    def add_highscore(self, name, score, mode):
        """Adiciona uma nova pontuação ao ranking - APENAS para modos INFINITE e ARROW"""
        # Só salva no highscore se for modo INFINITE ou ARROW
        if mode not in [2, 3]:  # GAME_MODE_INFINITE = 2, GAME_MODE_ARROW = 3
            return
            
        mode_names = {
            0: "single",
            1: "alternating", 
            2: "infinite",
            3: "arrow"
        }
        
        mode_key = mode_names.get(mode, "infinite")
        
        if mode_key not in self.highscores:
            self.highscores[mode_key] = []
        
        clean_name = name.strip() if name and name.strip() else "Anônimo"
        new_score = {
            "name": clean_name,
            "score": score,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        self.highscores[mode_key].append(new_score)
        
        # Ordena por pontuação (maior primeiro) e mantém apenas top 10
        self.highscores[mode_key].sort(key=lambda x: x["score"], reverse=True)
        self.highscores[mode_key] = self.highscores[mode_key][:10]
        
        self.save_highscores()
    
    def is_highscore(self, score, mode):
        """Verifica se a pontuação é um highscore - APENAS para modos INFINITE e ARROW"""
        # Só considera highscore se for modo INFINITE ou ARROW
        if mode not in [2, 3]:
            return False
            
        mode_names = {
            0: "single",
            1: "alternating",
            2: "infinite",
            3: "arrow"
        }
        
        mode_key = mode_names.get(mode, "infinite")
        scores = self.highscores[mode_key]
        
        # Se tem menos de 10 pontuações, sempre é highscore
        if len(scores) < 10:
            return True
        
        # Se a pontuação é maior que a menor do top 10
        return score > scores[-1]["score"]
    
    def save_highscores(self):
        """Salva os highscores no arquivo"""
        try:
            highscore_dir = os.path.join("playerdata", "highscore")
            os.makedirs(highscore_dir, exist_ok=True)
            
            highscore_path = os.path.join(highscore_dir, "highscores.json")
            with open(highscore_path, 'w', encoding='utf-8') as f:
                json.dump(self.highscores, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar highscores: {e}")
    
    def get_mode_highscores(self, mode):
        """Retorna os highscores de um modo específico"""
        mode_names = {
            0: "single",
            1: "alternating",
            2: "infinite",
            3: "arrow"
        }
        mode_key = mode_names.get(mode, "infinite")
        return self.highscores.get(mode_key, [])
