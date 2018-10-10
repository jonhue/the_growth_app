from marshmallow import Schema, fields


class UserSchema(Schema):
    private = fields.Boolean()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    class Meta:
        fields = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        ordered = True
