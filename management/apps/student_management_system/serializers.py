from rest_framework import serializers
from .models import *
from django.db.models import Avg
from .tasks import send_email


class CreateStudentSerializer(serializers.ModelSerializer):
    # average_marks = serializers.SerializerMethodField(method_name='average')
    # grade = serializers.CharField()
    class Meta:
        model = Student
        fields =["id", "name", "roll", "class_name", "email", "created_at"]

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student    
    

class AllStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'class_name']

    
class StudentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'roll', 'class_name', 'email']


class SubjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = 'name', 'code'

    def create(self, validated_data):
        subject = Subject.objects.create(**validated_data)
        return subject


class ResultCreateSerializer(serializers.ModelSerializer):
    # subject = SubjectCreateSerializer(read_only=True)
    student_roll = serializers.IntegerField()
    subject_code = serializers.CharField()
    # email = serializers.EmailField(write_only=True)

    class Meta:
        model = Result
        fields = ['id', 'marks', 'student_roll', 'subject_code']

    def create(self, validated_data):
        student_roll = validated_data.pop('student_roll')
        subject_code = validated_data.pop('subject_code')
        marks = validated_data.get('marks')
        if (0 <= marks <= 100):
            try:
                student_obj = Student.objects.get(roll=student_roll)
            except Student.DoesNotExist:
                raise serializers.ValidationError("This roll of student doesn't exist.")
            try:
                subject_obj = Subject.objects.get(code=subject_code)
            except Subject.DoesNotExist:
                raise serializers.ValidationError("This subject doesn't exist.")
            if (Result.objects.filter(student=student_obj, subject=subject_obj).exists()):
                raise serializers.ValidationError("This result already exist for this student with this subject.")
            else:
                result = Result.objects.create(
                    student = student_obj,
                    subject = subject_obj,
                    marks = marks
                )
            student_mail = student_obj.email
            send_email.delay(student_mail)
            return result
        else:
            raise serializers.ValidationError("Marks must be between 0 to 100.")
        

# class ResultSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Res

class ResultListSerializer(serializers.ModelSerializer):
    student = StudentDetailsSerializer(read_only=True)
    subject = SubjectCreateSerializer(read_only=True)
    
    class Meta:
        model = Result
        fields = ['marks', 'student', 'subject']


class StudentGetByRollSerializer(serializers.ModelSerializer):
    result  = ResultListSerializer(read_only=True, many=True)
    average_marks = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
         
    def get_average_marks(self, obj):
        mark = obj.result.aggregate(average=Avg('marks'))['average']
        return mark 


    def get_grade(self, obj):
        mark = obj.result.aggregate(grade_mark=Avg('marks'))["grade_mark"]
        if (80 <= mark <= 100):
            return "A+"
        elif (70 <= mark <= 79):
            return "A"
        elif (60 <= mark <= 69):
            return "A-"
        elif (50 <= mark <= 59):
            return "B"
        elif (40 <= mark <= 49):
            return "C"
        elif (33 <= mark <=39):
            return "D"
        else:
            return "F"

    class Meta:
        model = Student
        fields = ['result', 'average_marks', 'grade']
        
        
