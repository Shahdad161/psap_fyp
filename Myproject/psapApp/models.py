import datetime
from django.db import models


class UniInfoTable(models.Model):
    university_name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    # abbreviated_as = models.CharField(max_length=20)
    hec_registration_number = models.CharField(max_length=15)
    hec_recognized = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)  # Adjust length as needed
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    campus = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)  # Adjust length as needed
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.university_name


class Admission(models.Model):
    SESSION_CHOICES = (
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Winter', 'Winter'),
    )

    PROGRAM_CHOICES = (
        ('Bachelors/BS', 'Bachelors/BS'),
        ('MS/M.phil', 'MS/M.phil'),
        ('Phd', 'Phd'),
    )

    ADMISSION_TEST_CHOICES = (
        ('Not required', 'Not required'),
        ('NTS NAT', 'NTS NAT'),
        ('ECAT', 'ECAT'),
        ('MCAT', 'MCAT'),
    )

    session = models.CharField(max_length=10, choices=SESSION_CHOICES)
    campus = models.CharField(max_length=300, default=True)
    program = models.CharField(max_length=15, choices=PROGRAM_CHOICES)
    admission_test = models.CharField(
        max_length=20, choices=ADMISSION_TEST_CHOICES)
    no_of_shortlisted_students = models.IntegerField()
    intermediate_required_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)
    bachelor_required_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)
    test_required_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    departments = models.CharField(max_length=100)
    university_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session} - {self.program}"


# Student work


class StdInfoTable(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()
    cnic = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    password = models.CharField(max_length=255, default='')
    phone = models.CharField(max_length=15)
    province = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    address = models.CharField(max_length=200)

    # Education Records
    intermediate = models.CharField(max_length=50)
    college_name = models.CharField(max_length=100)
    college_graduation_date = models.DateField()
    inter_obtained_marks = models.PositiveIntegerField(null=True)
    inter_total_marks = models.PositiveIntegerField(null=True)

    matriculation = models.CharField(max_length=50)
    school_name = models.CharField(max_length=100)
    matric_graduation_date = models.DateField()
    matric_obtained_marks = models.PositiveIntegerField(null=True)
    matric_total_marks = models.PositiveIntegerField(null=True)

    # Documents
    self_photo = models.ImageField(upload_to='student/')
    id_card_photo = models.ImageField(upload_to='student/')
    inter_transcript = models.FileField(upload_to='student/')
    inter_degree = models.FileField(upload_to='student/')
    matric_transcript = models.FileField(upload_to='student/')
    matric_degree = models.FileField(upload_to='student/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# class AppliedForAdmissionForm(models.Model):
#     university = models.CharField(max_length=100)
#     campus = models.CharField(max_length=100)
#     program = models.CharField(max_length=100)
#     department = models.CharField(max_length=100)
#     required_test = models.CharField(max_length=100)
#     test_obtained_marks = models.IntegerField()
#     test_total_marks = models.IntegerField()
#     fees_slip = models.FileField(upload_to='fees_slips/')

#     # Link to the student info using a foreign key
#     student_info = models.ForeignKey(StdInfoTable, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.university} - {self.program} - {self.department}"
