class Fields:
    class ActionItem:
        default = ('id', 'user', 'growthbook', 'scheduling', 'events', 'parent', 'goal', 'title', 'state', 'position', 'created_at')
        compact = ('id', 'title', 'state')
    class Client:
        default = ('id', 'name', 'user', 'subscriptions', 'token', 'created_at')
        compact = ('id', 'name')
    class Collaboration:
        default = ('id', 'inviter', 'invited', 'state', 'position', 'notifications', 'created_at')
        compact = ('id', 'inviter', 'invited', 'state', 'created_at')
    class Entity:
        default = ('id', 'type', 'datapoints')
        compact = ('id', 'type')
    class Event:
        default = ('id', 'user', 'growthbook', 'datetime', 'created_at')
        compact = ('id', 'datetime')
    class Goal:
        default = ('id', 'user', 'growthbook', 'scheduling', 'events', 'logs', 'name', 'state', 'position', 'created_at')
        compact = ('id', 'name', 'state')
    class Growthbook:
        default = ('id', 'user', 'collaborations', 'state', 'name', 'position', 'notifications', 'created_at')
        compact = ('id', 'state', 'name')
    class LogAttachment:
        default = ('id', 'url', 'created_at')
        compact = ('id', 'url')
    class Log:
        default = ('id', 'user', 'content', 'attachments', 'created_at')
        compact = ('id', 'content', 'attachments')
    class Metric:
        default = ('id', 'type', 'user', 'growthbook', 'item', 'entities', 'style', 'y_axis', 'x_axis', 'created_at')
        compact = ('id', 'type', 'style')
    class Scheduling:
        default = ('id', 'user', 'type', 'time', 'ends_at', 'ends_after', 'created_at')
        compact = ('id', 'type', 'time', 'ends_at', 'ends_after')
    class User:
        default = ('username', 'email', 'name', 'avatar', 'private', 'notifications', 'language', 'created_at')
        compact = ('username', 'name', 'avatar')
    class WebhookEvent:
        default = ('id', 'users', 'type', 'payload', 'created_at')
        compact = ('id', 'type')
    class WebhookSubscription:
        default = ('id', 'client', 'user', 'url', 'event_types', 'events', 'created_at')
        compact = ('id', 'url', 'event_types')
    class XAxis:
        default = ('id', 'interval', 'length', 'ends_at')
        compact = ('id', 'interval', 'length')
    class YAxis:
        default = ('id', 'scale', 'max', 'min')
        compact = ('id', 'scale')
