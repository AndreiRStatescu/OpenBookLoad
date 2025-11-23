from pathlib import Path
import subprocess

from services.honeyfeed import HoneyFeed
from models.novel import Novel


def save_novel_to_html(novel: Novel, output_path: Path) -> Path:
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


def convert_to_azw3(input_path: Path) -> Path:
    from shutil import which

    ebook_convert = which("ebook-convert")
    if not ebook_convert:
        fallback = Path("/Applications/calibre.app/Contents/MacOS/ebook-convert")
        if fallback.is_file():
            ebook_convert = str(fallback)
        else:
            raise FileNotFoundError("ebook-convert not found. Install Calibre CLI or add it to PATH.")

    output_path = input_path.with_suffix(".azw3")
    subprocess.run(
        [ebook_convert, str(input_path), str(output_path)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_path


def main():
    novel_id = "21714"
    print(f"\nScraping novel from: https://www.honeyfeed.fm/novels/{novel_id}")

    try:
        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        html_path = data_dir / f"honeyfeed_{novel_id}.html"

        if html_path.exists():
            print(f"\n✓ Found existing {html_path}, skipping scrape")
        else:
            result1 = HoneyFeed.scrape_novel(novel_id, chapter_numbers=[1])
            html_path = save_novel_to_html(result1, html_path)
            print(f"\n✓ Saved to {html_path}")

        azw3_path = convert_to_azw3(html_path)
        print(f"✓ Converted to {azw3_path}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
