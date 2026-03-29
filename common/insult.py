from urllib.request import urlopen

INSULT_URL = "https://evilinsult.com/generate_insult.php"


def get_insult():
    try:
        response = urlopen(INSULT_URL, timeout=5)
        return response.read().decode()
    except Exception as e:
        return "An error occurred while fetching insult: " + str(e)
