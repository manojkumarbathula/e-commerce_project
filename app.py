from flask import Flask,request,redirect,url_for,render_template,flash,session,make_response,jsonify
from flask_session import Session
from otp import genotp
import razorpay
from stoken import endata,dndata
from cmail import send_mail
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import re
from io import BytesIO
from xhtml2pdf import pisa
from werkzeug.utils import secure_filename #it checks wheather the file filename consists of unexpected '/',
from mysql.connector import (connection)
load_dotenv()
mydb = connection.MySQLConnection(
    host=os.environ.get('DB_HOST'),
    port=int(os.environ.get('DB_PORT')),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME'),
    ssl_ca=os.environ.get("DB_SSL_CA"),
    ssl_verify_cert=True
)
BASE_DIR=os.path.abspath(os.path.dirname(__file__))#it finds exact app file directory path
print(BASE_DIR)
UPLOAD_FOLDER=os.path.join(BASE_DIR,'static','uploads')
ALLOWED_EXTENSIONS={'png','jpeg','jpg','gif','webp'}
MAX_CONTENT_LENGTH=6 * 1024 * 1024 #6MB
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
client=razorpay.Client(auth=(os.environ.get('RAZORPAY_KEY_ID'),os.environ.get('RAZORPAY_KEY_SECRET')))
app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=MAX_CONTENT_LENGTH
bcrypt=Bcrypt(app)
app.secret_key=os.environ.get('SECRET_KEY')

Session(app)
@app.route('/')
def index():
    return render_template('welcome.html')
@app.route('/home')
def home():
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items')
        items_details=cursor.fetchall()
        print(items_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the items data')
        return redirect(url_for("home"))
    else:
        return render_template('index.html',allitems_details=items_details)
@app.route('/admincreate',methods=['GET','POST'])
def admincreate():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['email']
        address=request.form['address']
        password=request.form['password']
        agree=request.form['agree']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from admindata where adminemail=%s',[useremail])
            email_count=cursor.fetchone()[0] #(1,) or (0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('admincreate'))
        else:
            if email_count==0:
                gotp=genotp()
                admindata={'adminusername':username,'adminemail':useremail,'adminaddress':address,'adminpassword':password,'agree':agree,'server_otp':gotp}
                subject='Admin verification for ECOM APPLICATION'
                body=f'Use the given for verification {gotp}'
                send_mail(to=useremail,subject=subject,body=body)
                flash('otp has been sent to given mail')
                return redirect(url_for('adminotpverify',serverdata=endata(admindata)))
            elif email_count==1:
                flash('user already existed')
    return render_template('admincreate.html')
@app.route('/adminotpverify/<serverdata>',methods=['GET','POST'])
def adminotpverify(serverdata):
    try:
        data=dndata(serverdata)
    except Exception as e:
        print(e)
        flash('Could not verify user details')
        return redirect(url_for('adminotpverify'))
    else:
        if request.method=='POST':
            user_otp=request.form['otp']
            if data['server_otp']==user_otp:
                hash_password=bcrypt.generate_password_hash(data['adminpassword'])
                print(hash_password)
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into admindata(adminid,adminname,adminemail,address,password,agree) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s)',[data['adminusername'],data['adminemail'],data['adminaddress'],hash_password,data['agree']])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('Could not store user details')
                    return redirect(url_for('adminotpverify',serverdata=serverdata))
                else:
                    flash('details registred successfully')
                    return 'login'
            else:
                flash('Invalid OTP')
    return render_template('adminotp.html')
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if request.method=='POST':
        login_useremail=request.form['email']
        login_password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from admindata where adminemail=%s',[login_useremail])
            email_count=cursor.fetchone()[0] #(1,) or (0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('admincreate'))
        else:
            if email_count==1:
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select password from admindata where adminemail=%s',[login_useremail]) 
                    stored_password=cursor.fetchone()[0]
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('could not get password')
                    return redirect(url_for('adminlogin'))
                else:
                    if bcrypt.check_password_hash(stored_password,login_password):
                        print(session)
                        session['admin']=login_useremail
                        print(session)
                        return redirect(url_for('admindashboard'))
                    else:
                        flash('invalid password')
                        return redirect(url_for('adminlogin'))
            elif email_count==0:
                flash('No user found')
                return redirect(url_for('adminlogin'))
            else:
                flash('Email not verified')
    return render_template('adminlogin.html')
