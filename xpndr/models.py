from django.db import models
from django.urls import reverse
from django.utils import timezone
# from datetime import datetime  # import datetime
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
# from account.models import Profile


class Satellite(models.Model):
    satellite=models.CharField(max_length=50)
    def __str__(self):
        return self.satellite

class Transponder(models.Model):
    transponder_CHOICES = (('C', 'C'),('EXTC', 'EXTC'),('KU','KU'),('KA','KA'),)
    transponder=models.CharField(max_length=50,choices=transponder_CHOICES,default='C')
    transponder_number=models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    def __str__(self):
        return f'{self.transponder}{self.transponder_number}'

class Comment(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    # user=models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    #Ticket generation part
    date=models.DateField() 
    # date=models.DateField(default=timezone.localdate) # USE_TZ  for UTC
    time=models.TimeField(verbose_name="Time (HH:MM:SS)" )
    satellite = models.ForeignKey(Satellite,on_delete=models.CASCADE,related_name='comments')
    transponder = models.ForeignKey(Transponder,on_delete=models.CASCADE,related_name='comments')
    frequency=models.CharField(verbose_name="Affected frequency & Bandwidth (MHz)",max_length=100,blank=True)
    user_detail=models.CharField(verbose_name="User Detail",max_length=200,blank=True)
    complaint_CHOICES = (('Interference', 'Interference'),('Signal Degradation', 'Signal_Degradation'),('Overdrive','Overdrive'),('Sat Anamoly','Sat Anamoly'))
    complaint_type=models.CharField(max_length=50,choices=complaint_CHOICES,default='Interference')
    impact = models.TextField(verbose_name="Impact on user link",blank=True)
    issue_time=models.DateTimeField(verbose_name="Issue Start Date & Time ",blank=True)
    ticket=models.CharField(max_length=50,blank=True)
    # Analysis Part
    helix_dc=models.CharField(verbose_name="Helix Current/DC Input Power",max_length=50,blank=True)
    operating_point_CHOICES=(('P','P'),('P-1','P-1'),('P-2','P-2'),('P-3','P-3'),('P-4','P-4'),('P-5','P-5'),('P-6','P-6'),('P-7','P-7'),('P-8','P-8'),('P-10','P-10'),('P-11','P-11'),('P-12','P-12'),
    ('P-13','P-13'),('P-14','P-14'),('P-15','P-15'),('P-16','P-16'),('P-17','P-17'),('P-18','P-18'),('P-19','P-19'),('P-20','P-20'),('P-21','P-21'),('P-22','P-22'),('P-23','P-23'),('P-24','P-24'))
    operating_point=models.CharField(choices=operating_point_CHOICES,default='P-3',max_length=100,blank=True)
    bandwidth=models.CharField(verbose_name="Frequency and Bandwidth of Interference",max_length=100,blank=True)
    priority_CHOICES = (('High Priority', 'Highest_Priority'),('Priority', 'Priority'),('Normal','Normal'))
    priority=models.CharField(max_length=50,choices=priority_CHOICES,default='Normal',blank=True)
    details = models.TextField(verbose_name="Details of Interference/issue")
    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/',null=True,blank=True)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/',null=True,blank=True)
    slug = models.SlugField(max_length=250,unique_for_date='publish',blank=True)
    publish=models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True,blank=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Satellite {self.satellite} transponder {self.transponder}' 

    def get_absolute_url(self):
        return reverse("xpndr:comment_detail",args=[self.id])
        # return reverse("xpndr:comment_detail",args=[self.id, self.slug,self.publish.year,self.publish.month,self.publish.day])
        # return reverse("xpndr:comment_detail",args={self.satellite,self.transponder,self.transponder.transponder_number})
    
    # def get_absolute_url(self):
    #     return reverse("xpndr:comment_delete",args=[self.id,]) (self.date).replace('-', '')
    
    def save(self, *args, **kwargs):
        complaint_type1=" "
        sat=" "
        if self.complaint_type=="Interference":
            complaint_type1="I"
        elif self.complaint_type=="Signal_Degradation":
            complaint_type1="SD"
        elif self.complaint_type=="Overdrive":
            complaint_type1="S"
        else :
            complaint_type1="SA"
        sat=str(self.satellite)
        
        self.ticket=f"MCF/{sat[0]+sat[-2:]}{self.transponder}{complaint_type1}{(self.date.strftime('%Y''%m''%d'))}"
        # self.ticket=f"MCF/{sat.replace('SAT','')}{self.transponder}{complaint_type1}{(self.date.strftime('%Y''%m''%d'))}"
        if not self.slug:
            self.slug = slugify(str(timezone.now()))
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.upload:
            self.upload.delete()
        if self.photo:
            self.photo.delete()
        super().delete(*args, **kwargs)
