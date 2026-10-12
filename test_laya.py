from laya import Router

router = Router()

state = {
    "health": 30,
    "ammo": 4,
    "visible_enemies": 2,
    "situation": (
        "The player has low health, limited ammunition, "
        "and two visible enemies."
    ),
}

questions = {
    "action": {
        "type": "choice",
        "instructions": (
            "Choose the most appropriate immediate action."
        ),
        "criteria": {
            "attack": "Attack a visible enemy.",
            "retreat": "Move away from immediate danger.",
            "wait": "Wait and observe the situation.",
        },
    },
    "danger": {
        "type": "score",
        "instructions": "Assess the immediate danger.",
        "criteria": [
            "low",
            "moderate",
            "high",
        ],
    },
}

result = router.predict(state, questions)

print("Full result:")
print(result)

print("Chosen action:")
print(result["answers"]["action"]["choice"])

print("Danger assessment:")
print(result["answers"]["danger"])