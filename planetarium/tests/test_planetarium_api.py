from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from planetarium.models import (
    AstronomyShow,
    ShowTheme,
    PlanetariumDome,
    ShowSession,
    Reservation,
    Ticket
)

SHOW_URL = reverse("planetarium:astronomyshow-list")
RESERVATION_URL = reverse("planetarium:reservation-list")


def sample_astronomy_show(**params):
    defaults = {
        "title": "Sample Show",
        "description": "Sample description",
    }
    defaults.update(params)
    return AstronomyShow.objects.create(**defaults)


def sample_show_session(**params):
    theme = ShowTheme.objects.create(name="Science")
    show = sample_astronomy_show()
    show.themes.add(theme)
    dome = PlanetariumDome.objects.create(name="Main Dome", rows=10, seats_in_row=10)

    defaults = {
        "show_time": "2026-03-01T12:00:00Z",
        "astronomy_show": show,
        "planetarium_dome": dome,
    }
    defaults.update(params)
    return ShowSession.objects.create(**defaults)


class PlanetariumApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com", password="password123"
        )
        self.client.force_authenticate(self.user)

    def test_list_shows(self):
        sample_astronomy_show()
        res = self.client.get(SHOW_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_filter_shows_by_title(self):
        show1 = sample_astronomy_show(title="Mars")
        show2 = sample_astronomy_show(title="Saturn")
        res = self.client.get(SHOW_URL, {"title": "Mars"})
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Mars")

    def test_filter_shows_by_themes(self):
        theme1 = ShowTheme.objects.create(name="Theme 1")
        theme2 = ShowTheme.objects.create(name="Theme 2")
        show1 = sample_astronomy_show(title="Show 1")
        show2 = sample_astronomy_show(title="Show 2")
        show1.themes.add(theme1)
        show2.themes.add(theme2)

        res = self.client.get(SHOW_URL, {"themes": f"{theme1.id}"})
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Show 1")

    def test_create_reservation(self):
        session = sample_show_session()
        payload = {
            "tickets": [{"row": 1, "seat": 1, "show_session": session.id}]
        }
        res = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_ticket_validation_already_taken(self):
        session = sample_show_session()
        res_obj = Reservation.objects.create(user=self.user)
        Ticket.objects.create(row=1, seat=1, show_session=session, reservation=res_obj)

        payload = {
            "tickets": [{"row": 1, "seat": 1, "show_session": session.id}]
        }
        res = self.client.post(RESERVATION_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)