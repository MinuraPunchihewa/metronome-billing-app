import os

from dotenv import load_dotenv
from metronome import Metronome

load_dotenv()

def test_metronome_connection():
    client = Metronome(bearer_token=os.getenv("METRONOME_BEARER_TOKEN"))
    try:
        response = client.v1.customers.list()
        print(response)
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Hello from metronome-billing-app!")
    test_metronome_connection()

if __name__ == "__main__":
    main()
