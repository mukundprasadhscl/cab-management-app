"""SQLAlchemy ORM models for the Cab Management App."""

from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """Shared declarative base for all models."""


# ---------------------------------------------------------------------------
# Vehicle
# ---------------------------------------------------------------------------
class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    registration_number = Column(String(20), unique=True, nullable=False)
    model = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False, default=4)
    status = Column(
        Enum("available", "on_trip", "maintenance", "retired", name="vehicle_status"),
        nullable=False,
        default="available",
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    drivers = relationship("Driver", back_populates="vehicle")
    trips = relationship("Trip", back_populates="vehicle")

    def __repr__(self):
        return f"<Vehicle {self.registration_number} ({self.model})>"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------
class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    phone = Column(String(15), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    status = Column(
        Enum("available", "on_trip", "off_duty", name="driver_status"),
        nullable=False,
        default="available",
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="drivers")
    trips = relationship("Trip", back_populates="driver")

    def __repr__(self):
        return f"<Driver {self.name} ({self.license_number})>"


# ---------------------------------------------------------------------------
# Ride Request
# ---------------------------------------------------------------------------
class RideRequest(Base):
    __tablename__ = "ride_requests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_name = Column(String(100), nullable=False)
    pickup_location = Column(String(200), nullable=False)
    drop_location = Column(String(200), nullable=False)
    ride_date = Column(DateTime, nullable=False)
    purpose = Column(Text, nullable=True)
    status = Column(
        Enum("pending", "approved", "rejected", name="request_status"),
        nullable=False,
        default="pending",
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    trip = relationship("Trip", back_populates="ride_request", uselist=False)

    def __repr__(self):
        return f"<RideRequest {self.id} by {self.employee_name}>"


# ---------------------------------------------------------------------------
# Trip
# ---------------------------------------------------------------------------
class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ride_request_id = Column(
        Integer, ForeignKey("ride_requests.id"), nullable=False, unique=True
    )
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    status = Column(
        Enum(
            "scheduled",
            "in_progress",
            "completed",
            "cancelled",
            name="trip_status",
        ),
        nullable=False,
        default="scheduled",
    )
    scheduled_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    ride_request = relationship("RideRequest", back_populates="trip")
    vehicle = relationship("Vehicle", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")

    def __repr__(self):
        return f"<Trip {self.id} — {self.status}>"
