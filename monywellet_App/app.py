import os
import pymysql
from flask import Flask, render_template, request, url_for, redirect, flash, session, jsonify 

pymysql.install_as_MySQLdb()

# 1. முதலில் 'app' ஐ உருவாக்க வேண்டும்!
app = Flask(__name__, static_url_path='/static')
app.secret_key = 'secret123'
CORRECT_PASSWORD = "1234"

# 2. அதற்குப் பிறகுதான் UPLOAD_FOLDER ஐ 'app'-க்குள் செட் செய்ய வேண்டும்!
UPLOAD_FOLDER = 'static/uploads/profile_pics'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# இந்த ஃபோல்டர் இல்லை என்றால் பைத்தானே உருவாக்கிவிடும்
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Simple translations dictionary for English (en) and Tamil (ta)
TRANSLATIONS = {
    'en': {
        'lang_tamil': 'தமிழ்',
        'lang_english': 'English',
        'login_title': 'Login Wallet',
        'login_sub': 'Secure access to your digital wallet payment',
        'user_id': 'User ID',
        'password': 'Password',
        'mobile_number': 'Mobile Number',
        'login_now': 'Login Now',
        'new_register': 'New Register Wallet Payment?',
        'register_here': 'Register Here',
        'sent_any': 'Sent Anyone',
        'bank_transfer': 'Bank Transfer',
        'mobile_recharge': 'Mobile Recharge',
        'help_text': 'Help People You Trust Make Payments',
        'settings': 'Settings',
        'manage_google': 'Manage Google Account',
        'get_help': 'Get Help',
        'language': 'Language',
        'logout': 'Logout',
        'home': 'Home',
        'money': 'Money',
        'about': 'About',
        'register_title': 'MoneyWallet Registration',
        'register_sub': 'Create your secure payment wallet account',
        'full_name': 'Full Name',
        'create_pin': 'Create Security PIN',
        'continue_register': 'Continue & Register',
        'already_registered': 'Already Registered Wallet Payment?',
        'login_here': 'Login Here',
            'transaction': 'Transaction',
            'names': 'Names',
            'amount_col': 'Amount',
            'sent': 'Sent',
            'received': 'Received',
            'no_transactions': 'No transactions found.',
            'transaction_check': 'Transaction Check',
            'view_history': 'View History',
            'balance_amount': 'Balance Amount',
            'current_balance': 'Current Balance',
            'receiver_id': "Receiver User ID",
            'amount_label': 'Amount (₹)',
            'send_money': 'Send Money',
            'back_home': 'Back to Home',
            'enter_pin': 'Enter 4-Digit Security PIN',
            'verify_proceed': 'Verify & Proceed',
            'pin_error': 'Something went wrong. Try again!',
            'welcome_wallet': 'Welcome To Wallet',
            'enter_mobile_number': 'Enter the Mobile Number',
            'enter_10_digits': 'Please enter a 10 digit number.'
            ,
            'check_balance': 'Check Balance'
            ,
            'success': 'Successfully',
            'hello': 'Hello'
    },
    'ta': {
        'lang_tamil': 'தமிழ்',
        'lang_english': 'ஆங்கிலம்',
        'login_title': 'லாகின் வாலெட்',
        'login_sub': 'உங்கள் டிஜிட்டல் வாலெட்டுக்கு பாதுகாப்பான அணுகல்',
        'user_id': 'பயனர் ஐடி',
        'password': 'கடவுச்சொல்',
        'mobile_number': 'மொபைல் எண்',
        'login_now': 'உள்நுழையவும்',
        'new_register': 'புது பதிவு தேவையா?',
        'register_here': 'பதிவு செய்யவும்',
        'sent_any': 'யாருக்காவது அனுப்பு',
        'bank_transfer': 'வங்கி பரிமாற்றம்',
        'mobile_recharge': 'மொபைல் ரீச்சார்ஜ்',
        'help_text': 'நீங்கள் நம்பும் நபர்களுக்கு பணத்தை அனுப்ப உதவுங்கள்',
        'settings': 'அமைப்புகள்',
        'manage_google': 'கூகிள் கணக்கை நிர்வகிக்கவும்',
        'get_help': 'உதவி பெறுக',
        'language': 'மொழி',
        'logout': 'வெளியேறு',
        'home': 'முகப்பு',
        'money': 'பணம்',
        'about': 'பற்றி',
        'register_title': 'மணிவாலெட் பதிவு',
        'register_sub': 'உங்கள் பாதுகாப்பான பணப்பைத்தியை உருவாக்குக',
        'full_name': 'பெயர்',
        'create_pin': 'பின் எண்ணை உருவாக்கவும்',
        'continue_register': 'தொடரவும் & பதிவு',
        'already_registered': 'ஏற்கனவே பதிவு செய்தவரா?',
        'login_here': 'இங்கே உள்நுழையுங்கள்',
            'transaction': 'பரிவர்த்தனை',
            'names': 'பெயர்கள்',
            'amount_col': 'தொகை',
            'sent': 'அனுப்பப்பட்டது',
            'received': 'பெறப்பட்டது',
            'no_transactions': 'பரிவர்தனைகள் இல்லை.',
            'transaction_check': 'பரிவர்த்தனை சரிபார்',
            'view_history': 'பதிவுகளைப் பார்க்கவும்',
            'balance_amount': 'இருமதுக் தொகை',
            'current_balance': 'தற்போதைய இருப்பு',
            'receiver_id': 'பெறுநர் பயனர் ஐடி',
            'amount_label': 'தொகை (₹)',
            'send_money': 'பணம் அனுப்பு',
            'back_home': 'முகப்புக்கு திரும்பு',
            'enter_pin': '4 இலக்க பாதுகாப்பு PIN ஐ உள்ளிடவும்',
            'verify_proceed': 'சரிபார்த்து முன்னேறு',
            'pin_error': 'ஏதோ சிக்கல் உருவானது. மீண்டும் முயற்சிக்கவும்!',
            'welcome_wallet': 'வாலெட்டுக்கு வருக',
            'enter_mobile_number': 'மொபைல் எண்ணை உள்ளிடவும்',
            'enter_10_digits': '10 இலக்க எண்ணை உள்ளிடவும்.'
            ,
            'check_balance': 'மீதமுள்ள இருப்பை சரிபார்'
            ,
            'success': 'வெற்றிகரமாக',
            'hello': 'வணக்கம்'
    }
}


