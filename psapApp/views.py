# from .models import Student
# Assuming you have a Student model defined for your database table
# from .models import StdApplyAdmission
# Import the User model if you're using it
from django.contrib.auth.models import User
from .models import AppliedForAdmissionForm, StudentMeritData, Admission, StdInfoTable
from .models import AppliedForAdmissionForm  # Import your model
from django.http import JsonResponse
from .models import AppliedForAdmissionForm
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from .models import StdInfoTable,UniInfoTable
from django.db import connection
from .models import StdInfoTable
from .models import Admission
from .forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse
from django.db import connection as conn

from django.contrib import messages

# Create your views here.

# main page index file
email = ''
password = ''


def index(request):
    universities = UniInfoTable.objects.all()  # Fetch all universities from the database
    testimonials= Testimonial.objects.all()
    context = {'universities': universities, 'testimonials':testimonials}
    return render(request, 'index.html',context)


def uniOrStd(request):
    return render(request, 'uniorstd.html')


def loginasUni(request):
    return render(request, 'loginasUni.html')


def loginasStd(request):
    # Add your view logic here
    return render(request, 'loginasStd.html',{})


def registerasUniPage(request):
    # Add your view logic here
    return render(request, 'registerasUni.html')


def registerasStd(request):
    # Add your view logic here
    return render(request, 'registerasStd.html')

from django.shortcuts import render
from .models import StudentMeritData  # Import your StudentMeritData model
 # Import the StudentInfo model

