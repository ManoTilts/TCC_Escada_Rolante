"""
Funções de renderização das telas do jogo
"""
import pygame
from config import *
import time


def draw_gradient_background(screen):
    """Desenha o fundo com gradiente"""
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(135 + (45 - 135) * ratio)
        g = int(206 + (85 - 206) * ratio)
        b = int(235 + (160 - 235) * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def draw_text_with_shadow(screen, text, font, color, x, y, shadow_color=(0, 0, 0)):
    """Desenha texto com sombra para melhor legibilidade"""
    # Sombra
    for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
        shadow = font.render(text, True, shadow_color)
        screen.blit(shadow, (x + dx, y + dy))
    
    # Texto principal
    main_text = font.render(text, True, color)
    screen.blit(main_text, (x, y))


def draw_menu(screen, buttons):
    """Desenha o menu principal"""
    draw_gradient_background(screen)
    
    # Título
    title_text = "Memory Escalator"
    title_x = WIDTH//2 - GAME_TITLE_FONT.size(title_text)[0]//2
    draw_text_with_shadow(screen, title_text, GAME_TITLE_FONT, (255, 255, 255), title_x, 50)
    
    # Subtítulo
    subtitle_text = "Jogo da Memória na Escada Rolante"
    subtitle_x = WIDTH//2 - GAME_SUBTITLE_FONT.size(subtitle_text)[0]//2
    draw_text_with_shadow(screen, subtitle_text, GAME_SUBTITLE_FONT, (255, 255, 255), subtitle_x, 120)
    
    # Linha decorativa
    pygame.draw.line(screen, (30, 50, 90), (WIDTH//2 - 200, 160), (WIDTH//2 + 200, 160), 2)
    
    # Instruções
    instructions = SMALL_FONT.render("Selecione o Modo de Jogo:", True, (255, 255, 255))
    screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 190))
    
    # Desenha os botões
    for button in buttons:
        button.draw(screen)
    
    # PS
    ps_text = "PS: Para descobrir mais sobre como jogar e os modos de jogo, clique em 'Como Jogar'"
    ps_render = TINY_FONT.render(ps_text, True, (200, 200, 200))
    screen.blit(ps_render, (WIDTH//2 - ps_render.get_width()//2, HEIGHT - 80))
    
    # Footer
    footer_text = "Pressione ESC para sair"
    footer = TINY_FONT.render(footer_text, True, (200, 200, 200))
    screen.blit(footer, (WIDTH//2 - footer.get_width()//2, HEIGHT - 40))


def draw_display_target(screen, target_character, game_mode, display_time, 
                        target_display_start, is_first_target, score):
    """Desenha a tela de exibição do alvo"""
    # Fundo branco para melhor visualização
    screen.fill((255, 255, 255))
    
    if game_mode == 0:  # SINGLE
        mode_text = "Modo Aparição Única"
    elif game_mode == 1:  # ALTERNATING
        mode_text = "Modo Alternado"
    else:  # INFINITE
        mode_text = "Modo Infinito"

    mode_render = SMALL_FONT.render(mode_text, True, (50, 50, 150))
    screen.blit(mode_render, (WIDTH//2 - mode_render.get_width()//2, 20))
    
    # Texto diferente para modo alternado
    if game_mode == 1 and not is_first_target:  # ALTERNATING
        memorize_text = GAME_TITLE_FONT.render("NOVO ALVO!", True, (220, 30, 30))
        subtitle_text = SMALL_FONT.render("Memorize o novo personagem", True, (0, 0, 0))
        screen.blit(subtitle_text, (WIDTH//2 - subtitle_text.get_width()//2, HEIGHT//4 + 60))
    else:
        memorize_text = GAME_TITLE_FONT.render("MEMORIZE", True, (0, 0, 0))
    screen.blit(memorize_text, (WIDTH//2 - memorize_text.get_width()//2, HEIGHT//4))
    
    # Desenha o personagem alvo
    if target_character:
        # Desenha um retângulo de fundo para destacar o personagem
        char_bg_rect = pygame.Rect(
            target_character.x - 10, 
            target_character.y - 10, 
            target_character.size + 20, 
            target_character.size + 20
        )
        pygame.draw.rect(screen, (240, 240, 240), char_bg_rect, border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), char_bg_rect, 3, border_radius=10)
        
        target_character.draw(screen)
    
    # Contagem regressiva
    if game_mode == 1 and not is_first_target:  # ALTERNATING
        countdown_text = "Continuando em:"
    else:
        countdown_text = "Iniciando em:"
    
    time_left = max(0, display_time - (time.time() - target_display_start))
    countdown = FONT.render(f"{countdown_text} {time_left:.1f}", True, (0, 0, 0))
    screen.blit(countdown, (WIDTH//2 - countdown.get_width()//2, HEIGHT*3//4))
    
    # Mostra pontuação atual no modo alternado
    if game_mode == 1 and score > 0:  # ALTERNATING
        score_text = SMALL_FONT.render(f"Pontuação atual: {score}", True, (0, 100, 0))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT*3//4 + 40))


def draw_playing_state(screen, escalators, game_mode, score, time_limit, start_time, 
                       target_traits, is_first_target=True):
    """Desenha o estado de jogo para modos com personagens"""
    # Desenha todas as escadas rolantes
    for escalator in escalators:
        escalator.draw(screen)
    
    # Barra de progresso de tempo
    time_left = max(0, time_limit - (time.time() - start_time))
    progress = time_left / time_limit if time_limit > 0 else 0

    progress_bar_width = WIDTH - 40
    progress_bar_height = 20
    progress_bar_x = 20
    progress_bar_y = 10
    
    pygame.draw.rect(screen, (100, 100, 100), 
                    (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height))
    
    if progress > 0.5:
        bar_color = (0, 180, 0)
    elif progress > 0.25:
        bar_color = (255, 215, 0)
    else:
        bar_color = (220, 30, 30)
    
    progress_width = int(progress_bar_width * progress)
    if progress_width > 0:
        pygame.draw.rect(screen, bar_color, 
                        (progress_bar_x, progress_bar_y, progress_width, progress_bar_height))
    
    pygame.draw.rect(screen, (50, 50, 50), 
                    (progress_bar_x, progress_bar_y, progress_bar_width, progress_bar_height), 2)
    
    # Texto de pontuação
    if game_mode == 0:  # SINGLE
        mode_text = "Encontre uma vez"
    elif game_mode == 1:  # ALTERNATING
        mode_text = f"Personagem alterna: {score} acertos"
    else:  # INFINITE
        mode_text = f"+5s por acerto"
    
    score_text = SMALL_FONT.render(f"Pontuação: {score} - {mode_text}", True, (0, 0, 0))
    screen.blit(score_text, (10, 40))
    
    # Mini personagem de lembrete (exceto no modo single)
    if game_mode != 0:  # not SINGLE
        reminder_text = TINY_FONT.render("Personagem Alvo:", True, (0, 0, 0))
        screen.blit(reminder_text, (10, 70))
        
        mini_size = int(CHARACTER_SIZE * 0.75)
        mini_segment_height = mini_size // 3
        
        body_img = pygame.transform.scale(target_traits["body"]["image"], 
                                         (mini_size, mini_segment_height))
        head_img = pygame.transform.scale(target_traits["head"]["image"], 
                                         (mini_size, mini_segment_height))
        face_img = pygame.transform.scale(target_traits["face"]["image"], 
                                         (mini_size, mini_segment_height))
        hat_img = pygame.transform.scale(target_traits["hat"]["image"], 
                                        (mini_size, mini_segment_height))
        
        mini_x, mini_y = 20, 90
        
        screen.blit(body_img, (mini_x, mini_y + mini_segment_height * 2))
        screen.blit(head_img, (mini_x, mini_y + mini_segment_height))
        screen.blit(face_img, (mini_x, mini_y + mini_segment_height))
        screen.blit(hat_img, (mini_x, mini_y))


def draw_name_input(screen, is_new_highscore, last_score, highscore_input, confirm_button):
    """Desenha a tela de entrada de nome"""
    draw_gradient_background(screen)
    
    if is_new_highscore:
        title = GAME_SUBTITLE_FONT.render("NOVO RECORDE!", True, GAME_GOLD)
        subtitle = SMALL_FONT.render(f"Você fez {last_score} pontos!", True, GAME_WHITE)
    else:
        title = GAME_SUBTITLE_FONT.render("Fim de Jogo", True, GAME_WHITE)
        subtitle = SMALL_FONT.render(f"Pontuação: {last_score}", True, GAME_WHITE)
    
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 60))
    
    prompt = SMALL_FONT.render("Digite seu nome:", True, GAME_WHITE)
    screen.blit(prompt, (WIDTH//2 - prompt.get_width()//2, HEIGHT//2 - 20))
    
    highscore_input.draw(screen)
    confirm_button.draw(screen)
    
    instruction = TINY_FONT.render("Pressione Enter ou clique em Salvar", 
                                   True, GAME_WHITE)
    screen.blit(instruction, (WIDTH//2 - instruction.get_width()//2, HEIGHT//2 + 150))


def draw_instructions(screen, back_button):
    """Desenha a tela de instruções"""
    draw_gradient_background(screen)
    
    title_text = "TUTORIAL - Como Jogar"
    title = INSTRUCTIONS_TITLE_FONT.render(title_text, True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
    
    sections = [
        {
            "title": "PASSO 1: MEMORIZE",
            "color": GAME_GOLD,
            "items": [
                "Um personagem aparecerá na tela por 4 segundos",
                "Observe TODAS as características: cabeça, rosto, corpo e chapéu", 
                "Memorize bem! Você precisará encontrá-lo depois"
            ]
        },
        {
            "title": "PASSO 2: PROCURE", 
            "color": GAME_GOLD,
            "items": [
                "Personagens começarão a descer pelas escadas rolantes",
                "Cada escada tem velocidade diferente (rápida, média, lenta)",
                "Encontre o personagem EXATO que você memorizou"
            ]
        },
        {
            "title": "PASSO 3: CLIQUE",
            "color": GAME_GOLD, 
            "items": [
                "Clique NO personagem correto quando ele aparecer",
                "Acertou = Pontos!",
                "Errou = Fim de jogo (exceto no modo infinito: -3s)"
            ]
        },
        {
            "title": "MODOS DISPONÍVEIS:",
            "color": GAME_LIGHT_BLUE,
            "items": [
                "APARIÇÃO ÚNICA: Encontre o personagem 1 vez (30 segundos)",
                "MODO ALTERNADO: Personagem muda a cada acerto (30 segundos)", 
                "MODO INFINITO: Continue encontrando, ganhe +5s por acerto!",
                "MODO SETA: 90 segundos fixos - máxima pontuação possível!"
            ]
        },
        {
            "title": "MODO SETA - REGRAS ESPECIAIS:",
            "color": GAME_LIGHT_BLUE,
            "items": [
                "Você tem EXATOS 90 segundos para pontuar o máximo possível",
                "A seta gira e muda de cor constantemente",
                "Clique no quadrante da mesma COR da seta",
                "TIMING É TUDO: Só vale quando a seta APONTA para o quadrante!",
                "Velocidade muda a cada acerto - mantenha o foco!"
            ]
        },
        {
            "title": "DICAS IMPORTANTES:",
            "color": GAME_GREEN,
            "items": [
                "Preste atenção nos DETALHES de cada parte do personagem",
                "Não clique muito rápido - observe bem antes de clicar",
                "Use ESC para voltar ao menu a qualquer momento",
                "No modo infinito: erro reduz tempo, acerto adiciona tempo"
            ]
        }
    ]
    
    y_pos = 100
    for section in sections:
        if section["title"].startswith("DICAS"):
            title_font = TINY_FONT
            item_font = TINY_FONT
            title_spacing = 24
            item_spacing = 18
            section_spacing = 10
        elif section["title"].startswith("MODO SETA"):
            title_font = SMALL_FONT
            item_font = TINY_FONT
            title_spacing = 30
            item_spacing = 20
            section_spacing = 12
        else:
            title_font = INSTRUCTIONS_TEXT_FONT
            item_font = SMALL_FONT
            title_spacing = 32
            item_spacing = 23
            section_spacing = 14
        
        title_text = title_font.render(section["title"], True, section["color"])
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, y_pos))
        y_pos += title_spacing
        
        if section["title"].startswith("PASSO"):
            pygame.draw.line(screen, section["color"], 
                           (WIDTH//2 - 250, y_pos), 
                           (WIDTH//2 + 250, y_pos), 3)
            y_pos += 12
        
        for item in section["items"]:
            if section["title"].startswith("MODOS"):
                item_text = item_font.render(item, True, GAME_SILVER)
            else:
                item_text = item_font.render(item, True, GAME_WHITE)
            
            item_x = WIDTH//2 - item_text.get_width()//2
            screen.blit(item_text, (item_x, y_pos))
            y_pos += item_spacing
        
        y_pos += section_spacing
    
    back_button.draw(screen)


def draw_highscores(screen, highscores, back_button):
    """Desenha a tela de highscores"""
    draw_gradient_background(screen)
    
    title_text = "Melhores Pontuações"
    title = HIGHSCORE_TITLE_FONT.render(title_text, True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
    
    left_x = WIDTH // 4
    right_x = WIDTH * 3 // 4
    
    # Modo Infinito
    mode_title_infinite = HIGHSCORE_TEXT_FONT.render("Modo Infinito", True, GAME_GOLD)
    screen.blit(mode_title_infinite, (left_x - mode_title_infinite.get_width()//2, 100))
    pygame.draw.line(screen, GAME_GOLD, (left_x - 120, 140), (left_x + 120, 140), 3)
    
    scores_infinite = highscores.get("infinite", [])
    y_pos_left = 160
    
    if not scores_infinite:
        no_scores = SMALL_FONT.render("Nenhuma pontuação ainda", True, GAME_WHITE)
        screen.blit(no_scores, (left_x - no_scores.get_width()//2, y_pos_left))
    else:
        for j, score_data in enumerate(scores_infinite[:5]):
            rank = f"{j+1}º"
            name = score_data["name"][:12]
            score = score_data["score"]
            
            if j == 0:
                color = GAME_GOLD
                medal = "🥇"
            elif j == 1:
                color = GAME_SILVER  
                medal = "🥈"
            elif j == 2:
                color = (205, 127, 50)
                medal = "🥉"
            else:
                color = GAME_WHITE
                medal = ""
            
            if j < 3:
                score_text = f"{medal} {rank} {name} - {score}"
            else:
                score_text = f"{rank} {name} - {score}"
            
            text_surf = SMALL_FONT.render(score_text, True, color)
            screen.blit(text_surf, (left_x - text_surf.get_width()//2, y_pos_left))
            y_pos_left += 40

    # Modo Seta
    mode_title_arrow = HIGHSCORE_TEXT_FONT.render("Modo Seta", True, GAME_LIGHT_BLUE)
    screen.blit(mode_title_arrow, (right_x - mode_title_arrow.get_width()//2, 100))
    pygame.draw.line(screen, GAME_LIGHT_BLUE, (right_x - 120, 140), (right_x + 120, 140), 3)
    
    scores_arrow = highscores.get("arrow", [])
    y_pos_right = 160
    
    if not scores_arrow:
        no_scores = SMALL_FONT.render("Nenhuma pontuação ainda", True, GAME_WHITE)
        screen.blit(no_scores, (right_x - no_scores.get_width()//2, y_pos_right))
    else:
        for j, score_data in enumerate(scores_arrow[:5]):
            rank = f"{j+1}º"
            name = score_data["name"][:12]
            score = score_data["score"]
            
            if j == 0:
                color = GAME_GOLD
                medal = "🥇"
            elif j == 1:
                color = GAME_SILVER  
                medal = "🥈"
            elif j == 2:
                color = (205, 127, 50)
                medal = "🥉"
            else:
                color = GAME_WHITE
                medal = ""
            
            if j < 3:
                score_text = f"{medal} {rank} {name} - {score}"
            else:
                score_text = f"{rank} {name} - {score}"
            
            text_surf = SMALL_FONT.render(score_text, True, color)
            screen.blit(text_surf, (right_x - text_surf.get_width()//2, y_pos_right))
            y_pos_right += 40
    
    back_button.draw(screen)
