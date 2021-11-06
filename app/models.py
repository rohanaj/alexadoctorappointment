from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class User1(models.Model):
    user = (
    
        ('doctor','Doctor'),
        ('patient','Patient'),
        ('assistant','Assistant')
    
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(choices=user, max_length=9, default='assistant')
    def __str__(self):
        return self.first_name + " " + self.last_name


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User1, on_delete=models.CASCADE)
    user.user_type = "doctor"
    
    def __str__(self):
        return str(self.user)
    
    
class Assistant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User1, on_delete=models.CASCADE)
    user.user_type = "assistant"
    def __str__(self):
        return str(self.user)
    

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User1, on_delete=models.CASCADE)
    user.user_type = "patient"
    def __str__(self):
        return str(self.user)
        
@receiver(post_save, sender=User1)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "doctor":
            Doctor.objects.create(user=instance)
        elif instance.user_type == "patient":
            Patient.objects.create(user=instance)

@receiver(post_save, sender=User1)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "doctor":
        instance.doctor.save()
    elif instance.user_type == "patient":
        instance.patient.save()        
class Appointment(models.Model):
    TIMESLOT_LIST = (
        (1, '10:00 – 11:00'),
        (2, '11:00 – 12:00'),
        (3, '12:00 – 13:00'),
        (4, '13:00 – 14:00'),
        (5, '14:00 – 15:00'),
        (6, '15:00 – 16:00'),
        (7, '16:00 – 17:00'),
        (8, '17:00 – 18:00'),
        (9, '18:00 – 19:00'),
    )

    #timeslot = models.IntegerField(choices=TIMESLOT_LIST, null=True)
    time = models.DateTimeField(blank=True)
    doctor = models.ForeignKey(Doctor, on_delete = models.CASCADE, related_name='doctor')
    patient = models.ForeignKey(Patient, on_delete = models.CASCADE, related_name='patient')


    def __str__(self):
        return str(self.doctor) + " " + str(self.patient) 
