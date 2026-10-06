from fastapi.testclient import TestClient


def test_sheets_and_a_sheet_with_its_exercises(api: TestClient) -> None:
    sheets = api.get("/api/llistes").json()
    assert {s["id"] for s in sheets} >= {"tema-2"} and all(s["n_exercicis"] == len(s["exercicis"]) for s in sheets)
    sheet = api.get("/api/llistes/tema-2").json()
    assert sheet["exercicis"][0]["llista"] == "tema-2" and sheet["problemes"][0]["exercicis"]
    assert api.get("/api/llistes/nope").status_code == 404


def test_theory_index_and_items(api: TestClient) -> None:
    index = api.get("/api/teoria").json()
    assert len(index["temes"]) == 6 and index["problemes_pdf"].startswith("/pdf/")
    item = index["temes"][2]["items"][0]
    full = api.get(f"/api/teoria/{item['id']}").json()
    assert full["etiqueta"] == item["etiqueta"] and full["pdf"].startswith("/pdf/")
    assert api.get("/api/teoria/T9.999").status_code == 404


def test_config_and_static_frontend(api: TestClient) -> None:
    cfg = api.get("/api/config").json()
    assert cfg["panell_professor"] is True and cfg["provider"] == "openai" and cfg["api_key"] is True
    assert "diagnosis" in cfg["stages"]
    assert api.get("/").status_code == 200 and "html" in api.get("/").headers["content-type"]
