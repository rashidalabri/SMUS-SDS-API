from flask import Flask, jsonify, abort, make_response
import smussdsparser

app = Flask(__name__)


@app.route('/smussds/api/v1.0/<string:session_id>')
def student(session_id):
    try:
        session = smussdsparser.Session(session_id)
        student = smussdsparser.Student(session)
        student_dict = student.__dict__
        student_dict.pop('courses')
        student_dict.pop('session')
        return jsonify({'student': student.__dict__})
    except smussdsparser.NotLoggedInException:
        return abort(make_response(jsonify(message="The session id provided is not logged in."), 401))


@app.route('/smussds/api/v1.0/<string:session_id>/courses')
def courses(session_id):
    try:
        session = smussdsparser.Session(session_id)
        student = smussdsparser.Student(session)
        return jsonify({'courses': [{'id': x.course_id, 'name': x.course_name, 'teacher_name': x.teacher_name} for x in student.get_student_courses()]})
    except smussdsparser.NotLoggedInException:
        return abort(make_response(jsonify(message="The session id provided is not logged in."), 401))


@app.route('/smussds/api/v1.0/<string:session_id>/course/<int:course_id>')
def course(session_id, course_id):
    try:
        session = smussdsparser.Session(session_id)
        course = smussdsparser.Course(session, course_id)
        return jsonify({'course': course.get_course_information()})
    except smussdsparser.NotLoggedInException:
        return abort(make_response(jsonify(message="The session id provided is not logged in."), 401))


@app.route('/smussds/api/v1.0/<string:session_id>/course/<int:course_id>/assignments')
def assignments(session_id, course_id):
    try:
        session = smussdsparser.Session(session_id)
        course = smussdsparser.Course(session, course_id)
        return jsonify({'assignments': [x.__dict__ for x in course.get_assignments()]})
    except smussdsparser.NotLoggedInException:
        return abort(make_response(jsonify(message="The session id provided is not logged in."), 401))


@app.route('/smussds/api/v1.0/<string:session_id>/course/<int:course_id>/assignment_marks')
def assignment_marks(session_id, course_id):
    try:
        session = smussdsparser.Session(session_id)
        course = smussdsparser.Course(session, course_id)
        return jsonify({'assignment_marks': [x.__dict__ for x in course.get_assignment_marks()]})
    except smussdsparser.NotLoggedInException:
        return abort(make_response(jsonify(message="The session id provided is not logged in."), 401))


if __name__ == '__main__':
    app.run(debug=True)
