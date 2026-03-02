from flask import Flask, jsonify

app = Flask(__name__)

# Simulated Nsongwa Credit Union Data
member_data = {
    "union_name": "Nsongwa Credit Union",
    "account_holder": "Board Demonstration User",
    "balance_xaf": 500000,
    "status": "SECURE",
    "currency": "XAF"
}

@app.route('/api/v1/balance')
def get_balance():
    return jsonify(member_data)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)