from datetime import datetime
from functools import wraps
from flask import render_template, redirect, request, jsonify, abort, session, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import Forbidden
import dao
from app import app, login, db
from app.models import Lop, HocSinh, QuyDinh, VaiTroTaiKhoan, MonHoc, HocKy, NamHoc

"""
Các chức năng
1.Đăng nhập

2.Tiếp nhận học sinh ==> R
3.Chỉnh sửa học sinh
4.Hiển thị danh sách học sinh ==> R

9.Chỉnh sửa lớp ==> R
10.Hiển thị danh sách lớp ==> R

11.Thêm môn học ==> R
12.Chỉnh sửa môn học(Xóa) ==> R
13.Tìm kiếm môn học ==> R
14.Hiển thị danh sách môn học ==> R

13.Nhập điểm
14.Xuất điểm

15.Báo cáo tổng kết
16.Thay đổi quy định  ==> R
"""


@app.route('/')
def index():
    lops = Lop.query.all()
    mons = MonHoc.query.all()
    return render_template('index.html',
                           lops=lops,
                           mons=mons)


# 1.Đăng nhập
@login.user_loader
def lay_tai_khoan(tai_khoan_id):
    return dao.lay_tai_khoan_theo_id(tai_khoan_id)

#Xác thực người dùng
def check_role(role):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            # import pdb
            # pdb.set_trace()
            if current_user.loaiTaiKhoan == VaiTroTaiKhoan(role):
                return function(*args, **kwargs)
            else:
                # Lỗi 403 Forbidden
                raise Forbidden('Bạn không có quyền truy cập vào chức năng này.')

        return wrapper
    return decorator


@app.route('/admin/login', methods=['post'])
def dang_nhap_admin():
    err_msg = ""
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.xac_thuc_user(username=username, password=password)
    if user:
        login_user(user=user)
        return redirect('/admin')
    else:
        err_msg = 'Thông tin tài khoản không đúng vui lòng nhập lại!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def dang_nhap():
    err_msg = ""
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.xac_thuc_user(username=username, password=password)
        if user:
            login_user(user=user)

            next = request.args.get('next')
            return redirect("/" if next is None else next)
        else:
            err_msg = 'Thông tin tài khoản không đúng vui lòng nhập lại!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/logout')
def dang_xuat():
    logout_user()
    return redirect("/")


# 2.Tiếp nhận học sinh
@app.route("/tiepnhan", methods=['get', 'post'])
@login_required
@check_role(VaiTroTaiKhoan.STAFF)
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


# 3.Chỉnh sửa học sinh
# Route để lấy danh sách học sinh
@app.route('/get_ds_hoc_sinh', methods=['GET'])
def get_ds_hoc_sinh():
    ds_hoc_sinh = HocSinh.query.all()
    import pdb
    pdb.set_trace()
    return jsonify([{'id': hs.id,
                     'hoTen': hs.hoTen,
                     'ngaySinh': hs.ngaySinh,
                     'gioitinh': hs.gioiTinh,
                     'diaChi': hs.diaChi,
                     'soDT': hs.soDT,
                     'email': hs.email,
                     'ngayNhapHoc': hs.ngayNhapHoc,
                     'lop_id': hs.lop_id} for hs in ds_hoc_sinh])


# Route để lấy thông tin học sinh
@app.route('/get_hoc_sinh/<int:hs_id>', methods=['GET'])
def get_hoc_sinh(hs_id):
    hs = HocSinh.query.get(hs_id)
    return jsonify({'id': hs.id,
                    'hoTen': hs.hoTen,
                    'ngaySinh': hs.ngaySinh,
                    'gioiTinh': hs.gioiTinh,
                    'diaChi': hs.diaChi,
                    'soDT': hs.soDT,
                    'email': hs.email,
                    'ngayNhapHoc': hs.ngayNhapHoc,
                    'lop_id': hs.lop_id})


# Route để chỉnh sửa thông tin học sinh
@app.route('/sua_hs/<int:hs_id>', methods=['POST'])
def sua_hs(hs_id):
    hs = HocSinh.query.get(hs_id)

    if request.method == 'POST':
        hs.hoTen = request.form.get('hoten')
        hs.ngaySinh = request.form.get('ngaysinh')
        hs.gioiTinh = request.form.get('gioitinh')
        hs.diaChi = request.form.get('diachi')
        hs.soDT = request.form.get('sodienthoai')
        hs.email = request.form.get('email')
        hs.ngayNhapHoc = request.form.get('ngaynhaphoc')
        hs.lop_id = request.form.get('lopid')
        db.session.commit()

        return jsonify({'message': 'Thông tin lớp học đã được cập nhật thành công.'})


# Route để xóa thông tin học sinh
@app.route('/xoa_hs/<int:hs_id>', methods=['DELETE'])
def xoa_hs(hs_id):
    hs = dao.lay_ds_hs_theo_id(hs_id)

    if not hs:
        return jsonify({'error': 'Học sinh không tồn tại.'}), 404

    db.session.delete(hs)
    db.session.commit()

    return jsonify({'message': 'Học sinh đã được xóa thành công.'})


# 4.Hiển thị danh sách học sinh
@app.route("/dshocsinh")
@login_required
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
    lop = dao.lay_ds_lop_theo_id(lop_id)
    return jsonify({'id': lop.id, 'tenLop': lop.tenLop, 'siSo': lop.siSo})


# Route để chỉnh sửa thông tin lớp học
@app.route('/sua_lop/<int:lop_id>', methods=['POST'])
def sua_lop(lop_id):
    lop = dao.lay_ds_lop_theo_id(lop_id)

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
@login_required
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


# 13.Nhập điểm
@app.route("/nhapdiem", methods=['get', 'post'])
@login_required
@check_role(VaiTroTaiKhoan.TEACHER)
def nhapdiem():
    dslop = Lop.query.all()
    dsmonhoc = MonHoc.query.all()
    dshocky = HocKy.query.all()
    dsnamhoc = NamHoc.query.all()
    return render_template('nhapdiem.html',
                           dsmonhoc=dsmonhoc,
                           dslop=dslop,
                           dshocky=dshocky,
                           dsnamhoc=dsnamhoc)


#Lấy học sinh theo lớp
@app.route('/classes/<int:class_id>/students')
def layhstheolop(class_id):
    students = HocSinh.query.filter_by(class_id=class_id).all()
    return jsonify({'students': [student.to_dict() for student in students]})


# 14.Hiển thị danh sách môn học
@app.route("/dsmonhoc")
@login_required
def dsmonhoc():
    kw = request.args.get('kw')

    dsmonhoc = dao.lay_ds_mon_hoc(kw=kw)

    return render_template('dsmonhoc.html',
                           dsmonhoc=dsmonhoc)

# 15. Báo cáo tổng kết


if __name__ == '__main__':
    from app import admin
    app.run(debug=True)
