from pathlib import Path
from django.db import models
from django.contrib.auth.models import AbstractUser
from schools.models import Course, School, Institution
from django.core.exceptions import ValidationError
import re
import csv
from decimal import Decimal


# Create your models here.
# Helper to load CSV choices
def load_choices(filename):
    choices_path = Path(__file__).resolve().parent / "choices" / filename
    with open(choices_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [(row[0], row[1]) for row in reader]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # @setter
    # def set_password(self):
    #     pass

    # class Login(models.Model):
    #     email = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    #     password = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

class ChooseSubjects(models.Model):

    SymbolChoices = [(code, int(value)) for code, value in load_choices("symbol_choices.csv")]


    Selectives = load_choices("selectives.csv")

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, choices=[(choice[1], choice[1]) for choice in Selectives], default=None)
    percentage = models.IntegerField(default=0)
    level = models.IntegerField(choices=[(choice[1], choice[1]) for choice in SymbolChoices], default=0)

    def clean(self):
        if self.percentage not in range(0, 101):
            raise ValidationError('Invalid percentage, enter number between 0 and 100')

        # Check level-percentage consistency
        percentage_to_level = {
            range(0, 30): 1,
            range(30, 40): 2,
            range(40, 50): 3,
            range(50, 60): 4,
            range(60, 70): 5,
            range(70, 80): 6,
            range(80, 101): 7
        }
        for perc_range, level in percentage_to_level.items():
            if self.percentage in perc_range and self.level != level:
                raise ValidationError('Invalid inputs, there is a mismatch in your percentages and achievement levels')

    def __str__(self):
        return f'{self.name}  {self.percentage}%  {self.level}'

class ComputeAPS(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    Average = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    APS = models.IntegerField(default=0)
    FPS = models.IntegerField(default=0)
    WPS = models.IntegerField(default=0)
        

    # @property
    def get_user_subjects(self):
        Score = 0
        chosen_subjects = ChooseSubjects.objects.filter(user=self.user)

        if self.institution.name == "University of the Witwatersrand, Johannesburg":
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

        elif self.institution.name == "University of Johannesburg":
            pass


    def set_average(self):
        chosen_subjects = ChooseSubjects.objects.filter(user=self.user)
        if not chosen_subjects:
            return Decimal('0.00')
        
        total = sum(Decimal(subject.percentage) for subject in chosen_subjects)
        return total / Decimal(len(chosen_subjects))

    def save(self, *args, **kwargs):
        self.APS = self.get_user_subjects() or 0  # fallback to 0 if None
        self.Average = self.set_average() or 0     # fallback to 0 if None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user}  -  APS Score: {self.APS}"


class GetCourses(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    chosen_institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
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

            print("No APS match")
            print("Eligible courses:", eligible_courses)

        return '\n'.join(eligible_courses)

                    
    def save(self, *args, **kwargs):
        self.Courses = self.retrievecourses()   
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.Courses}'