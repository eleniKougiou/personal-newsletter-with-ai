from concurrent.futures import ThreadPoolExecutor
from fetcher import load_interests
from curator import curate_interest
from state import save_last_run


def run_curator():
    interests = load_interests()

    # Run curation for each interest in parallel
    with ThreadPoolExecutor() as executor:
        sections = list(executor.map(curate_interest, interests))

    # Filter out None results (interests with no news today)
    sections = [s for s in sections if s]

    if not sections:
        print("No news today!")
        return

    for section in sections:
        print(section)
        print("\n---\n")

    save_last_run()



if __name__ == "__main__":
    run_curator()