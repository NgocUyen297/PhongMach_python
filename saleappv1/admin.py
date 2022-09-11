from saleappv1 import app, db, utils
from flask_admin.contrib.sqla import ModelView
from saleappv1.models import  Bills, UserRole, Medicine
from flask_admin import BaseView, expose, Admin
from flask_login import current_user, logout_user
from flask import redirect
from flask_admin import AdminIndexView
from flask import request
from datetime import datetime


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class BillsView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['cus_id', 'name']
    column_filters = ['cus_id', 'name']
    can_edit = None


class MedicineView(AuthenticatedModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    column_searchable_list = ['id', 'name', 'unit']


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',
                           month_stats=utils.bill_month_stats(year=year),
                           medi_month_stats=utils.medicine_month_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.ADMIN)


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.bill_stats())


admin = Admin(app=app,
              name="E-commerce Administration",
              template_mode='bootstrap4',
              index_view=MyAdminIndexView())
admin.add_view(AuthenticatedModelView(Bills, db.session))
admin.add_view(MedicineView(Medicine, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name='Logout'))
