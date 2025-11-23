from services.conversion_service import ConversionService, Website, OutputFormat


def main():
    novel_id = "21714"
    print(f"\nScraping novel from: https://www.honeyfeed.fm/novels/{novel_id}")

    try:
        ConversionService.run(
            website=Website.HONEYFEED,
            novel_id=novel_id,
            output_format=OutputFormat.AZW3
        )
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
