from flask import Flask, render_template_string, request, session, redirect, url_for
import hashlib  # This line fixes the error in your screenshot!

app = Flask(__name__)
app.secret_key = 'nsongwa_secure_gateway_2026' 

# --- SECURE MEMBER DATABASE ---
members = {
    "1001": {
        "name": "Frank Fru",
        "balance": 450000,
        "pin_hash": hashlib.sha256("Nsongwa#2026!".encode()).hexdigest()[:12],
        "transactions": [] 
    }
}

# --- UI TEMPLATES ---
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<body style="font-family: sans-serif; text-align: center; padding-top: 100px; background: #f0f2f5;">
    <div style="display: inline-block; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <h2 style="color: #004a99;">🏦 Nsongwa Credit Union</h2>
        <p>Member Portal Login</p>
        <form method="POST" action="/login">
            <input type="text" name="user_id" placeholder="Member ID" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <input type="password" name="pin" placeholder="Secret PIN" required style="display: block; width: 200px; margin: 10px auto; padding: 10px; border: 1px solid #ccc; border-radius: 5px;"><br>
            <button type="submit" style="background: #007bff; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">Secure Login</button>
        </form>
    </div>
</body>
</html>
'''

DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<body style="font-family: sans-serif; background: #f0f2f5;">
    <div style="max-width: 600px; margin: 30px auto; background: white; padding: 40px; border-radius: 10px; border-top: 10px solid #28a745; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2>🏦 Nsongwa Credit Union <br> <small>Welcome, {{ name }}!</small></h2>
            <span style="background: #d4edda; color: #155724; padding: 5px 10px; border-radius: 15px; font-size: 0.8em;">ID: {{ uid }}</span>
        </div>
        <hr style="border: 0; border-top: 1px solid #eee;">
        
        <div style="text-align: center; margin: 20px 0;">
            <p style="color: #6c757d; margin-bottom: 5px;">Current Available Balance</p>
            <h1 style="color: #28a745; font-size: 3em; margin: 0;">{{ "{:,}".format(balance) }} XAF</h1>
        </div>

        <div style="background: #fff9db; padding: 20px; border-radius: 8px; border: 1px solid #ffe066; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #856404;">📱 Fast Deposit via MoMo</h4>
            <form method="POST" action="/deposit" style="display: flex; gap: 10px;">
                <input type="number" name="amount" placeholder="Amount (XAF)" required style="flex-grow: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px;">
                <button type="submit" style="background: #ffcc00; color: black; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer;">Deposit</button>
            </form>
        </div>

        <div style="margin-top: 20px;">
            <h4>Recent Activity</h4>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                <tr style="background: #f8f9fa;">
                    <th style="text-align: left; padding: 8px; border-bottom: 1px solid #eee;">Type</th>
                    <th style="text-align: right; padding: 8px; border-bottom: 1px solid #eee;">Amount</th>
                </tr>
                {% for tx in transactions %}
                <tr>
                    <td style="padding: 8px; border-bottom: 1px solid #eee;">MoMo Deposit</td>
                    <td style="padding: 8px; border-bottom: 1px solid #eee; text-align: right; color: #28a745;">+{{ "{:,}".format(tx) }} XAF</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px;">
            <p style="margin: 0; font-size: 0.8em; color: green;">● SECURE SESSION ACTIVE</p>
            <a href="/logout" style="color: #dc3545; text-decoration: none; font-size: 0.9em;">Logout Securely</a>
        </div>
    </div>
</body>
</html>
'''

# --- SERVER ROUTES ---
@app.route('/')
def index():
    if 'user_id' in session:
        user = members[session['user_id']]
        return render_template_string(DASHBOARD_HTML, name=user['name'], balance=user['balance'], uid=session['user_id'], transactions=user['transactions'])
    return render_template_string(LOGIN_HTML)

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('user_id')
    pin = request.form.get('pin')
    if uid in members:
        input_hash = hashlib.sha256(pin.encode()).hexdigest()[:12]
        if input_hash == members[uid]['pin_hash']:
            session['user_id'] = uid
            return redirect(url_for('index'))
    return "<h3>Login Failed</h3><a href='/'>Try again</a>", 401

@app.route('/deposit', methods=['POST'])
def deposit():
    if 'user_id' not in session: return redirect(url_for('index'))
    amount = int(request.form.get('amount'))
    user_id = session['user_id']
    if amount > 0:
        members[user_id]['balance'] += amount
        members[user_id]['transactions'].insert(0, amount)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)