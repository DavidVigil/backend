from marshmallow import fields, validates, ValidationError, Schema
import re

class AppSchema(Schema):
    # Define the fields for the schema with their validation requirements
    name = fields.String(required=True)  # App name is mandatory
    info = fields.String(required=True)  # Info is mandatory
    description = fields.String(required=True)  # Description is mandatory
    url = fields.String(required=True)  # URL is mandatory
    logo_url = fields.String(required=True)  # Logo URL is mandatory
    origin = fields.String(required=True)  # Origin is mandatory
    author = fields.String(required=True)  # Author is mandalorian, is the _id of the user

    @validates('name')
    def validate_name(self, value):
        # Ensure the app name has a minimum and maximum length
        if len(value) < 3:
            raise ValidationError('App name must be at least 3 characters long')
        if len(value) > 50:
            raise ValidationError('App name must not exceed 50 characters')

    @validates('info')
    def validate_info(self, value):
        # Ensure the info field has a minimum and maximum length
        if len(value) < 5:
            raise ValidationError('Info must be at least 10 characters long')
        if len(value) > 200:
            raise ValidationError('Info must not exceed 200 characters')

    @validates('description')
    def validate_description(self, value):
        # If a description is provided, ensure it is not too long
        if value and len(value) > 500:
            raise ValidationError('Description must not exceed 500 characters')

    @validates('url')
    def validate_url(self, value):
        # Validate the URL format using a regular expression
        url_regex = r'^(https?:\/\/)?([\w\-])+(\.[\w\-]+)+[\w\-\.,@?^=%&:/~+#]*[\w\-\@?^=%&/~+#]$'
        if not re.match(url_regex, value):
            raise ValidationError('Invalid URL format')
        if len(value) > 200:
            raise ValidationError('URL must not exceed 200 characters')

    @validates('logo_url')
    def validate_logo_url(self, value):
        # If a logo URL is provided, validate its format and length
        if value:
            url_regex = r'^(https?:\/\/)?([\w\-])+(\.[\w\-]+)+[\w\-\.,@?^=%&:/~+#]*[\w\-\@?^=%&/~+#]$'
            if not re.match(url_regex, value):
                raise ValidationError('Invalid logo URL format')
            if len(value) > 200:
                raise ValidationError('Logo URL must not exceed 200 characters')
