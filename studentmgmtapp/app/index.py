from datetime import datetime

from flask import render_template, redirect, request, jsonify
from flask_login import login_user, logout_user

import dao
from app import app, login, db
from app.models import Lop, HocSinh, QuyDinh

"""
Các chức năng
1.Đăng nhập
2.Tiếp nhận học sinh
3.Chỉnh sửa học sinh
4.Hiển thị danh sách học sinh

5.Thêm giáo viên
6.Chỉnh sửa giáo viên
7.Hiển thị danh sách giáo viên

9.Chỉnh sửa lớp
10.Hiển thị danh sách lớp

11.Thêm môn học
12.Chỉnh sửa môn học(Xóa)
13.Tìm kiếm môn học
14.Hiển thị danh sách môn học

13.Nhập điểm
14.Xuất điểm

15.Báo cáo tổng kết
16.Thay đổi quy định
"""


@app.route('/')
def index():
    return render_template('index.html')


# 1.Đăng nhập
@login.user_loader
def lay_tai_khoan(tai_khoan_id):
    return dao.lay_tai_khoan_theo_id(tai_khoan_id)


# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if not session.get("taiKhoan"):
#
#             return redirect(url_for('index', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function


@app.route('/admin/login', methods=['post'])
def dang_nhap_admin():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.xac_thuc_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route("/login", methods=['get', 'post'])
def dang_nhap():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.xac_thuc_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect("/" if next is None else next)

    return render_template('login.html')


@app.route('/logout')
def dang_xuat():
    logout_user()
    return redirect("/")


# 2.Tiếp nhận sinh viên
@app.route("/tiepnhan", methods=['get', 'post'])
# @login_required
def tiepnhan():
    err_msg = ""
    if request.method.__eq__('POST'):
        hoten = request.form.get('hoten')
        gioitinh = request.form.get('gioitinh')
        ngaysinh = request.form.get('ngaysinh')
        diachi = request.form.get('diachi')
        sodt = request.form.get('sodt')
        email = request.form.get('email')
        ngaynhaphoc = request.form.get('ngaynhaphoc')
        malop = request.form.get('malop')

        if hoten and gioitinh and ngaysinh and diachi and sodt and email and ngaynhaphoc and malop:
            ngaysinh = datetime.strptime(ngaysinh, "%Y-%m-%d").date()
            ngayhientai = datetime.now().year

            tuoi = ngayhientai - ngaysinh.year

            qd = dao.lay_quy_dinh()

            tuoitoithieu = qd.tuoiToiThieu
            tuoitoida = qd.tuoiToiDa
            if tuoitoithieu < tuoi < tuoitoida:

                try:
                    dao.them_hoc_sinh(hoten=hoten, ngaysinh=ngaysinh, gioitinh=gioitinh, diachi=diachi, sodt=sodt,
                                      email=email, ngaynhaphoc=ngaynhaphoc, malop=malop)
                except:
                    err_msg = 'Hệ thống đang bị lỗi!'
                else:
                    return redirect('/tiepnhan')
            else:
                err_msg = 'Tuổi KHÔNG đúng quy định!Vui lòng kiểm tra và nhập lại'
        else:
            err_msg = 'Vui lòng nhập đầy đủ thông tin!'

    return render_template('tiepnhan.html', err_msg=err_msg)


# 4.Hiển thị danh sách học sinh
@app.route("/dshocsinh")
def dshocsinh():
    kw = request.args.get('kw')

    dshocsinh = dao.lay_ds_hoc_sinh(kw=kw)

    return render_template('dshocsinh.html',
                           dshocsinh=dshocsinh)


# 9.Chỉnh sửa lớp
# Route để lấy danh sách lớp học
@app.route('/get_danh_sach_lop', methods=['GET'])
def get_danh_sach_lop():
    danh_sach_lop = Lop.query.all()
    return jsonify([{'id': lop.id, 'tenLop': lop.tenLop, 'siSo': lop.siSo} for lop in danh_sach_lop])

# Route để lấy thông tin lớp học
@app.route('/get_lop/<int:lop_id>', methods=['GET'])
def get_lop(lop_id):
    lop = Lop.query.get(lop_id)
    return jsonify({'id': lop.id, 'tenLop': lop.tenLop, 'siSo': lop.siSo})

# Route để chỉnh sửa thông tin lớp học
@app.route('/sua_lop/<int:lop_id>', methods=['POST'])
def sua_lop(lop_id):
    lop = Lop.query.get(lop_id)

    if request.method == 'POST':
        ten_lop_moi = request.form['ten_lop']
        si_so_moi = int(request.form['si_so'])

        lop.tenLop = ten_lop_moi
        lop.siSo = si_so_moi
        db.session.commit()

        return jsonify({'message': 'Thông tin lớp học đã được cập nhật thành công.'})


# Route để xóa thông tin lớp học
@app.route('/xoa_lop/<int:lop_id>', methods=['DELETE'])
def xoa_lop(lop_id):
    lop = Lop.query.get(lop_id)

    if not lop:
        return jsonify({'error': 'Lớp không tồn tại.'}), 404

    db.session.delete(lop)
    db.session.commit()

    return jsonify({'message': 'Lớp học đã được xóa thành công.'})


# 10.Hiển thị danh sách lớp
@app.route("/dslop")
def dslop():
    kw = request.args.get('kw')

    dslop = dao.lay_ds_lop(kw=kw)

    return render_template('dslop.html',
                           dslop=dslop)


# Hiển thị theo từng lớp
@app.route('/get_data', methods=['POST'])
def get_data():
    selected_class_id = request.form.get('selected_class_id')
    data = db.session.query(Lop, HocSinh).join(HocSinh).filter(Lop.id == selected_class_id).all()

    # Format data as a list of dictionaries
    formatted_data = [
        {
            'id': hocsinh.id,
            'tenHocSinh': hocsinh.hoTen,
            'gioiTinh': hocsinh.gioiTinh,
            'ngaySinh': hocsinh.ngaySinh,
            'diaChi': hocsinh.diaChi
        }
        for lop, hocsinh in data
    ]

    return jsonify(formatted_data)


# 11.Thêm môn học
@app.route("/themmon")
def themmon():
    return render_template('themmon.html')


# 13.Nhập điểm
@app.route("/nhapdiem")
def nhapdiem():
    kw = request.args.get('kw')
    dslop = dao.lay_ds_lop(kw)
    dsmonhoc = dao.lay_ds_mon_hoc(kw)
    return render_template('nhapdiem.html',
                           dsmonhoc=dsmonhoc,
                           dslop=dslop)


# 14.Hiển thị danh sách môn học
@app.route("/dsmonhoc")
def dsmonhoc():
    kw = request.args.get('kw')

    dsmonhoc = dao.lay_ds_mon_hoc(kw=kw)

    return render_template('dsmonhoc.html',
                           dsmonhoc=dsmonhoc)


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
