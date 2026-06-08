from flask import Blueprint

from api.v1.routes.status import statusBP
from api.v1.routes.entity import entityBP
from api.v1.routes.interactor import interactorBP
from api.v1.routes.student import studentBP
from api.v1.routes.role import roleBP
from api.v1.routes.permissionLevel import permissionLevelBP
from api.v1.routes.attendance import attendanceBP
from api.v1.routes.attendanceDayTime import attendanceDayTimeBP
from api.v1.routes.attendanceMethod import attendanceMethodBP
from api.v1.routes.fingerprint import fingerprintBP
from api.v1.routes.fingerprintName import fingerprintNameBP
from api.v1.routes.fingerprintType import fingerprintTypeBP
from api.v1.routes.auth import authBP
from api.v1.routes.system import systemBP

v1BP = Blueprint('v1', __name__)

v1BP.register_blueprint(statusBP, url_prefix='/status')
v1BP.register_blueprint(entityBP, url_prefix='/entity')
v1BP.register_blueprint(interactorBP, url_prefix='/interactor')
v1BP.register_blueprint(studentBP, url_prefix='/student')
v1BP.register_blueprint(roleBP, url_prefix='/role')
v1BP.register_blueprint(permissionLevelBP, url_prefix='/permission-level')
v1BP.register_blueprint(attendanceBP, url_prefix='/attendance')
v1BP.register_blueprint(attendanceDayTimeBP, url_prefix='/attendance-day-time')
v1BP.register_blueprint(attendanceMethodBP, url_prefix='/attendance-method')
v1BP.register_blueprint(fingerprintBP, url_prefix='/fingerprint')
v1BP.register_blueprint(fingerprintNameBP, url_prefix='/fingerprint-name')
v1BP.register_blueprint(fingerprintTypeBP, url_prefix='/fingerprint-type')
v1BP.register_blueprint(authBP, url_prefix='/auth')
v1BP.register_blueprint(systemBP, url_prefix='/system')