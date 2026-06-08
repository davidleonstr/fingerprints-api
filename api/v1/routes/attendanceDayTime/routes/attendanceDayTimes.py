from api.v1.routes.attendanceDayTime import attendanceDayTimeBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.attendanceDayTime.controller import AttendanceDayTimeController

@attendanceDayTimeBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createAttendanceDayTime():
    return AttendanceDayTimeController.create()

@attendanceDayTimeBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllAttendanceDayTimes():
    return AttendanceDayTimeController.getAll()

@attendanceDayTimeBP.route('/<int:attendanceDayTimeId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAttendanceDayTime(attendanceDayTimeId: int):
    return AttendanceDayTimeController.getOne(attendanceDayTimeId=attendanceDayTimeId)

@attendanceDayTimeBP.route('/<int:attendanceDayTimeId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=3)
def updateAttendanceDayTime(attendanceDayTimeId: int):
    return AttendanceDayTimeController.update(attendanceDayTimeId=attendanceDayTimeId)

@attendanceDayTimeBP.route('/<int:attendanceDayTimeId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteAttendanceDayTime(attendanceDayTimeId: int):
    return AttendanceDayTimeController.delete(attendanceDayTimeId=attendanceDayTimeId)