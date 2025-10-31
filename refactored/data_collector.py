"""
Sistema de coleta de dados de jogabilidade
"""
import os
import json
import time
from datetime import datetime


class GameDataCollector:
    """Coleta e armazena dados de jogabilidade para análise"""
    def __init__(self):
        self.all_sessions = self.load_existing_data()
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "username": "Anônimo",
            "game_mode": None,
            "trials": [],
            "mouse_tracking": [],
            "session_metrics": {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        }
        self.current_trial = None
        self.target_spawn_time = None
        self.last_interaction_time = time.time()
        self.clicks_positions = []
        self.mouse_movement_count = 0
        self.last_mouse_pos = None
        self.total_mouse_distance = 0
    
    def load_existing_data(self):
        """Carrega dados existentes ou cria novo arquivo"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_str_no_dash = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M%S")
        base_dir = "playerdata"
        date_dir = os.path.join(base_dir, date_str)
        
        os.makedirs(date_dir, exist_ok=True)
        
        filename = os.path.join(date_dir, f"game_data_{date_str_no_dash}_{time_str}.json")
        
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {"sessions": []}
        
        return {"sessions": []}
    
    def set_username(self, username):
        """Define o nome do usuário"""
        self.current_session["username"] = username if username else "Anônimo"
    
    def start_new_trial(self, game_mode):
        """Inicia uma nova tentativa"""
        self.current_trial = {
            "trial_start_time": time.time(),
            "game_mode": game_mode,
            "target_character": None,
            "target_spawn_time": None,
            "selection_time": None,
            "success": False,
            "reaction_time": None,
            "score": 0,
            "trial_metrics": {
                "mouse_movements": 0,
                "hesitation_time": 0,
                "clicks_before_success": 0,
                "average_mouse_speed": 0,
                "mouse_path_length": 0
            }
        }
        
        if game_mode == 3:  # GAME_MODE_ARROW
            self.current_trial["target_spawn_time"] = time.time()
        
        self.clicks_positions = []
        self.mouse_movement_count = 0
        self.last_mouse_pos = None
        self.total_mouse_distance = 0
    
    def update_trial_score(self, score):
        """Atualiza a pontuação da tentativa atual"""
        if self.current_trial:
            self.current_trial["score"] = score
    
    def record_target_spawn(self, character_traits):
        """Registra o aparecimento de um personagem alvo"""
        if self.current_trial:
            serializable_traits = {
                'head': {'name': character_traits['head']['name']},
                'face': {'name': character_traits['face']['name']},
                'body': {'name': character_traits['body']['name']},
                'hat': {'name': character_traits['hat']['name']}
            }
            self.current_trial["target_character"] = serializable_traits
            self.current_trial["target_spawn_time"] = time.time()
            self.target_spawn_time = time.time()

    def record_mouse_position(self, mouse_pos, game_state):
        """Registra a posição do mouse"""
        current_time = time.time()
        
        self.current_session["mouse_tracking"].append({
            "timestamp": current_time,
            "x": mouse_pos[0],
            "y": mouse_pos[1],
            "game_state": game_state
        })
        
        if self.current_trial and self.last_mouse_pos:
            dx = mouse_pos[0] - self.last_mouse_pos[0]
            dy = mouse_pos[1] - self.last_mouse_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 5:
                self.mouse_movement_count += 1
                self.total_mouse_distance += distance
        
        if "session_metrics" not in self.current_session:
            self.current_session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        if current_time - self.last_interaction_time > 3.0:
            self.current_session["session_metrics"]["focus_breaks"] += 1
        
        self.last_interaction_time = current_time
        self.last_mouse_pos = mouse_pos
    
    def record_click(self, position, success):
        """Registra um clique"""
        self.clicks_positions.append({
            "x": position[0],
            "y": position[1],
            "timestamp": time.time(),
            "success": success
        })
        
        if "session_metrics" not in self.current_session:
            self.current_session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        self.current_session["session_metrics"]["total_clicks"] += 1
        if success:
            self.current_session["session_metrics"]["correct_clicks"] += 1
        else:
            self.current_session["session_metrics"]["incorrect_clicks"] += 1
            self.current_session["session_metrics"]["false_positives"] += 1
        
        if self.current_trial:
            self.current_trial["trial_metrics"]["clicks_before_success"] += 1
    
    def record_selection(self, success):
        """Registra uma seleção de personagem"""
        if self.current_trial and self.target_spawn_time:
            selection_time = time.time()
            self.current_trial["selection_time"] = selection_time
            self.current_trial["success"] = success
            self.current_trial["reaction_time"] = selection_time - self.target_spawn_time
            
            trial_duration = selection_time - self.current_trial["trial_start_time"]
            self.current_trial["trial_metrics"]["mouse_movements"] = self.mouse_movement_count
            
            if self.total_mouse_distance > 0 and trial_duration > 0:
                self.current_trial["trial_metrics"]["average_mouse_speed"] = self.total_mouse_distance / trial_duration
                self.current_trial["trial_metrics"]["mouse_path_length"] = self.total_mouse_distance
            
            if self.current_trial["target_spawn_time"]:
                hesitation = selection_time - self.current_trial["target_spawn_time"]
                self.current_trial["trial_metrics"]["hesitation_time"] = hesitation
            
            self.current_trial["clicks"] = self.clicks_positions.copy()
            
            self.current_session["trials"].append(self.current_trial)
            self.current_trial = None
            
            self.clicks_positions = []
            self.mouse_movement_count = 0
            self.total_mouse_distance = 0
    
    def record_arrow_selection(self, success, clicked_quadrant, target_quadrant, 
                              arrow_angle, arrow_speed, arrow_in_zone):
        """Registra uma seleção do modo seta"""
        if self.current_trial:
            selection_time = time.time()
            self.current_trial["selection_time"] = selection_time
            self.current_trial["success"] = success
            self.current_trial["reaction_time"] = selection_time - self.current_trial["trial_start_time"]
            
            self.current_trial["arrow_metrics"] = {
                "clicked_quadrant": clicked_quadrant,
                "target_quadrant": target_quadrant,
                "arrow_angle_at_click": arrow_angle,
                "arrow_rotation_speed": arrow_speed,
                "arrow_in_target_zone": arrow_in_zone,
                "timing_accuracy": "perfect" if arrow_in_zone else "missed_timing",
                "quadrant_accuracy": "correct" if clicked_quadrant == target_quadrant else "wrong_quadrant"
            }
            
            trial_duration = selection_time - self.current_trial["trial_start_time"]
            self.current_trial["trial_metrics"]["mouse_movements"] = self.mouse_movement_count
            
            if self.total_mouse_distance > 0 and trial_duration > 0:
                self.current_trial["trial_metrics"]["average_mouse_speed"] = self.total_mouse_distance / trial_duration
                self.current_trial["trial_metrics"]["mouse_path_length"] = self.total_mouse_distance
            
            self.current_trial["clicks"] = self.clicks_positions.copy()
            
            self.current_session["trials"].append(self.current_trial)
            self.current_trial = None
            
            self.clicks_positions = []
            self.mouse_movement_count = 0
            self.total_mouse_distance = 0
    
    def create_new_session(self, game_mode=None):
        """Cria uma nova sessão de jogo"""
        if len(self.current_session["trials"]) > 0:
            serializable_session = self.prepare_session_for_saving(self.current_session)
            self.all_sessions["sessions"].append(serializable_session)
        
        self.current_session = {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S_%f"),
            "username": self.current_session["username"],
            "game_mode": game_mode,
            "trials": [],
            "mouse_tracking": [],
            "session_metrics": {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        }
    
    def prepare_session_for_saving(self, session):
        """Prepara a sessão para ser salva em JSON"""
        if "session_metrics" not in session:
            session["session_metrics"] = {
                "total_clicks": 0,
                "correct_clicks": 0,
                "incorrect_clicks": 0,
                "missed_targets": 0,
                "false_positives": 0,
                "session_duration": 0,
                "focus_breaks": 0
            }
        
        if session["trials"]:
            first_trial_time = session["trials"][0]["trial_start_time"]
            last_trial_time = session["trials"][-1].get("selection_time", 
                                                        session["trials"][-1]["trial_start_time"])
            session["session_metrics"]["session_duration"] = last_trial_time - first_trial_time
        
        serializable_session = {
            "session_id": session["session_id"],
            "username": session["username"],
            "game_mode": session["game_mode"],
            "trials": [],
            "mouse_tracking": session["mouse_tracking"],
            "session_metrics": session["session_metrics"]
        }
        
        for trial in session["trials"]:
            serializable_trial = {
                "trial_start_time": trial["trial_start_time"],
                "game_mode": trial["game_mode"],
                "target_spawn_time": trial["target_spawn_time"],
                "selection_time": trial["selection_time"],
                "success": trial["success"],
                "reaction_time": trial["reaction_time"],
                "score": trial.get("score", 0),
                "trial_metrics": trial.get("trial_metrics", {}),
                "clicks": trial.get("clicks", [])
            }
            
            if trial.get("target_character"):
                serializable_trial["target_character"] = {
                    'head': {'name': trial["target_character"]["head"]["name"]},
                    'face': {'name': trial["target_character"]["face"]["name"]},
                    'body': {'name': trial["target_character"]["body"]["name"]},
                    'hat': {'name': trial["target_character"]["hat"]["name"]}
                }
            
            if trial.get("arrow_metrics"):
                serializable_trial["arrow_metrics"] = trial["arrow_metrics"]
                
            serializable_session["trials"].append(serializable_trial)
            
        return serializable_session
    
    def save_session_data(self):
        """Salva os dados da sessão em arquivo"""
        if self.current_session and len(self.current_session["trials"]) > 0:
            serializable_session = self.prepare_session_for_saving(self.current_session)
            self.all_sessions["sessions"].append(serializable_session)
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        date_str_no_dash = datetime.now().strftime("%Y%m%d")
        time_str = datetime.now().strftime("%H%M%S")
        base_dir = "playerdata"
        date_dir = os.path.join(base_dir, date_str)
        
        os.makedirs(date_dir, exist_ok=True)
        
        filename = os.path.join(date_dir, f"game_data_{date_str_no_dash}_{time_str}.json")
        
        with open(filename, 'w') as f:
            json.dump(self.all_sessions, f, indent=2)
