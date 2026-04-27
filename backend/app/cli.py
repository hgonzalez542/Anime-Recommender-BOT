from app.recommender import AnimeRecommender

rec = AnimeRecommender()

while True:
    q = input("Enter anime request (or quit): ")
    if q == "quit":
        break
    prefs, results = rec.recommend(q)
    print("Preferences:", prefs)
    for r in results:
        print(r["title"], r["score"], r["reason"])
