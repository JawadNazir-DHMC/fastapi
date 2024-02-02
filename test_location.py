from fastapi.testclient import TestClient
from fastapi import HTTPException,status
from location import app,Location,get_location_or_404

locations={
    "jawad":Location(name="Jawad",location="Lahore"),
    "moin":Location(name="Moin",location="Karachi")
}
def fake_get_location_or_404(name:str)->Location:
    loc=locations.get(name.lower())
    if not loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No LOcation found for {name}")
    return loc

app.dependency_overrides[get_location_or_404]=fake_get_location_or_404

client=TestClient(app)

def test_read_location():
    response=client.get("location/jawad")
    assert response.status_code== 200
    assert response.json() == {"name":"Jawad","location":"Lahore"}

def test_locatio_404():
    response=client.get("/location/imran")
    assert response.status_code == status.HTTP_404_NOT_FOUND