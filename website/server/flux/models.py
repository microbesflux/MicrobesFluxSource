from django.contrib.auth.models import User
from django.db import models
from constants import user_filebase
import uuid

""" This Profile model describes a user's optimization problem
and pathway target.
"""

class Profile(models.Model):
    name = models.CharField(max_length = 30)
    user = models.ForeignKey(User)
    diskfile    = models.FileField(max_length=100, upload_to=user_filebase + "fba")
    status      = models.CharField(max_length= 30)
    model_type  = models.CharField(max_length= 10)
    submitted   = models.BooleanField(default=False)
    submitted_date = models.CharField(max_length=30)

class Compound(models.Model):
    name      = models.CharField(max_length = 10)
    alias     = models.CharField(max_length = 10)
    long_name = models.CharField(max_length =140)

    def __unicode__(self):
        return self.name + " A:" + self.alias + " L:" + self.long_name

class Task(models.Model):
    task_id   =  models.AutoField(primary_key = True)
    task_type =  models.CharField(max_length = 10)
    main_file =  models.CharField(max_length = 50) 
    additional_file =  models.CharField(max_length = 50)
    email     = models.EmailField(max_length = 75)
    status    = models.CharField(max_length = 10)
	uuid      = models.CharField(max_length = 50, primary_key = True, default = make_uuid, editable = False)
    	

	def make_uuid(self):
	    return str(uuid.uuid4().int>>64)
    def __unicode__(self):
        return str(self.uuid) + "," + str(self.task_id) + "," + self.main_file + "," + self.task_type + "," + self.email + "," + self.status + "," + self.additional_file

# User can save/load their models. We put the serialized PathwayNetwork
# object in "Collection".
class Collection(models.Model):
    id =  models.AutoField(primary_key = True)
    user = models.ForeignKey(User)
    name = models.CharField(max_length = 140)
    pickle = models.BinaryField()

# Intermediate file storage
class UserFile(models.Model):
    file_id = models.AutoField(primary_key = True)
    user_id = models.ForeignKey(User)
    collection_id = models.ForeignKey(Collection)
