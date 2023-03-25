from time import timezone
from django.db import models
from ecousers.models import Account
import uuid
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
# Create your models here.
class Problem(models.Model):

    def get_image_path(instance,filename):
        title, ext = filename.split('.')
        image_path = 'problem_photos/{problem_title}/{photo_name}.{ext}'.format(problem_title=instance.title,photo_name=title,ext=ext)
        return image_path

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    created = models.DateTimeField(default = timezone.now)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    location = models.CharField(max_length=100,blank=True, null=True)
    problem_photo_main = models.ImageField(upload_to=get_image_path)
    problem_photo_1 = models.ImageField(upload_to=get_image_path,blank=True)
    problem_photo_2 = models.ImageField(upload_to=get_image_path,blank=True)
    problem_photo_3 = models.ImageField(upload_to=get_image_path,blank=True)
    

    slug = models.SlugField(blank=True,null=True)
    isTrending = models.BooleanField(default=False)
    
    upvotes = models.ManyToManyField(Account, blank=True, related_name='upvoted_problems')
    downvotes = models.ManyToManyField(Account, blank=True, related_name='downvoted_problems')

    def save(self,*args,**kwargs):
        self.slug =slugify(self.title)
        super(Problem,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Problem'
        verbose_name_plural = 'Problems'
        
        
class Project(models.Model):
    
    def get_image_path(instance,filename):
        title, ext = filename.split('.')
        image_path = 'project_photos/{project_title}/{photo_name}.{ext}'.format(project_title=instance.title,photo_name=title,ext=ext)
        return image_path

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    location = models.CharField(max_length=100,blank=True, null=True)
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    created = models.DateTimeField(default = timezone.now)
    category = models.ForeignKey('Category',on_delete=models.SET_NULL,null=True)
    project_photo_main = models.ImageField(upload_to=get_image_path)
    project_photo_1 = models.ImageField(upload_to=get_image_path,blank=True)
    project_photo_2 = models.ImageField(upload_to=get_image_path,blank=True)
    project_photo_3 = models.ImageField(upload_to=get_image_path,blank=True)
   
  
    slug = models.SlugField(blank=True,null=True)
    isTrending = models.BooleanField(default=False)
    
    upvotes = models.ManyToManyField(Account, blank=True, related_name='upvoted_projects')
    downvotes = models.ManyToManyField(Account, blank=True, related_name='downvoted_projects')

    def save(self,*args,**kwargs):
        self.slug =slugify(self.title)
        super(Project,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        
class Category(models.Model):
    ## for project and problem category
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/', blank=True, null=True)
    
    slug = models.SlugField(blank=True, null=True) 
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)    
        super(Category ,self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_url(self):
        return reverse('projects_by_category', args=[self.slug])
    
    
    
    def __str__(self):
        return self.name 