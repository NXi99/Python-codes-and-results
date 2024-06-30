import requests
import json


countries = ["AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ",
             "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS",
             "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
             "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
             "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF",
             "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
             "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM",
             "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC",
             "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
             "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA",
             "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG",
             "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW",
             "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS",
             "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO",
             "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI",
             "VN", "VU", "WF", "WS", "XK", "YE", "YT", "ZA", "ZM", "ZW"]


def get_nodes_by_country(country_code):
    url = f"https://mempool.space/api/v1/lightning/nodes/country/{country_code}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()["nodes"]  # Assuming 'nodes' is the key containing the list of nodes
    else:
        print(f"Failed to fetch nodes data for {country_code}")
        return []


def extract_high_connectivity_nodes(nodes, min_channels=50):
    """Filter nodes with a high number of channels and sort them."""
    high_conn_nodes = [node for node in nodes if node.get('channels', 0) >= min_channels]
    high_conn_nodes.sort(key=lambda x: x['channels'], reverse=True)  # Sort by number of channels
    return high_conn_nodes


all_high_conn_nodes = []

for country_code in countries:
    nodes_data = get_nodes_by_country(country_code)
    if nodes_data:
        high_conn_nodes = extract_high_connectivity_nodes(nodes_data)
        all_high_conn_nodes.extend(high_conn_nodes)
        print(f"High connectivity nodes data for {country_code} fetched and added.")
    else:
        print(f"No high connectivity nodes data added for {country_code}")


# Save all high connectivity nodes data to a single file
with open("high_connectivity_nodes.json", "w") as f:
    json.dump(all_high_conn_nodes, f)

# Print the total number of high connectivity nodes collected
print(f"Total number of high connectivity nodes collected: {len(all_high_conn_nodes)}")
