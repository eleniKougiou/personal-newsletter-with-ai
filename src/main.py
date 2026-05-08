from concurrent.futures import ThreadPoolExecutor
from fetcher import load_interests
from curator import curate_interest
from newsletter import assemble_newsletter
from email_sender import send_newsletter
from state import save_last_run


def run_curator():
    interests = load_interests()

    print("Starting curation for all interests...")
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(curate_interest, interests))

    sections = {
        interest["name"]: section
        for interest, section in zip(interests, results)
        if section is not None
    }

    if not sections:
        print("No news today!")
        return

    print(f"Curated {len(sections)} sections, assembling newsletter...")
    newsletter = assemble_newsletter(sections)

    send_newsletter(newsletter)
    save_last_run()


if __name__ == "__main__":
    run_curator()
