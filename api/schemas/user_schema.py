from marshmallow import Schema, fields


class UserSchema(Schema):
    private = fields.Boolean()
    notifications = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)

    class Meta(object):
        DEFAULT_FIELDS = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        COMPACT_FIELDS = ('username', 'name', 'avatar')

        fields = DEFAULT_FIELDS
        ordered = True
