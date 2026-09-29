import os
from flask import Flask, render_template, request, jsonify
import requests
import base64

app = Flask(__name__)

# 4. Key Configuration
SECRET_KEY = os.environ.get("TOSS_SECRET_KEY", "test_gsk_docs_OaPz8L5KdmQXkzRz3y47BMw6")

def get_auth_header():
    # Secret Key encoding: SecretKey + ":" and then Base64 encode
    auth_str = f"{SECRET_KEY}:"
    encoded_auth = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
    return {"Authorization": f"Basic {encoded_auth}"}

@app.route('/')
def index():
    # 17. GET / : index.html
    return render_template('index.html')

@app.route('/success')
def success():
    # 17. GET /success : 쿼리의 paymentKey, orderId, amount를 받아 서버에서 결제 승인 API를 호출한다.
    payment_key = request.args.get('paymentKey')
    order_id = request.args.get('orderId')
    amount_str = request.args.get('amount')

    if not all([payment_key, order_id, amount_str]):
        return "Missing required parameters", 400

    try:
        amount = int(amount_str)
    except ValueError:
        return "Invalid amount format", 400

    # 19. Check if amount is 1000
    if amount != 1000:
        return f"Amount mismatch Error: Expected 1000, got {amount}", 400

    # Call Toss Payments Approval API
    # Reference: https://docs.tosspayments.com/reference/payments/confirm
    api_url = f"https://api.tosspayments.com/v1/payments/{payment_key}/confirm"
    payload = {
        "orderId": order_id,
        "amount": amount
    }
    
    response = requests.post(
        api_url,
        json=payload,
        headers=get_auth_header()
    )

    if response.status_code == 200:
        # Success: Show results in table and raw JSON
        result_data = response.json()
        return render_template('success.html', 
                               result=result_data, 
                               raw_json=result_data)
    else:
        # Failure: Show HTTP status and error details
        error_data = response.json()
        return render_template('fail.html', 
                               error_info=error_data,
                               status_code=response.status_code), response.status_code

@app.route('/fail')
def fail():
    # 18. GET /fail : 쿼리의 code, message를 보여 준다.
    code = request.args.get('code')
    message = request.args.get('message')
    return render_template('fail.html', code=code, message=message)

# Note: The templates need to be updated to handle the variables passed from Flask.
# I'll re-write the success/fail templates in the next step to properly use Jinja2.

if __name__ == '__main__':
    app.run(debug=True, port=8000)
