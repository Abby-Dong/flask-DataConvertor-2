# This script is to search product data from the iotmart website using a GET request.
# GET https://www.iotmart.com/en-en/s/global-search/{ProductModelName}?language=en_US
# ProductModelName = "ARK-2251-S3A1U"

import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.iotmart.com/en-en/s/sfsites/aura?r=23&aura.ApexAction.execute=8"

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6,it-IT;q=0.5,it;q=0.4",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "priority": "u=1, i",
    "sec-ch-ua": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-b3-sampled": "1",
    "x-b3-spanid": "8ca7da603b48c067",
    "x-b3-traceid": "d586453016e92df3",
    "x-sfdc-lds-endpoints": "ApexActionController.execute:CC_API_Lib_LWC_SearchController.productSearch, ApexActionController.execute:CC_API_Lib_LWC_SearchController.getCartSummary, ApexActionController.execute:Lib_LWC_AuraEnabled.getWebStore_SupportedLanguage_L, ApexActionController.execute:Lib_LWC_AuraEnabled.getWebStore_SupportedCurrencie_L, ApexActionController.execute:CC_API_Lib_LWC_SearchController.getSortRules, ApexActionController.execute:Lib_LWC_AuraEnabled.getStore_Default_Value",
    "x-sfdc-page-cache": "ae17bde1b97557c5",
    "x-sfdc-page-scope-id": "45e9b52f-cbc8-49c0-bf59-43e8568eb4a4",
    "x-sfdc-request-id": "9169457900002c8523"
}

def fetch_product_details(product_model_name):
    body = {
        "message": '{"actions":[{"id":"805;a","descriptor":"aura://ApexActionController/ACTION$execute","callingDescriptor":"UNKNOWN","params":{"namespace":"","classname":"CC_API_Lib_LWC_SearchController","method":"productSearch","params":{"communityId":"0DB2y000000XZZR","searchQuery":"{\\"searchTerm\\":\\"' + product_model_name + '\\",\\"refinements\\":[],\\"page\\":0,\\"includePrices\\":true}","effectiveAccountId":null},"cacheable":false,"isContinuation":false}}]}',
        "aura.context": '{"mode":"PROD","fwuid":"c1ItM3NYNWFUOE5oQkUwZk1sYW1vQWg5TGxiTHU3MEQ5RnBMM0VzVXc1cmcxMS4zMjc2OC4z","app":"siteforce:communityApp","loaded":{"APPLICATION@markup://siteforce:communityApp":"1233_RswVGF3YJuF30XUGfC3LUQ"},"dn":[],"globals":{},"uad":true}',
        "aura.pageURI": f"/en-en/s/global-search/{product_model_name}?language=en_US",
        "aura.token": "null"
    }
    print(f"Fetching product details for: {product_model_name}")
    response = requests.post(BASE_URL, headers=HEADERS, data=body)
    
    if response.status_code != 200:
        print(f"Failed to fetch product details. Status code: {response.status_code}")
        return None
    result = {}
    result['product_name'] = product_model_name
    result['product_id'] = ""
    result['product_description'] = "(NA)"
    result['product_price'] = ""
    result['product_price_orginal'] = ""

    try:
        data = response.json()
        actions = data.get('actions', [])
        
        for action in actions:
            if action['id'] == "805;a":
                products_result = action['returnValue']['returnValue']['productsPage']['products']

                if (products_result[0]['name'] != product_model_name):
                    print("There is no this %s product in the system." % product_model_name)
                    return result
                # print(f"The result is {products_result[0]}")
                result['product_id'] = products_result[0]['id']
                result['product_name'] = products_result[0]['name']
                result['product_description'] = products_result[0]['fields']['Description']['value']
                result['product_price'] = products_result[0]['priceInfo']['unitPrice']
                result['prduct_price_orginal'] = products_result[0]['priceInfo']['unitPrice_org']
        
        print(f"Product details fetched successfully for: {product_model_name}")
        return result
    except (KeyError, ValueError):
        print("Failed to parse JSON response.")
        return result

if __name__ == "__main__":
    product_model_name = "UNO-2272G-J2AE"
    result = fetch_product_details(product_model_name)
    print(json.dumps(result))
    # Example Output: {'search_results': {...}, 'cart_summary': {...}}
