from pathlib import Path
import subprocess

from services.honeyfeed import HoneyFeed
from models.novel import Novel


def save_novel_to_txt(novel: Novel, output_path: Path) -> Path:
    lines = [f"Title: {novel.title}", f"URL: {novel.url}", ""]
    for chapter in novel.chapters:
        lines.append(f"Chapter {chapter.number}: {chapter.title}")
        lines.append(chapter.content)
        lines.append("")
    output_path.write_text("\n".join(lines).strip(), encoding="utf-8")
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
        txt_path = data_dir / f"honeyfeed_{novel_id}.txt"

        if txt_path.exists():
            print(f"\n✓ Found existing {txt_path}, skipping scrape")
        else:
            result1 = HoneyFeed.scrape_novel(novel_id, chapter_numbers=[1])
            txt_path = save_novel_to_txt(result1, txt_path)
            print(f"\n✓ Saved to {txt_path}")

        azw3_path = convert_to_azw3(txt_path)
        print(f"✓ Converted to {azw3_path}")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