@app.route('/admindashboard')
def admindashboard():
    if session.get('admin'):
        return render_template('adminpanel.html')
    else:
        flash('pls login to get dashboard')
        return redirect(url_for('adminlogin'))
def allowed_file(filename:str)->bool:
    return '.' in filename and filename.rsplit('.',1)[-1].lower() in ALLOWED_EXTENSIONS

@app.route('/additem',methods=['GET','POST'])
def additem():
    if session.get('admin'):
        if request.method=='POST':
            item_name=request.form['title']
            item_desc=request.form['Description']
            item_about=request.form['About_item']
            item_category=request.form['category']
            item_price=request.form['price']
            item_quantity=request.form['quantity']
            item_filedata=request.files['file']
            print(item_filedata)
            print(item_filedata.filename)
            item_filename=item_filedata.filename
            if item_filedata and item_filename:
                if not allowed_file(item_filename):
                    flash('File type not allowed: png,jpg,jpeg,webp,gif')
                    return redirect(url_for('additem'))
                #storing data in a static file
                orig_secure=secure_filename(item_filename)
                ext=os.path.splitext(orig_secure)[1] # 'anusha.txt'--->.txt
                print(ext)
                filename=genotp()+ext # creating a new file name
                save_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
                try:
                    item_filedata.save(save_path)
                except Exception as e:
                    app.logger.exception("Failed to save the file")
                    flash('Could not save image')
                    return redirect(url_for("additem"))
                #database save 
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
                    adminid=cursor.fetchone()[0]
                    cursor.execute('insert into items(itemid,item_name,item_description,item_about,price,quantity,item_category,item_imgname,added_by) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s,%s,%s)',[item_name,item_desc,item_about,item_price,item_quantity,item_category,filename,adminid])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    app.logger.exception("Failed to save the item data")
                    flash('Could not save item data')
                    return redirect(url_for("additem"))
                else:
                    flash('item added successfully')
                    return redirect(url_for("additem"))
        return render_template('additem.html')
    else:
        flash('pls login first ')
        return redirect(url_for('adminlogin'))
