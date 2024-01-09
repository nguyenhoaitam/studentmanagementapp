from app.models import TaiKhoan, HocSinh, Lop, MonHoc, VaiTroTaiKhoan, QuyDinh, KhoiLop, Diem, ChiTietDiem
from app import app, db
from sqlalchemy import func, case
from sqlalchemy.orm import sessionmaker
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
        dslop = dslop.filter(Lop.tenLop.contains(kw))

    return dslop.all()


def lay_ds_lop_theo_id(id):
    return db.session.get(Lop, id)


def lay_ds_hs_theo_id(id):
    return db.session.get((HocSinh, id))



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


# Thống kê và Vẽ biểu đồ
def dem_lop():
    return db.session.query(KhoiLop.id, KhoiLop.tenKhoi, func.count(Lop.id)).join(Lop, Lop.khoiLop_id == KhoiLop.id, isouter=True).group_by(KhoiLop.id).all()


def thong_ke_mon_theo_lop():
    # so_luong_dat = func.sum(case([(ChiTietDiem.diem >= 5, 1)], else_=0)).label('soLuongDat')
    # kq = (db.session.query(Lop, Lop.tenLop).join(HocSinh, Lop.id == HocSinh.lop_id).join(Diem, HocSinh.id == Diem.hocSinh_id).join(MonHoc, Diem.monHoc_id == MonHoc.id).join(ChiTietDiem, Diem.id == ChiTietDiem.diem_id).with_entities(
    #     (Lop.tenLop).label('tenLop'),
    #     func.count(HocSinh.id).label('siSo'),
    #     func.sum(case([(ChiTietDiem.diem >= 5, 1)], else_=0)).label('soLuongDat')
    #     # func.count(Diem.id).filter(Diem.id == ChiTietDiem.diem_id, ChiTietDiem.diem >= 5).label('soLuongDat')
    # )).group_by(Lop.tenLop).all()
    kq = (db.session.query(Lop.tenLop.label('tenLop'),
                           func.count(HocSinh.id).label('siSo'),
                           func.sum(case((ChiTietDiem.diem >= 5, 1), else_=0)).label('soLuongDat'),
                           (func.sum(case((ChiTietDiem.diem >= 5, 1), else_=0)) / func.count(HocSinh.id) * 100).label(
                               'tyLeDat'))
          .join(HocSinh, Lop.id == HocSinh.lop_id)
          .join(Diem, HocSinh.id == Diem.hocSinh_id)
          .join(MonHoc, Diem.monHoc_id == MonHoc.id)
          .join(ChiTietDiem, Diem.id == ChiTietDiem.diem_id)
          .group_by(Lop.tenLop)
          .all())
    return kq


def thong_ke_tung_mon_theo_lop(id=None):
    kq = (db.session.query(Lop.tenLop.label('tenLop'),
                           func.count(HocSinh.id).label('siSo'),
                           func.sum(case((ChiTietDiem.diem >= 5, 1), else_=0)).label('soLuongDat'),
                           (func.sum(case((ChiTietDiem.diem >= 5, 1), else_=0)) / func.count(HocSinh.id) * 100).label(
                               'tyLeDat'))
          .join(HocSinh, Lop.id == HocSinh.lop_id)
          .join(Diem, HocSinh.id == Diem.hocSinh_id)
          .join(MonHoc, Diem.monHoc_id == MonHoc.id)
          .join(ChiTietDiem, Diem.id == ChiTietDiem.diem_id)
          .filter(MonHoc.id == id)
          .group_by(Lop.tenLop)
          .all())
    return kq


if __name__ == '__main__':
    with app.app_context():
        print()