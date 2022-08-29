import requests

payload = {"email": "Hvac5218@gmail.com", "password": "bradkin525"}
with requests.Session() as s:
    p = s.post(
        "https://vendor.choicehomewarranty.com/index.php?sec=cadsavail/index.php",
        data=payload,
    )
    x = requests.get("https://vendor.choicehomewarranty.com/index.php?sec=cadsavail")
    print(x.text)
