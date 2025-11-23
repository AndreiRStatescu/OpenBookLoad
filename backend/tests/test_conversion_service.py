import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from services.conversion_service import ConversionService, Website, OutputFormat


class TestConversionService:
    def test_run_creates_html_and_azw3(self, scraped_novel, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)

        with patch(
            "services.conversion_service.ConversionService._scrape_novel",
            return_value=scraped_novel,
        ):
            result_path = ConversionService.run(
                website=Website.HONEYFEED,
                novel_id="21714",
                output_format=OutputFormat.AZW3,
                chapter_numbers=[1],
            )

        assert result_path.exists()
        assert result_path.suffix == ".azw3"

        html_path = result_path.with_suffix(".html")
        assert html_path.exists()

        html_content = html_path.read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in html_content
        assert scraped_novel.title in html_content
        assert scraped_novel.chapters[0].title in html_content

    def test_run_skips_scrape_when_html_exists(
        self, scraped_novel, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)

        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        html_path = data_dir / "honeyfeed_21714.html"
        html_path.write_text("<html>existing content</html>", encoding="utf-8")

        with patch(
            "services.conversion_service.ConversionService._scrape_novel"
        ) as mock_scrape, patch(
            "services.conversion_service.ConversionService._convert_to_azw3",
            return_value=Path("data/honeyfeed_21714.azw3"),
        ):
            result_path = ConversionService.run(
                website=Website.HONEYFEED,
                novel_id="21714",
                output_format=OutputFormat.AZW3,
                chapter_numbers=[1],
                override=False,
            )

            mock_scrape.assert_not_called()

        assert html_path.read_text(encoding="utf-8") == "<html>existing content</html>"

    def test_run_override_scrapes_when_html_exists(
        self, scraped_novel, tmp_path, monkeypatch
    ):
        monkeypatch.chdir(tmp_path)

        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        html_path = data_dir / "honeyfeed_21714.html"
        html_path.write_text("<html>old content</html>", encoding="utf-8")

        with patch(
            "services.conversion_service.ConversionService._scrape_novel",
            return_value=scraped_novel,
        ) as mock_scrape:
            result_path = ConversionService.run(
                website=Website.HONEYFEED,
                novel_id="21714",
                output_format=OutputFormat.AZW3,
                chapter_numbers=[1],
            )

            mock_scrape.assert_called_once()

        html_content = html_path.read_text(encoding="utf-8")
        assert "<html>old content</html>" not in html_content
        assert scraped_novel.title in html_content
