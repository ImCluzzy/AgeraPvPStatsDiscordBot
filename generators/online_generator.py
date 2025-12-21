from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import io
import os


class OnlineImageGenerator:
    
    def __init__(self):
        self.width = 600
        self.height = 300
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
    
    def generate(self, online_data: Dict) -> Optional[io.BytesIO]:
        try:
            img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
            draw = ImageDraw.Draw(img)
            
            title_font = self._get_font(36)
            number_font = self._get_font(72)
            small_font = self._get_font(14)
            
            title = "Онлайн игроков"
            draw.text((self.width // 2, 60), title, font=title_font,
                     fill=self.primary_color, anchor="mm")
            
            online_count = online_data.get('online', 0)
            online_text = str(online_count)
            
            draw.text((self.width // 2, self.height // 2), online_text, font=number_font,
                     fill=self.accent_color, anchor="mm")
            
            footer_text = "AgeraPvP Stats Bot"
            draw.text((self.width // 2, self.height - 20),
                     footer_text, font=small_font,
                     fill=(150, 150, 150), anchor="mm")
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            print(f"Ошибка при генерации изображения общего онлайн: {e}")
            return None