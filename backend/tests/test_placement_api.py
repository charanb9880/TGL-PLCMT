import pytest


# Dataset and schema verification
def test_dataset_status_returns_metadata_and_schema(api_client, base_url):
    response = api_client.get(f"{base_url}/api/dataset/status")
    assert response.status_code == 200

    data = response.json()
    assert data["column_count"] == 164
    assert isinstance(data["columns"], list)
    assert len(data["columns"]) == 164
    assert isinstance(data.get("available_sheets"), list)
    assert data["row_count"] > 0
    assert data["database_configured"] is True
    assert data["database_table_ready"] is True


# Company listing and filters
def test_companies_returns_list_and_filter_metadata(api_client, base_url):
    response = api_client.get(f"{base_url}/api/companies")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["items"], list)
    assert data["total"] == len(data["items"])
    assert isinstance(data.get("filters"), dict)
    assert isinstance(data.get("sort_options"), list)
    assert len(data["items"]) > 0


def test_companies_search_filter_changes_results(api_client, base_url):
    all_response = api_client.get(f"{base_url}/api/companies")
    assert all_response.status_code == 200
    all_data = all_response.json()
    assert len(all_data["items"]) > 0

    query = str(all_data["items"][0].get("Company Name", "")).split(" ")[0]
    filtered_response = api_client.get(f"{base_url}/api/companies", params={"search": query})
    assert filtered_response.status_code == 200

    filtered_data = filtered_response.json()
    assert filtered_data["total"] <= all_data["total"]
    assert all(
        query.lower() in " ".join(str(v).lower() for v in item.values())
        for item in filtered_data["items"]
    )


@pytest.fixture(scope="module")
def first_company_id(api_client, base_url):
    response = api_client.get(f"{base_url}/api/companies")
    if response.status_code != 200:
        pytest.skip("Unable to list companies for dependent tests")
    items = response.json().get("items", [])
    if not items:
        pytest.skip("No companies available for dependent tests")

    first = items[0]
    company_id = first.get("company_id") or first.get("Company Name") or first.get("Short Name")
    if not company_id:
        pytest.skip("No usable company identifier found")
    return str(company_id)


@pytest.fixture(scope="module")
def second_company_id(api_client, base_url):
    response = api_client.get(f"{base_url}/api/companies")
    if response.status_code != 200:
        pytest.skip("Unable to list companies for compare test")
    items = response.json().get("items", [])
    if len(items) < 2:
        pytest.skip("Need at least two companies for compare")

    second = items[1]
    company_id = second.get("company_id") or second.get("Company Name") or second.get("Short Name")
    if not company_id:
        pytest.skip("No usable second company identifier found")
    return str(company_id)


# Company detail endpoint
def test_company_detail_returns_company_and_highlights(api_client, base_url, first_company_id):
    response = api_client.get(f"{base_url}/api/companies/{first_company_id}")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data.get("company"), dict)
    assert isinstance(data.get("highlights"), dict)
    assert "strengths" in data["highlights"]
    assert "risks" in data["highlights"]


# Compare endpoint
def test_compare_returns_side_by_side_payload(api_client, base_url, first_company_id, second_company_id):
    response = api_client.get(
        f"{base_url}/api/compare",
        params={"left_company_id": first_company_id, "right_company_id": second_company_id},
    )
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data.get("left_company"), dict)
    assert isinstance(data.get("right_company"), dict)
    assert isinstance(data.get("left_highlights"), dict)
    assert isinstance(data.get("right_highlights"), dict)


# Skill matching endpoint
def test_skill_match_returns_fit_gap_and_suggestions(api_client, base_url, first_company_id):
    payload = {"company_id": first_company_id, "skills": ["Python", "SQL", "React"]}
    response = api_client.post(f"{base_url}/api/skill-match", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["company_id"] == first_company_id
    assert isinstance(data.get("result"), dict)
    assert data["result"]["fit_level"] in {"High", "Medium", "Low"}
    assert isinstance(data["result"].get("matched_skills"), list)
    assert isinstance(data["result"].get("skill_gaps"), list)
    assert isinstance(data["result"].get("preparation_suggestions"), list)


# Categories and analytics summary endpoints
def test_categories_summary_returns_tiles(api_client, base_url):
    response = api_client.get(f"{base_url}/api/categories")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data.get("categories"), list)
    if data["categories"]:
        first = data["categories"][0]
        assert "label" in first
        assert "count" in first


def test_analytics_summary_returns_core_distributions(api_client, base_url):
    response = api_client.get(f"{base_url}/api/analytics")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data.get("total_companies"), int)
    assert isinstance(data.get("category_distribution"), list)
    assert isinstance(data.get("hiring_velocity_distribution"), list)
    assert isinstance(data.get("profitability_mix"), list)
    assert isinstance(data.get("work_mode_distribution"), list)
