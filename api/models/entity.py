from mongoengine import *


class Entity(EmbeddedDocument):
    TYPES = ('goal', 'action_item', 'collaboration', 'log')

    type = StringField(required=True, choices=TYPES)
    datapoints = SortedListField(StringField(), required=True)

    def clean(self):
        if self.type == 'goal' or self.type == 'action_item':
            permitted_datapoints = Task.STATES + ('count')
        if self.type == 'collaboration':
            permitted_datapoints = Collaboration.STATES + ('count')
        if self.type == 'log':
            permitted_datapoints = ('count')

        if not self.datasets.issubset(permitted_datapoints):
            raise ValidationError('For ' + self.type + 'entities, you may only use ' + str(permitted_datapoints) + 'as datapoints')
