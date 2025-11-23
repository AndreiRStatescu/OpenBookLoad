import pytest
from pathlib import Path

from services.conversion_service import ConversionService, Website, OutputFormat


class TestConversionService:
    def test_run_creates_html_and_azw3(self, scraped_novel, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        
        result_path = ConversionService.run(
            website=Website.HONEYFEED,
            novel_id="21714",
            output_format=OutputFormat.AZW3,
            chapter_numbers=[1]
        )
        
        assert result_path.exists()
        assert result_path.suffix == ".azw3"
        
        html_path = result_path.with_suffix(".html")
        assert html_path.exists()
        
        html_content = html_path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in html_content
        assert scraped_novel.title in html_content
        assert scraped_novel.chapters[0].title in html_content
