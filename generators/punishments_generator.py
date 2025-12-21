from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
import io
import os


class PunishmentsImageGenerator:
    
    def __init__(self):
        self.width = 800
        self.height = 500
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
    
    def generate(self, stats_data: Dict) -> Optional[io.BytesIO]:
        try:
            img = Image.new('RGB', (self.width, self.height), color=self.bg_color)
            draw = ImageDraw.Draw(img)
            
            title_font = self._get_font(40)
            header_font = self._get_font(24)
            text_font = self._get_font(20)
            small_font = self._get_font(14)
            
            title = "Статистика наказаний"
            draw.text((self.width // 2, 50), title, font=title_font,
                     fill=self.primary_color, anchor="mm")
            
            draw.line([(50, 100), (self.width - 50, 100)], fill=self.primary_color, width=2)
            
            y_offset = 140
            line_height = 45
            
            stats_items = [
                ("Всего банов", stats_data.get('totalBans', 0)),
                ("Всего мутов", stats_data.get('totalMutes', 0)),
                ("Активных банов", stats_data.get('totalActiveBans', 0)),
                ("Активных мутов", stats_data.get('totalActiveMutes', 0)),
                ("Банов за неделю", stats_data.get('totalWeekBans', 0)),
                ("Мутов за неделю", stats_data.get('totalWeekMutes', 0))
            ]
            
            max_label_width = 0
            for label, value in stats_items:
                label_text = f"{label}:"
                label_width = draw.textlength(label_text, font=text_font)
                if label_width > max_label_width:
                    max_label_width = label_width
            
            label_value_spacing = 30
            total_label_area = max_label_width + label_value_spacing
            
            max_value_width = 0
            for label, value in stats_items:
                value_str = str(value)
                value_width = draw.textlength(value_str, font=text_font)
                if value_width > max_value_width:
                    max_value_width = value_width
            
            total_item_width = total_label_area + max_value_width
            item_start_x = self.width // 2 - total_item_width // 2
            
            for label, value in stats_items:
                label_text = f"{label}:"
                value_str = str(value)
                
                label_x = item_start_x + max_label_width - draw.textlength(label_text, font=text_font)
                draw.text((label_x, y_offset), label_text,
                         font=text_font, fill=self.text_color, anchor="lt")
                
                draw.text((item_start_x + total_label_area, y_offset), value_str,
                         font=text_font, fill=self.accent_color, anchor="lt")
                
                y_offset += line_height
            
            footer_text = "AgeraPvP Stats Bot"
            draw.text((self.width // 2, self.height - 20),
                     footer_text, font=small_font,
                     fill=(150, 150, 150), anchor="mm")
            
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            return img_bytes
            
        except Exception as e:
            print(f"Ошибка при генерации изображения статистики наказаний: {e}")
            return None