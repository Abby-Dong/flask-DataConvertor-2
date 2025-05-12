import sys
import os

# 加入專案根目錄到 sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from searcher import fetch_product_details  # 正確的函式名稱



def scrape_product_data(product_model_name):
    """
    Wrapper function to fetch product details and format them for testing.
    """
    product_details = fetch_product_details(product_model_name)
    if not product_details:
        return None

    # Format the result to match the expected keys in the test
    formatted_result = {
        "part_number_desc": product_details.get("product_description", "(NA)"),
        "price": product_details.get("product_price", ""),
        "link": f"https://www.iotmart.com/en-en/s/global-search/{product_model_name}?language=en_US"
    }
    return formatted_result

if __name__ == "__main__":
    # Example usage
    product_model_name = "WISE-4220-A"
    result = scrape_product_data(product_model_name)
    print(result)
