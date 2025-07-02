from django.db import models
from django.contrib.auth.models import AbstractUser
from schools.models import Course, School
from django.core.exceptions import ValidationError
import re

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # @setter
    # def set_password(self):
    #     pass

    # class Login(models.Model):
    #     email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #     password = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class ChooseSubjects(models.Model):
    SymbolChoices = [
        ('LEVEL_1', 1),
        ('LEVEL_2', 2),
        ('LEVEL_3', 3),
        ('LEVEL_4', 4),
        ('LEVEL_5', 5),
        ('LEVEL_6', 6),
        ('LEVEL_7', 7),
    ]

    Selectives = [
    ('HHL' ,'Hindi Home Language'),
    ('HFAL' ,'Hindi First Additional Language'),
    ('HSAL' ,'Hindi Second Additional Language'), 
    ('GHL' ,'Gujarati Home Language'),
    ('GFAL' ,'Gujarati First Additional Language'),
    ('GSAL' ,'Gujarati Second Additional Language'), 
    ('THL' ,'Tamil Home Language'),
    ('TSAL' ,'Tamil Second Additional Language'),
    ('TFAL' ,'Tamil First Additional Language'),
    ('THL' , 'Telegu Home Language'),
    ('TFAL' ,'Telegu First Additional Language'),
    ('TSAL' ,'Telegu Second Additional Language'),
    ('UHL' ,'Urdu Home Language'), 
    ('UFAL' ,'Urdu First Additional Language'),  
    ('USAL','Urdu Second Additional Language'),
    ('AHL' ,'Arabic Home Language'),
    ('AFAL' ,'Arabic First Additional Language'),
    ('ASAL' ,'Arabic Second Additional Language'),
    ('FHL' ,'French Home Language'),
    ('FHAL' ,'French Home Additional Language'),
    ('FSAL' ,'French Second Additional Language'),
    ('HHL' ,'Hebrew Home Language'),
    ('HSAL' ,'Hebrew Second Additional Language'),
    ('HFAL' ,'Hebrew First Additional Language'),
    ('IHL' ,'Italian Home Language'),
    ('ISAL', 'Italian Second Additional Language'),
    ('IFAL', 'Italian First Additional Language'),
    ('Modern Greek', 'Modern Greek'), 
    ('Serbian', 'Serbian'), 
    ('SSAL' ,'Spanish Second Additional Language'),
    ('LSAL' ,'Latin Second Additional Language'),
    ('EHL','English Home Language'),
    ('EFAL','English First Additional Language'),
    ('ESAL','English Second Additional Language'),
    ('PHL' ,'Portuguese Home Language'), 
    ('GHL','German Home Language'),
    ('PSAL','Portuguese Second Additional Language'), 
    ('PFAL', 'Portuguese First Additional Language'), 
    ('GSAL' ,'German Second Additional Language'),
    ('Religion', 'Religion Studies'),
    ('IT', 'Information Technology'), 
    ('South African Sign Language Home Language', 'South African Sign Language Home Language'),
    ('Mandarin Second Additional Language', 'Mandarin Second Additional Language'),
    ('Afrikaans Home Language', 'Afrikaans Home Language'),
    ('Afrikaans First Additional Language', 'Afrikaans First Additional Language'),
    ('Afrikaans Second Additional Language', 'Afrikaans Second Additional Language'),
    ('isiZulu Home Language', 'isiZulu Home Language'),
    ('isiZulu Second Additional Language', 'isiZulu Second Additional Language'),
    ('isiZulu First Additional Language', 'isiZulu First Additional Language'),
    ('isiXhosa Home Language', 'isiXhosa Home Language'),
    ('isiXhosa First Additional Language', 'isiXhosa First Additional Language'),
    ('isiXhosa Second Additional Language', 'isiXhosa Second Additional Language'), 
    ('SiSwati Home Language', 'SiSwati Home Language'),
    ('SiSwati First Additional Language', 'SiSwati First Additional Language'),
    ('SiSwati Second Additional Language', 'SiSwati Second Additional Language'), 
    ('isiNdebele Home Language', 'isiNdebele Home Language'), 
    ('isiNdebele First Additional Language', 'isiNdebele First Additional Language'),
    ('isiNdebele Second Additional Language', 'isiNdebele Second Additional Language'), 
    ('Sepedi Home Language', 'Sepedi Home Language'),
    ('Sepedi First Additional Language', 'Sepedi First Additional Language'),
    ('Sepedi Second Additional Language', 'Sepedi Second Additional Language'),
    ('Sesotho Home Language', 'Sesotho Home Language'),
    ('Sesotho First Additional Language', 'Sesotho First Additional Language'),
    ('Sesotho Second Additional Language', 'Sesotho Second Additional Language'),
    ('Setswana Home Language', 'Setswana Home Language'),   
    ('Setswana First Additional Language', 'Setswana First Additional Language'),
    ('Setswana Second Additional Language', 'Setswana Second Additional Language'),
    ('Xitsonga Home Language', 'Xitsonga Home Language'),
    ('Xitsonga First Additional Language', 'Xitsonga First Additional Language'),
    ('Tshivenda Home Language', 'Tshivenda Home Language'),
    ('Tshivenda First Additional Language', 'Tshivenda First Additional Language'), 
    ('Tshivenda Second Additional Language', 'Tshivenda Second Additional Language'),
    ('Mathematics', 'Mathematics'),
    ('Mathematical Literacy', 'Mathematical Literacy'), 
    ('Technical Mathematics', 'Technical Mathematics'),
    ('Mandarin Second Additional Language', 'Mandarin Second Additional Language'),
    ('Engineering Graphics and Design', 'Engineering Graphics and Design'),
    ('Technical Mathematics', 'Technical Mathematics'),
    ('CAT', 'Computer Applications Technology'),
    ('Religion Studies', 'Religion Studies'),
    ('Sport and Exercise Science', 'Sport and Exercise Science'),
    ('Civil Technology', 'Civil Technology'),
    ('Information Technology', 'Information Technology'),
    ('Physical Sciences', 'Physical Sciences'),
    ('Technical Sciences', 'Technical Sciences'),
    ('Dance Studies', 'Dance Studies'),
    ('Nautical Science', 'Nautical Science'),
    ('Engineering Graphics and Design', 'Engineering Graphics and Design'),
    ('Geography', 'Geography'),
    ('Marine Sciences', 'Marine Sciences'),
    ('Mechanical Technology', 'Mechanical Technology'),
    ('Life Sciences', 'Life Sciences'),
    ('Electrical Technology', 'Electrical Technology'),
    ('Design', 'Design'),
    ('Accounting', 'Accounting'),
    ('Maritime Economics', 'Maritime Economics'), 
    ('Equine Studies', 'Equine Studies'),
    ('Consumer Studies', 'Consumer Studies'),
    ('Hospitality Studies', 'Hospitality Studies'),
    ('Dramatic Arts', 'Dramatic Arts'),
    ('Tourism', 'Tourism'),
    ('Visual Arts', 'Visual Arts'),
    ('Agricultural Management Practices', 'Agricultural Management Practices'),
    ('Business Studies', 'Business Studies'),
    ('Marine Sciences', 'Marine Sciences'),
    ('History', 'History'),
    ('Agricultural Technology', 'Agricultural Technology'),
    ('Agricultural Sciences', 'Agricultural Sciences'),
    ('Music', 'Music'),
    ('Economics', 'Economics'),
    ('History', 'History'),
    ('LO', 'Life Orientation'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, choices=[(choice[1], choice[1]) for choice in Selectives], default=None)
    percentage = models.IntegerField(default=0)
    level = models.IntegerField(choices=[(choice[1], choice[1]) for choice in SymbolChoices], default=0)

    def clean(self):
        if self.percentage not in range(0, 100):
            raise ValidationError('Invalid percentage, enter number between 0 and 100')
        elif 0 <= self.percentage <= 29 and self.level != 1:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 30 <= self.percentage <= 39 and self.level != 2:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 40 <= self.percentage <= 49 and self.level != 3:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 50 <= self.percentage <= 59 and self.level != 4:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 60 <= self.percentage <= 69 and self.level != 5:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 70 <= self.percentage <= 79 and self.level != 6:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')
        
        elif 80 <= self.percentage <= 100 and self.level != 7:
            raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')

    def __str__(self):
        return f'{self.name}  {self.percentage}%  {self.level}'

class ComputeAPS(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    APS = models.IntegerField(default=0)
    FPS = models.IntegerField(default=0)
    WPS = models.IntegerField(default=0)
        

    # @property
    def get_user_subjects(self):
        Score = 0
        chosen_subjects = ChooseSubjects.objects.filter(user=self.user)

        for subject in chosen_subjects:
            if subject.name not in ("Mathematics", "English Home Language", "English First Additional Language", "Life Orientation"):
                if subject.level > 2 and subject.percentage < 90:
                    Score += subject.level
                elif subject.percentage > 90:
                    Score += subject.level + 1 # Expected subject level to be 7.
            elif subject.name == "Life Orientation":
                if subject.level < 5:
                    pass
                elif subject.level == 5:
                    Score += 1
                elif subject.level == 6:
                    Score += 2
                elif subject.level == 7 and subject.percentage < 90:
                    Score += 3
                elif subject.percentage > 90:
                    Score += 4
            elif subject.name in ("Mathematics", "English Home Language", "English First Additional Language"):
                if subject.level < 3:
                    pass
                elif subject.level < 5:
                    Score += subject.level
                elif subject.percentage < 90:
                    Score += subject.level + 2
                else:
                    Score += subject.level + 3
        return Score
    
    def save(self, *args, **kwargs):
        self.APS = self.get_user_subjects()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user}  -  APS Score: {self.APS}"


class GetCourses(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # prospective_courses = models.ManyToManyField(Course, related_name='prospective_courses')
    Courses = models.CharField(max_length=10000)
    

    def retrievecourses(self):
        chosen_subjects = ChooseSubjects.objects.filter(user=self.user)
        prospective_courses = Course.objects.all()
        eligible_courses = []

        user_aps = ComputeAPS.objects.get(user=self.user).APS

        print("Chosen Subjects", chosen_subjects)
        print("Prospective Courses", prospective_courses)
        print("User APS:", user_aps)

        for course in prospective_courses:
            print("Course:", course.name)
            print("Course APS:", course.APS)
            if user_aps >= course.APS:
                print("APS match")
                for subject in chosen_subjects:
                    print("Subject:", subject)
                    print("Required Subject: ", course.Subjects.filter(name=subject.name).exists())
                    course_subject = course.Subjects.filter(name=subject.name)
                    if course.Subjects.filter(name=subject.name).exists() and subject.level >= course_subject.first().level:
                         print("Subject match")
                         print("Institution: ", course.institution)
                         print("Faculty: ", course.faculty)
                         eligible_courses.append(course.name)
                         continue
                    else:
                         print("no subject match")
                         break
            else:
                print("No APS match")
        print("Eligible courses:", eligible_courses)

        return '\n'.join(eligible_courses) 
                
    def save(self, *args, **kwargs):
        self.Courses = self.retrievecourses()   
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.Courses}'