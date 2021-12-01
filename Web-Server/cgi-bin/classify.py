
import fetch_data
import json
import predict
import requests
import sys


def is_news_site(site):
    url = "https://www.klazify.com/api/categorize"
    payload = "{\"url\":\"https://" + site + "\"}\n"
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/json",
        'Authorization': "Bearer <YOUR-KLAZIFY-API-KEY>",
        'cache-control': "no-cache"
    }

    try:
        response = requests.request("POST", url, data=payload, headers=headers)
        data = response.json()
        category = data["domain"]["categories"][0]["name"]
        if category.startswith("/News"):
            return True
        else:
            return False
    except:
        return False


def parse_interesting_characteristics():
    site_data = open("<PATH-TO-WORKING-DIRECTORY>\site_data.csv", "r")

    for data in site_data:
        data_split = data.split(",")

        registrar = data_split[1];
        domain_age = data_split[6];
        novelty_tld = data_split[15];

        trusted_registrars = ["Network Solutions LLC", "MarkMonitor Inc.", "CSC CORPORATE DOMAINS INC."]
        if registrar and registrar in trusted_registrars:
            registrar = "Yes"
        else:
            registrar = "No"

        if domain_age and float(domain_age) > 14.99:
            domain_age = "Yes"
        else:
            domain_age = "No"

        if novelty_tld and novelty_tld == "No":
            novelty_tld = "Yes"
        else:
            novelty_tld = "No"

        return registrar, domain_age, novelty_tld

def main(argv):
    site = argv[1]

    response = {}

    if is_news_site(site):
        fetch_data.run(site)
        response["score"] = predict.run()
        (response["trustedRegistrar"], response["trustedDomainAge"], response["trustedTLD"]) = parse_interesting_characteristics()
    else:
        response["score"] = "-1"
        response["trustedRegistrar"] = ""
        response["trustedDomainAge"] = ""
        response["trustedTLD"] = ""

    print(json.dumps(response), end='')


if __name__ == "__main__":
    main(sys.argv)
