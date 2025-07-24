from flask.views import MethodView
from flask_smorest import Blueprint, abort
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from app.models import db, Event
from app.schemas import EventSchema

load_dotenv()  # Load .env file

blp = Blueprint(
    "Events",
    "events",
    url_prefix="/events",
    description="Endpoints for managing events",
)

event_schema = EventSchema()
events_schema = EventSchema(many=True)

# PUBLIC_INTERFACE
@blp.route("/")
class EventListResource(MethodView):
    """List all events, or create a new event."""

    # PUBLIC_INTERFACE
    @blp.response(200, EventSchema(many=True), description="List of all events.")
    def get(self):
        """Get a list of all events."""
        events = Event.query.order_by(Event.start_time.asc()).all()
        return events_schema.dump(events)

    # PUBLIC_INTERFACE
    @blp.arguments(EventSchema, location="json")
    @blp.response(201, EventSchema, description="Event created successfully.")
    def post(self, new_data):
        """Create a new event."""
        try:
            event = Event(
                title=new_data["title"],
                description=new_data.get("description"),
                start_time=new_data["start_time"],
                end_time=new_data["end_time"],
                location=new_data.get("location"),
            )
            db.session.add(event)
            db.session.commit()
            return event, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))


# PUBLIC_INTERFACE
@blp.route("/<int:event_id>")
class EventResource(MethodView):
    """Retrieve, update, or delete a specific event."""

    # PUBLIC_INTERFACE
    @blp.response(200, EventSchema, description="Event retrieved successfully.")
    def get(self, event_id):
        """Retrieve an event by ID."""
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")
        return event_schema.dump(event)

    # PUBLIC_INTERFACE
    @blp.arguments(EventSchema(partial=True), location="json")
    @blp.response(200, EventSchema, description="Event updated successfully.")
    def patch(self, update_data, event_id):
        """Update an event by ID. Partial update allowed."""
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")

        for key, value in update_data.items():
            setattr(event, key, value)
        event.updated_at = datetime.utcnow()
        try:
            db.session.commit()
            return event
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))

    # PUBLIC_INTERFACE
    @blp.response(204, description="Event deleted successfully.")
    def delete(self, event_id):
        """Delete an event by ID."""
        event = Event.query.get(event_id)
        if not event:
            abort(404, message="Event not found.")

        try:
            db.session.delete(event)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=str(e))
        return "", 204
