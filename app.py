from flask import Flask, render_template, request

app = Flask(__name__)

RECIPES = [
    {
        "id": 1,
        "name": "Banana Pancakes",
        "emoji": "🥞",
        "ingredients": ["banana", "egg", "milk", "flour"],
        "time": "20 minutes",
        "difficulty": "Easy",
        "steps": [
            "Mash the banana in a bowl.",
            "Add the egg and milk and mix.",
            "Add the flour and stir until smooth.",
            "Heat a lightly greased pan.",
            "Pour small portions into the pan and cook both sides.",
            "Serve and enjoy!"
        ],
        "tip": "Ask an adult for help when using a hot stove."
    },
    {
        "id": 2,
        "name": "Egg & Tomato Toast",
        "emoji": "🍳",
        "ingredients": ["egg", "bread", "tomato", "onion"],
        "time": "15 minutes",
        "difficulty": "Easy",
        "steps": [
            "Wash the vegetables.",
            "Chop the tomato and onion.",
            "Beat the egg in a bowl.",
            "Cook the vegetables in a pan.",
            "Add the egg and cook until set.",
            "Toast the bread and serve."
        ],
        "tip": "Use a safe chopping technique and ask an adult for help with heat."
    },
    {
        "id": 3,
        "name": "Fruit Smoothie",
        "emoji": "🥤",
        "ingredients": ["banana", "milk", "mango"],
        "time": "10 minutes",
        "difficulty": "Easy",
        "steps": [
            "Wash and peel the fruits.",
            "Cut the fruit into small pieces.",
            "Put the fruit and milk into a blender.",
            "Blend until smooth.",
            "Pour into a cup and enjoy."
        ],
        "tip": "Make sure the blender is switched off before opening it."
    },
    {
        "id": 4,
        "name": "Vegetable Fried Rice",
        "emoji": "🍚",
        "ingredients": ["rice", "egg", "carrot", "peas", "onion"],
        "time": "35 minutes",
        "difficulty": "Medium",
        "steps": [
            "Wash and prepare the vegetables.",
            "Cook the rice until tender.",
            "Stir-fry onion and vegetables.",
            "Add the cooked rice.",
            "Add scrambled egg and mix well.",
            "Serve while warm."
        ],
        "tip": "Be careful around hot oil and ask an adult for help."
    }
]

QUESTIONS = [
    {
        "question": "Why does an egg become firm when it is cooked?",
        "answer": "Heat changes the proteins in the egg. They unfold and join together, making the egg firmer."
    },
    {
        "question": "Why does bread turn brown when toasted?",
        "answer": "Heat causes chemical reactions between sugars and proteins on the surface. These reactions create the brown colour and toasted flavour."
    },
    {
        "question": "Why do oil and water separate?",
        "answer": "Their molecules interact differently. Oil molecules do not mix well with water molecules, so the liquids form separate layers."
    },
    {
        "question": "Why does dough rise?",
        "answer": "Yeast can produce carbon dioxide gas. The gas gets trapped in the dough and makes it expand."
    }
]

QUIZ = [
    {"q": "Which ingredient is commonly used to help pancakes hold together?", "options": ["Egg", "Salt", "Oil", "Pepper"], "answer": "Egg"},
    {"q": "What should you do before handling food?", "options": ["Wash your hands", "Turn on the stove", "Add sugar", "Taste everything"], "answer": "Wash your hands"},
    {"q": "Which appliance is useful for making a smoothie?", "options": ["Blender", "Toaster", "Kettle", "Oven"], "answer": "Blender"},
    {"q": "What happens to an egg when it is heated?", "options": ["Its proteins change", "It becomes ice", "It disappears", "It turns into water"], "answer": "Its proteins change"},
    {"q": "Which is a good way to reduce food waste?", "options": ["Reuse suitable leftovers", "Throw everything away", "Buy more than needed", "Leave food uncovered"], "answer": "Reuse suitable leftovers"}
]

FOOD_WASTE = {
    "banana": ["Banana pancakes", "Fruit smoothie", "Banana bread"],
    "bread": ["Egg & tomato toast", "Bread crumbs", "French toast"],
    "tomato": ["Egg & tomato toast", "Tomato sauce", "Fresh salad"],
    "rice": ["Vegetable fried rice", "Rice and vegetables bowl"],
    "mango": ["Fruit smoothie", "Fruit salad", "Mango yoghurt"],
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recipes")
def recipes():
    return render_template("recipes.html", recipes=RECIPES)

@app.route("/find", methods=["POST"])
def find_recipe():
    selected = [x.strip().lower() for x in request.form.getlist("ingredients") if x.strip()]
    matches = []
    for recipe in RECIPES:
        score = len(set(selected) & set(recipe["ingredients"]))
        if score:
            matches.append((score, recipe))
    matches.sort(key=lambda item: (-item[0], len(item[1]["ingredients"])))
    return render_template("find.html", selected=selected, matches=matches)

@app.route("/recipe/<int:recipe_id>")
def recipe(recipe_id):
    item = next((r for r in RECIPES if r["id"] == recipe_id), None)
    if item is None:
        return "Recipe not found", 404
    return render_template("recipe.html", recipe=item)

@app.route("/curious")
def curious():
    return render_template("curious.html", questions=QUESTIONS)

@app.route("/waste", methods=["GET", "POST"])
def waste():
    results = []
    ingredient = ""
    if request.method == "POST":
        ingredient = request.form.get("ingredient", "").strip().lower()
        results = FOOD_WASTE.get(ingredient, [])
    return render_template("waste.html", results=results, ingredient=ingredient)

@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    score = None
    if request.method == "POST":
        score = 0
        for i, item in enumerate(QUIZ):
            if request.form.get(f"q{i}") == item["answer"]:
                score += 1
    return render_template("quiz.html", quiz=QUIZ, score=score)

if __name__ == "__main__":
    app.run(debug=True)
