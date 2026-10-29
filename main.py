from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'woldia_city_admin_secret_key_2026'  # ለአስተዳዳሪ ሴክሽን (Session) ማስጠበቂያ

# የኢን-ሜሞሪ ዴታቤዝ ምትክ (ለጊዜው መረጃዎችን እዚህ እንይዛለን፤ ወደፊት በ PostgreSQL ወይም SQLite መቀየር ይቻላል)
feedbacks_db = []
cqms_db = []

@app.route('/')
def home():
    return render_template('index.html')

# የደንበኛ አስተያየት መቀበያ API (ከዲጂታል ፊርማ እና ከቀን/ሰዓት ጋር)
@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    date_time = data.get('dateTime')
    signature = data.get('signature') # Base64 ፊርማ ፎርማት

    # መረጃውን በሰርቨር ሊስት ውስጥ መዝገብ
    feedback_entry = {
        'name': name,
        'email': email,
        'message': message,
        'dateTime': date_time,
        'has_signature': bool(signature)
    }
    feedbacks_db.append(feedback_entry)

    return jsonify({
        'success': True, 
        'message': f'እናመሰግናለን {name}! አስተያየትዎ እና ፊርማዎ በተሳካ ሁኔታ ተመዝግቧል።'
    })

# የአስተዳዳሪ መግቢያ PageRoute
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # ጀርባ ላይ የሚገባውን መረጃ መቀበል (FormData ወይም JSON)
        email = request.form.get('email') or (request.json.get('email') if request.is_json else None)
        password = request.form.get('password') or (request.json.get('password') if request.is_json else None)
        
        # ቀላል የአስተዳዳሪ ማረጋገጫ (Admin Authentication)
        if email == 'admin@woldiacityadmin.gov.et' and password == 'Woldia@2026#Admin':
            session['is_admin'] = True
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('admin_dashboard')})
            return redirect(url_for('admin_dashboard'))
        else:
            if request.is_json:
                return jsonify({'success': False, 'message': 'የተሳሳተ ኢሜይል ወይም የይለፍ ቃል!'}), 401
            return render_template('admin_login.html', error='የተሳሳተ ኢሜይል ወይም የይለፍ ቃል!')
            
    return render_template('admin_login.html')

# የአስተዳዳሪ ዳሽቦርድ (Protected Route - በሎጊን ብቻ የሚከፈት)
@app.route('/admin')
def admin_dashboard():
    # አስተዳዳሪ መሆኑን ማረጋገጥ (Access Control)
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    # መረጃዎችን ወደ ዳሽቦርዱ መላክ
    return render_template('admin.html', feedbacks=feedbacks_db, cqms_records=cqms_db)

# ከእንግዲህ ወዲያ ሲወጡ (Logout)
@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    return redirect(url_for('admin_login'))

if __name__ == '__main__':
    app.run(debug=True)
