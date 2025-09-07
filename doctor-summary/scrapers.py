import json
from curl_cffi import requests as cureq
import re
from bs4 import BeautifulSoup
from datetime import datetime
from metadata import qlife_specialization_map, qlife_prefecture_values_map, qlife_wards_map
from japanese_address import parse as japanese_parser

class QLifeScraper:
    def __init__(self, address, specialization, max_review_pages=999):
        self.specialization = specialization
        self.max_review_pages = max_review_pages
        
        parsed_address = japanese_parser(address)
        self.prefecture = parsed_address["prefecture"]
        self.full_ward = self._get_ward(parsed_address)

    def _get_ward(self, parsed_address):
        addr = ""
        if "city" in parsed_address and parsed_address["city"]:
            addr += parsed_address["city"]
        
        if "ward" in parsed_address and parsed_address["ward"]:
            addr += parsed_address["ward"]

        return addr

    def find_all_reviews(self, num_listing=1):
        specialization_id = qlife_specialization_map[self.specialization]
        pref_id = qlife_prefecture_values_map[self.prefecture]
        ward_id = qlife_wards_map[self.prefecture][self.full_ward]
        data = list()
        # I cannot find where this 11b and 13b is coming from. 
        url = f"https://www.qlife.jp/search_hospital11b_{specialization_id}_{pref_id}_{ward_id}_{num_listing}"
        response = cureq.get(url, impersonate="chrome", timeout=10)
        if response.status_code != 200:
            return None

        # Find clinics from this text. Then find the link that contains the reviews for each clinic.
        # Follow that link and download the reviews.
        soup = BeautifulSoup(response.text, "html.parser")
        hospitals_list = soup.find_all("article", class_="hospital_list_wrapper")
        if len(hospitals_list) == 0:
            return None

        for hospital in hospitals_list:
            this_clinic_data = dict()
            hospital_header = hospital.find("h2", class_="hospital_name")
            hospital_name = hospital_header.find("a").text.strip()
            this_clinic_data['name'] = hospital_name
            dd = hospital.find("dl", class_="hospital_basic_info").find("dd")
            clinic_address = ''.join(dd.find_all(string=True, recursive=False)).strip()

            this_clinic_data['doctor'] = list()
            this_clinic_data['department'] = self.specialization
            this_clinic_data['address'] = clinic_address
            this_clinic_data['reviews'] = dict()
            reviews_dict = dict()
            
            hospital_link = hospital_header.find("a")["href"]
            hospital_id = re.search(r'/hospital_detail_(\d+)', hospital_link).group(1)
            num_kuchikomi_list = 1
            while num_kuchikomi_list <= self.max_review_pages:
                try:
                    hospital_resp = cureq.get(f"https://www.qlife.jp/kuchikomi_list_{hospital_id}_{num_kuchikomi_list}", 
                                            impersonate="chrome", timeout=10)
                except:
                    continue

                if hospital_resp.status_code != 200:
                    break

                hospital_response = BeautifulSoup(hospital_resp.text, "html.parser")
                reviews = hospital_response.find_all("section", class_="kuchikomi_list")
                for review in reviews:
                    review_aref = review.find_all("a")
                    num_review = 1
                    for a in review_aref:
                        if "kuchikomi_" in a["href"] and "kuchikomi_list" not in a["href"]:
                            try:
                                bb = cureq.get(f"https://www.qlife.jp/{a['href']}", impersonate="chrome", timeout=10)
                            except:
                                continue

                            if bb.status_code == 200:
                                bb_response = BeautifulSoup(bb.text, "html.parser").find("section", class_="kuchikomi_body")

                                kuchikomi_text = bb_response.find("p").text.strip()
                                kuchikomi_date = datetime.strptime(
                                    bb_response.find("small").text.strip().replace("投稿", ""),
                                    "%Y年%m月%d日")
                                
                                reviews_dict[f"review{num_review}"] = {
                                    "content" : kuchikomi_text,
                                    "date" : kuchikomi_date.strftime("%Y-%m-%d"),
                                    "stars" : ""
                                }
                                num_review += 1

                print(f"Hospital {hospital_name} - {num_kuchikomi_list} pages of reviews downloaded.")
                num_kuchikomi_list += 1
            this_clinic_data['reviews']['qlife'] = reviews_dict
            data.append(this_clinic_data)

        return data
