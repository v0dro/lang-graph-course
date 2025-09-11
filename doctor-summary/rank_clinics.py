# Rank clinics using reviews pulled from QLife.
import argparse
from japanese_address import parse as japanese_address_parser

def find_prefecture_ward_city(address):
    parsed_address = japanese_address_parser(address)
    prefecture = parsed_address.get("prefecture", "")
    ward = parsed_address.get("ward", "")
    city = parsed_address.get("city", "")
    return prefecture, ward, city

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank clinics using reviews")
    specialization = parser.add_argument("--specialization", type=str, default="内科", help="Medical specialization")
    address = parser.add_argument("--address", type=str, default="山梨県中央市", help="Address to search")
    args = parser.parse_args()

    prefecture, ward, city = find_prefecture_ward_city(args.address)
