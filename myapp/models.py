
from flask_login import UserMixin
from myapp import login, db






'''
user role
0: admin
1: user
2. BN - patient
3. BS - doctor
'''



class TreatmentDoctor (db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  patients = db.relationship('User', backref='treatment_doctor', uselist=False)
  result_id = db.Column(db.Integer, db.ForeignKey('result.id'))
  service_id = db.Column( db.Integer, db.ForeignKey('service.id'))
  role = db.Column(db.Integer, nullable=True, default=3)

userservice = db.Table('userservice',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)



class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password = db.Column(db.String(128))
  role = db.Column(db.Integer, nullable=True, default=1)


  treatment_doctor_id = db.Column(db.Integer, db.ForeignKey('treatment_doctor.id'))


  results = db.relationship('Result',  backref='patient')


  services = db.relationship('Service', secondary=userservice, backref=db.backref('users', lazy=True))

  medicins = db.relationship('Medicine', backref='patient')

  bills = db.relationship('Bill', backref='patient')

  def check_password(self, password):
    if(password == self.password):
      return True
    else:
      return False


  # def follow(self, user):
  #   if not self.is_following(user):
  #     self.doctors.append(user)

  # def unfollow(self, user):
  #   if self.is_following(user):
  #     self.doctors.remove(user)

  # def is_following(self, user):
  #   return self.doctors.filter(
  #     treatment.c.patient_id == user.id).count() > 0


  def __repr__(self):
    return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
  return User.query.get(int(id))







class Service(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  service_name = db.Column(db.String(64), index=True, unique=True)
  price = db.Column(db.String(64))

  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))


  service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))  # real column


  def __repr__(self):
    return (self.service_name)

class ServiceType(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  service_type_name = db.Column(db.String(64), index=True, unique=True)

  services = db.relationship('Service', backref='service_type')


  def __repr__(self):
    return '<Service Type {}>'.format(self.service_type_name)



class Result(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  result = db.Column(db.String(64))
  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  is_nhap_vien = db.Column(db.Boolean, default=False)
  is_toa_thuoc = db.Column(db.Boolean, default=False)


#   def __repr__(self):
#     return '<Result {}>'.format(self.result)


class Medicine(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, unique=True)
  count = db.Column(db.Integer, default=0)
  price = db.Column(db.String(64))
  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))


#   def __repr__(self):
#     return '<Medicine {}>'.format(self.name)


class Bill(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  total = db.Column(db.String(20), default=0 )
  patient_id = db.Column(db.Integer, db.ForeignKey('user.id'))


  def tongtien(self):
    patient = User.query.get(self.patient_id)






#   def __repr__(self):
#     return '<Bill {}>'.format(self.id)
