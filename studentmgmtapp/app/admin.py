from flask import redirect, request, jsonify
from flask_admin import Admin, BaseView, expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import logout_user, current_user
from app import app, db, dao
from app.models import MonHoc, KhoiLop, Lop, QuyDinh, VaiTroTaiKhoan


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', demlop=dao.dem_lop())


admin = Admin(app=app, name='Quản trị', template_mode='bootstrap4', index_view=MyAdminIndex())


class xacThucAdminMo(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.loaiTaiKhoan == VaiTroTaiKhoan.ADMIN


class xacThucAdminBa(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.loaiTaiKhoan == VaiTroTaiKhoan.ADMIN


class xacThucNguoiDungDN(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class MonHocView(xacThucAdminMo):
    column_list = ['id', 'tenMon']
    column_searchable_list = ['tenMon']
    column_filters = ['tenMon']
    can_export = True
    can_view_details = True
    column_labels = {'id': 'Mã môn', 'tenMon': 'Tên môn'}


class KhoiLopView(xacThucAdminMo):
    column_list = ['id', 'tenKhoi', 'dslop']
    column_labels = {'id': 'Mã khối', 'tenKhoi': 'Tên khối', 'dslop': 'Danh sách lớp trong khối'}


class LopView(xacThucAdminMo):
    column_list = ['id', 'tenLop', 'siSo', 'khoiLop_id']
    column_searchable_list = ['tenLop']
    column_filters = ['tenLop', 'siSo']
    can_export = True
    can_view_details = True
    column_labels = {'id': 'Mã lớp', 'tenLop': 'Tên lớp', 'siSo': 'Sĩ số', 'khoiLop_id': 'Mã khối'}


class QuyDinhView(xacThucAdminMo):
    column_list = ['id', 'tuoiToiThieu', 'tuoiToiDa', 'siSoToiDa']
    column_labels = {'id': 'Mã quy định', 'tuoiToiThieu': 'Tuổi tối thiếu', 'tuoiToiDa': 'Tuổi tối đa',
                     'siSoToiDa': 'Sĩ số tối đa của lớp'}


class thongKeView(xacThucAdminBa):
    @expose('/')
    def index(self):
        dsmon = dao.lay_ds_mon_hoc()
        idmonchon = request.args.get('tenmon')
        tktheomon = dao.thong_ke_tung_mon_theo_lop(idmonchon)
        tenmon = MonHoc.query.get(idmonchon)
        return self.render('admin/thongke.html',
                           dsmon=dsmon,
                           tk=dao.thong_ke_mon_theo_lop(),
                           tktheomon=tktheomon,
                           tenmon=tenmon.tenMon)


class veTrangChu(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')


class dangXuat(xacThucNguoiDungDN):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/')


admin.add_view(MonHocView(MonHoc, db.session, name='Môn học'))
admin.add_view(KhoiLopView(KhoiLop, db.session, name='Khối lớp'))
admin.add_view(LopView(Lop, db.session, name='Lớp'))
admin.add_view(QuyDinhView(QuyDinh, db.session, name='Quy định'))
admin.add_view(thongKeView(name='Thống kê'))
admin.add_view(veTrangChu(name='Về trang chủ'))
admin.add_view(dangXuat(name='Đăng xuất'))
