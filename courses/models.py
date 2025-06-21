from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType # عشان اخزن صور او فيديو او ملف
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify

class Subject(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return str(self.title)


class Courses(models.Model):
    class Status(models.TextChoices):
        AVALIABLE = 'AV', 'Avaliable'
        DEREFT = 'DF', 'Dereft'
    owner = models.ForeignKey(User, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=250, verbose_name="عنوان الدورة")
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    overview = models.TextField()  
    photo = models.ImageField(upload_to='courses/photos', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=Status, default=Status.AVALIABLE)
    students = models.ManyToManyField(User, related_name='enrolled_courses', blank=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title 

    def clean_title(self, title):
    # استبدال الرموز غير المرغوبة بكلمات
        return title.replace('++', 'plus-plus').replace('+', 'plus').replace('#', 'sharp')

    def generate_unique_slug(self):
        base_slug = slugify(self.clean_title(self.title))
        slug = base_slug
        suffixes = ['course', 'online', 'class', 'learning', 'study', 'edu']
        index = 0

        while Courses.objects.filter(slug=slug).exists():
            if Courses.objects.filter(pk=self.pk, slug=slug).exists():
                # إذا نفس الدورة، نسمح بنفس السُّلَغ (عند التحديث)
                break
            if index >= len(suffixes):
                raise ValueError("لا يمكن توليد slug فريد بدون أرقام أو رموز، حاول تغيير العنوان.")
            slug = slugify(f"{base_slug}-{suffixes[index]}")
            index += 1

        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        else:
            try:
                old = Courses.objects.get(pk=self.pk)
                if old.title != self.title:
                    self.slug = self.generate_unique_slug()
            except Courses.DoesNotExist:
                self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)



class Module(models.Model):
    course = models.ForeignKey(Courses, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return str(self.title)    


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='content', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('text','file', 'image', 'video')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


class ItemBase(models.Model):
    owner = models.ForeignKey(User, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # معناه انه مابيتشئ في قاعدة البيانات بس المودل اللي بيورث منه بتظهر كل الخصائص فيه

    def __str__(self) -> str:
        return str(self.title)


class Text(ItemBase):
    text = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    image = models.FileField(upload_to='images')


class Video(ItemBase):
    video = models.URLField()