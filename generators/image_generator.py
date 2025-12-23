from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import io
import os


class StatsImageGenerator:
    
    def __init__(self):
        self.width = 1600
        self.height = 900
        self.bg_color = (30, 30, 40)
        self.primary_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.accent_color = (255, 200, 50)
        self.divider_color = (255, 234, 0)
        self.mode_color = (255, 234, 0)
        
        self.mode_names = {
            'BW': 'BedWars',
            'Duels': 'Duels'
        }
        
        self.rank_colors = {
            'default': (128, 128, 128),
            'IRON': (144, 238, 144),
            'GOLD': (255, 165, 0),
            'DELUXE': (173, 216, 230),
            'MASTER': (255, 0, 0),
            'RUBIUM': (139, 0, 0),
            'ULTRA': (255, 192, 203),
            'SPONSOR': (0, 100, 0),
            'YOUTUBE': None,
            'BETA': (128, 128, 128),
            'BUILD': (0, 128, 0),
            'HELPER': (128, 128, 128),
            'MODERATOR': (128, 128, 128),
            'SR_MODER': (0, 0, 139),
            'HEAD_MODERATOR': (0, 0, 139),
            'AX_TEAM': (128, 0, 128),
            'ADMINISTRATOR': (255, 0, 0),
            'DEVELOPER': (255, 255, 255),
            'OWNER': (139, 0, 0),
        }
        self.background_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "fon.jpg"
        )
        
        self.title_y = 200
        self.mode_y = 265
        self.divider_y = 324
        self.stats_start_y = 381
        self.margin_left = 50
        self.margin_right = 50
        self.line_height = 38
        self.stats_x_left = 80
        self.stats_x_right = None
        self.label_width = 250
        self.value_offset = 150
        self.footer_y_offset = 30
        
    def _get_font(self, size: int):
        try:
            if os.name == 'nt':
                font_path = "Unbounded-Regular.ttf"
            else:
                font_path = "Unbounded-Regular.ttf"
            
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            pass
        
        return ImageFont.load_default()

    def _create_canvas(self, width: int, height: int) -> Image.Image:
        try:
            if os.path.exists(self.background_path):
                background = Image.open(self.background_path).convert("RGB")
                if hasattr(Image, "Resampling"):
                    background = background.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    background = background.resize((width, height), Image.ANTIALIAS)
                return background
        except Exception as e:
            print(f"Ошибка загрузки фонового изображения: {e}")
        return Image.new('RGB', (width, height), color=self.bg_color)
    
    def _get_mode_name(self, mode: str) -> str:
        mode_upper = mode.upper()
        return self.mode_names.get(mode_upper, mode_upper)
    
    def _remove_minecraft_formatting(self, text: str) -> str:
        if not text:
            return text
        
        import re
        return re.sub(r'§[0-9a-fA-Fk-oK-OrR]', '', text)
    
    def _format_rank_name(self, rank_name: str) -> str:
        if not rank_name:
            return rank_name
        
        if rank_name.upper() == 'AX_TEAM':
            return 'TEAM'
        
        return rank_name
    
    def _get_rank_color(self, rank_name: str) -> tuple:
        if not rank_name:
            return self.text_color
        
        rank_upper = rank_name.upper()
        return self.rank_colors.get(rank_upper, self.text_color)
    
    def _format_stat_label(self, key: str) -> str:
        translations = {
            'wins': 'Побед',
            'losses': 'Поражений',
            'kills': 'Убийств',
            'deaths': 'Смертей',
            'games': 'Игр',
            'winstreak': 'Серия побед',
            'best_winstreak': 'Лучшая серия',
            'kd': 'K/D',
            'wl': 'W/L',
            'level': 'Уровень',
            'exp': 'Опыт',
            'experience': 'Опыт',
            'coins': 'Монеты',
            'final_kills': 'Финальных убийств',
            'final_deaths': 'Финальных смертей',
            'beds_broken': 'Разрушенных кроватей',
            'beds_lost': 'Потерянных кроватей',
            'beds': 'Кроватей',
            'playtime': 'Время игры',
            'winrate': 'Процент побед',
            'top_gold': 'Топ золота',
            'blocks_placed': 'Блоков поставлено',
            'top_iron': 'Топ железа',
            'bow_hits': 'Попаданий из лука',
            'bow_shots': 'Выстрелов из лука',
            'blocks_traveled': 'Блоков пройдено',
            'day': 'День',
            'blocks_broken': 'Блоков разрушено'
        }
        
        if key.lower() in translations:
            return translations[key.lower()]
        
        formatted = key.replace('_', ' ').title()
        return formatted
    
    def generate(self, player_name: str, mode: str, stats_data: Dict, rank: str = None) -> Optional[io.BytesIO]:
        try:
            print(f"DEBUG: stats_data type: {type(stats_data)}")
            if isinstance(stats_data, dict):
                print(f"DEBUG: stats_data keys: {list(stats_data.keys())}")
                for key, value in stats_data.items():
                    print(f"DEBUG: {key} = {value} (type: {type(value)})")
            
            img = self._create_canvas(self.width, self.height)
            draw = ImageDraw.Draw(img)
            
            title_font = self._get_font(48)
            header_font = self._get_font(32)
            text_font = self._get_font(24)
            small_font = self._get_font(16)
            
            mode_name = self._get_mode_name(mode)
            mode_prefix = "Режим: "
            
            if rank:
                rank = self._remove_minecraft_formatting(rank)
                rank_display = self._format_rank_name(rank)
                rank_color = self._get_rank_color(rank)
                
                if rank_display.upper() == 'YOUTUBE':
                    prefix = "Статистика игрока "
                    you_text = "You"
                    tube_text = "Tube"
                    
                    prefix_width = draw.textlength(prefix, font=title_font)
                    you_width = draw.textlength(you_text, font=title_font)
                    tube_width = draw.textlength(tube_text, font=title_font)
                    nickname_width = draw.textlength(f" {player_name}", font=title_font)
                    
                    total_width = prefix_width + you_width + tube_width + nickname_width
                    start_x = self.width // 2 - total_width // 2
                    
                    draw.text((start_x, self.title_y), prefix, font=title_font,
                             fill=self.text_color, anchor="lt")
                    draw.text((start_x + prefix_width, self.title_y), you_text, font=title_font,
                             fill=(255, 0, 0), anchor="lt")
                    draw.text((start_x + prefix_width + you_width, self.title_y), tube_text, font=title_font,
                             fill=(255, 255, 255), anchor="lt")
                    draw.text((start_x + prefix_width + you_width + tube_width, self.title_y), f" {player_name}", font=title_font,
                             fill=(255, 255, 255), anchor="lt")
                else:
                    prefix = "Статистика игрока "
                    rank_text = f"{rank_display} "
                    nickname_text = player_name
                    
                    prefix_width = draw.textlength(prefix, font=title_font)
                    rank_width = draw.textlength(rank_text, font=title_font)
                    
                    total_width = prefix_width + rank_width + draw.textlength(nickname_text, font=title_font)
                    start_x = self.width // 2 - total_width // 2
                    
                    draw.text((start_x, self.title_y), prefix, font=title_font,
                             fill=self.text_color, anchor="lt")
                    draw.text((start_x + prefix_width, self.title_y), rank_text, font=title_font,
                             fill=rank_color, anchor="lt")
                    draw.text((start_x + prefix_width + rank_width, self.title_y), nickname_text, font=title_font,
                             fill=rank_color, anchor="lt")
            else:
                title = f"Статистика игрока {player_name}"
                draw.text((self.width // 2, self.title_y), title, font=title_font, 
                         fill=self.text_color, anchor="mm")
            
            mode_prefix_width = draw.textlength(mode_prefix, font=header_font)
            mode_name_width = draw.textlength(mode_name, font=header_font)
            total_mode_width = mode_prefix_width + mode_name_width
            mode_start_x = self.width // 2 - total_mode_width // 2
            
            draw.text((mode_start_x, self.mode_y), mode_prefix, font=header_font,
                     fill=self.text_color, anchor="lt")
            draw.text((mode_start_x + mode_prefix_width, self.mode_y), mode_name, font=header_font,
                     fill=self.mode_color, anchor="lt")
            
            draw.line([(self.margin_left, self.divider_y), (self.width - self.margin_right, self.divider_y)], fill=self.divider_color, width=2)
            
            y_offset = self.stats_start_y
            line_height = self.line_height
            
            if isinstance(stats_data, dict):
                data = None
                
                possible_data_keys = ['data', 'stats', 'values', 'statistics', 'playerStats']
                for key in possible_data_keys:
                    if key in stats_data and isinstance(stats_data[key], dict):
                        data = stats_data[key]
                        break
                
                if data is None:
                    data = stats_data
                
                if not isinstance(data, dict):
                    draw.text((self.width // 2, self.height // 2),
                             "Неверный формат данных от API",
                             font=header_font, fill=self.text_color, anchor="mm")
                    img_bytes = io.BytesIO()
                    img.save(img_bytes, format='PNG')
                    img_bytes.seek(0)
                    return img_bytes
                
                stats_to_display = []
                
                excluded_keys = {'success', 'message', 'name', 'mode', 'player', 'playerName', 'day'}
                
                priority_keys = ['wins', 'kills', 'deaths', 'losses', 'games', 
                               'winstreak', 'best_winstreak', 'kd', 'wl', 
                               'final_kills', 'final_deaths', 'beds_broken', 
                               'beds_lost', 'beds', 'level', 'exp', 'experience', 
                               'coins', 'playtime', 'winrate', 'top_gold', 
                               'blocks_placed', 'top_iron', 'bow_hits', 'bow_shots', 
                               'blocks_traveled', 'blocks_broken']
                
                added_keys = set()
                for key in priority_keys:
                    if key in data and data[key] is not None:
                        value = data[key]
                        if isinstance(value, (dict, list)):
                            continue
                        label = self._format_stat_label(key)
                        stats_to_display.append((label, str(value)))
                        added_keys.add(key)
                
                for key, value in data.items():
                    if (key in excluded_keys or 
                        key in added_keys or 
                        value is None):
                        continue
                    
                    if isinstance(value, dict):
                        for nested_key, nested_value in value.items():
                            if nested_key in excluded_keys:
                                continue
                            if nested_value is not None and not isinstance(nested_value, (dict, list)):
                                nested_label = self._format_stat_label(nested_key)
                                stats_to_display.append((nested_label, str(nested_value)))
                        continue
                    
                    if isinstance(value, list):
                        continue
                    
                    label = self._format_stat_label(key)
                    stats_to_display.append((label, str(value)))
                
                if not stats_to_display:
                    draw.text((self.width // 2, self.height // 2),
                             "Данные статистики не найдены",
                             font=header_font, fill=self.text_color, anchor="mm")
                else:
                    num_stats = len(stats_to_display)
                    rows = (num_stats + 1) // 2
                    max_height_needed = y_offset + (rows * line_height) + 50
                    
                    if max_height_needed > self.height:
                        new_img = self._create_canvas(self.width, max_height_needed)
                        new_draw = ImageDraw.Draw(new_img)
                        
                        if rank:
                            rank_display_redraw = self._format_rank_name(rank)
                            rank_color = self._get_rank_color(rank)
                            if rank_display_redraw.upper() == 'YOUTUBE':
                                prefix = "Статистика игрока "
                                you_text = "You"
                                tube_text = "Tube"
                                prefix_width = new_draw.textlength(prefix, font=title_font)
                                you_width = new_draw.textlength(you_text, font=title_font)
                                tube_width = new_draw.textlength(tube_text, font=title_font)
                                nickname_width = new_draw.textlength(f" {player_name}", font=title_font)
                                total_width = prefix_width + you_width + tube_width + nickname_width
                                start_x = self.width // 2 - total_width // 2
                                new_draw.text((start_x, self.title_y), prefix, font=title_font, fill=self.text_color, anchor="lt")
                                new_draw.text((start_x + prefix_width, self.title_y), you_text, font=title_font, fill=(255, 0, 0), anchor="lt")
                                new_draw.text((start_x + prefix_width + you_width, self.title_y), tube_text, font=title_font, fill=(255, 255, 255), anchor="lt")
                                new_draw.text((start_x + prefix_width + you_width + tube_width, self.title_y), f" {player_name}", font=title_font, fill=(255, 255, 255), anchor="lt")
                            else:
                                prefix = "Статистика игрока "
                                rank_text = f"{rank_display_redraw} "
                                nickname_text = player_name
                                prefix_width = new_draw.textlength(prefix, font=title_font)
                                rank_width = new_draw.textlength(rank_text, font=title_font)
                                total_width = prefix_width + rank_width + new_draw.textlength(nickname_text, font=title_font)
                                start_x = self.width // 2 - total_width // 2
                                new_draw.text((start_x, self.title_y), prefix, font=title_font, fill=self.text_color, anchor="lt")
                                new_draw.text((start_x + prefix_width, self.title_y), rank_text, font=title_font, fill=rank_color, anchor="lt")
                                new_draw.text((start_x + prefix_width + rank_width, self.title_y), nickname_text, font=title_font, fill=rank_color, anchor="lt")
                        else:
                            title = f"Статистика игрока {player_name}"
                            new_draw.text((self.width // 2, self.title_y), title, font=title_font, fill=self.text_color, anchor="mm")
                        
                        mode_prefix_width = new_draw.textlength(mode_prefix, font=header_font)
                        mode_name_width = new_draw.textlength(mode_name, font=header_font)
                        total_mode_width = mode_prefix_width + mode_name_width
                        mode_start_x = self.width // 2 - total_mode_width // 2
                        
                        new_draw.text((mode_start_x, self.mode_y), mode_prefix, font=header_font,
                                     fill=self.text_color, anchor="lt")
                        new_draw.text((mode_start_x + mode_prefix_width, self.mode_y), mode_name, font=header_font,
                                     fill=self.mode_color, anchor="lt")
                        new_draw.line([(self.margin_left, self.divider_y), (self.width - self.margin_right, self.divider_y)], fill=self.divider_color, width=2)
                        
                        img = new_img
                        draw = new_draw
                    
                    x_left = self.stats_x_left
                    x_right = self.width // 2 + 50 if self.stats_x_right is None else self.stats_x_right
                    label_width = self.label_width
                    
                    for i, (label, value) in enumerate(stats_to_display):
                        if i < (num_stats + 1) // 2:
                            current_x = x_left
                            current_y = y_offset + (i * line_height)
                        else:
                            current_x = x_right
                            current_y = y_offset + ((i - (num_stats + 1) // 2) * line_height)
                        
                        draw.text((current_x, current_y), f"{label}:", 
                                 font=text_font, fill=self.text_color)
                        
                        draw.text((current_x + label_width + self.value_offset, current_y), value,
                                 font=text_font, fill=self.accent_color)
            else:
                draw.text((self.width // 2, self.height // 2),
                         "Неверный формат данных от API",
                         font=header_font, fill=self.text_color, anchor="mm")
            
            footer_text = "AgeraPvP Stats Bot"
            img_height = img.size[1]
            draw.text((self.width // 2, img_height - self.footer_y_offset),
                     footer_text, font=small_font,
                     fill=(150, 150, 150), anchor="mm")
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            print(f"Ошибка при генерации изображения: {e}")
            return None