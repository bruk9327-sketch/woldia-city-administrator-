from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/feedback', methods=['POST'])
def feedback():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    # እዚህጋ መረጃውን በዳታቤዝ ማስቀመጥ ወይም በኢሜይል መቀበል ይቻላል
    return jsonify({
        'success': True, 
        'message': f'እናመሰግናለን {name}! አስተያየትዎ በተሳካ ሁኔታ ደርሷል።'
    })

if __name__ == '__main__':
    app.run(debug=True)