def stdHome(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')

        # Fetch the student's first name
        student_info = StdInfoTable.objects.get(email=email)
        stdName = student_info.first_name

        # Fetch data from the StudentMeritData model based on the relationship
        merit_data = StudentMeritData.objects.filter(student_info=student_info)

        return render(request, 'stdHome.html', {'stdName': stdName, 'merit_data': merit_data})


from django.shortcuts import render, redirect
from .models import Admission, AppliedForAdmissionForm

def stdApplied(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')

        try:
            # Fetch the student's information from the StudentInfoTable
            student_info = StdInfoTable.objects.get(email=email)

            if request.method == 'POST':
                # Get the form data from the POST request
                university_name = request.POST.get('university')
                campus = request.POST.get('campus')
                program = request.POST.get('program')
                department = request.POST.get('department')
                required_test = request.POST.get('required_test')
                test_obtained_marks = request.POST.get('test_obtained_marks')
                test_total_marks = request.POST.get('test_total_marks')
                fees_slip = request.FILES.get('fees_slip')

                # Check if the student has already applied for the same combination
                if AppliedForAdmissionForm.objects.filter(
                    university=university_name,
                    campus=campus,
                    program=program,
                    department=department,
                    std_email=email,
                ).exists():
                    return render(request, 'stdNewApplication.html', {'error_message': 'Already applied for this program.'})

                # Fetch the admission conditions for the selected university
                admission_conditions = Admission.objects.filter(
                    university_name=university_name).first()

                # Calculate the student's merit based on the formula defined in Admission model
                # Replace this with your actual merit calculation formula

                # Fetch the required percentages from the Admission model and convert them to float
                intermediate_required_percentage = float(
                    admission_conditions.intermediate_required_percentage)
                matric_required_percentage = float(
                    admission_conditions.bachelor_required_percentage)
                test_required_percentage = float(
                    admission_conditions.test_required_percentage)

                # Convert the obtained marks to float
                inter_obtained_marks = float(student_info.inter_obtained_marks)
                matric_obtained_marks = float(
                    student_info.matric_obtained_marks)

                # Calculate the student's merit based on the formula defined in Admission model
                merit_percentage = (
                    (inter_obtained_marks / student_info.inter_total_marks) * intermediate_required_percentage +
                    (matric_obtained_marks / student_info.matric_total_marks) * matric_required_percentage +
                    (float(test_obtained_marks) / float(test_total_marks)) *
                    test_required_percentage
                )

                # Save the form data into the table
                admission_form = AppliedForAdmissionForm.objects.create(
                    university=university_name,
                    campus=campus,
                    program=program,
                    department=department,
                    required_test=required_test,
                    test_obtained_marks=test_obtained_marks,
                    test_total_marks=test_total_marks,
                    fees_slip=fees_slip,
                    std_email=email,
                    student_info=student_info,  # Associate the application with student info
                )
                admission_form.save()

                # Save the calculated merit data in the StudentMeritData model
                student_merit_data = StudentMeritData(
                    student_info=student_info,
                    selected_university=university_name,
                    campus=campus,
                    department=department,
                    merit_percentage=merit_percentage,
                )
                student_merit_data.save()

                # Render the same page with a success message
                return render(request, 'stdNewApplication.html', {'success_message': 'Your application was Submitted'})

            # Render the same page with an error message if the request method is not POST
            return render(request, 'stdNewApplication.html', {'error_message': 'Invalid request method'})

        except StdInfoTable.DoesNotExist:
            return render(request, 'stdNewApplication.html', {'error_message': 'Student information not found.'})

        except Admission.DoesNotExist:
            return render(request, 'stdNewApplication.html', {'error_message': 'University not found in admission conditions.'})

    else:
        return redirect('university_login/')


def stdNewApplication(request):
    email = request.session.get('email')
    cursor = conn.cursor()
    cursor.execute(
        "SELECT first_name FROM psapapp_stdinfotable WHERE email=%s", [email])
    stdName = cursor.fetchone()[0]

    # Get the selected university from the query parameter
    selected_university = request.GET.get("university")

    # Fetch all admissions data initially
    admissions = Admission.objects.all()

    # Filter admissions based on the selected university, if available
    if selected_university:
        admissions = admissions.filter(university_name=selected_university)

    admission_data = []
    for admission in admissions:
        data = {
            'university_name': admission.university_name,
            'department': admission.departments,
            'campus': admission.campus,
            "admission_test": admission.admission_test,
            'program': admission.program,
        }
        admission_data.append(data)

    context = {
        'admissions': admission_data,
        'stdName': stdName,
        'selected_university': selected_university,
    }
    return render(request, 'stdNewApplication.html', context)


def uniHome(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
        admissions = Admission.objects.filter(university_name=uniName)
        context = {
            'admissions': admissions,
            'uniName': uniName,
        }
        return render(request, 'uniHome.html', context)

# page display functiom

def uniNewAdmissions(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
    return render(request, 'uniNewAdmissions.html', {'uniName': uniName})

# not neceessayr


def uniRegistrationForm(request):
    # Add your view logic here
    return render(request, 'uniRegistrationForm.html')


def registerasUni(request):
    if request.method == 'POST':
        d = request.POST
        email = d.get("email")
        password = d.get("password")
        university_name = d.get("university_name")
        hec_recognized = d.get("hec_recognized", "no")
        hec_registration_number = d.get("hec_registration_number")
        phone = d.get("phone")
        province = d.get("province")
        city = d.get("city")
        campus = d.get("campus")
        zip_code = d.get("zip_code")
        address = d.get("address")

        # Check if the email already exists in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_uniinfotable WHERE email=%s", [email])
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            error_message = "Email is already registered to another account. Please use a different email."
            return render(request, 'uniRegistrationForm.html', {'error_message': error_message})

        else:
            # Create a new record
            c = "INSERT INTO psapapp_uniinfotable (university_name, email, password, hec_recognized, hec_registration_number, phone, province, city, campus, zip_code, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(c, [university_name, email, password, hec_recognized,
                           hec_registration_number, phone, province, city, campus, zip_code, address])

        cursor.close()

        # Redirect to the appropriate page after successful registration/update
        if 'signupasUni' in request.POST:
            success_message = messages.success(request, 'Account created successfully. Please login.')
            return render(request, 'loginasUni.html',{'success_message':success_message})

    else:
        return render(request, 'registerasUni.html')


def uniUpdateForm(request):
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email and password match an existing record in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_uniinfotable WHERE email=%s AND password=%s", [email, password])
        email_password_match = cursor.fetchone()[0]

        if email_password_match > 0:
            # Email and password match, proceed to update the university data
            university_name = request.POST.get("university_name")
            hec_recognized = request.POST.get("hec_recognized", "no")
            hec_registration_number = request.POST.get(
                "hec_registration_number")
            phone = request.POST.get("phone")
            province = request.POST.get("province")
            city = request.POST.get("city")
            campus = request.POST.get("campus")
            zip_code = request.POST.get("zip_code")
            address = request.POST.get("address")

            # Update the record
            c = "UPDATE psapapp_uniinfotable SET university_name=%s, hec_recognized=%s, hec_registration_number=%s, phone=%s, province=%s, city=%s, campus=%s, zip_code=%s, address=%s WHERE email=%s"
            cursor.execute(c, [university_name, hec_recognized, hec_registration_number,
                               phone, province, city, campus, zip_code, address, email])
            conn.commit()

            # Redirect to the uniHome page with a success message
            success_message = "Data updated successfully!"
            university_data = UniInfoTable.objects.get(email=email)
            return render(request, 'uniUpdateForm.html', {'success_message': success_message, 'university_data': university_data})

        else:
            # Email and password do not match, show an error message
            error_messageInvalidEmail = "Invalid email or password. Please try again."
            university_data = UniInfoTable.objects.get(email=email)
            return render(request, 'uniUpdateForm.html', {'error_messageInvalidEmail': error_messageInvalidEmail, 'university_data': university_data})

    else:
        if request.session.get('authenticated') == True:
            email = request.session.get('email')
            try:
                university_data = UniInfoTable.objects.get(email=email)
            except UniInfoTable.DoesNotExist:
                # Handle the case where the record does not exist
                return render(request, 'uniUpdateForm.html', {'error_messageInvalidEmail': "University data not found.", 'university_data': university_data})

            # Render the form with existing data
            return render(request, 'uniUpdateForm.html', {'university_data': university_data})


# annouce button
def announce_admissions(request):
    if request.method == 'POST':
        session = request.POST.get('session')
        campus = request.POST.get('campus')
        program = request.POST.get('program')
        admission_test = request.POST.get('admission_test')
        no_of_shortlisted_students = request.POST.get(
            'no_of_shortlisted_students')
        intermediate_required_percentage = request.POST.get(
            'intermedaite_required_percentage')
        bachelor_required_percentage = request.POST.get(
            'bachelor_required_percentage')
        test_required_percentage = request.POST.get(
            'Test_required_percentage_percentage')
        departments_list = request.POST.getlist('department')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        email = request.session.get('email')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
        uniName = cursor.fetchone()[0]
        # Join the list of department names into a comma-separated string
        departments = ', '.join(departments_list)

        admission = Admission(
            session=session,
            campus=campus,
            program=program,
            admission_test=admission_test,
            no_of_shortlisted_students=no_of_shortlisted_students,
            intermediate_required_percentage=intermediate_required_percentage,
            bachelor_required_percentage=bachelor_required_percentage,
            test_required_percentage=test_required_percentage,
            start_date=start_date,
            end_date=end_date,
            departments=departments,
            university_name=uniName,
        )
        admission.save()

        admissions = Admission.objects.filter(university_name=uniName)
        context = {
            'admissions': admissions,
            'uniName': uniName,
        }
        return render(request, 'uniHome.html', context)

    return render(request, 'uniHome.html', {'uniName': uniName})


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Admission, StudentMeritData  # Import your models

# ... (previous code)

# ... (previous code)

def university_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Perform authentication and retrieve university name
        # Assuming you have already established a database connection
        cursor = conn.cursor()
        c = "SELECT * FROM psapapp_uniinfotable WHERE email=%s AND password=%s"
        cursor.execute(c, (email, password))
        authenticated = cursor.fetchone()

        if authenticated:
            request.session['authenticated'] = True
            request.session['email'] = email

            cursor.execute("SELECT university_name FROM psapapp_uniinfotable WHERE email=%s", [email])
            uniName = cursor.fetchone()[0]

            # Query admissions and merits data
            admissions = Admission.objects.filter(university_name=uniName)

            # Query and count the number of students applied for each admission
            for admission in admissions:
                admission.students_applied = StudentMeritData.objects.filter(selected_university=uniName, department=admission.departments).count()

            context = {
                'admissions': admissions,
                'uniName': uniName,
            }

            return render(request, 'uniHome.html', context)
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'loginasUni.html')
    else:
        logout(request)
        return render(request, 'loginasUni.html')




# Student Work


def student_registration(request):
    if request.method == 'POST':
        d = request.POST
        first_name = d.get("first_name")
        last_name = d.get("last_name")
        dob = d.get("dob")
        cnic = d.get("cnic")
        gender = d.get("gender")
        email = d.get("email")
        password = d.get("password")
        phone = d.get("phone")
        province = d.get("province")
        city = d.get("city")
        zip_code = d.get("zip_code")
        address = d.get("address")
        intermediate = d.get("intermediate")
        college_name = d.get("college_name")
        college_graduation_date = d.get("college_graduation_date")
        inter_obtained_marks = d.get("inter_obtained_marks", 0)
        inter_total_marks = d.get("inter_total_marks", 0)
        matriculation = d.get("matriculation")
        school_name = d.get("school_name")
        matric_graduation_date = d.get("matric_graduation_date")
        matric_obtained_marks = d.get("matric_obtained_marks", 0)
        matric_total_marks = d.get("matric_total_marks", 0)
        # document
        self_photo = request.FILES['self_photo']
        id_card_photo = request.FILES['id_card_photo']
        inter_transcript = request.FILES['inter_transcript']
        inter_degree = request.FILES['inter_degree']
        matric_transcript = request.FILES['matric_transcript']
        matric_degree = request.FILES['matric_degree']

        # Check if the email already exists in the database
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_stdinfotable WHERE email=%s", [email])
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            error_message = "Email is already registered to another account. Please use a different email."
            return render(request, 'registerasStd.html', {'error_message': error_message})

        else:
            # Create a new student record
            # password_hashed = make_password(password)
            c = "INSERT INTO psapapp_stdinfotable (first_name, last_name, dob, cnic, gender, email, password, phone, province, city, zip_code, address, intermediate, college_name, college_graduation_date, inter_obtained_marks, inter_total_marks, matriculation, school_name, matric_graduation_date, matric_obtained_marks, matric_total_marks, self_photo, id_card_photo, inter_transcript, inter_degree, matric_transcript, matric_degree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(c, [first_name, last_name, dob, cnic, gender, email, password, phone, province, city, zip_code, address, intermediate, college_name,
                               college_graduation_date, inter_obtained_marks, inter_total_marks, matriculation, school_name, matric_graduation_date, matric_obtained_marks, matric_total_marks, self_photo, id_card_photo, inter_transcript, inter_degree, matric_transcript, matric_degree])

            cursor.close()

        # Redirect to the appropriate page after successful registration/update
        if 'signupasStd' in request.POST:
            return render(request, 'loginasStd.html')
        success_message = "Account created successfully! Please login"
        return render(request, 'registerasStd.html', {'success_message': success_message})

    else:
        return render(request, 'registerasUni.html')


