from services.honeyfeed import HoneyFeed


def print_novel_info(result, test_description):
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
        print("\n" + "#" * 80)
        print("# Test 1: Scraping specific chapters [1, 3, 5]")
        print("#" * 80)
        result1 = HoneyFeed.scrape_novel(novel_id, chapter_numbers=[1])
        print_novel_info(result1, "Specific Chapters [1, 3, 5]")

    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
