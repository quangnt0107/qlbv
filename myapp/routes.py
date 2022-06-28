
from flask import redirect, render_template, request, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse
from myapp import app, db
from myapp.forms import LoginForm, RegisterServiceForm, RegistrationForm
from myapp.models import Bill, Medicine, Result, Service, ServiceType, User, TreatmentDoctor

from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView



@app.route('/', methods=['GET', 'POST'])
@login_required
def home():

  return render_template('index.html', title='home')


@app.route('/result', methods =['GET'])
def result():

  return render_template('result.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    if current_user.role == 0:
      return redirect(url_for('admin.index'))
    return redirect(url_for('home'))


  form= LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()

    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password, please try again!', 'warning')
      return redirect(url_for('login'))

    login_user(user, form.remember_me.data)
    flash('Login successful', 'success')

    if current_user.role == 0:
      return redirect(url_for('admin.index'))

    return redirect(url_for('home'))

  return render_template('login.html', title='login', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))


  form= RegistrationForm()

  if form.validate_on_submit():
    u = User(
      username=form.username.data,
      email=form.email.data,
      password=form.password.data
    )
    db.session.add(u)
    db.session.commit()
    flash('dang ky thanh cong!', 'success')
    return redirect(url_for('login'))

  return render_template('register.html', title='login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
  logout_user()
  return redirect(url_for('login'))



# service
@app.route('/chose_service_type', methods=['GET', 'POST'])
def chose_service_type():


  service_types = ServiceType.query.all()

  return render_template('chose_service_type.html', service_types=service_types)


@app.route('/register_service/<sv_type_id>', methods=['GET', 'POST'])
def register_service(sv_type_id):

  services = Service.query.filter_by(service_type_id=sv_type_id).all()
  print(services)

  form = RegisterServiceForm()
  form.services.choices=services

  form.name.data = current_user.username
  form.email.data = current_user.email


  if form.validate_on_submit():
    current_user.role = 2
    service=Service.query.filter_by(service_name=form.services.data).first()
    current_user.services.append(service)
    db.session.commit()

    flash('Successfully registered service!', 'success')
    return redirect(url_for('home'))



  return render_template('register_service.html', title='register service', form=form)




# admin dashboard
class MyAdminIndexView(AdminIndexView):

  @login_required
  @expose('/')
  def index(self):

    # if(current_user is None or current_user.role != 0):
    #   flash('You should an administrator', 'info')
    #   return redirect(url_for('home'))

    flash('Welcome!', 'success')
    return self.render('admin.html')



admin = Admin(app, name='Admin', template_mode='bootstrap4', index_view=MyAdminIndexView(name="Dashboard"))


class AuthenticatedBaseView(BaseView):
  def is_accessible(self):
    return current_user.is_authenticated

  def inaccessible_callback(self, name, **kwargs):
    # redirect to login page if user doesn't have access
    logout_user()
    flash('You are not allowed to access this page', 'error')
    return redirect(url_for('login'))


class AuthenticatedModelView(ModelView):
  def is_accessible(self):
    return current_user.is_authenticated and current_user.role == 0

  def inaccessible_callback(self, name, **kwargs):
    pass


class LogoutView(AuthenticatedBaseView):
  @expose('/')
  def logout(self):
    logout_user()
    return redirect(url_for('home'))


class UserView(AuthenticatedModelView):
  column_searchable_list=['username']
  column_exclude_list=['password']
  column_details_exclude_list=['password']
  can_view_details=True
  details_modal=True


class ServiceView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True


class ServiceTypeView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True


class TreatmentDoctorView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True


class ResultView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True

class MedicineView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True

class BillView(AuthenticatedModelView):
  can_view_details=True
  details_modal=True




admin.add_view(UserView(User, db.session))
admin.add_view(ServiceView(Service, db.session))
admin.add_view(ServiceTypeView(ServiceType, db.session))
admin.add_view(TreatmentDoctorView(TreatmentDoctor, db.session))
admin.add_view(ResultView(Result, db.session))
admin.add_view(MedicineView(Medicine, db.session))
admin.add_view(BillView(Bill, db.session))

admin.add_view(LogoutView(name='Logout'))