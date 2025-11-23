from services.honeyfeed import HoneyFeedScraper


def main():
    novel_id = "21714"
    print(f"\nScraping novel from: https://www.honeyfeed.fm/novels/{novel_id}")
    print("-" * 80)

    try:
        scraper = HoneyFeedScraper(novel_id)
        result = scraper.scrape_novel()

        print(f"\n✓ Novel Title: {result.title}")
        print(f"✓ Novel URL: {result.url}")
        print(f"✓ Total Chapters: {len(result.chapters)}")
        print("\n" + "=" * 80)
        print("CHAPTERS:")
        print("=" * 80)

        for chapter in result.chapters:
            print(f"\n[Chapter {chapter.number}]")
            print(f"  Title: {chapter.title}")
            print(f"  URL: {chapter.url}")

        print("\n" + "=" * 80)
        print(f"✓ Successfully scraped {len(result.chapters)} chapters!")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")


if __name__ == "__main__":
    main()
