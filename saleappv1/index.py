from saleappv1 import *
from flask import render_template, url_for, session, jsonify
from flask_login import login_user, login_required, logout_user
from saleappv1.admin import *
import cloudinary.uploader


@app.route("/")
def home():
   return render_template('index.html')


#Dang ki dang nhap
@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username,
                               password=password, email=email,
                               avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mật khẩu không khớp!!!'
        except Exception as ex:
            err_msg = 'Hệ thống đang có lỗi: ' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            return redirect(url_for(request.args.get('next', 'home')))
        else:
            err_msg = 'Username hoac password KHONG chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                            password=password,
                             role=UserRole.ADMIN)
    if user:
        login_user(user=user)
    return redirect('/admin')


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


#trang danh sach hoa don
@app.route("/bills", methods=['get', 'post'])
def bills_list():
    user_id = request.form.get('user_id')
    bills = utils.load_list_bills(user_id)
    return render_template('bills.html', bills=bills)


# tao lich kham online
@app.route('/made_schedule', methods=['get', 'post'])
def made_schedule():
    err_msg = ""
    msg_success = ''
    full_patient = ''
    if request.method.__eq__('POST'):
        date = request.form.get('date')
        created_date = datetime.strptime(date, "%Y-%m-%d")
        name = request.form.get('name')
        gender = request.form.get('gender')
        year_born = request.form.get('year_born')
        address = request.form.get('address')

        try:
            count = utils.count_schedule_by_date(created_date)
            dem = 0
            for c in count:
                dem = dem + 1
            if dem < 30:
                utils.add_schedule(created_date=created_date, name=name, gender=gender, year_born=year_born,
                                   address=address)
            else:
                full_patient = " Đủ 30 bệnh nhân trong ngày"
        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)
        else:
            msg_success = "Đặt lịch thành công"
            message = client.messages.create(
                messaging_service_sid='MGd293cddd30bdb6f59766079f5687f6aa',
                body='hello',
                to='+84399088051'
            )

    return render_template('made_schedule.html', err_msg=err_msg, msg_success=msg_success,
                           full_patient=full_patient)


@app.route('/api/pay', methods=['post'])
def pay():
        data = request.json
        id = str(data.get('id'))
        try:
            utils.reload_state_pay(id)
        except:
            return jsonify({'code': 400})

        return jsonify({'code': 200})


#yêu cầu 2

@app.route('/phieu_kham')
def phieu_kham():
    med = Medicine.query.all()
    return render_template('phieuKham.html', medicine=med)


@app.route('/api/add_medicine_to_cart', methods=['post'])
def add_medicine_to_cart():
    data = request.json
    id = data.get('id')

    # import pdb
    # pdb.set_trace()
    p = utils.get_medicine_by_id(id=id)
    TienThuoc = p.TienThuoc

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        pass
    else:
        cart[id] = {
            'id': id,
            'TienThuoc': TienThuoc,
            'quantity': 1
        }

    session['cart'] = cart
    unit = p.unit
    how_to_use = p.how_to_use

    return jsonify({
        'unit': unit,
        'how_to_use': how_to_use
    })


@app.route('/api/add_phieu_kham', methods=['post'])
def lap_phieu_kham():
    err_msg = ""
    msg_success = ''
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        NgayKham = request.form.get('NgayKham')
        created_date = datetime.strptime(NgayKham, "%Y-%m-%d")
        symptom = request.form.get('symptom')
        prognostication = request.form.get('prognostication')

        try:
            cart = session.get('cart')
            utils.add_MedicalBill(name, created_date, symptom, prognostication, cart)
        except Exception as err:
            err_msg = " Hệ thống báo lỗi " + str(err)
        else:
             msg_success = "Đặt lịch thành công"

    med = Medicine.query.all()
    return render_template('phieuKham.html', err_msg=err_msg, msg_success=msg_success,  medicine=med)


# Cập nhật số lượng thuốc
@app.route('/api/update_quantity', methods=['put'])
def update_quantity():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    try:
        cart = session.get('cart')
        if cart and id in cart:
            cart[id]['quantity'] = quantity
            session['cart'] = cart
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


if __name__ == '__main__':
    from saleappv1.admin import *
    app.run(debug=True)

