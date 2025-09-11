# Rank clinics using reviews pulled from QLife.
import argparse
from japanese_address import parse as japanese_parser

def extract_address_components(address):
    address = japanese_parser(address)
    return address["prefecture"], address.get("ward", ""), address.get("city", "")

def rank_clinics(prefecture, ward, city, specialization, max_clinics=10):
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank clinics using reviews")
    specialization = parser.add_argument("--specialization", type=str, default="内科", help="Medical specialization")
    address = parser.add_argument("--address", type=str, default="山梨県中央市", help="Address to search")
    max_clinics = parser.add_argument("--max_clinics", type=int, default=10, help="Maximum number of clinics to return")
    args = parser.parse_args()

    prefecture, ward, city = extract_address_components(args.address)

    # Run agents for the given prefecture, ward, city, and specialization.
    clinics = rank_clinics(prefecture, ward, city, args.specialization, max_clinics=args.max_clinics)

    print(f"Best clinics for {args.specialization} around {args.address}:")
    for idx, clinic in enumerate(clinics):
        print("="*40)
        print(f"{idx+1}. {clinic['name']} - {clinic['address']}")
        print(f"\tQuality of healthcare: {clinic['quality_of_healthcare']}")
        print(f"\tRecommendations from others: {clinic['recommendations_from_others']}")
        print(f"\tHygiene: {clinic['hygiene']}")
        print(f"\tStaff manners: {clinic['staff_manners']}")
        print(f"\tStars: {clinic['stars']}")
        print(f"\tOverall score: {clinic['overall_score']}")
        print("="*40)

