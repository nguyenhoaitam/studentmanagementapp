import enum
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class VaiTroTaiKhoan(enum.Enum):
    ADMIN = 1
    TEACHER = 2
    STAFF = 3


class TaiKhoan(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(255),
                    default='https://res.cloudinary.com/dkmurrwq5/image/upload/v1704251718/user_ic.png')
    loaiTaiKhoan = Column(Enum(VaiTroTaiKhoan), default=VaiTroTaiKhoan.STAFF)


class NhanVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    ngaySinh = Column(DateTime)
    email = Column(String(50))
    soDT = Column(String(10), nullable=False)

    taiKhoan_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)


class GiaoVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(String(10), nullable=False)
    email = Column(String(50))
    diaChi = Column(String(255))
    soDT = Column(String(10), nullable=False)

    taiKhoan_id = Column(Integer, ForeignKey(TaiKhoan.id), nullable=False)
    dslopgiaovien = relationship('LopGiaoVien', backref='lgiaovien', lazy=True)
    dsmonhocgiaovien = relationship('MonHocGiaoVien', backref='mgiaovien', lazy=True)


class KhoiLop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenKhoi = Column(String(50), nullable=False)

    dslop = relationship('Lop', backref='lkhoilop', lazy=True)

    def __str__(self):
        return self.tenKhoi


class Lop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenLop = Column(String(50), nullable=False)
    siSo = Column(Integer, nullable=False)

    khoiLop_id = Column(Integer, ForeignKey(KhoiLop.id), nullable=False)
    dshocsinh = relationship('HocSinh', backref='hslop', lazy=True)
    dslopgiaovien = relationship('LopGiaoVien', backref='gvlop', lazy=True)

    def __str__(self):
        return self.tenLop


class HocSinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen = Column(String(50), nullable=False)
    ngaySinh = Column(DateTime, nullable=False)
    gioiTinh = Column(String(10), nullable=False)
    diaChi = Column(String(255))
    soDT = Column(String(10), nullable=False)
    email = Column(String(50))
    ngayNhapHoc = Column(DateTime, default=datetime.now())

    lop_id = Column(Integer, ForeignKey(Lop.id), nullable=False)
    dsdiem = relationship('Diem', backref='hocsinh', lazy=True)


class NamHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenNam = Column(String(50), nullable=False)

    dshocky = relationship('HocKy', backref='hknamhoc', lazy=True)


