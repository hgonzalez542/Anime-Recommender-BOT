def parse_prompt(prompt):
    prompt = prompt.lower()

    include = []
    exclude = []
    moods = []

    # GENRES
    if "action" in prompt: include.append("action")
    if "romance" in prompt: include.append("romance")
    if "comedy" in prompt or "funny" in prompt: include.append("comedy")
    if "dark" in prompt: include.append("dark")
    if "sports" in prompt: include.append("sports")

    # MOODS
    if "emotional" in prompt or "sad" in prompt:
        moods.append("emotional")

    if "hype" in prompt or "intense" in prompt:
        moods.append("hype")

    if "calm" in prompt:
        moods.append("calm")

    # EXCLUSIONS
    if "not comedy" in prompt:
        exclude.append("comedy")

    if "no romance" in prompt:
        exclude.append("romance")

    return {
    "include": include,
    "exclude": exclude,
    "moods": moods
    }