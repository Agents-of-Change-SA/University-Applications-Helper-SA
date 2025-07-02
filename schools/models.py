from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Institution(models.Model):
    """Allows for a choice of Institution.
    
    Institutions are presented in three forms following the actual representation in the country.
    These are - University, University of Technology and TVET Colleges. 
    A choice is made for each Institution at Instantiation.
    """
    type_choices = [
        ('UNI', 'University'),
        ('UoTech', 'University of Technology'),
        ('TVET', 'TVET College')
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=type_choices)

    def __str__(self):
        return f'''
            {self.name}\n
            {self.type}
        '''

class Faculty(models.Model):
    name = models.CharField(max_length=100)
    institution = models.ManyToManyField(Institution, through="Course")


    def __str__(self):
        return f'{self.name}'

class School(models.Model):    
    name = models.CharField(max_length=200, blank=True, null=True)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)
    faculty = models.ManyToManyField(Faculty, through="Course")    
    def __str__(self):
        return f'{self.name} - {self.abbreviation}'


class SubjectChoices(models.Model):
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
    ]

    SubjectLevels = {
        'Hindi Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Hindi First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Hindi Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'Gujarati Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Gujarati First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Gujarati Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'Tamil Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Tamil Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Tamil First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Telegu Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Telegu First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Telegu Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Urdu Home Language': [1, 2, 3, 4, 5, 6, 7], 
        'Urdu First Additional Language': [1, 2, 3, 4, 5, 6, 7],  
        'Urdu Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Arabic Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Arabic First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Arabic Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'French Home Language': [1, 2, 3, 4, 5, 6, 7],
        'French Home Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'French Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Hebrew Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Hebrew Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Hebrew First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Italian Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Italian Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Italian First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Modern Greek': [1, 2, 3, 4, 5, 6, 7], 
        'Serbian': [1, 2, 3, 4, 5, 6, 7], 
        'Spanish Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Latin Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'English Home Language': [1, 2, 3, 4, 5, 6, 7],
        'English First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'English Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Portuguese Home Language': [1, 2, 3, 4, 5, 6, 7], 
        'German Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Portuguese Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'Portuguese First Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'German Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Religion Studies': [1, 2, 3, 4, 5, 6, 7],
        'Information Technology': [1, 2, 3, 4, 5, 6, 7], 
        'South African Sign Language Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Mandarin Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Afrikaans Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Afrikaans First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Afrikaans Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'isiZulu Home Language': [1, 2, 3, 4, 5, 6, 7],
        'isiZulu Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'isiZulu First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'isiXhosa Home Language': [1, 2, 3, 4, 5, 6, 7],
        'isiXhosa First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'isiXhosa Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'SiSwati Home Language': [1, 2, 3, 4, 5, 6, 7],
        'SiSwati First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'SiSwati Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'isiNdebele Home Language': [1, 2, 3, 4, 5, 6, 7], 
        'isiNdebele First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'isiNdebele Second Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'Sepedi Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Sepedi First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Sepedi Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Sesotho Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Sesotho First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Sesotho Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Setswana Home Language': [1, 2, 3, 4, 5, 6, 7],   
        'Setswana First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Setswana Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Xitsonga Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Xitsonga First Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Tshivenda Home Language': [1, 2, 3, 4, 5, 6, 7],
        'Tshivenda First Additional Language': [1, 2, 3, 4, 5, 6, 7], 
        'Tshivenda Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Mathematics': [1, 2, 3, 4, 5, 6, 7],
        'Mathematical Literacy': [1, 2, 3, 4, 5, 6, 7], 
        'Technical Mathematics':[1, 2, 3, 4, 5, 6, 7],
        'Mandarin Second Additional Language': [1, 2, 3, 4, 5, 6, 7],
        'Engineering Graphics and Design': [1, 2, 3, 4, 5, 6, 7],
        'Technical Mathematics': [1, 2, 3, 4, 5, 6, 7],
        'Computer Applications Technology': [1, 2, 3, 4, 5, 6, 7],
        'Religion Studies': [1, 2, 3, 4, 5, 6, 7],
        'Sport and Exercise Science': [1, 2, 3, 4, 5, 6, 7],
        'Civil Technology': [1, 2, 3, 4, 5, 6, 7],
        'Information Technology': [1, 2, 3, 4, 5, 6, 7],
        'Physical Sciences': [1, 2, 3, 4, 5, 6, 7],
        'Technical Sciences': [1, 2, 3, 4, 5, 6, 7],
        'Dance Studies': [1, 2, 3, 4, 5, 6, 7],
        'Nautical Science': [1, 2, 3, 4, 5, 6, 7],
        'Engineering Graphics and Design': [1, 2, 3, 4, 5, 6, 7],
        'Geography': [1, 2, 3, 4, 5, 6, 7],
        'Marine Sciences': [1, 2, 3, 4, 5, 6, 7],
        'Mechanical Technology': [1, 2, 3, 4, 5, 6, 7],
        'Life Sciences': [1, 2, 3, 4, 5, 6, 7],
        'Electrical Technology': [1, 2, 3, 4, 5, 6, 7],
        'Design': [1, 2, 3, 4, 5, 6, 7],
        'Accounting': [1, 2, 3, 4, 5, 6, 7],
        'Maritime Economics': [1, 2, 3, 4, 5, 6, 7], 
        'Equine Studies': [1, 2, 3, 4, 5, 6, 7],
        'Consumer Studies': [1, 2, 3, 4, 5, 6, 7],
        'Hospitality Studies': [1, 2, 3, 4, 5, 6, 7],
        'Dramatic Arts': [1, 2, 3, 4, 5, 6, 7],
        'Tourism': [1, 2, 3, 4, 5, 6, 7],
        'Visual Arts': [1, 2, 3, 4, 5, 6, 7],
        'Agricultural Management Practices': [1, 2, 3, 4, 5, 6, 7],
        'Business Studies': [1, 2, 3, 4, 5, 6, 7],
        'Marine Sciences': [1, 2, 3, 4, 5, 6, 7],
        'History': [1, 2, 3, 4, 5, 6, 7],
        'Agricultural Technology': [1, 2, 3, 4, 5, 6, 7],
        'Agricultural Sciences': [1, 2, 3, 4, 5, 6, 7],
        'Music': [1, 2, 3, 4, 5, 6, 7],
        'Economics': [1, 2, 3, 4, 5, 6, 7],
        'History': [1, 2, 3, 4, 5, 6, 7],
    }

    name = models.CharField(max_length=200, choices=[(choice[1], choice[1]) for choice in Selectives])
    level = models.IntegerField(choices=[(choice[1], choice[1]) for choice in SymbolChoices], default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.level not in self.SubjectLevels.get(self.name, []):
            raise ValidationError('Invalid level for the chosen subject')

    def __str__(self):
        return f'{self.name, self.level}'


class Course(models.Model):    
    """The Course model is about the courses of an institution.
    
    The Model keeps data about the courses and their requirements. 
    """
    name = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    Subjects = models.ManyToManyField(SubjectChoices)
    APS = models.IntegerField(default=0)
    Duration = models.IntegerField(default=0)
    NBT = models.BooleanField(default=False)
    Requirements = models.TextField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
    



    
    
