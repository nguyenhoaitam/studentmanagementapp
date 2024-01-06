from app.models import TaiKhoan, HocSinh, Lop, MonHoc, VaiTroTaiKhoan
from app import app, db
import hashlib


def lay_tai_khoan_theo_id(tai_khoan_id):
    return TaiKhoan.query.get(tai_khoan_id)


def lay_ds_hoc_sinh(kw=None):
    dshocsinh = HocSinh.query

    if kw:
        dshocsinh = dshocsinh.filter(HocSinh.hoTen.contains(kw))

    return dshocsinh.all()


def them_hoc_sinh(hoten, ngaysinh, gioitinh, diachi, sodt, email, ngaynhaphoc, malop):
    h = HocSinh(hoTen=hoten, ngaySinh=ngaysinh, gioiTinh=gioitinh, diaChi=diachi, soDT=sodt, email=email, ngayNhapHoc=ngaynhaphoc, lop_id=malop)

    db.session.add(h)
    db.session.commit()


def lay_ds_lop(kw=None):
    dslop = Lop.query

    if kw:
        dslop = dslop.filter(HocSinh.tenLop.contains(kw))

    return dslop.all()


def lay_ds_mon_hoc(kw=None):
    dsmonhoc = MonHoc.query

    if kw:
        dsmonhoc = dsmonhoc.filter(MonHoc.tenMon.contains(kw))

    return dsmonhoc.all()


def xac_thuc_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                             TaiKhoan.password.__eq__(password)).first()