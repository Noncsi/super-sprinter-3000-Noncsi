from super_sprinter_3000.connectdatabase import ConnectDatabase
from peewee import *


class Entries(Model):
    story_title = CharField(null=True)
    user_story = CharField(null=True)
    acceptance_criteria = CharField(null=True)
    business_value = IntegerField()
    estimation_time = FloatField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
