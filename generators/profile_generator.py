from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import io
import os
import requests


class ProfileImageGenerator:
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.bg_color = (30, 30, 40)
        self.primary_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.accent_color = (255, 200, 50)
        
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
        
    def _get_font(self, size: int):
        try:
            if os.name == 'nt':
                font_path = "C:/Windows/Fonts/arial.ttf"
            else:
                font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except:
            pass
        
        return ImageFont.load_default()
    
    def _load_skin_image(self, nickname: str) -> Optional[Image.Image]:
        try:
            url = f"https://skin.agerapvp.club/v1/body/{nickname}/1024"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                skin_img = Image.open(io.BytesIO(response.content))
                
                if skin_img.mode == 'RGB':
                    skin_img = skin_img.convert('RGBA')
                
                data = skin_img.getdata()
                new_data = []
                for item in data:
                    if item[0] > 240 and item[1] > 240 and item[2] > 240:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                
                skin_img.putdata(new_data)
                return skin_img
        except Exception as e:
            print(f"Ошибка при загрузке скина: {e}")
        return None
    
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
    
    def _format_value(self, value) -> str:
        if value is None:
            return "Не указано"
        if isinstance(value, bool):
            return "Да" if value else "Нет"
        if isinstance(value, (dict, list)):
            return str(value)
        return str(value)
    
    def generate(self, nickname: str, profile_data: Dict) -> Optional[io.BytesIO]:
        try:
            skin_img = self._load_skin_image(nickname)
            
            info_items = []
            
            username = profile_data.get('username', nickname)
            display_name = profile_data.get('displayName', username)
            display_name = self._remove_minecraft_formatting(display_name)
            
            user_id = profile_data.get('userId')
            language = profile_data.get('language')
            current_server = profile_data.get('currentServer')
            last_login = profile_data.get('lastLogin')
            online = profile_data.get('online', False)
            
            first_rank = None
            ranks = profile_data.get('ranks', [])
            if ranks and isinstance(ranks, list) and len(ranks) > 0:
                rank_obj = ranks[0]
                if isinstance(rank_obj, dict):
                    first_rank = rank_obj.get('name') or rank_obj.get('displayName')
                    if first_rank:
                        first_rank = self._remove_minecraft_formatting(first_rank)
                elif isinstance(rank_obj, str):
                    first_rank = self._remove_minecraft_formatting(rank_obj)
            
            rank_display = None
            if first_rank:
                rank_display = self._format_rank_name(first_rank)
                info_items.append(("Ранг", rank_display))
            if user_id is not None:
                info_items.append(("ID пользователя", str(user_id)))
            if display_name and display_name != username:
                info_items.append(("Отображаемое имя", display_name))
            if language:
                info_items.append(("Язык", language))
            if current_server:
                info_items.append(("Текущий сервер", current_server))
            info_items.append(("Онлайн", "Да" if online else "Нет"))
            if last_login:
                info_items.append(("Последний вход", str(last_login)))
            
            base_height = 200 if skin_img else 150
            info_height = len(info_items) * 35 + 50
            total_height = base_height + info_height
            
            img = Image.new('RGB', (self.width, total_height), color=self.bg_color)
            draw = ImageDraw.Draw(img)
            
            title_font = self._get_font(40)
            text_font = self._get_font(18)
            small_font = self._get_font(14)
            
            y_offset = 20
            skin_size = 150
            skin_x = 50
            actual_skin_width = 0
            
            if skin_img:
                original_width, original_height = skin_img.size
                aspect_ratio = original_height / original_width
                
                new_width = skin_size
                new_height = int(skin_size * aspect_ratio)
                
                skin_img = skin_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                actual_skin_width = new_width
                
                img.paste(skin_img, (skin_x, y_offset), skin_img if skin_img.mode == 'RGBA' else None)
            
            content_start_x = skin_x + actual_skin_width + 50
            content_width = self.width - content_start_x - 50
            text_x = content_start_x + content_width // 2
            
            if first_rank:
                if rank_display is None:
                    rank_display = self._format_rank_name(first_rank)
                rank_color = self._get_rank_color(first_rank)
                
                if rank_display.upper() == 'YOUTUBE':
                    you_text = "You"
                    tube_text = "Tube"
                    
                    you_width = draw.textlength(you_text, font=title_font)
                    tube_width = draw.textlength(tube_text, font=title_font)
                    nickname_width = draw.textlength(f" {nickname}", font=title_font)
                    total_width = you_width + tube_width + nickname_width
                    start_x = text_x - total_width // 2
                    
                    draw.text((start_x, y_offset), you_text, font=title_font,
                             fill=(255, 0, 0), anchor="lt")
                    draw.text((start_x + you_width, y_offset), tube_text, font=title_font,
                             fill=(255, 255, 255), anchor="lt")
                    draw.text((start_x + you_width + tube_width, y_offset), f" {nickname}", font=title_font,
                             fill=(255, 255, 255), anchor="lt")
                else:
                    rank_text = f"{rank_display} "
                    nickname_text = nickname
                    
                    rank_width = draw.textlength(rank_text, font=title_font)
                    nickname_width = draw.textlength(nickname_text, font=title_font)
                    total_width = rank_width + nickname_width
                    start_x = text_x - total_width // 2
                    
                    draw.text((start_x, y_offset), rank_text, font=title_font,
                             fill=rank_color, anchor="lt")
                    draw.text((start_x + rank_width, y_offset), nickname_text, font=title_font,
                             fill=rank_color, anchor="lt")
            else:
                title = nickname
                draw.text((text_x, y_offset), title, font=title_font,
                         fill=self.primary_color, anchor="mm")
            
            y_offset += 50
            
            draw.line([(content_start_x, y_offset), (self.width - 50, y_offset)], fill=self.primary_color, width=2)
            y_offset += 30
            
            max_label_width = 0
            for label, value in info_items:
                label_text = f"{label}:"
                label_width = draw.textlength(label_text, font=text_font)
                if label_width > max_label_width:
                    max_label_width = label_width
            
            label_value_spacing = 30
            total_label_area = max_label_width + label_value_spacing
            
            max_value_width = 0
            for label, value in info_items:
                value_str = self._format_value(value)
                value_width = draw.textlength(value_str, font=text_font)
                if value_width > max_value_width:
                    max_value_width = value_width
            
            total_item_width = total_label_area + max_value_width
            item_start_x = text_x - total_item_width // 2
            
            for label, value in info_items:
                label_text = f"{label}:"
                value_str = self._format_value(value)
                
                label_x = item_start_x + max_label_width - draw.textlength(label_text, font=text_font)
                draw.text((label_x, y_offset), label_text, 
                         font=text_font, fill=self.text_color, anchor="lt")
                
                draw.text((item_start_x + total_label_area, y_offset), value_str,
                         font=text_font, fill=self.accent_color, anchor="lt")
                
                y_offset += 35
            
            footer_text = "AgeraPvP Stats Bot"
            draw.text((self.width // 2, total_height - 20),
                     footer_text, font=small_font,
                     fill=(150, 150, 150), anchor="mm")
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            print(f"Ошибка при генерации изображения профиля: {e}")
            return None