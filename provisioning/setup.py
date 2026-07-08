from client.metronome import MetronomeClient


def main() -> None:
    metronome_client = MetronomeClient()
    billable_metric = metronome_client.create_image_generation_billable_metric()
    print("Metronome provisioning complete.")


if __name__ == "__main__":
    main()
