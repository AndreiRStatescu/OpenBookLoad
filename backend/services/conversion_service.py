from pathlib import Path
import subprocess
import sys
from enum import Enum
from shutil import which

from models.novel import Novel
from services.honeyfeed import HoneyFeed


class Website(Enum):
    HONEYFEED = "honeyfeed"


class OutputFormat(Enum):
    AZW3 = "azw3"
    EPUB = "epub"


class ConversionService:
    @staticmethod
    def run(
        website: Website,
        novel_id: str,
        output_format: OutputFormat,
        chapter_numbers: list[int] = None,
        override: bool = True,
    ) -> Path:
        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        
        html_path = data_dir / f"{website.value}_{novel_id}.html"
        
        if html_path.exists() and not override:
            print(f"\n✓ Found existing {html_path}, skipping scrape")
        else:
            novel = ConversionService._scrape_novel(website, novel_id, chapter_numbers)
            html_path = ConversionService._save_novel_to_html(novel, html_path)
            print(f"\n✓ Saved to {html_path}")
        
        if output_format == OutputFormat.AZW3:
            output_path = ConversionService._convert_to_azw3(html_path)
            print(f"✓ Converted to {output_path}")
            return output_path
        elif output_format == OutputFormat.EPUB:
            output_path = ConversionService._convert_to_epub(html_path)
            print(f"✓ Converted to {output_path}")
            return output_path
        
        return html_path
    
    @staticmethod
    def _scrape_novel(website: Website, novel_id: str, chapter_numbers: list[int] = None) -> Novel:
        if website == Website.HONEYFEED:
            return HoneyFeed.scrape_novel(novel_id, chapter_numbers=chapter_numbers)
        raise ValueError(f"Unsupported website: {website}")
    
    @staticmethod
    def _save_novel_to_html(novel: Novel, output_path: Path) -> Path:
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            '<meta charset="utf-8">',
            f"<title>{novel.title}</title>",
            "</head>",
            "<body>",
            f"<h1>{novel.title}</h1>",
        ]
        
        for chapter in novel.chapters:
            html_parts.append(f"<h2>Chapter {chapter.number}: {chapter.title}</h2>")
            html_parts.append(chapter.content)
        
        html_parts.extend(["</body>", "</html>"])
        output_path.write_text("\n".join(html_parts), encoding="utf-8")
        return output_path
    
    @staticmethod
    def _get_ebook_convert_path() -> str:
        ebook_convert = which("ebook-convert")
        if not ebook_convert:
            if sys.platform == "darwin":
                fallback = Path("/Applications/calibre.app/Contents/MacOS/ebook-convert")
            elif sys.platform == "win32":
                fallback = Path("C:/Program Files/Calibre2/ebook-convert.exe")
                if not fallback.exists():
                    fallback = Path("C:/Program Files (x86)/Calibre2/ebook-convert.exe")
            else:
                fallback = Path("/usr/bin/ebook-convert")
            
            if fallback.is_file():
                ebook_convert = str(fallback)
            else:
                raise FileNotFoundError("ebook-convert not found. Install Calibre CLI or add it to PATH.")
        
        return ebook_convert
    
    @staticmethod
    def _convert_to_azw3(input_path: Path) -> Path:
        ebook_convert = ConversionService._get_ebook_convert_path()
        output_path = input_path.with_suffix(".azw3")
        subprocess.run(
            [ebook_convert, str(input_path), str(output_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output_path
    
    @staticmethod
    def _convert_to_epub(input_path: Path) -> Path:
        ebook_convert = ConversionService._get_ebook_convert_path()
        output_path = input_path.with_suffix(".epub")
        subprocess.run(
            [ebook_convert, str(input_path), str(output_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return output_path
