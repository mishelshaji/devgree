from django.db import models

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    description = models.CharField(max_length = 250, blank=True, null=True)
    
    def __str__(self):
        return self.name



class Course(models.Model):
    id = models.AutoField(primary_key=True)
    coursename = models.CharField(max_length=15, unique=True)
    departmentname = models.ForeignKey(to=Department,on_delete=models.CASCADE)
    level = models.CharField(max_length=2)
    duration = models.CharField(max_length=2)
    
    
    def __str__(self):
        return self.coursename