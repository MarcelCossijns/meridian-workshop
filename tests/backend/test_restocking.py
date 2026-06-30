"""
Tests for restocking recommendations API endpoint.
"""
import pytest


class TestRestockingEndpoints:
    """Test suite for the /api/restocking/recommendations endpoint."""

    def test_get_recommendations_returns_200(self, client):
        """Test that the endpoint returns a 200 response."""
        response = client.get("/api/restocking/recommendations")
        assert response.status_code == 200

    def test_response_top_level_structure(self, client):
        """Test that the response has all required top-level keys."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        assert isinstance(data, dict)
        assert "budget" in data
        assert "total_estimated_cost" in data
        assert "items_recommended" in data
        assert "recommendations" in data
        assert "filters" in data
        assert isinstance(data["recommendations"], list)

    def test_filters_field_contains_warehouses_and_categories(self, client):
        """Test that the filters field includes warehouse and category lists."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        filters = data["filters"]
        assert "warehouses" in filters
        assert "categories" in filters
        assert isinstance(filters["warehouses"], list)
        assert isinstance(filters["categories"], list)
        assert len(filters["warehouses"]) > 0
        assert len(filters["categories"]) > 0

    def test_recommendation_item_structure(self, client):
        """Test that each recommendation has all required fields."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        required_fields = [
            "sku", "name", "category", "warehouse",
            "quantity_on_hand", "reorder_point", "recommended_quantity",
            "unit_cost", "estimated_cost", "urgency", "urgency_score",
            "rationale",
        ]

        for item in data["recommendations"]:
            for field in required_fields:
                assert field in item, f"Missing field '{field}' in {item.get('sku')}"

    def test_urgency_labels_are_valid(self, client):
        """Test that all urgency labels are one of the four valid values."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        valid_labels = {"critical", "high", "medium", "low"}
        for item in data["recommendations"]:
            assert item["urgency"] in valid_labels, (
                f"{item['sku']} has invalid urgency '{item['urgency']}'"
            )

    def test_urgency_scores_are_in_range(self, client):
        """Test that all urgency scores are between 0.0 and 1.0."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        for item in data["recommendations"]:
            score = item["urgency_score"]
            assert isinstance(score, float)
            assert 0.0 <= score <= 1.0, (
                f"{item['sku']} has out-of-range urgency_score {score}"
            )

    def test_estimated_cost_equals_quantity_times_unit_cost(self, client):
        """Test that estimated_cost = recommended_quantity * unit_cost for every item."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        for item in data["recommendations"]:
            expected = item["recommended_quantity"] * item["unit_cost"]
            assert abs(item["estimated_cost"] - expected) < 0.01, (
                f"{item['sku']}: estimated_cost {item['estimated_cost']} != "
                f"{item['recommended_quantity']} × {item['unit_cost']}"
            )

    def test_items_recommended_count_matches_list_length(self, client):
        """Test that items_recommended equals the length of the recommendations list."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        assert data["items_recommended"] == len(data["recommendations"])

    def test_results_ordered_by_urgency_score_descending(self, client):
        """Test that recommendations are sorted by urgency_score highest first."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        scores = [item["urgency_score"] for item in data["recommendations"]]
        assert scores == sorted(scores, reverse=True), (
            "Recommendations are not sorted by urgency_score descending"
        )

    def test_tmp201_appears_in_unfiltered_results(self, client):
        """Test that TMP-201 is always included (low stock, increasing demand)."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        skus = [item["sku"] for item in data["recommendations"]]
        assert "TMP-201" in skus, "TMP-201 not found in unfiltered recommendations"

    def test_tmp201_has_critical_urgency(self, client):
        """Test that TMP-201 is rated critical (regression guard for urgency algorithm)."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        tmp201 = next((i for i in data["recommendations"] if i["sku"] == "TMP-201"), None)
        assert tmp201 is not None, "TMP-201 not found in recommendations"
        assert tmp201["urgency"] == "critical", (
            f"TMP-201 expected urgency 'critical', got '{tmp201['urgency']}'"
        )

    def test_warehouse_filter_restricts_results(self, client):
        """Test that warehouse filter returns only items from that warehouse."""
        response = client.get("/api/restocking/recommendations?warehouse=London")
        assert response.status_code == 200

        data = response.json()
        for item in data["recommendations"]:
            assert item["warehouse"] == "London", (
                f"{item['sku']} has warehouse '{item['warehouse']}', expected 'London'"
            )

    def test_category_filter_restricts_results(self, client):
        """Test that category filter returns only items from that category."""
        response = client.get("/api/restocking/recommendations?category=Sensors")
        assert response.status_code == 200

        data = response.json()
        for item in data["recommendations"]:
            assert item["category"].lower() == "sensors", (
                f"{item['sku']} has category '{item['category']}', expected 'Sensors'"
            )

    def test_budget_constraint_is_respected(self, client):
        """Test that total_estimated_cost never exceeds the requested budget."""
        response = client.get("/api/restocking/recommendations?budget=50000")
        assert response.status_code == 200

        data = response.json()
        assert data["total_estimated_cost"] <= 50000, (
            f"total_estimated_cost {data['total_estimated_cost']} exceeds budget 50000"
        )

    def test_budget_zero_returns_all_candidates(self, client):
        """Test that budget=0 applies no budget ceiling (all candidates returned)."""
        response_no_budget = client.get("/api/restocking/recommendations")
        response_zero = client.get("/api/restocking/recommendations?budget=0")

        assert response_no_budget.status_code == 200
        assert response_zero.status_code == 200

        count_no_budget = response_no_budget.json()["items_recommended"]
        count_zero = response_zero.json()["items_recommended"]
        assert count_no_budget == count_zero

    def test_tiny_budget_triggers_empty_state(self, client):
        """Test that a budget smaller than any single item returns no recommendations."""
        response = client.get("/api/restocking/recommendations?budget=1")
        assert response.status_code == 200

        data = response.json()
        assert data["items_recommended"] == 0
        assert data["recommendations"] == []

    def test_well_stocked_item_excluded(self, client):
        """Test that PCB-001 (450 on hand, reorder 200, stable demand) is not recommended."""
        response = client.get("/api/restocking/recommendations")
        data = response.json()

        skus = [item["sku"] for item in data["recommendations"]]
        assert "PCB-001" not in skus, (
            "PCB-001 should not be recommended (well above reorder point, stable demand)"
        )
