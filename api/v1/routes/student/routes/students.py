from api.v1.routes.student import studentBP
from api.v1.auth import permissionLevel, apiKey
from api.v1.routes.student.controller import StudentController

@studentBP.route('/', methods=['POST'])
@apiKey()
@permissionLevel(levelRequired=3)
def createStudent():
    return StudentController.create()

@studentBP.route('/', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getAllStudents():
    return StudentController.getAll()

@studentBP.route('/<string:studentId>', methods=['GET'])
@apiKey()
@permissionLevel(levelRequired=1)
def getStudent(studentId: str):
    return StudentController.getOne(studentId=studentId)

@studentBP.route('/<string:studentId>', methods=['PUT'])
@apiKey()
@permissionLevel(levelRequired=2)
def updateStudent(studentId: str):
    return StudentController.update(studentId=studentId)

@studentBP.route('/<string:studentId>', methods=['DELETE'])
@apiKey()
@permissionLevel(levelRequired=3)
def deleteStudent(studentId: str):
    return StudentController.delete(studentId=studentId)