@app.route('/viewallitems')
def viewallitems():
    if not session.get('admin'):
        flash('pls login to view items')
        return redirect(url_for('adminlogin'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
        adminid=cursor.fetchone()[0]
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where added_by=%s',[adminid])
        items_details=cursor.fetchall()
        print(items_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the items data')
        return redirect(url_for("admindashboard"))
    else:
        return render_template('viewall_items.html',allitems_data=items_details)
@app.route('/viewitem/<itemid>')
def viewitem(itemid):
    if not session.get('admin'):
        flash('pls login to view items')
        return redirect(url_for('adminlogin'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
        adminid=cursor.fetchone()[0]
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where added_by=%s and itemid=uuid_to_bin(%s)',[adminid,itemid])
        item_details=cursor.fetchone()
        print(item_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for("viewallitems"))
    else:
        return render_template('view_item.html',item_data=item_details)
@app.route('/deleteitem/<itemid>')
def deleteitem(itemid):
    if not session.get('admin'):
        flash('pls login to view items')
        return redirect(url_for('adminlogin'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
        adminid=cursor.fetchone()[0]
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where added_by=%s and itemid=uuid_to_bin(%s)',[adminid,itemid])
        item_details=cursor.fetchone() #(135t23,'cup','cup desc',)
        print(item_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for("viewallitems"))
    else:
        try:
            remove_path=os.path.join(app.config['UPLOAD_FOLDER'],item_details[7])
            print(remove_path)
            os.remove(remove_path)
        except Exception as e:
            print(e)
            flash('could not remove file')
            return redirect(url_for('viewallitems'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
        adminid=cursor.fetchone()[0]
        cursor.execute('delete from items where added_by=%s and itemid=uuid_to_bin(%s)',[adminid,itemid])
        mydb.commit()
        cursor.close()
    except Exception as e:
        print(e)
        flash('Could not delete item details')
        return redirect(url_for('viewallitems'))
    else:
        flash('item deleted successfully')
        return redirect(url_for('viewallitems')) 
@app.route('/updateitem/<itemid>',methods=['GET','POST'])
def updateitem(itemid):
    if not session.get('admin'):
        flash('pls login to view items')
        return redirect(url_for('adminlogin'))
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
        adminid=cursor.fetchone()[0]
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where added_by=%s and itemid=uuid_to_bin(%s)',[adminid,itemid])
        item_details=cursor.fetchone()
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for('updateitem',itemid=itemid))
    else:
        if request.method=='POST':
            updateditem_name=request.form['title']
            updateditem_desc=request.form['Description']
            updateditem_about=request.form['About_item']
            updateditem_category=request.form['category']
            updateditem_price=request.form['price']
            updateditem_quantity=request.form['quantity']
            updateditem_filedata=request.files['file']
            print(request.form)
            print(updateditem_filedata)
            item_filename=updateditem_filedata.filename
            if item_filename == '':
                filename=item_details[7]
            else:
                if updateditem_filedata and item_filename:
                    if not allowed_file(item_filename):
                        flash('File type not allowed: png,jpg,jpeg,webp,gif')
                        return redirect(url_for('updateitem',itemid=itemid))
                    orig_secure=secure_filename(item_filename)
                    ext=os.path.splitext(orig_secure)[1] # 'anusha.txt'--->.txt
                    print(ext)
                    filename=genotp()+ext # creating a new file name
                    save_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
                    try:
                        updateditem_filedata.save(save_path)
                        remove_path=os.path.join(app.config['UPLOAD_FOLDER'],item_details[7])
                        os.remove(remove_path)
                    except Exception as e:
                        print(e)
                        app.logger.exception("Failed to save the file")
                        flash('Could not save image')
                        return redirect(url_for("updateitem",itemid=itemid))
            #update database
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
                adminid=cursor.fetchone()[0]
                cursor.execute('update items set item_name=%s,item_description=%s,item_about=%s,price=%s,quantity=%s,item_category=%s,item_imgname=%s where added_by=%s and itemid=uuid_to_bin(%s)',[updateditem_name,updateditem_desc,updateditem_about,updateditem_price,updateditem_quantity,updateditem_category,filename,adminid,itemid])
                mydb.commit()
                cursor.close()
            except Exception as e:
                app.logger.exception("Failed to update the item data")
                flash('Could not update item data')
                return redirect(url_for("updateitem",itemid=itemid))
            else:
                flash('item update successfully')
                return redirect(url_for("updateitem",itemid=itemid))            
        return render_template('updateitem.html',item_data=item_details)
@app.route('/adminupdate',methods=['GET','POST'])
def adminupdate():
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select adminid,adminname,address,admin_phno,admin_profileimg from admindata where adminemail=%s',[session.get('admin')])
            admin_details=cursor.fetchone()
            cursor.close()
        except Exception as e:
            app.logger.exception("Failed to update the admin data")
            flash('Could not update admin data')
            return redirect(url_for("admindashboard"))
        else:
            if request.method=='POST':
                updatedadmin_name=request.form['adminname']
                updatedadmin_address=request.form['address']
                updatedadmin_phno=request.form['ph_no']
                updatedadmin_filedata=request.files['file']
                print(request.form)
                print(updatedadmin_filedata)
                item_filename=updatedadmin_filedata.filename
                if item_filename == '':
                    filename=admin_details[4]
                else:
                    if updatedadmin_filedata and item_filename:
                        if not allowed_file(item_filename):
                            flash('File type not allowed: png,jpg,jpeg,webp,gif')
                            return redirect(url_for('adminupdate'))
                        orig_secure=secure_filename(item_filename)
                        ext=os.path.splitext(orig_secure)[1] # 'anusha.txt'--->.txt
                        print(ext)
                        filename=genotp()+ext # creating a new file name
                        save_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
                        try:
                            updatedadmin_filedata.save(save_path)
                            if admin_details[4]:
                                remove_path=os.path.join(app.config['UPLOAD_FOLDER'],admin_details[4])
                                os.remove(remove_path)
                        except Exception as e:
                            print(e)
                            app.logger.exception("Failed to save the file")
                            flash('Could not save image')
                            return redirect(url_for("adminupdate"))
                    #update database
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select adminid from admindata where adminemail=%s',[session.get('admin')])
                    adminid=cursor.fetchone()[0]
                    cursor.execute('update admindata set adminname=%s,address=%s,admin_phno=%s,admin_profileimg=%s where adminid=%s ',[updatedadmin_name,updatedadmin_address,updatedadmin_phno,filename,adminid])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    app.logger.exception("Failed to update the admin data")
                    flash('Could not update admin data')
                    return redirect(url_for("adminupdate"))
                else:
                    flash('admin details updated successfully')
                    return redirect(url_for("adminupdate"))                     
            return render_template('adminupdate.html',admin_details=admin_details)
@app.route('/adminlogout')
def adminlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('home'))
    else:
        flash('pls login to logout')
        return redirect(url_for('adminlogin')) 
@app.route('/userlogout')
def userlogout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    else:
        flash('pls login to logout')
        return redirect(url_for('userlogin'))
@app.route('/usercreate',methods=['GET','POST'])
def usercreate():
    if request.method=='POST':
        username=request.form['name']
        useremail=request.form['email']
        address=request.form['address']
        password=request.form['password']
        phone_no=request.form['phone_no']
        user_gender=request.form['usergender']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[useremail])
            email_count=cursor.fetchone()[0] #(1,) or (0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('usercreate'))
        else:
            if email_count==0:
                gotp=genotp()
                userdata={'username':username,'useremail':useremail,'useraddress':address,'userpassword':password,'user_phno':phone_no,'user_gender':user_gender,'server_otp':gotp}
                subject='User verification for ECOM APPLICATION'
                body=f'Use the given for verification {gotp}'
                send_mail(to=useremail,subject=subject,body=body)
                flash('otp has been sent to given mail')
                return redirect(url_for('userotpverify',serverdata=endata(userdata)))
            elif email_count==1:
                flash('user already existed')
    return render_template('usersignup.html')
@app.route('/userotpverify/<serverdata>',methods=['GET','POST'])
def userotpverify(serverdata):
    try:
        data=dndata(serverdata)
    except Exception as e:
        print(e)
        flash('Could not verify user details')
        return redirect(url_for('userotpverify'))
    else:
        if request.method=='POST':
            user_otp=request.form['otp']
            if data['server_otp']==user_otp:
                hash_password=bcrypt.generate_password_hash(data['userpassword'])
                print(hash_password)
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into userdata(userid,username,useremail,user_address,user_password,user_phno,user_gender) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s)',[data['username'],data['useremail'],data['useraddress'],hash_password,data['user_phno'],data['user_gender']])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('Could not store user details')
                    return redirect(url_for('userotpverify',serverdata=serverdata))
                else:
                    flash('details registred successfully')
                    return 'login'
            else:
                flash('Invalid OTP')
    return render_template('userotp.html')
@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if request.method=='POST':
        login_useremail=request.form['email']
        login_password=request.form['password']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[login_useremail])
            email_count=cursor.fetchone()[0] #(1,) or (0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('usercreate'))
        else:
            if email_count==1:
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select user_password from userdata where useremail=%s',[login_useremail]) 
                    stored_password=cursor.fetchone()[0]
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('could not get password')
                    return redirect(url_for('userlogin'))
                else:
                    if bcrypt.check_password_hash(stored_password,login_password):
                        print(session)
                        session['user']=login_useremail
                        if not session.get(login_useremail):
                            session[session.get('user')]={}
                        print(session)
                        return redirect(url_for('home'))
                    else:
                        flash('invalid password')
                        return redirect(url_for('userlogin'))
            elif email_count==0:
                flash('No user found')
                return redirect(url_for('userlogin'))
            else:
                flash('Email not verified')
    return render_template('userlogin.html')
@app.route('/addcart/<itemid>')
def addcart(itemid):
    if not session.get('user'):
        flash('pls login to cart item')
        return redirect(url_for('home'))
    session.pop('single_buy', None)
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where itemid=uuid_to_bin(%s)',[itemid])
        item_details=cursor.fetchone()
        print(item_details)
        cursor.close()
    except Exception as e:
        app.logger.exception(f"Failed to get item details{e}")
        flash('Could not get the item data')
        return redirect(url_for("home"))
    else:
        if itemid not in session[session.get('user')]:
            print(session)
            session[session.get('user')][itemid]=[item_details[1],1,item_details[4],item_details[5],item_details[6],item_details[7]]
            session.modified=True
            print(session)
            flash('Item added to cart')
            return redirect(url_for('home'))
        else:
            session[session.get('user')][itemid][1]+=1
            session.modified=True
            print(session)
            flash('item alredy in cart')
            return redirect(url_for('home'))
@app.route('/viewcart')
def viewcart():
    if session.get('user'):
        session.pop('single_buy', None)
        cart=session.get(session.get('user'))
        print(cart)
        if not cart:
            flash('No items in cart')
            return redirect(url_for('home'))
        sub_total=0
        items_data=[]
        for i,j in cart.items():
            item_name=j[0]
            item_qyt=int(j[1])
            item_price=float(j[2])
            item_category=j[4]
            item_img=j[5]
            amount=item_price*item_qyt
            sub_total=sub_total+amount
            items_data.append([i,item_name,item_qyt,item_price,item_category,item_img])
        delivery=40
        tax=round(sub_total*0.05,2)
        grand_total=delivery+tax+sub_total
        return render_template('cart.html',delivery=delivery,tax=tax,grand_total=grand_total,sub_total=sub_total,items_data=items_data)
    else:
        flash('Pls login to view cart')
        return redirect(url_for('userlogin'))
@app.route('/updatecart/<itemid>',methods=['POST'])
def updatecart(itemid):
    if not session.get('user'):
        flash('pls login to cart item')
        return redirect(url_for('home'))
    if itemid in session[session.get('user')]:
        print(session)
        updated_qyt=request.form['quantity']
        session[session.get('user')][itemid][1]=updated_qyt
        session.modified=True
        print(session)
        flash('cart item quantity updated')
        return redirect(url_for('viewcart'))
    else:
        flash('No item found in cart')
        return redirect(url_for('viewcart')) 
@app.route('/removecart/<itemid>')
def removecart(itemid):
    if not session.get('user'):
        flash('pls login to cart item')
        return redirect(url_for('home'))
    if itemid in session[session.get('user')]:
        print(session)
        session[session.get('user')].pop(itemid)
        session.modified=True
        print(session)
        flash('cart item removed successfully')
        return redirect(url_for('viewcart'))
    else:
        flash('No item found in cart')
        return redirect(url_for('viewcart')) 
@app.route('/paycart')
def paycart():
    if session.get('user'):

        # ✅ always prefer cart first
        cart = session.get(session.get('user'))

        # ✅ only use single_buy if cart empty
        if not cart and 'single_buy' in session:
            cart = session['single_buy']
            session['payment_source'] = 'single'
        else:
            session['payment_source'] = 'cart'

        if not cart:
            flash('No items in cart')
            return redirect(url_for('home'))

        sub_total=0
        items_data=[]

        for i,j in cart.items():
            item_name=j[0]
            item_qyt=int(j[1])   # ✅ important
            item_price=float(j[2])

            amount=item_price*item_qyt
            sub_total+=amount

            items_data.append([i,item_name,item_qyt,item_price,j[4],j[5],amount])

        delivery=40
        tax=round(sub_total*0.05,2)
        grand_total=delivery+tax+sub_total

        razorpay_amount=int(grand_total*100)

        try:
            order=client.order.create({
                "amount": razorpay_amount,
                "currency": "INR",
                "receipt": session.get('user')
            })

            return render_template('pay.html',
                order=order,
                sub_total=sub_total,
                grand_total=grand_total,
                tax=tax,
                delivery=delivery,
                items_data=items_data)

        except Exception as e:
            print(e)
            flash('Could not process payment')
            return redirect(url_for('home'))
    else:
        flash('pls login to pay cart')
        return redirect(url_for('userlogin'))
@app.route('/success_cart',methods=['POST'])
def success_cart():
    try:
        razorpay_paymentid=request.form['razorpay_payment_id']
        razorpay_orderid=request.form['razorpay_order_id']
        razorpay_signature=request.form['razorpay_signature']
        amount=float(request.form['grand_total'])
        params_dict={
            'razorpay_payment_id':razorpay_paymentid,
            'razorpay_order_id':razorpay_orderid,
            'razorpay_signature':razorpay_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
        except Exception as e:
            print(e)
            flash('Payment verification failed')
            return redirect(url_for('home'))
        cart=session.get(session.get('user'))
        print(cart)
        #check if single buy
        if 'single_buy' in session:
            cart=session['single_buy']
            session['payment_source']='single'
        else:
            session['payment_source']='cart'
        if not cart:
            flash('No items in cart')
            return redirect(url_for('home'))
        items_total=sum(float(v[1]) *float(v[2]) for v in cart.values())
        #delivery+ tax
        delivery=40
        tax=round(items_total*0.05,2)
        grand_total=tax+delivery+items_total
        if amount==grand_total:
            #-------------save orders in table----------
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()[0]
                cursor.execute('insert into orders(razorpay_ordid,razorpay_paymentid,user_id,grand_total,tax,delivery,sub_total) values(%s,%s,%s,%s,%s,%s,%s)',[razorpay_orderid,razorpay_paymentid,user_id,grand_total,tax,delivery,items_total])
                order_table_id=cursor.lastrowid
                insert_item='''insert into order_items(orderid,itemid,item_name,item_price,item_qyt,item_category,sub_total,item_imgname) values(%s,uuid_to_bin(%s),%s,%s,%s,%s,%s,%s)'''
                for i,j in cart.items():
                    item_name=j[0]
                    item_qyt=int(j[1])
                    item_price=float(j[2])
                    item_category=j[4]
                    item_img=j[5]
                    amount=item_price*item_qyt
                    cursor.execute(insert_item,[order_table_id,i,item_name,item_price,item_qyt,item_category,amount,item_img])
                mydb.commit()
                cursor.close()
            except Exception as e:
                print(e)
                flash('Could not save orders')
                return redirect(url_for('paycart'))
            #------clearing the session data after payment
            payment_source=session.get('payment_source')
            if payment_source=='cart':
                session[session.get('user')]={}
                session.modified=True
            
            if payment_source=='single':
                session.pop('single_buy')
                session.modified=True
            #remove payment_source flag
            session.pop('payment_source',None)
            session.modified=True
            flash('Payment successfull')
            return redirect(url_for('home'))
        else:
            flash('Amount mismatched')
            return redirect(url_for('home'))
    except Exception as e:
        print(e)
        flash('Payment Failed')
        return redirect(url_for('home'))
@app.route('/myorders')
def myorders():
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('select orderid,razorpay_ordid,razorpay_paymentid,user_id,grand_total,tax,delivery,sub_total,status,created_at from orders where user_id=%s',[user_id])
            myorders_data=cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not fetch order details')
            return redirect(url_for('home'))
        else:
            return render_template('myorders.html',myorders_data=myorders_data)
    else:
        flash('pls login to view orders')
        return redirect(url_for('userlogin'))
@app.route('/myorders_details/<orderid>')
def myorders_details(orderid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('select orderid,razorpay_ordid,razorpay_paymentid,user_id,grand_total,tax,delivery,sub_total,status,created_at from orders where user_id=%s and orderid=%s',[user_id,orderid])
            myorders_data=cursor.fetchone()
            cursor.execute('select order_detailsid ,orderid,bin_to_uuid(itemid),item_name,item_price,item_qyt,item_category,sub_total,item_imgname from order_items where orderid=%s',[orderid])
            order_details=cursor.fetchall() 
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not fetch order details')
            return redirect(url_for('home'))
        else:
            return render_template('order_details.html',myorders_data=myorders_data,order_details=order_details)
    else:
        flash('pls login to view orders')
        return redirect(url_for('userlogin'))
@app.route('/get_invoice/<int:ordid>')
def get_invoice(ordid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
            user_id=cursor.fetchone()[0]
            cursor.execute('select orderid,razorpay_ordid,razorpay_paymentid,user_id,grand_total,tax,delivery,sub_total,status,created_at from orders where user_id=%s and orderid=%s',[user_id,ordid])
            myorders_data=cursor.fetchone()
            cursor.execute('select order_detailsid ,orderid,bin_to_uuid(itemid),item_name,item_price,item_qyt,item_category,sub_total,item_imgname from order_items where orderid=%s',[ordid])
            order_details=cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            flash('Could not fetch order details')
            return redirect(url_for('home'))
        else:
            html=render_template('invoice.html',myorders_data=myorders_data,order_details=order_details)
            #generate pdf
            pdf=BytesIO()
            pisa_status=pisa.CreatePDF(html,dest=pdf)
            if pisa_status.err:
                return 'Error Grenerating pdf'
            response=make_response(pdf.getvalue())
            response.headers['Content-Type']='application/pdf'
            response.headers['Content-Disposition']=f'attachement; filename=invoice_{ordid}.pdf'
            return response


    else:
        flash('pls loginto get invoice')
        return redirect(url_for('userlogin'))
@app.route('/category/<ctype>')
def category(ctype):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where item_category=%s',[ctype])
        item_details=cursor.fetchall()
        print(item_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for("home"))
    else:
        return render_template('dashboard.html',allitems_data=item_details)
@app.route('/buy_now',methods=['POST'])
def buy_now():
    if session.get('user'):
        itemid=request.form['itemid']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where itemid=uuid_to_bin(%s)',[itemid])
            item_data=cursor.fetchone() #(itemid,itemname)
            cursor.close()
        except Exception as e:
            print(e)
            flash('cloud not get item details')
            return redirect(url_for('home'))
        else:
            print(session)
            session['single_buy']={itemid:[item_data[1],1,item_data[4],item_data[5],item_data[6],item_data[7]]}
            session.modified=True
            print(session)
            return redirect(url_for('paycart'))
    else:
        flash('to buy pls login ')
        return redirect(url_for('userlogin'))
@app.route('/descitem/<itemid>')
def descitem(itemid):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where itemid=uuid_to_bin(%s)',[itemid])
        item_details=cursor.fetchone()
        print(item_details)
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for("home"))
    else:
        return render_template('desc.html',item_data=item_details)  
@app.route('/addreview/<itemid>',methods=['GET','POST'])  
def addreview(itemid):
    if session.get('user'):
        if request.method=='POST':
            reviewtext=request.form['review_text']
            rating=request.form['rating']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select userid from userdata where useremail=%s',[session.get('user')])
                user_id=cursor.fetchone()[0]
                cursor.execute('insert into reviews(reviewtext,rating,userid,itemid) values(%s,%s,%s,uuid_to_bin(%s))',[reviewtext,rating,user_id,itemid])
                mydb.commit()
                cursor.close()
            except Exception as e:
                app.logger.exception("Failed to add review")
                flash('Could notadd review')
                return redirect(url_for("descitem",itemid=itemid))
            else:
                flash('review added successfully')
                return redirect(url_for("descitem",itemid=itemid))
        return render_template('addreview.html')
    else:
        flash('To add review pls login')
        return redirect(url_for('userlogin'))
@app.route('/search',methods=["POST"])
def search():
    if session.get('user'):
        search_data=request.form['q'] #user search data ''
        strg=['A-Za-z0-9'] #defining a set of characters
        pattern=re.compile(f'^{strg}',re.IGNORECASE) #defines a pattern that consists of above set of characters
        if pattern.match(search_data): #checking the search data matches pattern that means no empty data
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select  bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where item_name like %s or item_description like %s or item_about like %s or price like %s or quantity like %s or item_category like %s ',[search_data+'%',search_data+'%',search_data+'%',search_data+'%',search_data+'%',search_data+'%'])
                #fetching the result and storing in notes
                item_details=cursor.fetchall()
                print(item_details)
                cursor.close()
            except Exception as e:
                app.logger.exception("Failed to get item details")
                flash('Could not get the item data')
                return redirect(url_for("home"))
            else:
                return render_template('dashboard.html',allitems_data=item_details) 
        else:
            flash('invalid search data')
            return redirect(url_for('home'))  
@app.route('/userforgot',methods=['GET','POST'])
def userforgot():
    if request.method=='POST':
        useremail=request.form['email']
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select count(*) from userdata where useremail=%s',[useremail])
            email_count=cursor.fetchone()[0] #(1,) or (0,)
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not verify the email')
            return redirect(url_for('usercreate'))
        else:
            if email_count==1:
                subject='Resetlink  for ECOM APPLICATION'
                body=f"Use the given link for  {url_for('usernewpassword',data=endata(useremail),_external=True)}"
                send_mail(to=useremail,subject=subject,body=body)
                flash('Resetlink has been sent to given mail')
                return redirect(url_for('userforgot'))
            elif email_count==0:
                flash('user not found')
    return render_template('userforgot.html')
@app.route('/usernewpassword/<data>',methods=['GET','PUT'])
def usernewpassword(data):
    try:
        useremail=dndata(data)
    except Exception as e:
        print(e)
        flash('Could not get user data')
        return redirect(url_for('usernewpassword',dat=data))
    else:
        if request.method=='PUT':
            npassword=request.get_json()['new_password']
            hash_password=bcrypt.generate_password_hash(npassword)
            print(hash_password)
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update userdata set user_password=%s where useremail=%s',[hash_password,useremail])
                mydb.commit() 
                cursor.close()
            except Exception as e:
                print(e)
                flash('Could not update newpassword')
                return redirect(url_for('usernewpassword',data=data))
            else:
                return jsonify({'message':'ok'})
    return render_template('usernewpassword.html',data=data)
@app.route('/reviewresult/<itemid>')
def reviewresult(itemid):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),item_name,item_description,item_about,price,quantity,item_category,item_imgname from items where itemid=uuid_to_bin(%s)',[itemid])
        item_details=cursor.fetchone()
        cursor.execute('select reviewtext,rating,userid,created_at from reviews where itemid=uuid_to_bin(%s)',[itemid])
        review_data=cursor.fetchall()
        cursor.close()
    except Exception as e:
        app.logger.exception("Failed to get item details")
        flash('Could not get the item data')
        return redirect(url_for("home"))
    else:
        return render_template('read_review.html',review_data=review_data,item_details=item_details)
if __name__=="__main__":
   app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))