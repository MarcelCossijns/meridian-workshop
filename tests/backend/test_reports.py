"""
Tests for Reports API endpoints.

Covers /api/reports/quarterly and /api/reports/monthly-trends, including
the quarter filter bug fix (Q1-2025 / Q2-2025 values must not produce empty results).
"""
import pytest


class TestQuarterlyReports:
    def test_returns_200(self, client):
        response = client.get("/api/reports/quarterly")
        assert response.status_code == 200

    def test_returns_list(self, client):
        data = client.get("/api/reports/quarterly").json()
        assert isinstance(data, list)

    def test_returns_data(self, client):
        data = client.get("/api/reports/quarterly").json()
        assert len(data) > 0

    def test_record_structure(self, client):
        record = client.get("/api/reports/quarterly").json()[0]
        assert "quarter" in record
        assert "total_orders" in record
        assert "total_revenue" in record
        assert "avg_order_value" in record
        assert "fulfillment_rate" in record

    def test_quarter_values_are_valid(self, client):
        data = client.get("/api/reports/quarterly").json()
        valid = {"Q1-2025", "Q2-2025", "Q3-2025", "Q4-2025"}
        for record in data:
            assert record["quarter"] in valid

    def test_total_orders_is_positive(self, client):
        for record in client.get("/api/reports/quarterly").json():
            assert record["total_orders"] > 0

    def test_total_revenue_is_positive(self, client):
        for record in client.get("/api/reports/quarterly").json():
            assert record["total_revenue"] > 0

    def test_fulfillment_rate_is_percentage(self, client):
        for record in client.get("/api/reports/quarterly").json():
            assert 0 <= record["fulfillment_rate"] <= 100

    def test_avg_order_value_consistent_with_totals(self, client):
        for record in client.get("/api/reports/quarterly").json():
            expected = record["total_revenue"] / record["total_orders"]
            assert abs(record["avg_order_value"] - expected) < 0.01

    def test_sorted_by_quarter(self, client):
        quarters = [r["quarter"] for r in client.get("/api/reports/quarterly").json()]
        assert quarters == sorted(quarters)

    # --- Quarter filter regression tests ---

    def test_quarter_filter_q1_returns_data(self, client):
        """Q1-2025 filter must return data, not an empty list."""
        data = client.get("/api/reports/quarterly?month=Q1-2025").json()
        assert isinstance(data, list)
        assert len(data) > 0, "Q1-2025 quarter filter returned no results"

    def test_quarter_filter_q2_returns_data(self, client):
        data = client.get("/api/reports/quarterly?month=Q2-2025").json()
        assert len(data) > 0, "Q2-2025 quarter filter returned no results"

    def test_quarter_filter_q3_returns_data(self, client):
        data = client.get("/api/reports/quarterly?month=Q3-2025").json()
        assert len(data) > 0, "Q3-2025 quarter filter returned no results"

    def test_quarter_filter_q4_returns_data(self, client):
        data = client.get("/api/reports/quarterly?month=Q4-2025").json()
        assert len(data) > 0, "Q4-2025 quarter filter returned no results"

    def test_quarter_filter_q1_only_contains_q1(self, client):
        """When filtering by Q1-2025, only Q1-2025 rows should appear."""
        data = client.get("/api/reports/quarterly?month=Q1-2025").json()
        for record in data:
            assert record["quarter"] == "Q1-2025"

    def test_month_filter_returns_data(self, client):
        data = client.get("/api/reports/quarterly?month=2025-03").json()
        assert len(data) > 0

    def test_warehouse_filter_reduces_results(self, client):
        all_data = client.get("/api/reports/quarterly").json()
        sf_data = client.get("/api/reports/quarterly?warehouse=San Francisco").json()
        total_all = sum(r["total_orders"] for r in all_data)
        total_sf = sum(r["total_orders"] for r in sf_data)
        assert total_sf <= total_all

    def test_category_filter_reduces_results(self, client):
        all_data = client.get("/api/reports/quarterly").json()
        cat_data = client.get("/api/reports/quarterly?category=Sensors").json()
        total_all = sum(r["total_orders"] for r in all_data)
        total_cat = sum(r["total_orders"] for r in cat_data)
        assert total_cat <= total_all


class TestMonthlyTrends:
    def test_returns_200(self, client):
        assert client.get("/api/reports/monthly-trends").status_code == 200

    def test_returns_list(self, client):
        assert isinstance(client.get("/api/reports/monthly-trends").json(), list)

    def test_returns_data(self, client):
        assert len(client.get("/api/reports/monthly-trends").json()) > 0

    def test_record_structure(self, client):
        record = client.get("/api/reports/monthly-trends").json()[0]
        assert "month" in record
        assert "order_count" in record
        assert "revenue" in record
        assert "delivered_count" in record

    def test_month_format_is_yyyy_mm(self, client):
        for record in client.get("/api/reports/monthly-trends").json():
            parts = record["month"].split("-")
            assert len(parts) == 2
            assert len(parts[0]) == 4  # year
            assert len(parts[1]) == 2  # month

    def test_order_count_is_non_negative(self, client):
        for record in client.get("/api/reports/monthly-trends").json():
            assert record["order_count"] >= 0

    def test_revenue_is_non_negative(self, client):
        for record in client.get("/api/reports/monthly-trends").json():
            assert record["revenue"] >= 0

    def test_delivered_count_not_exceed_order_count(self, client):
        for record in client.get("/api/reports/monthly-trends").json():
            assert record["delivered_count"] <= record["order_count"]

    def test_sorted_chronologically(self, client):
        months = [r["month"] for r in client.get("/api/reports/monthly-trends").json()]
        assert months == sorted(months)

    # --- Quarter filter regression tests ---

    def test_quarter_filter_q1_returns_data(self, client):
        data = client.get("/api/reports/monthly-trends?month=Q1-2025").json()
        assert len(data) > 0, "Q1-2025 monthly-trends filter returned no results"

    def test_quarter_filter_q1_only_q1_months(self, client):
        data = client.get("/api/reports/monthly-trends?month=Q1-2025").json()
        q1_months = {"2025-01", "2025-02", "2025-03"}
        for record in data:
            assert record["month"] in q1_months

    def test_quarter_filter_q2_only_q2_months(self, client):
        data = client.get("/api/reports/monthly-trends?month=Q2-2025").json()
        q2_months = {"2025-04", "2025-05", "2025-06"}
        for record in data:
            assert record["month"] in q2_months

    def test_single_month_filter(self, client):
        data = client.get("/api/reports/monthly-trends?month=2025-01").json()
        assert len(data) > 0
        for record in data:
            assert record["month"] == "2025-01"

    def test_warehouse_filter(self, client):
        all_data = client.get("/api/reports/monthly-trends").json()
        sf_data = client.get("/api/reports/monthly-trends?warehouse=San Francisco").json()
        total_all = sum(r["order_count"] for r in all_data)
        total_sf = sum(r["order_count"] for r in sf_data)
        assert total_sf <= total_all
