from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *


# Create your views here.
@api_view(['POST'])
def create_student(request):
    serializer = CreateStudentSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Student create successfully."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def all_student(request):
    students = Student.objects.filter()
    serializer = AllStudentSerializer(students, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def student_details(request, std_id):
    student = Student.objects.get(id=std_id)
    serializer = StudentDetailsSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def subject_create(request):
    serializer = SubjectCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({"message": "Subject created successfully."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def all_subject(request):
    subject = Subject.objects.all()
    serializer = SubjectCreateSerializer(subject, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def result_create(request):
    serializer = ResultCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
        # subject = serializer.validated_data.get('subject'),
        # message = serializer.validated_data.get('message')
    # value = serializer.student_roll.get_value()
    # print(value)
    serializer.save()
    return Response({"message": "Result create successfully."}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def result_list(request):
    result = Result.objects.all()
    serializer = ResultListSerializer(result, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_student_by_roll(request):
    roll = request.data.get('roll')
    # print(request.data)
    # print('=============================',roll)
    student = Student.objects.get(roll=roll)
    # print('=================',student)
    serializer = StudentGetByRollSerializer(student)
    return Response(serializer.data, status=status.HTTP_200_OK)