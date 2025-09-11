# Rank clinics using reviews pulled from QLife.
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank clinics using reviews")
    specialization = parser.add_argument("--specialization", type=str, default="内科", help="Medical specialization")
    address = parser.add_argument("--address", type=str, default="山梨県中央市", help="Address to search")
    args = parser.parse_args()

    