def student_login(request):
    if request.method == 'POST':
        cursor = conn.cursor()
        email = request.POST['email']
        password = request.POST['password']
        c = "SELECT * FROM psapapp_stdinfotable WHERE email='{}' AND password='{}'".format(
            email, password)
        cursor.execute(c)
        authenticated = tuple(cursor.fetchall())
        if authenticated:
            request.session['authenticated'] = True
            request.session['email'] = email

            cursor.execute(
                "SELECT first_name from psapapp_stdinfotable WHERE email=%s", [email])
            stdName = cursor.fetchone()[0]
            student_info = StdInfoTable.objects.get(email=email)
            stdName = student_info.first_name

        # Fetch data from the StudentMeritData model based on the relationship
            merit_data = StudentMeritData.objects.filter(student_info=student_info)
            return render(request, 'stdHome.html', {'stdName': stdName,'merit_data': merit_data})
        else:
            messages.error(request, 'Invalid Email or Password')
            return render(request, 'loginasStd.html')
    else:
        logout(request)
        return render(request, 'loginasStd.html')


def stdUpdateForm(request):
    if request.method == 'POST':
        # Get the email and password from the form
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email and password match an existing record in the database
        cursor = conn.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM psapapp_stdinfotable WHERE email=%s AND password=%s", [email, password])
        email_password_match = cursor.fetchone()[0]

        if email_password_match > 0:
            # Email and password match, proceed to update the student data
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            dob = request.POST.get("dob")
            cnic = request.POST.get("cnic")
            gender = request.POST.get("gender")
            phone = request.POST.get("phone")
            province = request.POST.get("province")
            city = request.POST.get("city")
            zip_code = request.POST.get("zip_code")
            address = request.POST.get("address")
            intermediate = request.POST.get("intermediate")
            college_name = request.POST.get("college_name")
            college_graduation_date = request.POST.get(
                "college_graduation_date")
            inter_obtained_marks = request.POST.get("inter_obtained_marks")
            inter_total_marks = request.POST.get("inter_total_marks")
            matriculation = request.POST.get("matriculation")
            school_name = request.POST.get("school_name")
            matric_graduation_date = request.POST.get("matric_graduation_date")
            matric_obtained_marks = request.POST.get("matric_obtained_marks")
            matric_total_marks = request.POST.get("matric_total_marks")

            # Update the record
            update_query = """
                    UPDATE psapapp_stdinfotable 
                    SET first_name = %s, last_name = %s, dob = %s, cnic = %s, gender = %s, 
                    phone = %s, province = %s, city = %s, zip_code = %s, address = %s, 
                    intermediate = %s, college_name = %s, college_graduation_date = %s, 
                    inter_obtained_marks = %s, inter_total_marks = %s, matriculation = %s, 
                    school_name = %s, matric_graduation_date = %s, matric_obtained_marks = %s, 
                    matric_total_marks = %s 
                    WHERE email = %s AND password = %s
                """

            # Execute the query
            cursor.execute(update_query, (first_name, last_name, dob, cnic, gender, phone,
                                          province, city, zip_code, address, intermediate,
                                          college_name, college_graduation_date,
                                          inter_obtained_marks, inter_total_marks,
                                          matriculation, school_name, matric_graduation_date,
                                          matric_obtained_marks, matric_total_marks,
                                          email, password))

            # Commit the changes to the database
            conn.commit()

            # Redirect to the update form page with a success message
            success_message = "Data updated successfully!"
            student_data = StdInfoTable.objects.get(email=email)

            return render(request, 'stdUpdate.html', {'success_message': success_message, 'student_data': student_data},)

        else:
            # Email and password do not match, show an error message
            error_message = "Invalid email or password. Please try again."
            student_data = StdInfoTable.objects.get(email=email)

            return render(request, 'stdUpdate.html', {'error_message': error_message, 'student_data': student_data},)
    else:
        if request.session.get('authenticated') == True:
            email = request.session.get('email')
            try:
                student_data = StdInfoTable.objects.get(email=email)
            except StdInfoTable.DoesNotExist:
                # Handle the case where the record does not exist
                return render(request, 'stdUpdate.html', {'error_messageInvalidEmail': "Student data not found.", 'student_data': student_data})

            # Render the form with existing data
            return render(request, 'stdUpdate.html', {'student_data': student_data})



