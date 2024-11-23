from marshmallow import fields, validates, ValidationError

class AppSchema:
    title = fields.String(required=True)
    info = fields.String(required=True)
    description = fields.String(required=True)
    logo = fields.String(required=True)
    url = fields.String(required=True)
    source = fields.String(required=True)
    @validates('title')
    def validate_title(self, value):
        if len(value) < 5:
            raise ValidationError('Title must be at least 5 characters long')
        
    @validates('info')
    def validate_info(self, value):
        if len(value) < 5:
            raise ValidationError('Information must be at least 5 characters long')
            
    @validates('description')
    def validate_description(self, value):
        if len(value) < 4:
            raise ValidationError('Description must be at least 4 characters long')

    @validates('logo')
    def validate_logo(self, value):
        #Valid extensions for the images
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp')
        if not any(value.lower().endswith(ext) for ext in valid_extensions):
            raise ValidationError(f"Logo must be an image file with one of the following extensions: {', '.join(valid_extensions)}")
        
        
    @validates('url')
    def validate_url(self, value):
        if not (value.startswith('http://') or value.startswith('https://')):
            raise ValidationError('URL must start with http:// or https://')

    @validates('source')
    def validate_source(self, value):
        if len(value) < 4:
            raise ValidationError('Source must be at least 4 characters long')

        
        
if __name__ == '__main__':
    from logger.logger_base import Logger
    
    logger = Logger()
    schema = AppSchema()
    
    schema.validate_title('Title 5')
    try:
        schema.validate_author('Aut')
    except ValidationError as e:
        logger.error(f'An error has occurred: {e}')