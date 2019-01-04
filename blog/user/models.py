from django.db import models
from django.db.models import Q,F
from tinymce.models import HTMLField

# Create your models here.
class TeaManager(models.Manager):
    def create_teacher(self,name):
        teacher=self.create(name=name)
        return teacher

class Teacher(models.Model):
    id=models.AutoField(primary_key=True)
    # age=models.
    name=models.CharField(max_length=50)
    age=models.IntegerField()
    useaddTea = TeaManager()

    def __str__(self):
        return "%s，姓名：%s，\t"%(self.id,self.name)

    '''
    @classmethod
    def creat_teacher(cls,name):
        teacher=cls(name=name)
        return teacher
    '''
class StuManager(models.Manager):
    def create_student(self,name):
        students=self.create(name=name)
        return students

class student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    teaid= models.ForeignKey(Teacher,on_delete=models.CASCADE)
    addStu=StuManager()
    def __str__(self):
        return ('学号：%s，姓名：%s，指导老师: %s；密码：%s')%(self.id,self.name,self.teaid, self.password)


class ArtManager(models.Manager):
    def create_art(self,name):
        articles=self.create(name=name)
        return articles

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    # content = models.TextField()
    content = HTMLField()
    author =models.CharField(max_length=50)
    stuid=models.ForeignKey(student,on_delete=models.CASCADE)  #直接查找所指向的表的主键
    addArt=ArtManager()
    def __str__(self):
        return "编号：%s，姓名：%s，文章名字：%s；"%(self.id,self.author,self.content)

