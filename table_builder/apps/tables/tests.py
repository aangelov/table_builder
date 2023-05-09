from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Table


class TableTests(APITestCase):
    client = APIClient()

    def setUp(self):
        self.table_name = "users"
        self.initial_payload = {
            "name": "users",
            "schema": [
                {"title": "name", "type": "string"},
                {"title": "age", "type": "number"},
                {"title": "is_active", "type": "boolean"}
            ]
        }

        self.updated_payload = {
            "name": "users",
            "schema": [
                {"title": "name", "type": "string"},
                {"title": "age", "type": "number"},
                {"title": "email", "type": "string"}
            ]
        }

        self.invalid_payload = {
            "name": "",
            "schema": []
        }

    def test_create_valid_table(self):
        response = self.client.post(
            reverse("table-list"),
            data=self.initial_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_table(self):
        response = self.client.post(
            reverse("table-list"),
            data=self.invalid_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_table_schema(self):
        table = Table.objects.create(
            name="users", schema=self.initial_payload["schema"]
        )
        response = self.client.put(
            reverse("table-detail", kwargs={"pk": table.pk}),
            data=self.updated_payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        table.refresh_from_db()
        self.assertEqual(table.schema, self.updated_payload["schema"])

    def test_add_row_to_table(self):
        table = Table.objects.create(name="users", schema=self.initial_payload["schema"])
        payload = {
            "data": {
                "name": "John",
                "age": 30,
                "is_active": True
            }
        }
        response = self.client.post(
            reverse("table-add-row", kwargs={"pk": table.pk}),
            data=payload,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(table.rows.count(), 1)

    def test_get_all_rows_in_table(self):
        table = Table.objects.create(name="users", schema=self.initial_payload["schema"])
        payload = {
            "data": {
                "name": "John",
                "age": 30,
                "is_active": True
            }
        }
        response = self.client.post(
            reverse("table-add-row", kwargs={"pk": table.pk}),
            data=payload,
            format="json"
        )
        response = self.client.get(
            reverse("table-get-rows", kwargs={"pk": table.pk}),
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: Fix this test, output data is in different format
        # OrderedDict vs dict, Decimal vs int
        self.assertEqual(response.data[0], payload["data"])
