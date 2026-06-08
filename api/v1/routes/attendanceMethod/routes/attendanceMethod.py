from api.v1.routes.attendanceMethod import attendanceMethodBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.attendanceMethod.controller import AttendanceMethodController

@attendanceMethodBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createAttendanceMethod():
    return AttendanceMethodController.create()

@attendanceMethodBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllAttendanceMethods():
    return AttendanceMethodController.getAll()

@attendanceMethodBP.route('/<int:attendanceMethodId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAttendanceMethod(attendanceMethodId: int):
    return AttendanceMethodController.getOne(attendanceMethodId=attendanceMethodId)

@attendanceMethodBP.route('/<int:attendanceMethodId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateAttendanceMethod(attendanceMethodId: int):
    return AttendanceMethodController.update(attendanceMethodId=attendanceMethodId)

@attendanceMethodBP.route('/<int:attendanceMethodId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteAttendanceMethod(attendanceMethodId: int):
    return AttendanceMethodController.delete(attendanceMethodId=attendanceMethodId)