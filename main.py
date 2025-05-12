from flask import Flask, request, render_template, send_file, redirect, url_for
import csv, os
from werkzeug.utils import secure_filename
from searcher import fetch_product_details
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    download_file = None

    if request.method == "POST":
        uploaded_file = request.files["csv_file"]
        if uploaded_file.filename.endswith(".csv"):
            filename = secure_filename(uploaded_file.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            uploaded_file.save(input_path)

            with open(input_path, encoding='utf-8') as f:
                reader = csv.DictReader(f)
                products = list(reader)

            for p in products:
                name = p['Product Name']
                data = fetch_product_details(name)
                if data:
                    if data['product_price'] == "":
                        data['product_price'] = "TBD"
                    if data['product_price'] == data['product_price_orginal']:
                        data['product_price'] += "(Manually Check)"
                    link = f"https://www.iotmart.com/s/product/detail/{data['product_id']}?language=en_US" if data.get("product_id") else ""
                    results.append({
                        "Product Name": name,
                        "Product Image": "",
                        "Part NumberDesc": data.get("product_description", ""),
                        "Product Price": "US$" + data["product_price"],
                        "Product Link": link
                    })

            # 存儲結果 CSV，檔名唯一化避免衝突
            original_name = os.path.splitext(uploaded_file.filename)[0]
            safe_name = secure_filename(original_name)
            download_filename = f"result_{safe_name}.csv"
            output_path = os.path.join(OUTPUT_FOLDER, download_filename)
            with open(output_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["Product Name", "Product Image", "Part NumberDesc", "Product Price", "Product Link"])
                writer.writeheader()
                writer.writerows(results)

            download_file = download_filename

    return render_template("index.html", results=results, download_file=download_file)

@app.route("/download/<filename>")
def download(filename):
    return send_file(
        os.path.join(OUTPUT_FOLDER, filename),
        as_attachment=True,
        download_name=filename
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)