from jinja2 import Environment, FileSystemLoader
from pathlib import Path

dummy_properties = [
    {
        "uprn": "1001",
        "address": "30 Alexandra Road, Muswell Hill, N10 2RT",
        "lat": 51.406,
        "long": -0.372,
        "score": 3,
    },
    {
        "uprn": "1002",
        "address": "",
        "lat": None,
        "long": None,
        "score": 2,
    },
]

def fake_url_for(endpoint, **values):
    if endpoint == "property":
        return f"/{values.get('uprn', '')}"
    return "/"

def test_home_template_renders():
    templates_dir = Path(__file__).parent.parent / "templates"
    env = Environment(loader=FileSystemLoader(str(templates_dir)))
    
    env.globals["url_for"] = fake_url_for
    
    template = env.get_template("home.html")
    
    rendered_html = template.render(properties=dummy_properties, key="dummykey")
    
    assert "Hard to Heat Homes" in rendered_html
    assert "30 Alexandra Road" in rendered_html
    assert 'id="1001"' in rendered_html  
    assert 'id="1002"' in rendered_html  
    assert "Click for address" in rendered_html  
    assert "51.406" in rendered_html
 


