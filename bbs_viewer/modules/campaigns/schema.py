from marshmallow import fields

from instashare.extensions import ma


class CommentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'text', 'created_at',)


class ImageSchema(ma.Schema):
    class Meta:
        fields = ('url', 'height', 'width',)


class ImagesSchema(ma.Schema):
    class Meta:
        fields = ('low_resolution', 'standard_resolution', 'thumbnail',)

    low_resolution = fields.Nested(ImageSchema)
    standard_resolution = fields.Nested(ImageSchema)
    thumbnail = fields.Nested(ImageSchema)


class MediaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'type', 'images', 'link', 'created_time', 'caption',)

    images = fields.Nested(ImagesSchema)
    caption = fields.Nested(CommentSchema)