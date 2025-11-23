import pytest
from services.honeyfeed import HoneyFeed


@pytest.fixture(scope="session")
def scraped_novel():
    return HoneyFeed.scrape_novel("21714", chapter_numbers=[1])
