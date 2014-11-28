from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    login = models.CharField(max_length=40)
    password = models.CharField(max_length=60)

    def __unicode__(self):
        return u'%s %s' % (self.first_name, self.last_name)
    class Meta:
        ordering = ['last_name']

class Dashboard(models.Model):
    author = models.ForeignKey(User, to_field='id')
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=30)
    type = models.CharField(max_length=30)
    resource = models.CharField(max_length=30)
    upload_date = models.DateTimeField()
    file_name = models.CharField(max_length=100)
    file_field = models.FileField(upload_to='')

    def __unicode__(self):
        return u'%s %s %s' % (self.author, self.title, self.upload_date)

class Message_form(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=50)
    contact_email = models.EmailField()
    message_info = models.TextField(max_length=256)

    def __unicode__(self):
        return u'%s %s %s' % (self.fname, self.lname, self.contact_email)
    def __str__(self):
        return u'%s %s %s' % (self.fname, self.lname, self.contact_email)

class Published(models.Model):
    id_user = models.ForeignKey(User, to_field='id')
    dashboard = models.CharField(max_length=100)
    name = models.CharField(max_length=150)
    resource = models.CharField(max_length=100)