@app.route('/set_language/<lang>')
def set_language(lang):
    # Accept only supported languages
    if lang not in ('en', 'ta'):
        lang = 'en'
    session['lang'] = lang
    # redirect back to previous page or home
    return redirect(request.referrer or url_for('home'))


@app.context_processor
def inject_translations():
    lang = session.get('lang', 'en')
    def trans(key):
        return TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
    return dict(trans=trans, current_lang=lang)

# Database connection function 
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="userdb",
        cursorclass=pymysql.cursors.DictCursor
        
    )
@app.route('/')
@app.route('/registration_page')
def registration_page():
    session.pop('logged_in_user', None) # இது செஷனில் இருந்த ID-யை நீக்குகிறது, இதனால் புதிய பயனர் பதிவு செய்யும் போது பழைய பயனர் ID-யுடன் குழப்பம் ஏற்படாது
    return render_template('register.html') 

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    userid = request.form['userid']
    password = request.form['password']
    email = request.form['email']
    epassword = request.form['epassword']
    mobile = request.form['mobile']
    pin = request.form['pin']


    if not mobile.isdigit() or len(mobile) != 10:
        flash('பதிவு தோல்வி! மொபைல் எண் கண்டிப்பாக 10 இலக்க எண்களாக மட்டுமே இருக்க வேண்டும்.')
        return redirect(url_for('registration_page'))

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 7 columns = 7 values (%s)
        sql = "INSERT INTO users (name, userid, password, email, epassword, mobile, balance, pin) VALUES (%s, %s, %s, %s, %s, %s, 500, %s)"
        cursor.execute(sql, (name, userid, password, email, epassword, mobile, pin))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Register Successfully')
        return redirect(url_for('loginpage')) # இது கீழேயுள்ள பங்க்ஷனை அழைக்கும்
    except Exception as e:
        return f"Error: {str(e)}" # ஏதாவது டேட்டாபேஸ் எரர் இருந்தால் இங்கே காட்டும்
    
    

