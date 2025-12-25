from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional
from datetime import datetime
import io
import os
import requests


class ProfileImageGenerator:

    def __init__(self):
        self.width = 1600
        self.height = 900
        self.bg_color = (30, 30, 40)
        self.primary_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.accent_color = (255, 200, 50)
        self.divider_color = (255, 234, 0)
        self.rank_colors = {
            'DEFAULT': (128, 128, 128),
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
        self.start_y = 250
        self.skin_x = 10
        self.skin_y = 10
        self.skin_size = 450
        self.skin_spacing = 50
        self.divider_offset = 100
        self.divider_y_offset = 46
        self.info_line_height = 50
        self.margin_right = 50
        self.footer_y_offset = 40

    def _get_font(self, size: int):
        try:
            font_path = "Unbounded-Regular.ttf"
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        except Exception:
            pass
        return ImageFont.load_default()

    def _create_canvas(self) -> Image.Image:
        try:
            if os.path.exists(self.background_path):
                bg = Image.open(self.background_path).convert("RGB")
                bg = bg.resize((self.width, self.height), Image.Resampling.LANCZOS)
                return bg
        except Exception:
            pass
        return Image.new("RGB", (self.width, self.height), self.bg_color)

    def _load_skin_image(self, nickname: str) -> Optional[Image.Image]:
        try:
            url = f"https://skin.agerapvp.club/v1/body/{nickname}/1024"
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return None
            img = Image.open(io.BytesIO(r.content)).convert("RGBA")
            pixels = []
            for p in img.getdata():
                if p[0] > 240 and p[1] > 240 and p[2] > 240:
                    pixels.append((255, 255, 255, 0))
                else:
                    pixels.append(p)
            img.putdata(pixels)
            return img
        except Exception:
            return None

    def _remove_mc_formatting(self, text: str) -> str:
        if not text:
            return text
        import re
        return re.sub(r'§[0-9a-fA-Fk-oK-OrR]', '', text)

    def _format_rank_name(self, name: str) -> str:
        if name.upper() == "AX_TEAM":
            return "TEAM"
        return name

    def _get_rank_color(self, rank: str):
        return self.rank_colors.get(rank.upper(), self.text_color)

    def _format_timestamp(self, ts_value) -> str:
        try:
            if ts_value is None:
                return "Не указано"

            if isinstance(ts_value, str):
                ts_value = ts_value.strip()
                ts_float = float(ts_value)
            else:
                ts_float = float(ts_value)

            if ts_float > 10000000000:
                ts_float = ts_float / 1000

            dt = datetime.fromtimestamp(ts_float)
            return dt.strftime("%d.%m.%Y %H:%M")

        except ValueError:
            return str(ts_value)
        except Exception:
            return str(ts_value)

    def generate(self, nickname: str, profile_data: Dict) -> Optional[io.BytesIO]:
        try:
            api_username = profile_data.get("username", nickname)
            display_name_raw = profile_data.get("displayName", api_username)
            display_name = self._remove_mc_formatting(display_name_raw)

            user_id = profile_data.get("userId")
            language = profile_data.get("language")
            current_server = profile_data.get("currentServer")
            online = profile_data.get("online", False)
            last_login = profile_data.get("lastLogin")

            first_rank = None
            ranks = profile_data.get("ranks", [])

            if isinstance(ranks, list) and ranks:
                r = ranks[0]
                if isinstance(r, dict):
                    rank_name = r.get("name")
                    rank_display_name = r.get("displayName")
                    first_rank = rank_name or rank_display_name
                elif isinstance(r, str):
                    first_rank = r

            if first_rank:
                first_rank = self._remove_mc_formatting(str(first_rank))
                rank_display = self._format_rank_name(first_rank)
            else:
                rank_display = None

            info_items = []

            if user_id is not None:
                info_items.append(("ID пользователя", str(user_id)))

            if rank_display:
                info_items.append(("Ранг", rank_display))
            else:
                info_items.append(("Ранг", "DEFAULT"))

            info_items.append(("Отображаемое имя", api_username))

            if language:
                info_items.append(("Язык", language))

            if current_server is not None:
                info_items.append(("Текущий сервер", current_server))

            info_items.append(("Онлайн", "Да" if online else "Нет"))

            if last_login is not None:
                formatted_login = self._format_timestamp(last_login)
                info_items.append(("Последний вход", formatted_login))

            img = self._create_canvas()
            draw = ImageDraw.Draw(img)

            title_font = self._get_font(48)
            text_font = self._get_font(32)

            skin = self._load_skin_image(nickname)
            skin_width = 0
            if skin:
                h_ratio = skin.height / skin.width
                new_h = int(self.skin_size * h_ratio)
                skin = skin.resize((self.skin_size, new_h), Image.Resampling.LANCZOS)
                img.paste(skin, (self.skin_x, self.skin_y), skin)
                skin_width = self.skin_size

            content_x = self.skin_x + skin_width + self.skin_spacing
            content_center_x = content_x + (self.width - content_x - 50) // 2

            if rank_display and first_rank and first_rank.upper() != "DEFAULT":
                color = self._get_rank_color(first_rank)
                title = f"{rank_display} {api_username}"
                draw.text((content_center_x, self.start_y),
                          title, font=title_font,
                          fill=color, anchor="mm")
            else:
                draw.text((content_center_x, self.start_y),
                          api_username,
                          font=title_font,
                          fill=self.primary_color, anchor="mm")

            y = self.start_y + self.divider_offset
            draw.line(
                [(content_x, y), (self.width - self.margin_right, y)],
                fill=self.divider_color, width=2
            )
            y += self.divider_y_offset

            max_label = max(draw.textlength(f"{k}:", text_font) for k, _ in info_items)
            spacing = 30
            start_x = content_center_x - 300

            for label, value in info_items:
                label_text = f"{label}:"
                draw.text((start_x + max_label - draw.textlength(label_text, text_font), y),
                          label_text, font=text_font, fill=self.text_color)
                draw.text((start_x + max_label + spacing, y),
                          str(value), font=text_font, fill=self.accent_color)
                y += self.info_line_height

            draw.text(
                (self.width // 2, self.height - self.footer_y_offset),
                "AgeraPvP Stats Bot",
                font=text_font,
                fill=(150, 150, 150),
                anchor="mm"
            )

            out = io.BytesIO()
            img.save(out, format="PNG")
            out.seek(0)
            return out

        except Exception:
            return None