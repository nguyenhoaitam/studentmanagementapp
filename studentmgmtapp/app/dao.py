from app.models import TaiKhoan, HocSinh, Lop, MonHoc, VaiTroTaiKhoan, QuyDinh, KhoiLop
from app import app, db
from sqlalchemy import func
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


def lay_ds_lop_theo_id(id):
    return db.session.get(Lop, id)


def lay_ds_mon_hoc(kw=None):
    dsmonhoc = MonHoc.query

    if kw:
        dsmonhoc = dsmonhoc.filter(MonHoc.tenMon.contains(kw))

    return dsmonhoc.all()


def lay_quy_dinh():
    qd = QuyDinh.query

    return qd.first()


def xac_thuc_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return TaiKhoan.query.filter(TaiKhoan.username.__eq__(username.strip()),
                             TaiKhoan.password.__eq__(password)).first()

# Danh sách lớp


# Vẽ biểu đồ
def dem_lop():
    return db.session.query(KhoiLop.id, KhoiLop.tenKhoi, func.count(Lop.id)).join(Lop, Lop.khoiLop_id == KhoiLop.id, isouter=True).group_by(KhoiLop.id).all()


if __name__ == '__main__':
    with app.app_context():
        print(lay_ds_lop_theo_id('1'))