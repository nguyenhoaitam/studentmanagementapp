from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from app import app, db
from app.models import MonHoc, KhoiLop, Lop, Diem, QuyDinh

admin = Admin(app=app, name='Quản trị', template_mode='bootstrap4')

class MonHocView(ModelView):
    column_list = ['id', 'tenMon']


class KhoiLopView(ModelView):
    column_list = ['tenKhoi', 'dslop']


class LopView(ModelView):
    column_list = ['id', 'tenLop', 'siSo', 'khoiLop_id']
    column_searchable_list = ['tenLop']
    column_filters = ['tenLop', 'siSo']
    can_export = True
    can_view_details = True


admin.add_view(MonHocView(MonHoc, db.session))
admin.add_view(KhoiLopView(KhoiLop, db.session))
admin.add_view(LopView(Lop, db.session))