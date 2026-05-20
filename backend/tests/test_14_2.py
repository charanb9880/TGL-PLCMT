import pytest

def is_vc(data):
    return data.get("Category") == "VC"

def is_bootstrapped(data):
    return data.get("Funding Status") == "Bootstrapped"

def is_remote(data):
    return "Remote" in (data.get("Remote Work Policy") or "")

def is_nonprofit(data):
    return "Non-Profit" in (data.get("Nature of Company") or "")

def is_govt(data):
    return "Govt" in (data.get("Nature of Company") or "")

def is_saas(data):
    return "SaaS" in (data.get("Industry") or "")

def is_manufacturing(data):
    return "Manufacturing" in (data.get("Industry") or "")

def is_large_company(size):
    try:
        return int(size) > 1000
    except:
        return False


def test_not_applicable_logic():

    # VC → no products
    data = {"Category": "VC", "Services / Offerings / Products": "SaaS"}
    assert not (is_vc(data) and data["Services / Offerings / Products"] != "N/A")

    # Bootstrapped → no investors
    data = {"Funding Status": "Bootstrapped", "Key Investors / Backers": "Sequoia"}
    assert not (is_bootstrapped(data) and data["Key Investors / Backers"] != "N/A")

    # Remote → no offices
    data = {"Remote Work Policy": "Remote", "Office Locations": "NY"}
    assert not (is_remote(data) and data["Office Locations"] != "N/A")

    # Nonprofit → no profit
    data = {"Nature of Company": "Non-Profit", "Annual Profits": "$5M"}
    assert not (is_nonprofit(data) and data["Annual Profits"] != "N/A")

    # Govt → no investors
    data = {"Nature of Company": "Govt", "Key Investors / Backers": "VC Fund"}
    assert not (is_govt(data) and data["Key Investors / Backers"] != "N/A")

    # Manufacturing → must have supply chain
    data = {"Industry": "Manufacturing", "Supply Chain Dependencies": "N/A"}
    assert not is_manufacturing(data)

    # Large company → diversity expected
    data = {"Employee Size": "10000", "Diversity Metrics": "N/A"}
    assert not (is_large_company(data["Employee Size"]) and data["Diversity Metrics"] == "N/A")