def apply_admission(request):
    if request.session.get('authenticated') == True:
        email = request.session.get('email')
        # Get the selected university from the form data
        selected_university = request.POST.get('university')

        # Check if a university is selected
        if selected_university:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT university_name FROM psapapp_uniinfotable WHERE email=%s AND university_name=%s",
                [email, selected_university]
            )
            university_name = cursor.fetchone()

            if university_name:
                return render(request, 'uniHome.html', {'email': email, 'university': university_name})
            else:
                return render(request, 'uniHome.html', {'message': 'University not found for the given email.'})
        else:
            return render(request, 'uniHome.html', {'message': 'Please select a university.'})
    else:
        return render(request, 'stdHome.html', {'message': 'User not authenticated.'})


# Merit calculation

from django.http import HttpResponseNotFound

def delete_merit_data(request, merit_id):
    try:
        merit_data = StudentMeritData.objects.get(pk=merit_id)

        # Check if the logged-in user is the owner of the record
        if merit_data.student_info.email == request.session.get('email'):
            merit_data.delete()
            return redirect('stdHome')  # Redirect to the student's home page after deletion
        else:
            return HttpResponseNotFound("Record not found.")
    except StudentMeritData.DoesNotExist:
        return HttpResponseNotFound("Record not found.")

# DOWNLOAD MERIT LIST



