"""Tests for SQLAlchemy models and database helpers."""

import pytest
from datetime import datetime

from database.models import Driver, RideRequest, Trip, Vehicle


# ---- Vehicle tests -------------------------------------------------------

class TestVehicle:
    def test_create_vehicle(self, db_session):
        v = Vehicle(
            registration_number="KA-01-AB-1234",
            model="Toyota Innova",
            capacity=6,
            status="available",
        )
        db_session.add(v)
        db_session.commit()

        result = db_session.query(Vehicle).first()
        assert result is not None
        assert result.registration_number == "KA-01-AB-1234"
        assert result.model == "Toyota Innova"
        assert result.capacity == 6
        assert result.status == "available"

    def test_vehicle_default_status(self, db_session):
        v = Vehicle(
            registration_number="KA-02-CD-5678",
            model="Maruti Ertiga",
            capacity=5,
        )
        db_session.add(v)
        db_session.commit()

        result = db_session.query(Vehicle).filter_by(
            registration_number="KA-02-CD-5678"
        ).one()
        assert result.status == "available"

    def test_vehicle_unique_registration(self, db_session):
        v1 = Vehicle(registration_number="KA-01-XX-0001", model="Swift", capacity=4)
        db_session.add(v1)
        db_session.commit()

        v2 = Vehicle(registration_number="KA-01-XX-0001", model="Dzire", capacity=4)
        db_session.add(v2)
        with pytest.raises(Exception):
            db_session.commit()

    def test_vehicle_repr(self, db_session):
        v = Vehicle(registration_number="KA-03-GH-9012", model="Sedan", capacity=4)
        db_session.add(v)
        db_session.commit()
        assert "KA-03-GH-9012" in repr(v)
        assert "Sedan" in repr(v)


# ---- Driver tests ---------------------------------------------------------

class TestDriver:
    def test_create_driver(self, db_session):
        d = Driver(
            name="Ravi Kumar",
            license_number="DL-1234567890",
            phone="9876543210",
            status="available",
        )
        db_session.add(d)
        db_session.commit()

        result = db_session.query(Driver).first()
        assert result.name == "Ravi Kumar"
        assert result.license_number == "DL-1234567890"
        assert result.phone == "9876543210"

    def test_driver_vehicle_assignment(self, db_session):
        v = Vehicle(registration_number="KA-05-EF-9999", model="Innova", capacity=6)
        db_session.add(v)
        db_session.commit()

        d = Driver(
            name="Suresh",
            license_number="DL-0000000001",
            phone="9000000001",
            vehicle_id=v.id,
        )
        db_session.add(d)
        db_session.commit()

        result = db_session.query(Driver).first()
        assert result.vehicle is not None
        assert result.vehicle.registration_number == "KA-05-EF-9999"

    def test_driver_default_status(self, db_session):
        d = Driver(name="Test", license_number="DL-0000000099", phone="9000000099")
        db_session.add(d)
        db_session.commit()
        assert db_session.query(Driver).first().status == "available"


# ---- RideRequest tests ----------------------------------------------------

class TestRideRequest:
    def test_create_ride_request(self, db_session):
        rr = RideRequest(
            employee_name="Alice",
            pickup_location="Office",
            drop_location="Airport",
            ride_date=datetime(2026, 10, 10, 9, 0),
            purpose="Client visit",
        )
        db_session.add(rr)
        db_session.commit()

        result = db_session.query(RideRequest).first()
        assert result.employee_name == "Alice"
        assert result.status == "pending"

    def test_ride_request_default_status(self, db_session):
        rr = RideRequest(
            employee_name="Bob",
            pickup_location="Home",
            drop_location="Office",
            ride_date=datetime(2026, 10, 11, 8, 30),
        )
        db_session.add(rr)
        db_session.commit()

        assert db_session.query(RideRequest).first().status == "pending"


# ---- Trip tests -----------------------------------------------------------

class TestTrip:
    def test_create_trip(self, db_session):
        v = Vehicle(registration_number="KA-99-ZZ-0001", model="Sedan", capacity=4)
        d = Driver(name="Mohan", license_number="DL-9999999999", phone="9111111111")
        rr = RideRequest(
            employee_name="Charlie",
            pickup_location="Campus A",
            drop_location="Campus B",
            ride_date=datetime(2026, 10, 12, 10, 0),
            status="approved",
        )
        db_session.add_all([v, d, rr])
        db_session.commit()

        trip = Trip(
            ride_request_id=rr.id,
            vehicle_id=v.id,
            driver_id=d.id,
            status="scheduled",
        )
        db_session.add(trip)
        db_session.commit()

        result = db_session.query(Trip).first()
        assert result.status == "scheduled"
        assert result.ride_request.employee_name == "Charlie"
        assert result.vehicle.registration_number == "KA-99-ZZ-0001"
        assert result.driver.name == "Mohan"

    def test_trip_default_status(self, db_session):
        v = Vehicle(registration_number="KA-88-YY-0002", model="SUV", capacity=7)
        d = Driver(name="Priya", license_number="DL-8888888888", phone="9222222222")
        rr = RideRequest(
            employee_name="Dana",
            pickup_location="Gate 1",
            drop_location="Gate 2",
            ride_date=datetime(2026, 10, 13, 14, 0),
            status="approved",
        )
        db_session.add_all([v, d, rr])
        db_session.commit()

        trip = Trip(ride_request_id=rr.id, vehicle_id=v.id, driver_id=d.id)
        db_session.add(trip)
        db_session.commit()

        assert db_session.query(Trip).first().status == "scheduled"

    def test_trip_relationships(self, db_session):
        """Verify the Trip model navigates back to its related entities."""
        v = Vehicle(registration_number="KA-77-WW-0003", model="Hatchback", capacity=4)
        d = Driver(name="Anita", license_number="DL-7777777777", phone="9333333333")
        rr = RideRequest(
            employee_name="Eve",
            pickup_location="Block A",
            drop_location="Block B",
            ride_date=datetime(2026, 10, 14, 16, 0),
            status="approved",
        )
        db_session.add_all([v, d, rr])
        db_session.commit()

        trip = Trip(ride_request_id=rr.id, vehicle_id=v.id, driver_id=d.id)
        db_session.add(trip)
        db_session.commit()

        # Navigate from ride_request back to trip
        assert rr.trip is not None
        assert rr.trip.id == trip.id
