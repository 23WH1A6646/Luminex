from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Generative AI with your API key
genai.configure(api_key="AIzaSyC98d4C-XWqaxUVoGnLjiix8bkL5FOkeHQ")  # Replace with your actual API key

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-nutrition', methods=['POST'])
def get_nutrition():
    data = request.json
    food_item = data.get("food_item", "").strip()
    ingredients = data.get("ingredients", [])  # If a recipe is provided

    if not food_item and not ingredients:
        return jsonify({"error": "Please provide either a food item or a recipe (list of ingredients)."}), 400

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        if food_item:  
            # If user provides a single food item
            prompt = f"Provide detailed nutritional information about {food_item}. Include macronutrients (protein, fat, carbohydrates), micronutrients (vitamins, minerals), and calorie content."
        else:  
            # If user provides a recipe (list of ingredients)
            prompt = f"""
            Calculate the total nutrition for this recipe, summing up the nutrients of each ingredient:
            {', '.join(ingredients)}
            Include total calories, macronutrients (protein, fats, carbohydrates), and key micronutrients.
            """

        response = model.generate_content(prompt)
        return jsonify({"nutrition": response.text})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate-meal-plan', methods=['POST'])
def generate_meal_plan():
    data = request.json
    food_category = data.get('food_category', 'vegetarian')  # Default to vegetarian

    user_input = f"""
    Generate a 7-day meal plan for a person with the following details:
    - Age: {data.get('age', 'Not specified')}
    - Weight: {data.get('weight', 'Not specified')}
    - Health conditions: {data.get('health_conditions', 'None')}
    - Food allergies: {data.get('allergies', 'None')}
    - Nutrient deficiencies: {data.get('nutrient_deficiencies', 'None')}
    - Activity level: {data.get('activity_level', 'Moderate')}
    - Food category: {food_category} (Ensure all meals align with this preference)

    Each day's meal plan should include:
    - Breakfast
    - Lunch
    - Dinner
    - 1-2 snack recommendations
    - Total daily calories and macronutrient breakdown

    Ensure that the meal plan is nutritious, balanced, and suited to the user's health needs.
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(user_input)
        return jsonify({"meal_plan": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
