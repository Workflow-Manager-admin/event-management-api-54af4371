from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class EventSchema(Schema):
    """Schema for serializing/deserializing Event model."""
    id = fields.Int(dump_only=True, description="Event ID")
    title = fields.Str(required=True, validate=validate.Length(min=1), description="Title of the event")
    description = fields.Str(missing=None, allow_none=True, description="Description of the event")
    start_time = fields.DateTime(required=True, description="Event start time (ISO format)")
    end_time = fields.DateTime(required=True, description="Event end time (ISO format)")
    location = fields.Str(missing=None, allow_none=True, description="Event Location")
    created_at = fields.DateTime(dump_only=True, description="Creation timestamp")
    updated_at = fields.DateTime(dump_only=True, description="Last updated timestamp")
