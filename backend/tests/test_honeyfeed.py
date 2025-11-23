import pytest


class TestHoneyFeed:

    def test_novel_has_title(self, scraped_novel):
        assert scraped_novel.title
        assert len(scraped_novel.title) > 0

    def test_novel_has_correct_url(self, scraped_novel):
        assert scraped_novel.url == "https://www.honeyfeed.fm/novels/21714/chapters"

    def test_novel_has_correct_id(self, scraped_novel):
        assert scraped_novel.novel_id == "21714"

    def test_single_chapter_scraped(self, scraped_novel):
        assert len(scraped_novel.chapters) == 1

    def test_chapter_has_correct_number(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.number == 1

    def test_chapter_has_title(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.title
        assert len(chapter.title) > 0

    def test_chapter_has_valid_url(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.url
        assert chapter.url.startswith("https://www.honeyfeed.fm/chapters/")

    def test_chapter_has_content(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.content
        assert len(chapter.content) > 1000

    def test_content_starts_correctly(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.content.startswith(
            "<p>The first thing I do upon opening my eyes"
        )

    def test_content_ends_correctly(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert chapter.content.endswith("“GROUND!!!!!”</p>")

    def test_no_unwanted_login_text(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert "Already a Honeyfeed member" not in chapter.content
        assert "Don't have an account?" not in chapter.content

    def test_no_unwanted_footer_text(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert "Join us on Honeyfeed SNS" not in chapter.content
        assert "© 2025 qdopp" not in chapter.content

    def test_content_has_paragraph_breaks(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        assert "</p><p>" in chapter.content

    def test_preserves_newlines_in_text(self, scraped_novel):
        chapter = scraped_novel.chapters[0]
        expected_text = "<p><b><i>[Divine Staff of Holy Light]<br/>Attributes: Holy, Wind<br/>Durability: 100/100</i></b></p>"
        assert expected_text in chapter.content