@app.route('/loginpage', methods=['GET', 'POST']) # Rendu methods-um inge venum
def loginpage():
    if request.method == 'GET' and 'logged_in_user' in session:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # --- Login Logic ---
        userid = request.form.get('userid').strip() # HTML-ல் இருந்து வரும் ID-யை எடுத்து, அதன் முன்/பின் உள்ள இடங்களை நீக்குகிறோம்
        password = request.form.get('password')
        # mobile = request.form.get('mobile')

        if userid.isdigit() and len(userid) != 10:
            flash('தவறான மொபைல் எண்! 10 இலக்கங்களை சரியாக உள்ளிடவும்.')
            return redirect(url_for('loginpage'))

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            sql = "SELECT * FROM users WHERE userid = %s AND password = %s"
            cursor.execute(sql, (userid, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['logged_in_user'] = user['userid'] 
                # செஷன் சேமிக்க மறக்க வேண்டாம்
                return redirect(url_for('home')) 
                # 'dashboard'-ஐ 'home' என மாற்றவும் # '#' ku badhila 'dashboard'
            else:
                flash('Invalid ID or Password!')
                return redirect(url_for('loginpage'))
        except Exception as e:
            return f"Error: {str(e)}"
    
    # --- GET Logic (Mudhala page open aagum podhu) ---
    return render_template('loginpage.html')

@app.route('/home')
def home():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
        
    uid = session['logged_in_user']
    lang = session.get('lang', 'en')  # செஷனில் மொழி இல்லை என்றால் 'en' (English) எடுக்கும்
    
    # டேட்டாபேஸிலிருந்து பயனரின் ப்ரொஃபைல் படத்தை எடுக்கிறோம்
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT profile_pic FROM users WHERE userid = %s", (uid,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # பயனர் படம் வைத்திருக்கவில்லை என்றால் default.png செட் செய்கிறோம்
    profile_pic = 'default.png'
    if user_data:
        # உங்கள் டேட்டாபேஸ் டிக்ஷ்னரியாக இருந்தால் user_data['profile_pic'], இல்லையெனில் user_data[0]
        profile_pic = user_data['profile_pic'] if isinstance(user_data, dict) else user_data[0]
        if not profile_pic:
            profile_pic = 'default.png'
            
    # முக்கியம்: Homepage.html-க்குத் தேவையான trans, lang, profile_pic மூன்றையும் அனுப்புகிறோம்
    return render_template('Homepage.html', lang=lang, profile_pic=profile_pic)
@app.route('/check_pin', methods=['POST'])
def check_pin():
    if 'logged_in_user' not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    data = request.json
    user_pin = data.get('pin') # HTML-ல் இருந்து வரும் பின் எண்
    uid = session['logged_in_user']
   

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # லாகின் செய்த பயனரின் PIN எண்ணை மட்டும் எடுக்கிறோம்
        cursor.execute("SELECT pin FROM users WHERE userid = %s", (uid,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user_data:
            return jsonify({"status": "error", "message": "User profile not found!"})

        # டேட்டாபேஸ் அமைப்பிற்கு ஏற்ப (Dict அல்லது Tuple) பின்னை எடுக்கிறோம்
        correct_pin = user_data['pin'] if isinstance(user_data, dict) else user_data[0]
        
        # PIN-ஐ ஒப்பிட்டுப் பார்க்கிறோம்
        if str(user_pin) != str(correct_pin):
            return jsonify({"status": "error", "message": "Incorrect PIN Number! Please try again."})
        session['pin_verified'] = True
        # PIN சரியாக இருந்தால், பேலன்ஸ் காட்டும் பக்கத்தின் URL-ஐ (url_for('balance')) அனுப்புகிறோம்
        return jsonify({"status": "success", "redirect": url_for('balance')})
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database Error: {str(e)}"})

@app.route('/transfer_check_pin', methods=['POST'])
def transfer_check_pin():
    if 'logged_in_user' not in session:
        return jsonify({"status": "error", "message": "Please login first!"})

    data = request.json
    user_pin = data.get('transfer_pin') # HTML-ல் இருந்து வரும் பின் எண்
    uid = session['logged_in_user']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # லாகின் செய்த பயனரின் PIN எண்ணை மட்டும் எடுக்கிறோம்
        cursor.execute("SELECT pin FROM users WHERE userid = %s", (uid,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data and user_data['transfer_pin'] == user_pin:
            session['pin_verified'] = True
            return jsonify({"status": "success", "redirect": url_for('tranfer')})
        else:
            return jsonify({"status": "error", "message": "Incorrect PIN Number!"})
            
    except Exception as e:
        return jsonify({"status": "error", "message": f"Database Error: {str(e)}"})


@app.route('/balance')
def balance():
    # 1. User login panni irukkara nu check panrom
    if 'logged_in_user' not in session:
        
        return redirect(url_for('loginpage'))
    
    if not session.get('pin_verified'):
        flash("Please enter your PIN first.")
        return redirect(url_for('pin'))

    uid = session['logged_in_user']
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 2. Database-la irunthu balance edukkirom
        cursor.execute("SELECT balance FROM users WHERE userid = %s", (uid,))
        user_data = cursor.fetchone()

        cursor.execute("""
            SELECT id, receiver_id AS name, amount, 'Sent' AS type, timestamp FROM transactions WHERE sender_id = %s
            UNION ALL
            SELECT id, sender_id AS name, amount, 'Received' AS type, timestamp FROM transactions WHERE receiver_id = %s
            ORDER BY id DESC
        """, (uid, uid))
        
        history = cursor.fetchall()
        cursor.close()
        
        session['pin_verified'] = False # Balance page-ku vandha pin-verified status-a false panrom, next time balance check panna pin verify panna vendum
        
        # 3. Data iruntha template-ku anupuroam, illana home-ku redirect panroam
        if user_data and 'balance' in user_data:
            return render_template('balance.html', balance=user_data['balance'], transactions=history)
        else:
            flash("Balance information not found in our records.")
            return redirect(url_for('home')) # Inga balance-ku thiruppi anupuna thaan loop aagum

    except Exception as e:
        return f"Database Error: {str(e)}"
    
    finally:
        if conn:
            conn.close()
            
@app.route('/about')
def about():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
        
    uid = session['logged_in_user']
    lang = session.get('lang', 'en')
    
    # டேட்டாபேஸிலிருந்து தற்போதைய பயனர் (Current User)-ன் ப்ரொஃபைல் படத்தை எடுக்கிறோம்
   # டேட்டாபேஸிலிருந்து ப்ரொஃபைல் படத்தை எடுக்கிறோம்
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, userid, mobile, profile_pic FROM users WHERE userid = %s", (uid,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()
    
    profile_pic = 'default.png'
    if user_data:
        profile_pic = user_data['profile_pic'] if isinstance(user_data, dict) else user_data[1]
        if not profile_pic:
            profile_pic = 'default.png'

    # தட்டச்சுப் பிழையை (trans=trans என) இங்குக் குணப்படுத்தியுள்ளோம்:
    return render_template('About.html', lang=lang, profile_pic=profile_pic, user=user_data)
@app.route('/tranfer')
def tranfer():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))

    uid = session['logged_in_user']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE userid = %s", (uid,))
    user_data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user_data:
        flash("User not found. Please login again.")
        return redirect(url_for('loginpage'))

    return render_template('tranfer.html', balance=user_data['balance'])

@app.route('/transfer_logic', methods=['POST'])
def transfer_logic():
    if 'logged_in_user' not in session:
        flash("Please login first!", "danger")
        return redirect(url_for('loginpage'))
        
    sender_id = session['logged_in_user']
    
    # FIX: Read from request.form instead of request.json
    receiver_id = request.form.get('receiver_id')
    amount_str = request.form.get('amount')
    pin_input = request.form.get('pin')
    
    if not receiver_id or not amount_str or not pin_input:
        flash("All fields are required!", "danger")
        return redirect(url_for('transfer_pin'))
        
    try:
        amount = float(amount_str)
    except ValueError:
        flash("Invalid amount format!", "danger")
        return redirect(url_for('transfer_pin'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. PIN Verification
    cursor.execute("SELECT pin, balance FROM users WHERE userid = %s", (sender_id,))
    sender_data = cursor.fetchone()
    
    if not sender_data:
        cursor.close()
        conn.close()
        flash("Sender profile not found!", "danger")
        return redirect(url_for('tranfer'))
        
    correct_pin = sender_data['pin'] if isinstance(sender_data, dict) else sender_data[0]
    current_balance = sender_data['balance'] if isinstance(sender_data, dict) else sender_data[1]

    # FIX: Flash error and redirect instead of returning JSON
    if str(pin_input) != str(correct_pin):
        cursor.close()
        conn.close()
        flash("Incorrect PIN Number! Please try again.", "danger")
        # Redirect back to transfer_pin, but we need to pass receiver_id and amount back
        return render_template('transfer_pin.html', receiver_id=receiver_id, amount=amount)

    # 2. Balance Check
    if current_balance < amount:
        cursor.close()
        conn.close()
        flash("Insufficient balance!", "danger")
        return redirect(url_for('tranfer'))

    # 3. Receiver Verification
    cursor.execute("SELECT userid FROM users WHERE userid = %s", (receiver_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        flash("Receiver User ID not found!", "danger")
        return redirect(url_for('tranfer'))

    # 4. Money Transfer Execution
    try:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE userid = %s", (amount, sender_id))
        cursor.execute("UPDATE users SET balance = balance + %s WHERE userid = %s", (amount, receiver_id))
        
        sql_transaction = "INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)"
        cursor.execute(sql_transaction, (sender_id, receiver_id, amount))
        
        conn.commit()
        flash(f"₹{amount:.2f} sent successfully to {receiver_id}!", "success")
        return redirect(url_for('tranfer'))
        
    except Exception as e:
        conn.rollback()
        flash("Transaction failed due to a server error.", "danger")
        return redirect(url_for('tranfer'))
    finally:
        cursor.close()
        conn.close()
@app.route('/pin')
def pin():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
    
    receiver_id = request.args.get('receiver_id', '')
    amount = request.args.get('amount', '')

    return render_template('pin.html', receiver_id=receiver_id, amount=amount)

@app.route('/transfer_pin', methods=['GET', 'POST'])
def transfer_pin():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
        
    if request.method == 'POST':
        # HTML Form-ல் இருந்து தரவை எடுக்கிறோம்
        receiver_id = request.form.get('receiver_id')
        amount = request.form.get('amount')
        
        # தரவுகள் சரியாக வருகிறதா என்று பார்க்க Terminal-ல் பிரிண்ட் செய்து சரிபார்க்கலாம்
        print(f"Debug: Receiver={receiver_id}, Amount={amount}") 
        
        return render_template('transfer_pin.html', receiver_id=receiver_id, amount=amount)
        
    return redirect(url_for('tranfer'))


@app.route('/logout')
def logout():
    session.pop('logged_in_user', None)
    return redirect(url_for('loginpage'))

@app.route('/search_user', methods=['GET'])
def search_user():
    search_id = request.args.get('userid', '').strip()
    if not search_id:
        return jsonify({'success': False, 'name': ''})

    conn = None
    try:
        conn = get_db_connection()  # உங்கள் app.py-ல் உள்ள டேட்டாபேஸ் கனெக்ஷன் பங்க்ஷன்
        cursor = conn.cursor()
        # பயனர் ஐடி பொருந்துகிறதா என்று தேடுகிறது
        cursor.execute("SELECT name FROM users WHERE userid = %s", (search_id,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            # result என்பது டிக்ஸ்னரி அல்லது டூப்பிள் ஆக இருக்கும் (உங்கள் fetchone அமைப்பைப் பொறுத்து)
            # பொதுவாக உங்கள் கோப்பில் user['name'] அல்லது result[0] என இருக்கும்.
            user_name = result['name'] if isinstance(result, dict) else result[0]
            return jsonify({'success': True, 'name': user_name})
        else:
            return jsonify({'success': False, 'name': 'User Not Found!'})
            
    except Exception as e:
        return jsonify({'success': False, 'name': 'Error occurred!'})
    finally:
        if conn:
            conn.close()

@app.route('/chat_list')
def chat_list():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
    
    uid = session['logged_in_user']
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # பயனர் இதுவரை சாட் செய்த நபர்களின் பட்டியலை எடுக்க (Distinct users from transactions or a new chat table)
    # தற்போதைக்கு எளிமையாக, பணம் அனுப்பிய/பெற்ற பயனர்களின் பட்டியலை Chat List-ஆகக் காட்டலாம்:
    cursor.execute("""
        SELECT u.userid AS user_id, u.profile_pic 
        FROM users u 
        WHERE u.userid IN (
            SELECT receiver_id FROM messages WHERE sender_id = %s
            UNION
            SELECT sender_id FROM messages WHERE receiver_id = %s
            UNION
            SELECT receiver_id FROM transactions WHERE sender_id = %s
            UNION
            SELECT sender_id FROM transactions WHERE receiver_id = %s
        )           
    """, (uid, uid, uid, uid))
    
    chats = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('chat_list.html', chats=chats)

@app.route('/chat/<receiver_id>')
def chat_room(receiver_id):
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
    
    uid = session['logged_in_user']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    # பெறுநரின் பெயரை எடுக்க
    cursor.execute("SELECT name FROM users WHERE userid = %s", (receiver_id,))
    receiver = cursor.fetchone()
   
    
    if not receiver:
        flash("User not found!")
        return redirect(url_for('chat_list'))
        
    receiver_name = receiver['name'] if isinstance(receiver, dict) else receiver[0]

    cursor.execute("""
        UPDATE messages 
        SET is_read = 1 
        WHERE sender_id = %s AND receiver_id = %s AND is_read = 0
    """, (receiver_id, uid))
    conn.commit()

    # முக்கியமானது: User1 மற்றும் User2 இருவருக்கும் இடையே நடந்த பழைய மெசேஜ்களை எடுக்கிறோம்
    cursor.execute("""
        SELECT sender_id, receiver_id, message, DATE_FORMAT(timestamp, '%%h:%%i %%p') AS msg_time
        FROM messages 
        WHERE (sender_id = %s AND receiver_id = %s) 
           OR (sender_id = %s AND receiver_id = %s)
        ORDER BY timestamp ASC
    """, (uid, receiver_id, receiver_id, uid))
    
    chat_messages = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('chat_room.html', 
                           receiver_id=receiver_id, 
                           receiver_name=receiver_name, 
                           chat_messages=chat_messages, 
                           current_user=uid)

@app.route('/send_message', methods=['POST'])
def send_message():
    if 'logged_in_user' not in session:
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401
        
    sender_id = session['logged_in_user']
    receiver_id = request.form.get('receiver_id')
    message_text = request.form.get('message')
    
    if not receiver_id or not message_text:
        return jsonify({'status': 'error', 'message': 'Missing data'}), 400
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # மெசேஜை டேட்டாபேஸில் சேமிக்கிறோம்
    cursor.execute("""
        INSERT INTO messages (sender_id, receiver_id, message) 
        VALUES (%s, %s, %s)
    """, (sender_id, receiver_id, message_text))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status': 'success'})

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():
    if 'logged_in_user' not in session:
        return redirect(url_for('loginpage'))
        
    if 'profile_image' not in request.files:
        flash('No file part')
        return redirect(url_for('home'))
        
    file = request.files['profile_image']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('home'))
        
    if file:
        uid = session['logged_in_user']
        # படத்தின் பெயரை பயனரின் ஐடி உடன் சேர்த்து தனித்துவமாக மாற்றுகிறோம் (எ.கா: manoj_profile.jpg)
        filename = secure_filename(f"{uid}_{file.filename}")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # டேட்டாபேஸில் புதிய படத்தின் பெயரை அப்டேட் செய்கிறோம்
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET profile_pic = %s WHERE userid = %s", (filename, uid))
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Profile picture updated successfully!')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)