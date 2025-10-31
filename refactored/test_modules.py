"""
Script de verificação rápida da versão refatorada
Testa a importação de todos os módulos
"""
import sys
import os

def test_imports():
    """Testa se todos os módulos importam corretamente"""
    print("🔍 Testando importação dos módulos...")
    
    try:
        print("  ├─ Importando config...", end=" ")
        import config
        print("✅")
        
        print("  ├─ Importando characters...", end=" ")
        import characters
        print("✅")
        
        print("  ├─ Importando ui_components...", end=" ")
        import ui_components
        print("✅")
        
        print("  ├─ Importando data_collector...", end=" ")
        import data_collector
        print("✅")
        
        print("  ├─ Importando highscore_manager...", end=" ")
        import highscore_manager
        print("✅")
        
        print("  ├─ Importando game_modes...", end=" ")
        import game_modes
        print("✅")
        
        print("  └─ Importando rendering...", end=" ")
        import rendering
        print("✅")
        
        print("\n✅ Todos os módulos importados com sucesso!\n")
        return True
        
    except ImportError as e:
        print(f"\n❌ Erro ao importar: {e}")
        return False

def test_config():
    """Testa as configurações"""
    print("🔍 Verificando configurações...")
    import config
    
    print(f"  ├─ Resolução: {config.WIDTH}x{config.HEIGHT}")
    print(f"  ├─ Estados de jogo: {config.GAME_STATE_MENU}, {config.GAME_STATE_PLAYING}")
    print(f"  ├─ Modos de jogo: {config.GAME_MODE_SINGLE}, {config.GAME_MODE_ARROW}")
    print(f"  └─ Escadas: {len(config.ESCALATOR_SPEEDS)} configuradas")
    print("✅ Configurações OK!\n")

def test_character_factory():
    """Testa a criação de personagens"""
    print("🔍 Testando fábrica de personagens...")
    from characters import load_assets, CharacterFactory
    
    assets = load_assets()
    print(f"  ├─ Bodies carregados: {len(assets['bodies'])}")
    print(f"  ├─ Faces carregadas: {len(assets['faces'])}")
    print(f"  ├─ Heads carregadas: {len(assets['heads'])}")
    print(f"  └─ Hats carregados: {len(assets['hats'])}")
    
    factory = CharacterFactory(assets)
    char = factory.create_random_character(100, 100)
    print(f"  ✅ Personagem criado em posição ({char.x}, {char.y})")
    print("✅ Fábrica de personagens OK!\n")

def test_game_modes():
    """Testa os modos de jogo"""
    print("🔍 Testando modos de jogo...")
    from game_modes import ArrowMode, CharacterMode
    from characters import load_assets, CharacterFactory
    
    print("  ├─ Criando ArrowMode...", end=" ")
    arrow = ArrowMode()
    print("✅")
    
    print("  ├─ Criando CharacterMode...", end=" ")
    assets = load_assets()
    factory = CharacterFactory(assets)
    char_mode = CharacterMode(factory)
    print("✅")
    
    print("  └─ Atualizando ArrowMode...", end=" ")
    arrow.update()
    print("✅")
    
    print("✅ Modos de jogo OK!\n")

def test_highscore():
    """Testa o sistema de highscores"""
    print("🔍 Testando sistema de highscores...")
    from highscore_manager import HighscoreManager
    
    manager = HighscoreManager()
    print(f"  ├─ Highscores carregados")
    print(f"  ├─ Modo Infinito: {len(manager.highscores.get('infinite', []))} pontuações")
    print(f"  └─ Modo Seta: {len(manager.highscores.get('arrow', []))} pontuações")
    print("✅ Sistema de highscores OK!\n")

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  VERIFICAÇÃO DA VERSÃO REFATORADA")
    print("  Memory Escalator v2.0")
    print("="*60 + "\n")
    
    # Testa imports
    if not test_imports():
        print("\n❌ Falha nos imports! Verifique os arquivos.\n")
        return
    
    # Testa componentes
    try:
        test_config()
        test_character_factory()
        test_game_modes()
        test_highscore()
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}\n")
        return
    
    # Sucesso!
    print("="*60)
    print("  ✅ TODOS OS TESTES PASSARAM!")
    print("  Pronto para jogar: python main.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
