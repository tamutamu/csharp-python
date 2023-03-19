from pprint import pprint
import requests

# urlを設定
url = f"https://api.mercari-shops.com/graphql"
token = "msp_ax2fjLP9pZkoWjLQHGoy6g_g37d6LrQSFAHiNKy1FNnEpFbLmmKn1eo19fHmxPV19z8"

# headersを設定
# 重要: Content-typeはapplication/graphqlではなくapplication/jsonじゃないと動かない
headers = {
    "Content-Type": "application/json",
    "Authorization": f"msp_ax2fjLP9pZkoWjLQHGoy6g_g37d6LrQSFAHiNKy1FNnEpFbLmmKn1eo19fHmxPV19z8",
}

print(headers)

# graphqlのqueryを記述
query = """{
        }"""

# requestする
response = requests.post(
    url,
    data={"query": query},
    headers=headers
)

pprint(response)