from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.shortcuts import get_object_or_404
from .models import StudentMeritData, Admission
from django.http import Http404



def download_merit_list(request, university_name, department):
    # Get the Admission object for the specified university and department
    admission = get_object_or_404(Admission, university_name=university_name, departments=department)

    # Query the StudentMeritData model to filter by university and department
    merit_list = StudentMeritData.objects.filter(selected_university=university_name, department=department).order_by('-merit_percentage')

    if not merit_list:
        raise Http404("No students found in the merit list for this department.")

    # Fetch all test marks for the students in the merit list
    student_emails = [entry.student_info.email for entry in merit_list]
    test_marks_dict = {}
    admission_forms = AppliedForAdmissionForm.objects.filter(
        university=university_name,
        campus__in=[entry.campus for entry in merit_list],
        department=department,
        std_email__in=student_emails,
    )
    for form in admission_forms:
        test_marks_dict[form.std_email] = form.test_obtained_marks

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{university_name}_{department}_merit_list.pdf"'

    # Create a PDF document using ReportLab
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define custom styles for the title and subtitle
    title_style = ParagraphStyle(
        'TitleStyle',
        fontSize=18,
        fontName='Helvetica-Bold',
        alignment=1,
        spaceAfter=12
    )
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        fontSize=14,
        fontName='Helvetica-Bold',
        alignment=1,
        spaceAfter=6
    )

    # Define data for the table
    table_data = [['CNIC', 'Student Name', 'Intermediate Marks', 'Matric Marks', 'Test Marks', 'Merit Percentage']]

    for entry in merit_list:
        student_info = entry.student_info  # This gets the related StdInfoTable object
        test_marks = test_marks_dict.get(student_info.email, "N/A")

        table_data.append([student_info.cnic, student_info.first_name + " " + student_info.last_name,
                           student_info.inter_obtained_marks, student_info.matric_obtained_marks, test_marks, entry.merit_percentage])

    # Create the table
    table = Table(table_data)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(table_style)

    # Build the PDF document
    story = []
    title = Paragraph('Merit List', title_style)
    subtitle = Paragraph(f'University: {university_name}, Department: {department}', subtitle_style)
    spacer = Spacer(1, 12)
    story.extend([title, subtitle, spacer, table])

    doc.build(story)

    # Move the buffer's cursor to the beginning
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()

    return response



# views.py
from django.shortcuts import render, redirect
from .models import Testimonial
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Testimonial  # Import your Testimonial model
def submit_testimonial(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        text = request.POST.get('text')
        
        # Validate the data (you can add your own validation logic here)
        if not name or not designation or not text:
            messages.error(request, 'Please fill in all fields.')
        else:
            # Create a new Testimonial object and save it to the database
            testimonial = Testimonial(name=name, designation=designation, text=text)
            testimonial.save()
            
            # Add a success message
            message = messages.success(request, 'Thank you for your testimonial!')
            
            return redirect('submit_testimonial')  # Redirect to a success page
    
    return render(request, 'submit_testimonial.html')
