from scrapers import QLifeScraper
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search for hospitals")
    parser.add_argument("--address", type=str, default="山梨県中央市", help="Address to search")
    parser.add_argument("--specialization", type=str, default="内科", help="Medical specialization")
    parser.add_argument("--max_review_pages", type=int, default=999, help="Maximum number of review pages to scrape per hospital")
    args = parser.parse_args()

    qlife = QLifeScraper(address=args.address, specialization=args.specialization, max_review_pages=args.max_review_pages)

    for listing in range(1, 1000):
        reviews = qlife.find_all_reviews(listing)
        if reviews is None:
            print(f"Stopping at listing {listing}")
            break

        with open(f"reviews_{args.specialization}_{args.address}_{listing}.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, ensure_ascii=False, indent=4)