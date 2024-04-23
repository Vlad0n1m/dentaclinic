from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extrafields):
        if not username:
            raise ValueError("You have not provided username")
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    def create_user(self, username, email=None, password=None, **extrafields):
        extrafields.setdefault('is_staff', False)
        extrafields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extrafields)
    
    def create_superuser(self, username, email=None, password=None, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extrafields)
    
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField( blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, default='')
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    class Meta:
        db_table = 'authuser_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def get_full_name(self):
        return self.name
    
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
    
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='patient')
    pasport_id = models.CharField(max_length=255, blank=True, verbose_name="Паспорт ID")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    adress = models.CharField(max_length=255,  blank=True, verbose_name="Адрес")
    medcard = models.CharField(max_length=255, blank=True,  verbose_name="Медицинская карта")
    age = models.IntegerField(verbose_name="Возраст", blank=True, null=True)
    balance = models.IntegerField(default=0, verbose_name="Баланс")
    date_created = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name="Дата обновления")
    def __str__(self):
        return str(self.user.id)
    
class Doctor(models.Model): 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    date_created = models.DateTimeField(auto_now=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now_add=True,blank=True, null=True, verbose_name="Дата обновления")
    def __str__(self):
        return str(self.user.name)
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return str(self.user.username)
    
@receiver(post_save, sender=User)
def create_user_entity(sender, instance, **kwargs):
    if instance.is_patient:
        patient = Patient(user=instance)
        patient.save()
    elif instance.is_doctor:
        doctor = Doctor(user=instance)
        doctor.save()
    elif instance.is_manager:
        manager = Manager(user=instance)
        manager.save()
