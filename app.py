"""Small Chroma persistence and semantic-search smoke test."""

import json
from pathlib import Path
from uuid import uuid4

SAMPLES = [
    ("focus", "Focus Creatures", "A productivity app that blocks distracting websites during timed work sessions and awards collectible creatures for successful sessions."),
    ("meals", "Pantry Planner", "An AI meal planner recommends recipes from ingredients users already have to reduce food waste."),
    ("fitness", "Lift Log", "A fitness tracker records strength workouts and suggests progressive weight training routines."),
    ("travel", "Trip Map", "A travel planner organizes flights, hotel bookings, and sightseeing itineraries for group vacations."),
    ("music", "Band Room", "A music collaboration service helps musicians share recordings and arrange remote rehearsals."),
    ("budget", "Budget Buddy", "A budgeting app categorizes expenses and helps households plan monthly savings goals."),
    ("education", "Math Mentor", "An education platform offers algebra practice exercises and step-by-step tutoring for school students."),
    ("fashion", "Closet Mix", "A fashion assistant suggests outfits from a personal wardrobe based on weather and occasion."),
    ("events", "Gather Together", "An event planning service manages invitations, venue reservations, and guest attendance for parties."),
    ("pets", "Pet Schedule", "A pet care organizer tracks veterinary appointments, medication reminders, and dog walking schedules."),
]

QUERIES = [
    ("Semantic test 1", "A tool that notices when college students drift to social media during homework and gives them a virtual pet for staying on task."),
    ("Semantic test 2", "People describe what's sitting in their fridge and get dinner suggestions before their groceries go bad."),
    ("Unrelated query", "Quantum marshmallow nebula dances inside a purple theorem."),
]


def add_user_idea(name: str, description: str) -> str:
    """Persist a user idea in yc_startups and return its generated ID.

    The description is embedded; the title and source are metadata. This can
    be called directly from a future CLI or form handler without running main.
    """
    import chromadb

    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a nonempty string")
    if not isinstance(description, str) or not description.strip():
        raise ValueError("description must be a nonempty string")

    client = chromadb.PersistentClient(
        path=str(Path(__file__).resolve().parent / "chroma_store")
    )
    collection = client.get_collection(name="yc_startups")
    idea_id = f"user:{uuid4()}"
    collection.add(
        ids=[idea_id],
        documents=[description.strip()],
        metadatas=[{"company_name": name.strip(), "source": "user"}],
    )
    return idea_id


def main():
    try:
        import chromadb
    except ModuleNotFoundError as error:
        if error.name != "chromadb":
            raise
        raise SystemExit(
            "ChromaDB is not installed. Run: python3 -m pip install chromadb"
        ) from error

    print(f"ChromaDB version: {chromadb.__version__}", flush=True)
    # Keep storage beside this script, regardless of the working directory.
    store = Path(__file__).resolve().parent / "chroma_store"
    client = chromadb.PersistentClient(path=str(store))
    # Uses Chroma's default embedding function and default squared L2 distance.
    collection = client.get_or_create_collection(name="startup_ideas")
    print(f"Collection count before insertion: {collection.count()}", flush=True)

    existing_ids = set(collection.get(include=[])["ids"])
    missing = [sample for sample in SAMPLES if sample[0] not in existing_ids]
    if missing:
        collection.add(
            ids=[sample[0] for sample in missing],
            documents=[sample[2] for sample in missing],
            metadatas=[{"name": sample[1]} for sample in missing],
        )
    print(f"Records added: {len(missing)}", flush=True)
    print(f"Collection count after insertion: {collection.count()}", flush=True)

    for label, query in QUERIES:
        print(f"\n{label}: {query}", flush=True)
        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"],
        )
        # IDs are always returned. Lower distance means a closer match;
        # even an unrelated query receives nearest neighbors.
        print(json.dumps({
            key: results[key]
            for key in ("ids", "documents", "metadatas", "distances")
        }, indent=2), flush=True)


if __name__ == "__main__":
    main()
