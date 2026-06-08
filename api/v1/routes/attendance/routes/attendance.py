from api.v1.routes.attendance import attendanceBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.attendance.controller import AttendanceController

@attendanceBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=2)
def createAttendance():
    return AttendanceController.create()

@attendanceBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllAttendances():
    return AttendanceController.getAll()

@attendanceBP.route('/<string:attendanceId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAttendance(attendanceId: str):
    return AttendanceController.getOne(attendanceId=attendanceId)

@attendanceBP.route('/<string:attendanceId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=2)
def updateAttendance(attendanceId: str):
    return AttendanceController.update(attendanceId=attendanceId)

@attendanceBP.route('/<string:attendanceId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteAttendance(attendanceId: str):
    return AttendanceController.delete(attendanceId=attendanceId)