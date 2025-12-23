import pygame
import sys
import math
import json
import os
from datetime import datetime
pygame.init()
monitor_info = pygame.display.Info()
SCREEN_WIDTH = monitor_info.current_w
SCREEN_HEIGHT = monitor_info.current_h
FPS = 60

class QuantumClicker:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Квантовый Кликер")
        self.clock = pygame.time.Clock()
        self.fullscreen = False
        try:
            icon_surface = pygame.Surface((32, 32))
            icon_surface.fill((100, 150, 255))
            pygame.display.set_icon(icon_surface)
        except:
            pass
        self.fonts = {
            'tiny': pygame.font.SysFont('Arial', 14),
            'small': pygame.font.SysFont('Arial', 18),
            'medium': pygame.font.SysFont('Arial', 24),
            'large': pygame.font.SysFont('Arial', 32),
            'title': pygame.font.SysFont('Arial', 42, bold=True),
            'huge': pygame.font.SysFont('Arial', 56, bold=True),
        }
        self.COLORS = {
            'bg_dark': (5, 10, 20),
            'bg_medium': (15, 20, 40),
            'bg_light': (25, 30, 60),
            'panel_dark': (20, 25, 50),
            'panel_medium': (30, 35, 70),
            'panel_light': (40, 45, 90),
            'text_bright': (230, 235, 255),
            'text_normal': (180, 190, 220),
            'text_dim': (130, 140, 180),
            'accent_blue': (80, 160, 255),
            'accent_cyan': (0, 200, 255),
            'accent_purple': (160, 100, 255),
            'accent_violet': (200, 120, 255),
            'accent_magenta': (255, 100, 200),
            'button_normal': (40, 50, 100),
            'button_hover': (60, 70, 130),
            'button_disabled': (30, 40, 80),
            'success': (0, 220, 150),
            'warning': (255, 200, 80),
            'danger': (255, 90, 120),
            'progress_blue': (60, 140, 255),
            'progress_purple': (140, 80, 255),
            'progress_bg': (30, 40, 80),
            'resource_quantum': (0, 180, 255),
            'resource_energy': (0, 255, 180),
            'resource_infinite': (180, 100, 255),
            'resource_eternity': (255, 100, 180),
            'resource_unity': (180, 140, 255),
        }
        self.init_save_system()
        self.reset_game_data()
        self.load_game()
        self.current_tab = 'main'
        self.notifications = []
        self.last_save_time = pygame.time.get_ticks()
        self.save_interval = 30000
        self.particles_buffer = []
        self.last_particle_time = 0

    def init_save_system(self):
        try:
            self.save_dir = os.path.join(os.path.expanduser("~"), "Documents", "QuantumClicker")
            os.makedirs(self.save_dir, exist_ok=True)
            self.save_file = os.path.join(self.save_dir, "save.json")
            self.backup_file = os.path.join(self.save_dir, "save_backup.json")
        except Exception as e:
            print(f"Ошибка: {e}")
            self.save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saves")
            os.makedirs(self.save_dir, exist_ok=True)
            self.save_file = os.path.join(self.save_dir, "save.json")
            self.backup_file = os.path.join(self.save_dir, "save_backup.json")

    def reset_game_data(self):
        self.quantum_particles = 0.0
        self.quantum_energy = 0.0
        self.infinite_points = 0
        self.eternity_points = 0
        self.unity_points = 0
        self.revolution_count = 0
        self.generators = {
            'Квантовый Источник': {'count': 0, 'base_cost': 10, 'base_rate': 0.1, 'unlocked': True},
            'Энергетическая Сфера': {'count': 0, 'base_cost': 100, 'base_rate': 1, 'unlocked': False},
            'Временная Петля': {'count': 0, 'base_cost': 1000, 'base_rate': 10, 'unlocked': False},
            'Сингулярность': {'count': 0, 'base_cost': 10000, 'base_rate': 100, 'unlocked': False},
            'Пространственный Разлом': {'count': 0, 'base_cost': 100000, 'base_rate': 1000, 'unlocked': False},
        }
        self.upgrades = {}
        self.init_upgrades()
        self.achievements = {}
        self.init_achievements()
        self.autoclickers = 0
        self.click_power = 1.0
        self.prestige_bonus = 1.0
        self.eternity_bonus = 1.0
        self.total_clicks = 0
        self.total_particles = 0.0
        self.start_time = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
        self.infinity_threshold = 1e6
        self.eternity_threshold = 1e12
        self.unity_threshold = 1e20
        self.infinity_unlocked = False
        self.eternity_unlocked = False
        self.unity_unlocked = False

    def init_upgrades(self):
        upgrades_data = [
            {'id': 1, 'name': 'Усиленный Щелчок', 'desc': 'Увеличивает силу щелчка на 1',
             'cost': 50, 'effect': 'click_power', 'value': 1.0, 'type': 'additive',
             'unlocked': True, 'max_level': 100, 'level': 0, 'bought': False},
            {'id': 2, 'name': 'Квантовый Множитель', 'desc': 'Удваивает генерацию частиц',
             'cost': 100, 'effect': 'particle_mult', 'value': 2.0, 'type': 'multiplicative',
             'unlocked': True, 'max_level': 10, 'level': 0, 'bought': False},
            {'id': 3, 'name': 'Автоматический Кликер', 'desc': 'Автоматически кликает 1 раз в секунду',
             'cost': 500, 'effect': 'autoclickers', 'value': 1, 'type': 'additive',
             'unlocked': True, 'max_level': 5, 'level': 0, 'bought': False},
        ]
        for upgrade in upgrades_data:
            self.upgrades[upgrade['id']] = upgrade

    def init_achievements(self):
        achievements_data = [
            {'id': 1, 'name': 'Первая Частица', 'desc': 'Собрать 1 квантовую частицу',
             'condition': lambda: self.total_particles >= 1, 'reward': 10, 'unlocked': False},
            {'id': 2, 'name': 'Начинающий Физик', 'desc': 'Собрать 100 частиц',
             'condition': lambda: self.total_particles >= 100, 'reward': 100, 'unlocked': False},
            {'id': 3, 'name': 'Квантовый Новачок', 'desc': 'Собрать 1000 частиц',
             'condition': lambda: self.total_particles >= 1000, 'reward': 1000, 'unlocked': False},
        ]
        for ach in achievements_data:
            ach['hidden'] = False
            self.achievements[ach['id']] = ach

    def save_game(self):
        try:
            save_data = {
                'version': '1.0',
                'basic': {
                    'quantum_particles': float(self.quantum_particles),
                    'quantum_energy': float(self.quantum_energy),
                    'infinite_points': int(self.infinite_points),
                    'eternity_points': int(self.eternity_points),
                    'unity_points': int(self.unity_points),
                    'revolution_count': int(self.revolution_count),
                    'total_clicks': int(self.total_clicks),
                    'total_particles': float(self.total_particles),
                    'click_power': float(self.click_power),
                    'autoclickers': int(self.autoclickers),
                    'prestige_bonus': float(self.prestige_bonus),
                    'eternity_bonus': float(self.eternity_bonus),
                },
                'generators': {},
                'upgrades': {},
                'achievements': {},
                'save_time': datetime.now().isoformat(),
            }
            for name, data in self.generators.items():
                save_data['generators'][name] = {
                    'count': data['count'],
                    'unlocked': data['unlocked']
                }
            for upgrade_id, upgrade in self.upgrades.items():
                save_data['upgrades'][str(upgrade_id)] = {
                    'level': upgrade['level'],
                    'bought': upgrade['bought']
                }
            for ach_id, ach in self.achievements.items():
                save_data['achievements'][str(ach_id)] = {
                    'unlocked': ach['unlocked']
                }
            temp_file = self.save_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            with open(temp_file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
            if os.path.exists(self.save_file):
                os.replace(self.save_file, self.backup_file)
            os.replace(temp_file, self.save_file)
            return True
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
            if os.path.exists(self.backup_file):
                try:
                    os.replace(self.backup_file, self.save_file)
                    return True
                except:
                    pass
            return False

    def load_game(self):
        try:
            if not os.path.exists(self.save_file):
                return True
            with open(self.save_file, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            if 'version' not in save_data:
                return False
            basic = save_data.get('basic', {})
            self.quantum_particles = float(basic.get('quantum_particles', 0))
            self.quantum_energy = float(basic.get('quantum_energy', 0))
            self.infinite_points = int(basic.get('infinite_points', 0))
            self.eternity_points = int(basic.get('eternity_points', 0))
            self.unity_points = int(basic.get('unity_points', 0))
            self.revolution_count = int(basic.get('revolution_count', 0))
            self.total_clicks = int(basic.get('total_clicks', 0))
            self.total_particles = float(basic.get('total_particles', 0))
            self.click_power = float(basic.get('click_power', 1.0))
            self.autoclickers = int(basic.get('autoclickers', 0))
            self.prestige_bonus = float(basic.get('prestige_bonus', 1.0))
            self.eternity_bonus = float(basic.get('eternity_bonus', 1.0))
            generators_data = save_data.get('generators', {})
            for name, data in self.generators.items():
                if name in generators_data:
                    self.generators[name]['count'] = generators_data[name].get('count', 0)
                    self.generators[name]['unlocked'] = generators_data[name].get('unlocked', data['unlocked'])
            upgrades_data = save_data.get('upgrades', {})
            for upgrade_id, upgrade in self.upgrades.items():
                str_id = str(upgrade_id)
                if str_id in upgrades_data:
                    upgrade['level'] = upgrades_data[str_id].get('level', 0)
                    upgrade['bought'] = upgrades_data[str_id].get('bought', False)
            achievements_data = save_data.get('achievements', {})
            for ach_id, ach in self.achievements.items():
                str_id = str(ach_id)
                if str_id in achievements_data:
                    ach['unlocked'] = achievements_data[str_id].get('unlocked', False)
            return True
        except json.JSONDecodeError as e:
            if os.path.exists(self.backup_file):
                try:
                    with open(self.backup_file, 'r', encoding='utf-8') as f:
                        backup_data = json.load(f)
                    os.replace(self.backup_file, self.save_file)
                    return self.load_game()
                except:
                    pass
            self.reset_game_data()
            return True
        except Exception as e:
            self.reset_game_data()
            return True

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    def format_number(self, num):
        if num == 0:
            return "0"
        suffixes = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No','UDc', 'DDc', 'TDc', 'QaDc', 'QiDc', 'SxDc', 'SpDc', 'ODc', 'NDc','Vg', 'UVg', 'DVg', 'TVg', 'QaVg', 'QiVg', 'SxVg', 'SpVg', 'OVg', 'NVg','Tg', 'UTg', 'DTg', 'TTg', 'QaTg', 'QiTg', 'SxTg', 'SpTg', 'OTg', 'NTg','Qd', 'UQd', 'DQd', 'TQd', 'QaQd', 'QiQd', 'SxQd', 'SpQd', 'OQd', 'NQd','Qt', 'UQt', 'DQt', 'TQt', 'QaQt', 'QiQt', 'SxQt', 'SpQt', 'OQt', 'NQt','Se', 'USe', 'DSe', 'TSe', 'QaSe', 'QiSe', 'SxSe', 'SpSe', 'OSe', 'NSe','St', 'USt', 'DSt', 'TSt', 'QaSt', 'QiSt', 'SxSt', 'SpSt', 'OSt', 'NSt','Og', 'UOg', 'DOg', 'TOg', 'QaOg', 'QiOg', 'SxOg', 'SpOg', 'OOg', 'NOg','Nn', 'UNn', 'DNn', 'TNn', 'QaNn', 'QiNn', 'SxNn', 'SpNn', 'ONn', 'NNn']
        if num < 1000:
            return f"{num:.1f}"
        magnitude = 0
        while abs(num) >= 1000 and magnitude < len(suffixes)-1:
            magnitude += 1
            num /= 1000.0
        return f"{num:.2f}{suffixes[magnitude]}"

    def format_percentage(self, num):
        if num == 0:
            return "0"
        suffixes = ['', 'K', 'M', 'B', 'T', 'Qa', 'Qi', 'Sx', 'Sp', 'Oc', 'No','UDc', 'DDc', 'TDc', 'QaDc', 'QiDc', 'SxDc', 'SpDc', 'ODc', 'NDc','Vg', 'UVg', 'DVg', 'TVg', 'QaVg', 'QiVg', 'SxVg', 'SpVg', 'OVg', 'NVg','Tg', 'UTg', 'DTg', 'TTg', 'QaTg', 'QiTg', 'SxTg', 'SpTg', 'OTg', 'NTg','Qd', 'UQd', 'DQd', 'TQd', 'QaQd', 'QiQd', 'SxQd', 'SpQd', 'OQd', 'NQd','Qt', 'UQt', 'DQt', 'TQt', 'QaQt', 'QiQt', 'SxQt', 'SpQt', 'OQt', 'NQt','Se', 'USe', 'DSe', 'TSe', 'QaSe', 'QiSe', 'SxSe', 'SpSe', 'OSe', 'NSe','St', 'USt', 'DSt', 'TSt', 'QaSt', 'QiSt', 'SxSt', 'SpSt', 'OSt', 'NSt','Og', 'UOg', 'DOg', 'TOg', 'QaOg', 'QiOg', 'SxOg', 'SpOg', 'OOg', 'NOg','Nn', 'UNn', 'DNn', 'TNn', 'QaNn', 'QiNn', 'SxNn', 'SpNn', 'ONn', 'NNn']
        if num < 1000:
            return f"{num:.1f}"
        magnitude = 0
        while abs(num) >= 1000 and magnitude < len(suffixes)-1:
            magnitude += 1
            num /= 1000.0
        return f"{num:.2f}{suffixes[magnitude]}"

    def create_button(self, x, y, width, height, text, enabled=True, hover=False, color=None):
        if not color:
            color = self.COLORS['button_hover'] if hover and enabled else self.COLORS['button_normal'] if enabled else self.COLORS['button_disabled']
        pygame.draw.rect(self.screen, color, (x, y, width, height), border_radius=8)
        border_color = self.COLORS['accent_blue'] if enabled else self.COLORS['text_dim']
        pygame.draw.rect(self.screen, border_color, (x, y, width, height), 2, border_radius=8)
        font = self.fonts['medium']
        text_color = self.COLORS['text_bright'] if enabled else self.COLORS['text_dim']
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=(x + width//2, y + height//2))
        self.screen.blit(text_surf, text_rect)
        return pygame.Rect(x, y, width, height)

    def create_panel(self, x, y, width, height, title="", alpha=230):
        panel_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        color1 = self.COLORS['panel_medium']
        color2 = self.COLORS['panel_light']
        for i in range(height):
            ratio = i / height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(panel_surface, (r, g, b, alpha), (0, i), (width, i))
        pygame.draw.rect(panel_surface, self.COLORS['accent_purple'], (0, 0, width, height), 2, border_radius=12)
        self.screen.blit(panel_surface, (x, y))
        if title:
            title_surf = self.fonts['medium'].render(title, True, self.COLORS['accent_cyan'])
            self.screen.blit(title_surf, (x + 15, y + 15))

    def draw_resource_bar(self, x, y, width, current, max_val, label, color):
        pygame.draw.rect(self.screen, self.COLORS['progress_bg'], (x, y, width, 25), border_radius=5)
        if max_val > 0 and current > 0:
            fill_width = min(width, width * (current / max_val))
            for i in range(int(fill_width)):
                r = min(255, color[0] + i // 50)
                g = min(255, color[1] + i // 50)
                b = min(255, color[2] + i // 50)
                pygame.draw.line(self.screen, (r, g, b), (x + i, y + 2), (x + i, y + 22))
        pygame.draw.rect(self.screen, color, (x, y, width, 25), 2, border_radius=5)
        # Создаем текст и выбираем шрифт в зависимости от длины
        text = f"{label}: {self.format_number(current)}"
        if max_val > 0:
            percent = (current / max_val * 100) if max_val > 0 else 100
            text += f" ({self.format_percentage(percent)}%)"
        # Проверяем, помещается ли текст в шкалу
        text_surf_small = self.fonts['small'].render(text, True, self.COLORS['text_bright'])
        if text_surf_small.get_width() > width - 10:  # Если текст слишком широкий, используем меньший шрифт
            text_surf = self.fonts['tiny'].render(text, True, self.COLORS['text_bright'])
        else:
            text_surf = text_surf_small
        text_rect = text_surf.get_rect(center=(x + width//2, y + 13))
        text_bg = pygame.Surface((text_surf.get_width() + 10, text_surf.get_height() + 4), pygame.SRCALPHA)
        text_bg.fill((0, 0, 0, 150))
        self.screen.blit(text_bg, (text_rect.x - 5, text_rect.y - 2))
        self.screen.blit(text_surf, text_rect)

    def show_main_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['huge'].render("КВАНТОВЫЙ КЛИКЕР", True, self.COLORS['accent_cyan'])
        subtitle = self.fonts['large'].render("Революция Бесконечности", True, self.COLORS['accent_purple'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 20))
        self.screen.blit(subtitle, (screen_width//2 - subtitle.get_width()//2, 90))

        # Кнопки вкладок - ПЕРЕМЕЩЕНЫ ВВЕРХ (над кликабельной кнопкой)
        tabs = [
            ('Генераторы', self.COLORS['accent_blue']),
            ('Улучшения', self.COLORS['success']),
            ('Бесконечность', self.COLORS['accent_purple']),
            ('Революции', self.COLORS['warning']),
            ('Достижения', self.COLORS['accent_magenta']),
            ('Настройки', self.COLORS['accent_violet'])
        ]
        tab_width = 170
        tab_height = 45
        tab_spacing = 8
        total_width = len(tabs) * tab_width + (len(tabs) - 1) * tab_spacing
        start_x = (screen_width - total_width) // 2
        tabs_y = 160  # Позиция вкладок - над кликабельной кнопкой
        for i, (tab_name, tab_color) in enumerate(tabs):
            tab_x = start_x + i * (tab_width + tab_spacing)
            tab_rect = pygame.Rect(tab_x, tabs_y, tab_width, tab_height)
            mouse_pos = pygame.mouse.get_pos()
            hover = tab_rect.collidepoint(mouse_pos)
            self.create_button(tab_x, tabs_y, tab_width, tab_height, tab_name, True, hover, tab_color)

        # Кликабельная кнопка - ПЕРЕМЕЩЕНА НИЖЕ вкладок
        click_size = min(screen_width, screen_height) // 4
        click_x = screen_width // 2 - click_size // 2
        click_y = tabs_y + tab_height + 40  # Кнопка начинается ниже вкладок
        self.create_panel(click_x - 15, click_y - 15, click_size + 30, click_size + 30, " ")
        pulse = (math.sin(pygame.time.get_ticks() * 0.001) + 1) * 0.5
        pulse_color = (
            int(100 + 155 * pulse),
            int(150 + 105 * pulse),
            int(255 + 0 * pulse)
        )
        click_rect = pygame.Rect(click_x, click_y, click_size, click_size)
        pygame.draw.rect(self.screen, pulse_color, click_rect, border_radius=20)
        pygame.draw.rect(self.screen, self.COLORS['text_bright'], click_rect, 3, border_radius=20)
        click_text = self.fonts['large'].render("ЖМИ!", True, self.COLORS['text_bright'])
        click_text_rect = click_text.get_rect(center=click_rect.center)
        self.screen.blit(click_text, click_text_rect)
        power_text = self.fonts['medium'].render(f"Сила: {self.format_number(self.click_power)}",
                                                True, self.COLORS['success'])
        power_rect = power_text.get_rect(center=(click_x + click_size//2, click_y + click_size + 25))
        self.screen.blit(power_text, power_rect)

        # Панель ресурсов - ПЕРЕМЕЩЕНА ЕЩЕ НИЖЕ, чтобы не перекрывать кнопку
        resources_y = click_y + click_size + 70  # Увеличено расстояние
        panel_height = 210
        self.create_panel(40, resources_y, screen_width-80, panel_height, "Ресурсы")
        resources_start_y = resources_y + 50
        resources = [
            ("Квантовые Частицы", self.quantum_particles, self.COLORS['resource_quantum'], self.infinity_threshold),
            ("Квантовая Энергия", self.quantum_energy, self.COLORS['resource_energy'], 0),
            ("Очки Бесконечности", self.infinite_points, self.COLORS['resource_infinite'], 0),
            ("Очки Вечности", self.eternity_points, self.COLORS['resource_eternity'], 0),
            ("Очки Единства", self.unity_points, self.COLORS['resource_unity'], 0),
        ]
        for i, (label, value, color, max_val) in enumerate(resources):
            y_pos = resources_start_y + i * 32
            self.draw_resource_bar(60, y_pos, screen_width-120, value, max_val, label, color)

    def show_generators_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("КВАНТОВЫЕ ГЕНЕРАТОРЫ", True, self.COLORS['accent_blue'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        y_offset = 120
        for name, data in self.generators.items():
            if y_offset + 90 > screen_height - 100:
                break
            if not data['unlocked']:
                self.create_panel(60, y_offset, screen_width-120, 80, name + " - Заблокировано")
                locked_text = self.fonts['small'].render("Разблокируется при прогрессе",
                                                        True, self.COLORS['text_dim'])
                self.screen.blit(locked_text, (80, y_offset + 50))
                y_offset += 90
                continue
            cost = data['base_cost'] * (1.15 ** data['count'])
            can_afford = self.quantum_particles >= cost
            income = data['count'] * data['base_rate'] * self.prestige_bonus
            self.create_panel(60, y_offset, screen_width-120, 80, name)
            count_text = self.fonts['small'].render(f"Количество: {data['count']}",
                                                    True, self.COLORS['text_normal'])
            self.screen.blit(count_text, (80, y_offset + 35))
            income_text = self.fonts['tiny'].render(f"Доход: {self.format_number(income)}/сек",
                                                   True, self.COLORS['success'])
            self.screen.blit(income_text, (80, y_offset + 60))
            cost_text = f"{self.format_number(cost)} частиц"
            cost_color = self.COLORS['success'] if can_afford else self.COLORS['danger']
            cost_surf = self.fonts['small'].render(cost_text, True, cost_color)
            self.screen.blit(cost_surf, (screen_width-240, y_offset + 15))
            btn_text = "КУПИТЬ" if can_afford else "НЕДОСТАТОЧНО"
            btn_color = self.COLORS['accent_blue'] if can_afford else self.COLORS['button_disabled']
            btn_rect = self.create_button(screen_width-240, y_offset + 35, 150, 35,
                                       btn_text, can_afford, False, btn_color)
            y_offset += 90

    def show_upgrades_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("УЛУЧШЕНИЯ", True, self.COLORS['success'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        y_offset = 120
        for upgrade_id, upgrade in self.upgrades.items():
            if y_offset + 90 > screen_height - 100:
                break
            if not upgrade.get('unlocked', False):
                continue
            can_afford = self.quantum_particles >= upgrade['cost']
            max_level = upgrade.get('max_level', 1)
            maxed = max_level > 0 and upgrade['level'] >= max_level
            self.create_panel(60, y_offset, screen_width-120, 80,
                           upgrade['name'] + f" (Уровень {upgrade['level']})")
            desc = self.fonts['tiny'].render(upgrade['desc'], True, self.COLORS['text_normal'])
            self.screen.blit(desc, (80, y_offset + 35))
            if maxed:
                max_text = self.fonts['small'].render("МАКСИМАЛЬНЫЙ УРОВЕНЬ",
                                                     True, self.COLORS['success'])
                self.screen.blit(max_text, (screen_width-240, y_offset + 35))
            else:
                cost_text = f"{self.format_number(upgrade['cost'])} частиц"
                cost_color = self.COLORS['success'] if can_afford else self.COLORS['danger']
                cost_surf = self.fonts['small'].render(cost_text, True, cost_color)
                self.screen.blit(cost_surf, (screen_width-240, y_offset + 15))
                btn_text = "КУПИТЬ" if can_afford else "НЕДОСТАТОЧНО"
                btn_color = self.COLORS['warning'] if can_afford else self.COLORS['button_disabled']
                btn_rect = self.create_button(screen_width-240, y_offset + 35, 150, 35,
                                           btn_text, can_afford, False, btn_color)
            y_offset += 90

    def show_infinity_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("БЕСКОНЕЧНОСТЬ", True, self.COLORS['accent_purple'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        info_y = 120
        info_sections = [
            ("БЕСКОНЕЧНОСТЬ", [
                f"Очки бесконечности: {self.infinite_points}",
                f"Бонус к генерации: +{self.infinite_points * 0.01:.2f}%",
                f"Следующее очко: {self.format_number(self.infinity_threshold)} частиц"
            ], self.COLORS['accent_purple']),
            ("ВЕЧНОСТЬ", [
                f"Очки вечности: {self.eternity_points}",
                f"Множитель кликов: x{self.eternity_bonus:.2f}",
                f"Требуется: 100 очков бесконечности"
            ], self.COLORS['accent_violet']),
            ("ЕДИНСТВО", [
                f"Очки единства: {self.unity_points}",
                f"Скидка: {self.unity_points * 2:.2f}%",
                f"Требуется: 1e20 частиц"
            ], self.COLORS['accent_magenta'])
        ]
        for section_title, lines, color in info_sections:
            title_surf = self.fonts['large'].render(section_title, True, color)
            self.screen.blit(title_surf, (60, info_y))
            info_y += 35
            for line in lines:
                line_surf = self.fonts['small'].render(line, True, self.COLORS['text_normal'])
                self.screen.blit(line_surf, (80, info_y))
                info_y += 25
            info_y += 15
        button_y = screen_height - 170
        if self.quantum_particles >= self.infinity_threshold:
            btn_rect = self.create_button(screen_width//2 - 180, button_y, 360, 50,
                                       "ДОСТИГНУТЬ БЕСКОНЕЧНОСТИ", True, False,
                                       self.COLORS['accent_purple'])
            button_y += 60
        if self.infinite_points >= 100:
            btn_rect = self.create_button(screen_width//2 - 180, button_y, 360, 50,
                                       "ВОЙТИ В ВЕЧНОСТЬ", True, False,
                                       self.COLORS['accent_violet'])

    def show_revolutions_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("РЕВОЛЮЦИИ", True, self.COLORS['warning'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        revolution_threshold = self.get_revolution_threshold()
        info_y = 120
        info_lines = [
            f"Совершено революций: {self.revolution_count}",
            f"Текущий множитель: x{self.prestige_bonus:.2f}",
            f"Требуется для следующей: {self.format_number(revolution_threshold)} частиц",
            f"Прогресс: {min(100, (self.quantum_particles / revolution_threshold) * 100):.1f}%",
            "",
            "Революция сбрасывает:",
            "  • Все частицы и энергию",
            "  • Все генераторы",
            "  • Обычные улучшения",
            "",
            "Революция сохраняет:",
            f"  • Очки бесконечности ({self.infinite_points})",
            f"  • Очки вечности ({self.eternity_points})",
            f"  • Очки единства ({self.unity_points})",
            f"  • Революции ({self.revolution_count})",
        ]
        for line in info_lines:
            color = self.COLORS['text_normal']
            line_surf = self.fonts['small'].render(line, True, color)
            self.screen.blit(line_surf, (60, info_y))
            info_y += 25
        if self.quantum_particles >= revolution_threshold:
            btn_rect = self.create_button(screen_width//2 - 180, screen_height - 170,
                                       360, 60, "СОВЕРШИТЬ РЕВОЛЮЦИЮ!", True, False,
                                       self.COLORS['danger'])

    def show_achievements_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("ДОСТИЖЕНИЯ", True, self.COLORS['accent_magenta'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        ach_size = 230
        margin = 15
        ach_per_row = min(3, (screen_width - 80) // (ach_size + margin))
        start_x = (screen_width - (ach_per_row * (ach_size + margin) - margin)) // 2
        start_y = 120
        for ach_id, ach in self.achievements.items():
            row = (ach_id - 1) // ach_per_row
            col = (ach_id - 1) % ach_per_row
            x = start_x + col * (ach_size + margin)
            y = start_y + row * (ach_size + margin)
            if y + ach_size > screen_height - 100:
                continue
            self.create_panel(x, y, ach_size, ach_size)
            name_surf = self.fonts['medium'].render(ach['name'], True,
                                                   self.COLORS['text_bright'] if ach['unlocked'] else self.COLORS['text_dim'])
            self.screen.blit(name_surf, (x + ach_size//2 - name_surf.get_width()//2, y + 25))
            desc_surf = self.fonts['tiny'].render(ach['desc'], True, self.COLORS['text_dim'])
            self.screen.blit(desc_surf, (x + ach_size//2 - desc_surf.get_width()//2, y + ach_size//2))
            if ach['unlocked']:
                status = f"Награда: +{self.format_number(ach['reward'])} энергии"
                status_color = self.COLORS['success']
            else:
                status = "Не разблокировано"
                status_color = self.COLORS['text_dim']
            status_surf = self.fonts['small'].render(status, True, status_color)
            self.screen.blit(status_surf, (x + ach_size//2 - status_surf.get_width()//2, y + ach_size - 45))

    def show_settings_tab(self):
        screen_width, screen_height = self.screen.get_size()
        title = self.fonts['title'].render("НАСТРОЙКИ", True, self.COLORS['accent_violet'])
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 30))
        self.create_panel(40, 100, screen_width-80, screen_height-180)
        back_rect = self.create_button(20, screen_height - 70, 140, 45, "На главную", True)
        settings_y = 120
        settings = [
            ("Полноэкранный режим",
             "Выйти из полноэкранного режима" if self.fullscreen else "Включить полноэкранный режим",
             self.COLORS['accent_blue']),
            ("Сохранить игру", "Сохранить текущий прогресс", self.COLORS['success']),
            ("Загрузить игру", "Загрузить последнее сохранение", self.COLORS['warning']),
            ("Сбросить прогресс", "Начать новую игру", self.COLORS['danger']),
        ]
        for i, (title_text, button_text, color) in enumerate(settings):
            title_surf = self.fonts['small'].render(title_text, True, self.COLORS['text_normal'])
            self.screen.blit(title_surf, (60, settings_y))
            btn_x = screen_width - 430
            btn_rect = self.create_button(btn_x, settings_y - 8, 375, 45, button_text, True, False, color)
            settings_y += 70
        info_y = settings_y + 15
        info_lines = [
            f"Папка сохранений: {os.path.basename(self.save_dir)}",
            f"Последнее сохранение: {self.get_last_save_time()}",
            "",
            "Управление:",
            "• F11 - Полноэкранный режим",
            "• ESC - Выход из игры",
            "• Ctrl+S - Быстрое сохранение",
            "• Ctrl+L - Быстрая загрузка",
            "• Пробел - Быстрый щелчок",
            "• ЛКМ - Взаимодействие",
        ]
        for line in info_lines:
            if line == "Управление:":
                color = self.COLORS['accent_cyan']
            elif line.startswith("•"):
                color = self.COLORS['text_dim']
            else:
                color = self.COLORS['text_normal']
            line_surf = self.fonts['tiny'].render(line, True, color)
            self.screen.blit(line_surf, (60, info_y))
            info_y += 22

    def get_last_save_time(self):
        try:
            if os.path.exists(self.save_file):
                mtime = os.path.getmtime(self.save_file)
                return datetime.fromtimestamp(mtime).strftime("%H:%M:%S")
        except:
            pass
        return "Никогда"

    def get_revolution_threshold(self):
        base = 1e15
        return base * (10 ** min(self.revolution_count, 10))

    def update_background(self):
        self.screen.fill(self.COLORS['bg_dark'])
        current_time = pygame.time.get_ticks()
        for i in range(50):
            x = (current_time * 0.02 + i * 73) % SCREEN_WIDTH
            y = (math.sin(current_time * 0.001 + i * 0.5) * 100 + i * 40) % SCREEN_HEIGHT
            size = 1 + math.sin(current_time * 0.003 + i) * 0.5
            color_choice = [
                (60, 100, 255, 100),
                (120, 80, 255, 80),
                (180, 60, 255, 60),
                (100, 150, 255, 120)
            ]
            color = color_choice[i % len(color_choice)]
            particle = pygame.Surface((int(size*4), int(size*4)), pygame.SRCALPHA)
            pygame.draw.circle(particle, color, (int(size*2), int(size*2)), int(size*2))
            self.screen.blit(particle, (int(x), int(y)))

    def draw_interface(self):
        self.update_background()
        # Отображение "Частиц/сек" в левом верхнем углу
        pps = self.get_particles_per_second()
        pps_text = self.fonts['small'].render(f"Частиц/сек: {self.format_number(pps)}", True, self.COLORS['success'])
        self.screen.blit(pps_text, (10, 10))

        screen_width, screen_height = self.screen.get_size()
        screen_width, screen_height = self.screen.get_size()
        tabs_functions = {
            'main': self.show_main_tab,
            'generators': self.show_generators_tab,
            'upgrades': self.show_upgrades_tab,
            'infinity': self.show_infinity_tab,
            'revolutions': self.show_revolutions_tab,
            'achievements': self.show_achievements_tab,
            'settings': self.show_settings_tab
        }
        if self.current_tab in tabs_functions:
            tabs_functions[self.current_tab]()
        current_time = pygame.time.get_ticks()
        self.notifications = [(text, created_time) for text, created_time in self.notifications
                            if current_time - created_time < 5000]
        for i, (notification, created_time) in enumerate(self.notifications[:3]):
            time_left = 5000 - (current_time - created_time)
            alpha = min(255, int(time_left / 5000 * 255))
            notif_surf = self.fonts['small'].render(notification, True, self.COLORS['text_bright'])
            bg_width = notif_surf.get_width() + 20
            bg_height = notif_surf.get_height() + 10
            bg = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
            bg_color = (0, 0, 0, alpha * 0.7)
            pygame.draw.rect(bg, bg_color, (0, 0, bg_width, bg_height), border_radius=5)
            pygame.draw.rect(bg, (self.COLORS['accent_blue'][0], self.COLORS['accent_blue'][1],
                                self.COLORS['accent_blue'][2], alpha),
                           (0, 0, bg_width, bg_height), 1, border_radius=5)
            self.screen.blit(bg, (screen_width - bg_width - 20, 10 + i * 35))
            text_color = (self.COLORS['text_bright'][0], self.COLORS['text_bright'][1],
                         self.COLORS['text_bright'][2], alpha)
            notif_surf = self.fonts['small'].render(notification, True, text_color)
            self.screen.blit(notif_surf, (screen_width - notif_surf.get_width() - 30,
                                        15 + i * 35))
        pygame.display.flip()

    def add_notification(self, text):
        self.notifications.append((text, pygame.time.get_ticks()))
        if len(self.notifications) > 10:
            self.notifications.pop(0)

    def get_particles_per_second(self):
        total = 0
        for name, data in self.generators.items():
            if data['unlocked']:
                total += data['count'] * data['base_rate']
        total *= self.prestige_bonus
        total *= (1 + self.infinite_points * 0.01)
        return total

    def add_particles(self, amount):
        self.quantum_particles += amount * self.prestige_bonus * self.eternity_bonus
        self.total_particles += amount
        current_time = pygame.time.get_ticks()
        if current_time - self.last_particle_time > 100:
            screen_width, screen_height = self.screen.get_size()
            self.particles_buffer.append({
                'x': screen_width // 2,
                'y': screen_height // 2 + 50,
                'text': f"+{self.format_number(amount)}",
                'time': current_time,
                'color': self.COLORS['accent_cyan']
            })
            self.last_particle_time = current_time

    def check_achievements(self):
        for ach_id, ach in self.achievements.items():
            if not ach['unlocked'] and ach['condition']():
                ach['unlocked'] = True
                self.quantum_energy += ach['reward']
                self.add_notification(f"ДОСТИЖЕНИЕ: {ach['name']}!")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game()
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.save_game()
                    return False
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                    self.add_notification("Режим экрана изменен")
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if self.save_game():
                        self.add_notification("Игра сохранена!")
                elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    if self.load_game():
                        self.add_notification("Игра загружена!")
                elif event.key == pygame.K_SPACE:
                    self.add_particles(self.click_power)
                    self.total_clicks += 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.handle_click(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
        return True

    def handle_click(self, pos):
        screen_width, screen_height = self.screen.get_size()
        if self.current_tab == 'main':
            # Проверка клика по основной кнопке
            click_size = min(screen_width, screen_height) // 4
            click_x = screen_width // 2 - click_size // 2
            click_y = 160 + 45 + 40  # tabs_y + tab_height + 40
            click_rect = pygame.Rect(click_x, click_y, click_size, click_size)
            if click_rect.collidepoint(pos):
                self.add_particles(self.click_power)
                self.total_clicks += 1
                return True
            # Проверка клика по кнопкам вкладок
            tabs = ['Генераторы', 'Улучшения', 'Бесконечность', 'Революции', 'Достижения', 'Настройки']
            tab_width = 150
            tab_height = 45
            tab_spacing = 8
            total_width = len(tabs) * tab_width + (len(tabs) - 1) * tab_spacing
            start_x = (screen_width - total_width) // 2
            tabs_y = 160  # Позиция вкладок
            for i, tab in enumerate(tabs):
                tab_x = start_x + i * (tab_width + tab_spacing)
                tab_rect = pygame.Rect(tab_x, tabs_y, tab_width, tab_height)
                if tab_rect.collidepoint(pos):
                    tab_mapping = {
                        'Генераторы': 'generators',
                        'Улучшения': 'upgrades',
                        'Бесконечность': 'infinity',
                        'Революции': 'revolutions',
                        'Достижения': 'achievements',
                        'Настройки': 'settings'
                    }
                    self.current_tab = tab_mapping[tab]
                    return True
        if self.current_tab != 'main':
            back_rect = pygame.Rect(20, screen_height - 70, 140, 45)
            if back_rect.collidepoint(pos):
                self.current_tab = 'main'
                return True
        tab_handlers = {
            'generators': self.handle_generators_click,
            'upgrades': self.handle_upgrades_click,
            'infinity': self.handle_infinity_click,
            'revolutions': self.handle_revolutions_click,
            'settings': self.handle_settings_click
        }
        if self.current_tab in tab_handlers:
            return tab_handlers[self.current_tab](pos)
        return False

    def handle_generators_click(self, pos):
        screen_width = self.screen.get_width()
        y_offset = 120
        for name, data in self.generators.items():
            if not data['unlocked']:
                y_offset += 90
                continue
            btn_rect = pygame.Rect(screen_width-240, y_offset + 35, 150, 35)
            if btn_rect.collidepoint(pos):
                cost = data['base_cost'] * (1.15 ** data['count'])
                if self.quantum_particles >= cost:
                    self.quantum_particles -= cost
                    data['count'] += 1
                    self.add_notification(f"Приобретен {name}!")
                return True
            y_offset += 90
        return False

    def handle_upgrades_click(self, pos):
        screen_width = self.screen.get_width()
        y_offset = 130
        for upgrade_id, upgrade in self.upgrades.items():
            if not upgrade.get('unlocked', False):
                y_offset += 90
                continue
            max_level = upgrade.get('max_level', 1)
            maxed = max_level > 0 and upgrade['level'] >= max_level
            if not maxed:
                btn_rect = pygame.Rect(screen_width-240, y_offset + 35, 150, 35)
                if btn_rect.collidepoint(pos):
                    self.buy_upgrade(upgrade_id)
                    return True
            y_offset += 90
        return False

    def handle_infinity_click(self, pos):
        screen_width, screen_height = self.screen.get_size()
        if self.quantum_particles >= self.infinity_threshold:
            btn_rect = pygame.Rect(screen_width//2 - 180, screen_height - 170, 360, 50)
            if btn_rect.collidepoint(pos):
                self.perform_infinity_reset()
                return True
        if self.infinite_points >= 100:
            btn_rect = pygame.Rect(screen_width//2 - 180, screen_height - 110, 360, 50)
            if btn_rect.collidepoint(pos):
                self.perform_eternity_reset()
                return True
        return False

    def handle_revolutions_click(self, pos):
        screen_width, screen_height = self.screen.get_size()
        if self.quantum_particles >= self.get_revolution_threshold():
            btn_rect = pygame.Rect(screen_width//2 - 180, screen_height - 170, 360, 60)
            if btn_rect.collidepoint(pos):
                self.perform_revolution()
                return True
        return False

    def handle_settings_click(self, pos):
        screen_width = self.screen.get_width()
        settings_y = 120
        btn_rect = pygame.Rect(screen_width - 320, settings_y - 8, 240, 45)
        if btn_rect.collidepoint(pos):
            self.toggle_fullscreen()
            self.add_notification("Режим экрана изменен")
            return True
        btn_rect = pygame.Rect(screen_width - 320, settings_y + 62, 240, 45)
        if btn_rect.collidepoint(pos):
            if self.save_game():
                self.add_notification("Игра сохранена!")
            return True
        btn_rect = pygame.Rect(screen_width - 320, settings_y + 132, 240, 45)
        if btn_rect.collidepoint(pos):
            if self.load_game():
                self.add_notification("Игра загружена!")
            return True
        btn_rect = pygame.Rect(screen_width - 320, settings_y + 202, 240, 45)
        if btn_rect.collidepoint(pos):
            self.reset_game_data()
            self.add_notification("Прогресс сброшен!")
            return True
        return False

    def buy_upgrade(self, upgrade_id):
        upgrade = self.upgrades[upgrade_id]
        if self.quantum_particles < upgrade['cost']:
            self.add_notification("Недостаточно ресурсов!")
            return
        max_level = upgrade.get('max_level', 1)
        if max_level > 0 and upgrade['level'] >= max_level:
            self.add_notification("Достигнут максимальный уровень!")
            return
        self.quantum_particles -= upgrade['cost']
        if upgrade['effect'] == 'click_power':
            self.click_power += upgrade['value']
        elif upgrade['effect'] == 'particle_mult':
            self.prestige_bonus *= upgrade['value']
        elif upgrade['effect'] == 'autoclickers':
            self.autoclickers += upgrade['value']
        upgrade['level'] += 1
        upgrade['bought'] = True
        upgrade['cost'] *= 2.5
        self.add_notification(f"Улучшение '{upgrade['name']}' приобретено!")

    def perform_infinity_reset(self):
        if self.quantum_particles < self.infinity_threshold:
            return
        infinite_gained = max(1, int(self.quantum_particles / self.infinity_threshold))
        self.infinite_points += infinite_gained
        self.quantum_particles = 0
        self.quantum_energy = 0
        for gen in self.generators.values():
            gen['count'] = 0
        for upgrade in self.upgrades.values():
            if upgrade.get('currency') not in ['infinite_points', 'eternity_points', 'unity_points']:
                upgrade['level'] = 0
                upgrade['bought'] = False
        self.infinity_threshold *= 2
        self.infinity_unlocked = True
        self.add_notification(f"Бесконечность достигнута! +{infinite_gained} очков")

    def perform_eternity_reset(self):
        if self.infinite_points < 100:
            return
        eternity_gained = max(1, int(self.infinite_points / 100))
        self.eternity_points += eternity_gained
        self.infinite_points = 0
        self.eternity_bonus *= 1.5
        self.eternity_unlocked = True
        self.add_notification(f"Вечность достигнута! +{eternity_gained} очков")

    def perform_revolution(self):
        revolution_threshold = self.get_revolution_threshold()
        if self.quantum_particles < revolution_threshold:
            return
        self.revolution_count += 1
        self.prestige_bonus *= 10
        self.quantum_particles = 0
        self.quantum_energy = 0
        for gen in self.generators.values():
            gen['count'] = 0
        for upgrade in self.upgrades.values():
            if upgrade.get('currency') not in ['infinite_points', 'eternity_points', 'unity_points', 'revolution_count']:
                upgrade['level'] = 0
                upgrade['bought'] = False
        self.add_notification(f"Революция #{self.revolution_count} совершена!")

    def update_game_state(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.last_update) / 1000.0
        self.last_update = current_time
        pps = self.get_particles_per_second()
        self.add_particles(pps * delta_time)
        if self.autoclickers > 0:
            self.add_particles(self.click_power * self.autoclickers * delta_time)
            self.total_clicks += self.autoclickers * delta_time
        self.check_achievements()
        if current_time - self.last_save_time > self.save_interval:
            self.save_game()
            self.last_save_time = current_time
        self.particles_buffer = [anim for anim in self.particles_buffer
                               if current_time - anim['time'] < 1000]

    def run_game_loop(self):
        running = True
        while running:
            running = self.handle_events()
            if running:
                self.update_game_state()
                self.draw_interface()
                self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = QuantumClicker()
    game.run_game_loop()
