
from collections import defaultdict
from datetime import datetime
from whois.parser import PywhoisError
import ipinfo
import ssl
import socket
import time
import whois


def record(msg_type, msg):
    if outputType is "stdout" or msg_type is "log":
        print(msg)
    elif outputType is "file":
        if msg_type is "log":
            output_log.write(msg + "\n")
        elif msg_type is "data":
            site_data.write(msg + "\n")


def privacy_enabled(identifier):
    lower_id = identifier.lower()
    if "privacy" in lower_id or "private" in lower_id or "redacted" in lower_id or "protect" in lower_id or \
            "domain" in lower_id or "guard" in lower_id or "proxy" in lower_id or "whois" in lower_id or \
            "mask" in lower_id:
        return "Yes"
    else:
        return "No"


def time_elapsed(start=None, end=None, date_format=None):
    try:
        if start is None:
            start_epoch = datetime.now().timestamp()
        else:
            if isinstance(start, list):
                start = start[0]
            if isinstance(start, str):
                start = datetime.strptime(start, date_format)
            start_epoch = start.timestamp()

        if end is None:
            end_epoch = datetime.now().timestamp()
        else:
            if isinstance(end, list):
                end = end[0]
            if isinstance(end, str):
                end = datetime.strptime(end, date_format)
            end_epoch = end.timestamp()

        elapsed_seconds = end_epoch - start_epoch
        elapsed_years = elapsed_seconds / 31536000

        return elapsed_years
    except ValueError as ve:
        print("ERROR!!! ValueError in time_elapsed!")
        print(ve)
        return 0


def fetch_whois_data(result, site):
    try:
        # Fetch WHOIS data
        whois_data = whois.whois(site)
        print(whois_data)

        # Parse data
        registrar = whois_data.registrar if whois_data.registrar is not None else ""
        creation_date = whois_data.creation_date if whois_data.creation_date is not None else ""
        updated_date = whois_data.updated_date if whois_data.updated_date is not None else ""
        expiration_date = whois_data.expiration_date if whois_data.expiration_date is not None else ""
        sld = whois_data.name_servers[0] if whois_data.name_servers is not None else ""

        name = ""
        if isinstance(whois_data.name, list):
            name = whois_data.name[0]
        elif isinstance(whois_data.name, str):
            name = whois_data.name

        org = ""
        if isinstance(whois_data.org, list):
            org = whois_data.org[0]
        elif isinstance(whois_data.org, str):
            org = whois_data.org

        country = ""
        if isinstance(whois_data.country, list):
            country = whois_data.country[0]
        elif isinstance(whois_data.country, str):
            country = whois_data.country

        # Determine interested values
        details_private = privacy_enabled(name)
        domain_age = round(time_elapsed(creation_date, None, "%Y-%m-%d %H:%M:%S"), 2) if creation_date is not "" else "0"
        domain_lifespan = round(time_elapsed(creation_date, expiration_date, "%Y-%m-%d %H:%M:%S"), 2) if creation_date is not "" and expiration_date is not "" else "0"
        until_expiration = round(time_elapsed(None, expiration_date, "%Y-%m-%d %H:%M:%S"), 2) if expiration_date is not "" else "0"
        since_updated = round(time_elapsed(updated_date, None, "%Y-%m-%d %H:%M:%S"), 2) if updated_date is not "" else "0"

        if sld is not "":
            sld = sld[sld.find(".") + 1:]
            sld = sld[:sld.find(".")]
            if "-" in sld:
                sld = sld[:sld.find("-")]

        result[1] = registrar
        result[2] = name
        result[3] = org
        result[4] = country
        result[5] = details_private
        result[6] = str(domain_age)
        result[7] = str(domain_lifespan)
        result[8] = str(until_expiration)
        result[9] = str(since_updated)
        result[14] = sld
    except PywhoisError:
        result[6] = "0"
        result[7] = "0"
        result[8] = "0"
        result[9] = "0"
        record("log", "No WHOIS data found for site: " + site)


def domain_traits(result, site):
    tld = site[site.rfind(".") + 1:]
    domain = site[:site.rfind(".")]
    if domain.startswith("www."):
        domain = domain[4:]

    # Domain length
    result[16] = str(len(domain))

    # "News" in domain
    result[11] = "Yes" if "news" in domain else "No"

    # Digit in domain
    result[12] = "Yes" if any(char.isdigit() for char in domain) else "No"

    # Hyphen in domain
    result[13] = "Yes" if "-" in domain else "No"

    # Common news keywords
    news_keywords = ["24", "365", "abc", "action", "activist", "advance", "alert", "alliance", "alternative", "america", "associate", "blast", "blog", "box", "breaking", "brief", "bulletin", "business", "buzz", "byte", "caller", "cbs", "channel", "christian", "chronicle", "citizen", "city", "club", "cnn", "conservative", "corner", "county", "courier", "currant", "daily", "democracy", "dig", "dispatch", "division", "edition", "editor", "election", "empire", "epoch", "evening", "examiner", "express", "extra", "fact", "feed", "file", "finesser", "flash", "focus", "fox", "free", "fresh", "gazette", "global", "guardian", "hangout", "headline", "herald", "hq", "hub", "idea", "independent", "index", "info", "inquire", "insider", "interesting", "international", "item", "journal", "leak", "learn", "ledger", "liberal", "liberty", "live", "local", "mag", "maga", "mail", "media", "metro", "movement", "nation", "nbc", "network", "now", "observer", "page", "paper", "patriot", "pioneer", "pipe", "plug", "politic", "post", "press", "progress", "proud", "publish", "radio", "react", "read", "record", "region", "religion", "report", "republic", "review", "rumor", "scoop", "sentinel", "share", "sharing", "show", "spirit", "spot", "spotlight", "standard", "star", "state", "statesman", "stories", "story", "studio", "sun", "surge", "syndicate", "telegram", "telegraph", "television", "times", "today", "top", "trend", "tribune", "truth", "tv", "twenty-four", "twentyfour", "uncut", "underground", "union", "update", "us", "usa", "view", "viral", "vision", "washington", "watch", "weekly", "wire", "your", "zine", "zone"]
    result[10] = "Yes" if any(keyword in domain for keyword in news_keywords) else "No"

    common_tld = ["com", "org", "net", "int", "edu", "gov", "mil", "arpa"]
    result[15] = "Yes" if tld not in common_tld and len(tld) > 2 else "No"


