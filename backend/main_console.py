from services.honeyfeed import HoneyFeed


def print_novel_info(result, test_description):
    """Helper function to print novel information."""
    print(f"\n{'='*80}")
    print(f"TEST: {test_description}")
    print(f"{'='*80}")
    print(f"\n✓ Novel Title: {result.title}")
    print(f"✓ Novel URL: {result.url}")
    print(f"✓ Chapters Retrieved: {len(result.chapters)}")
    print("\nCHAPTERS:")
    print("-" * 80)

    for chapter in result.chapters:
        print(f"\n[Chapter {chapter.number}]")
        print(f"  Title: {chapter.title}")
        print(f"  URL: {chapter.url}")
        print(f"  Content Preview: {chapter.content}")

    print(f"\n{'='*80}")
    print(f"✓ Test completed successfully!\n")


def main():
    novel_id = "21714"
    print(f"\nScraping novel from: https://www.honeyfeed.fm/novels/{novel_id}")
    print("=" * 80)

    try:
        # Test 1: Scrape specific chapters by number
        print("\n" + "#" * 80)
        print("# Test 1: Scraping specific chapters [1, 3, 5]")
        print("#" * 80)
        result1 = HoneyFeed.scrape_novel(novel_id, chapter_numbers=[1])
        print_novel_info(result1, "Specific Chapters [1, 3, 5]")

        # # Test 2: Scrape a range (chapters 1-3)
        # print("\n" + "#" * 80)
        # print("# Test 2: Scraping chapter range 1-3")
        # print("#" * 80)
        # result2 = HoneyFeed.scrape_novel(novel_id, start_chapter=1, end_chapter=3)
        # print_novel_info(result2, "Chapter Range 1-3")

        # # Test 3: Scrape from chapter 2 onwards (first 5 for testing)
        # print("\n" + "#" * 80)
        # print("# Test 3: Scraping from chapter 2 to 5")
        # print("#" * 80)
        # result3 = HoneyFeed.scrape_novel(novel_id, start_chapter=2, end_chapter=5)
        # print_novel_info(result3, "From Chapter 2 to 5")

        # # Test 4: Scrape just the first chapter
        # print("\n" + "#" * 80)
        # print("# Test 4: Scraping only chapter 1")
        # print("#" * 80)
        # result4 = HoneyFeed.scrape_novel(novel_id, chapter_numbers=[1])
        # print_novel_info(result4, "Single Chapter [1]")

        # Uncomment below to test scraping ALL chapters (warning: may be slow)
        # print("\n" + "#" * 80)
        # print("# Test 5: Scraping ALL chapters")
        # print("#" * 80)
        # result5 = HoneyFeed.scrape_novel(novel_id)
        # print_novel_info(result5, "All Chapters")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
