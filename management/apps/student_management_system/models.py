from django.db import models


# Create your models here.
class Student(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255, null=True, blank=True)
    roll = models.IntegerField(unique=True)
    class_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']



class Subject(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    


class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='result')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='result')
    marks = models.DecimalField(max_digits=5, decimal_places=2)
    crated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'subject')



