from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import io
import os


class StaffImageGenerator:
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.bg_color = (30, 30, 40)
        self.primary_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.accent_color = (255, 200, 50)
    
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
    
    def _remove_minecraft_formatting(self, text: str) -> str:
        if not text:
            return text
        
        import re
        return re.sub(r'§[0-9a-fA-Fk-oK-OrR]', '', text)
    
    def generate(self, staff_data: Dict) -> Optional[io.BytesIO]:
        try:
            players = staff_data.get('players', [])
            
            base_height = 150
            item_height = 35
            total_height = base_height + (len(players) * item_height) + 50
            
            img = Image.new('RGB', (self.width, total_height), color=self.bg_color)
            draw = ImageDraw.Draw(img)
            
            title_font = self._get_font(40)
            text_font = self._get_font(18)
            small_font = self._get_font(14)
            
            title = f"Онлайн стафф ({len(players)})"
            draw.text((self.width // 2, 50), title, font=title_font,
                     fill=self.primary_color, anchor="mm")
            
            draw.line([(50, 100), (self.width - 50, 100)], fill=self.primary_color, width=2)
            
            y_offset = 140
            
            if len(players) == 0:
                draw.text((self.width // 2, y_offset + 50),
                         "Нет онлайн стаффа",
                         font=text_font, fill=self.text_color, anchor="mm")
            else:
                for i, player in enumerate(players, 1):
                    display_name = player.get('displayName', 'Неизвестно')
                    user_id = player.get('userId', 'N/A')
                    
                    display_name = self._remove_minecraft_formatting(display_name)
                    
                    player_text = f"{i}. {display_name} (ID: {user_id})"
                    
                    draw.text((80, y_offset), player_text,
                             font=text_font, fill=self.text_color, anchor="lt")
                    
                    y_offset += item_height
            
            footer_text = "AgeraPvP Stats Bot"
            draw.text((self.width // 2, total_height - 20),
                     footer_text, font=small_font,
                     fill=(150, 150, 150), anchor="mm")
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            print(f"Ошибка при генерации изображения онлайн стаффа: {e}")
            return None