class HocKy(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenHocKy = Column(String(50), nullable=False)
    ngayBD = Column(DateTime, default=datetime.now(), nullable=False)
    ngayKT = Column(DateTime, nullable=False)

    namHoc_id = Column(Integer, ForeignKey(NamHoc.id), nullable=False)
    dsdiem = relationship('Diem', backref='dhocky', lazy=True)


class MonHoc(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenMon = Column(String(50), nullable=False)

    dsdiem = relationship('Diem', backref='dmonhoc', lazy=True)
    dsmonhocgiaovien = relationship('MonHocGiaoVien', backref='gvmonHoc', lazy=True)

class Diem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenDiem = Column(String(50), nullable=False)

    monHoc_id = Column(Integer, ForeignKey(MonHoc.id), nullable=False)
    hocSinh_id = Column(Integer, ForeignKey(HocSinh.id), nullable=False)
    hocKy_id = Column(Integer, ForeignKey(HocKy.id), nullable=False)
    dschitietdiem = relationship('ChiTietDiem', backref='ctdiem', lazy=True)


class LoaiDiem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenLoaiDiem = Column(String(50), nullable=False)

    dschitietdiem = relationship('ChiTietDiem', backref='loaidiem', lazy=True)


class ChiTietDiem(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    diem = Column(Float)

    loaiDiem_id = Column(Integer, ForeignKey(LoaiDiem.id), nullable=False)
    diem_id = Column(Integer, ForeignKey(Diem.id), nullable=False)


class LopGiaoVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    lop_id = Column(Integer, ForeignKey(Lop.id), nullable=False)
    giaoVien_id = Column(Integer, ForeignKey(GiaoVien.id), nullable=False)


class MonHocGiaoVien(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)

    giaoVien_id = Column(Integer, ForeignKey(GiaoVien.id), nullable=False)
    monHoc_id = Column(Integer, ForeignKey(MonHoc.id), nullable=False)


class QuyDinh(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tuoiToiThieu = Column(Integer)
    tuoiToiDa = Column(Integer)
    siSoToiDa = Column(Integer)


if __name__ == "__main__":
    from app import app

    with app.app_context():
        # db.create_all()

        # import  hashlib
        # tkadm = TaiKhoan(username='admin', password=str(hashlib.md5('admin123'.encode('utf-8')).hexdigest()), loaiTaiKhoan=VaiTroTaiKhoan.ADMIN)
        # tkgv = TaiKhoan(username='giaovien', password=str(hashlib.md5('giaovien123'.encode('utf-8')).hexdigest()), loaiTaiKhoan=VaiTroTaiKhoan.TEACHER)
        # tknv = TaiKhoan(username='nhanvien', password=str(hashlib.md5('nhanvien123'.encode('utf-8')).hexdigest()), loaiTaiKhoan=VaiTroTaiKhoan.STAFF)

        # db.session.add(tkadm)
        # db.session.add(tkgv)
        # db.session.add(tknv)

        # gv1 = GiaoVien(hoTen='Nguyễn Văn A', ngaySinh='2000-10-01', gioiTinh='Nam', email='example@gmail.com', diaChi='Hồ Chí Minh', soDT='0123456789', taiKhoan_id=2)
        # db.session.add(gv1)

        # nv1 = NhanVien(hoTen='Nguyễn Hoài Tâm', ngaySinh='2003-08-16', email='2151053055tam@ou.edu.vn', soDT='0394873588', taiKhoan_id=3)
        # db.session.add(nv1)

        # k10 = KhoiLop(tenKhoi='Khối 10')
        # k11 = KhoiLop(tenKhoi='Khối 11')
        # k12 = KhoiLop(tenKhoi='Khối 12')
        # db.session.add_all([k10, k11, k12])

        # l10a1 = Lop(tenLop='10A1', siSo=40, khoiLop_id=1)
        # l11a1 = Lop(tenLop='11A1', siSo=39, khoiLop_id=2)
        # l12a1 = Lop(tenLop='12A1', siSo=35, khoiLop_id=3)
        # db.session.add_all([l10a1, l11a1, l12a1])

        # hs1 = HocSinh(hoTen='Nguyễn Học Sinh', ngaySinh='2003-12-26', gioiTinh='Nam', diaChi='Hồ Chí Minh', soDT='012395784', email='sinh@ou.edu.vn', ngayNhapHoc='2022-05-02', lop_id=1)
        # db.session.add(hs1)

        # namhoc = NamHoc(tenNam='NH2425')
        # db.session.add(namhoc)

        # hk12425 = HocKy(tenHocKy='HK1_2425', ngayBD='2024-01-01', ngayKT='2024-05-21', namHoc_id=2)
        # db.session.add(hk12425)

        # mhtoan = MonHoc(tenMon='Toán 10')
        # db.session.add(mhtoan)

        # d1 = Diem(tenDiem='Điểm 15p', monHoc_id=1, hocSinh_id=1, hocKy_id=2)
        # db.session.add(d1)

        # ld15p = LoaiDiem(tenLoaiDiem='15 phút')
        # ld1t = LoaiDiem(tenLoaiDiem='1 tiết')
        # ldck = LoaiDiem(tenLoaiDiem='Cuối kỳ')
        # db.session.add_all([ld15p, ld1t, ldck])

        # ctd1 = ChiTietDiem(diem=10, loaiDiem_id=1, diem_id=2)
        # db.session.add(ctd1)

        # qd = QuyDinh(tuoiToiThieu=15, tuoiToiDa=20, siSoToiDa=40)
        # db.session.add(qd)
        #
        # lgv = LopGiaoVien(lop_id=1, giaoVien_id=1)
        # db.session.add(lgv)
        #
        # mhgv = MonHocGiaoVien(monHoc_id=1, giaoVien_id=1)
        # db.session.add(mhgv)

        db.session.commit()