
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)  # 啟用 CORS，讓前端可以跨網域請求

# 1. 連線到 MySQL 資料庫
db = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    database='fin'
)

# 2. 建立 /product 路由
@app.route('/product', methods=['GET'])
def get_product():
    # 從 GET 參數裡取得條碼
    barcode = request.args.get('barcode')

    # 建立資料庫游標
    cursor = db.cursor()
    sql = "SELECT * FROM products WHERE barcode=%s"
    cursor.execute(sql, (barcode,))

    result = cursor.fetchone()
    if not result:
        return jsonify({ "message": "找不到此商品" }), 404

    # 假設表欄位順序是 (id, barcode, name, price, image_url)
    product = {
        "id": result[0],
        "barcode": result[1],
        "name": result[2],
        "price": float(result[3]),
        "image_url": result[4]
    }
    return jsonify(product)

# 3. 啟動 Flask 伺服器
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