def fetch_cert_data(result, site):
    ip = -1
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=site) as s:
            s.connect((site, 443))
            cert = s.getpeercert()
            socket_response = str(s)
            s.close()

        issuer = dict(x[0] for x in cert["issuer"])

        common_name = issuer["commonName"] if issuer["commonName"] is not None else ""
        country = issuer["countryName"] if issuer["countryName"] is not None else ""
        validity_start = cert["notBefore"] if cert["notBefore"] is not None else ""
        validity_end = cert["notAfter"] if cert["notAfter"] is not None else ""

        san_count = 0
        has_wildcard = "No"
        if cert["subjectAltName"] is not None:
            has_wildcard = "Yes" if "*" in str(cert["subjectAltName"]) else "No"

            subject_alt_name = defaultdict(set)
            for type_, san in cert["subjectAltName"]:
                subject_alt_name[type_].add(san)

            san_count = len(subject_alt_name["DNS"])

        lifetime = round(time_elapsed(validity_start, validity_end, "%b %d %H:%M:%S %Y %Z"), 2) if validity_start is not "" and validity_end is not "" else "0"
        expired = "Yes" if validity_end is not "" and time_elapsed(None, validity_end, "%b %d %H:%M:%S %Y %Z") < 0 else "No"

        # Parse out IP address
        ip_with_ending = socket_response[socket_response.find("raddr") + 8:]
        ip = ip_with_ending[:ip_with_ending.find("'")]

        result[17] = "Yes"
        result[18] = "Yes"
        result[19] = common_name
        result[20] = country
        result[21] = str(lifetime)
        result[22] = expired
        result[23] = str(round(san_count, 2))
        result[24] = has_wildcard
        result[25] = "No"

    except:
        result[17] = "No"
        result[18] = "No"
        result[21] = "0"
        result[23] = "0"
        result[25] = "Yes"
        record("log", "SSL connection failed or result empty for site: " + site)

    return ip


def fetch_network_data(result, ip):
    if ip is not -1:
        ip_details = ipinfo.getHandler("<YOUR-IPINFO-API-KEY>").getDetails(ip)

        country = ip_details.country if ip_details.country is not None else ""

        if ip_details.org is not None:
            autonomous_system = ip_details.org[:ip_details.org.find(" ")]
            cdn = ip_details.org[ip_details.org.find(" ") + 1:]

            result[26] = autonomous_system
            result[28] = cdn

        result[27] = country


def clean_result(clean_str):
    temp = "|".join(clean_str)
    temp = temp.replace(",", "")
    temp = temp.replace("|", ",")

    return temp


def main():
    sites = open("<PATH-TO-WORKING-DIRECTORY>\sites.csv", "r")

    for data in sites:
        data_split = data.split(",")
        site = data_split[0]
        score = data_split[1]

        # Clean data
        site = site.rstrip()
        score = score.rstrip()

        # Create result object
        result = [""] * headers_count
        result[0] = site
        result[29] = str(score)

        # Fetch WHOIS details
        record("log", "Fetching WHOIS data for site: " + site)
        fetch_whois_data(result, site)

        # Determine domain traits
        record("log", "Determine domain traits for site: " + site)
        domain_traits(result, site)

        # Fetch certificate details
        record("log", "Fetching certificate data for site: " + site)
        ip = fetch_cert_data(result, site)

        # Fetch network details
        record("log", "Fetching network data for site: " + site)
        fetch_network_data(result, ip)

        final_result = clean_result(result)
        record("log", final_result)
        record("data", final_result)

        time.sleep(1)

    sites.close()


if __name__ == "__main__":
    outputType = "file"  # stdout

    if outputType is "file":
        output_log = open("<PATH-TO-WORKING-DIRECTORY>\output.log", "w")
        site_data = open("<PATH-TO-WORKING-DIRECTORY>\training_data.csv", "w")

    headers = ["Domain",  # 0~
               "Registrar",  # 1~
               "Name",  # 2~
               "Organization",  # 3~
               "Country",  # 4~
               "Private",  # 5~
               "DomainAge",  # 6~
               "DomainLifespan",  # 7~
               "TimeUntilExpiration",  # 8~
               "SinceLastUpdate",  # 9~
               "NewsKeywords",  # 10~
               "NewsInDomain",  # 11~
               "DigitInDomain",  # 12~
               "HyphenInDomain",  # 13~
               "NameServerSLD",  # 14~
               "NoveltyTLD",  # 15~
               "DomainNameLength",  # 16~
               "DomainResolves",  # 17~
               "CertAvailable",  # 18~
               "CertIssuer",  # 19~
               "CertCountry",  # 20~
               "CertLifeTime",  # 21~
               "CertExpired",  # 22~
               "SANCount",  # 23~
               "SANWildCard",  # 24~
               "SelfSignedCert",  # 25~
               "WebsiteAS",  # 26~
               "WebsiteCountry",  # 27~
               "WebsiteCDN",  # 28~
               "Score"  # 29~
               ]
    headers_count = len(headers)

    main()

    if outputType is "file":
        site_data.close()
        output_log.close()
