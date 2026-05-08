from crawl4ai import AsyncWebCrawler
import asyncio
import time


async def crawl_url(url: str, logger=None):

    start_time = time.time()

    def log(message):
        if logger:
            logger(message)

        print(message)

    log(f"[FETCH] Starting crawl...")
    log(f"↓ {url}")

    try:

        async with AsyncWebCrawler(verbose=True) as crawler:

            fetch_start = time.time()

            result = await crawler.arun(url=url)

            fetch_end = time.time()

            log(
                f"[FETCH COMPLETE] ✓ "
                f"⏱: {round(fetch_end - fetch_start, 2)}s"
            )

            if result.success:

                scrape_start = time.time()

                markdown = result.markdown

                scrape_end = time.time()

                log(
                    f"[SCRAPE COMPLETE] ✓ "
                    f"⏱: {round(scrape_end - scrape_start, 2)}s"
                )

                total = round(
                    time.time() - start_time,
                    2
                )

                log(
                    f"[COMPLETE] ● Total Time: {total}s"
                )

                return markdown

            else:

                log(
                    f"[ERROR] {result.error_message}"
                )

                return (
                    f"Failed to crawl: "
                    f"{result.error_message}"
                )

    except Exception as e:

        error_msg = f"""
[CRITICAL ERROR]

Unable to crawl URL.

Possible reasons:
- Invalid URL
- DNS failure
- Website blocking crawler
- Internet issue

Technical Error:
{str(e)}
"""

        log(error_msg)

        return error_msg


def run_crawler(url: str, logger=None):

    return asyncio.run(
        crawl_url(url, logger)
    )