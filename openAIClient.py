import openai
import base64
from PIL import Image
import io
import json
import numpy as np

def generate_settlement_story(settlement_data: dict) -> dict:

    map_array = settlement_data["blueprint"]
    water_map_array = settlement_data["water_map"]
    environment = settlement_data["data"]
    biome = settlement_data["biome"]

    # Convert the map array to a Base64 encoded image
    blueprint_image = Image.open("blueprint.png")
    water_map_img = Image.open("water_map.png")
    
    buffered_water_map = io.BytesIO()
    water_map_img.save(buffered_water_map, format="PNG")
    base64_image_water_map = base64.b64encode(buffered_water_map.getvalue()).decode("utf-8")

    buffered_blueprint = io.BytesIO()
    blueprint_image.save(buffered_blueprint, format="PNG")
    base64_image_blueprint = base64.b64encode(buffered_blueprint.getvalue()).decode("utf-8")
    example = {}
    with open('example.json') as f:
        example = json.load(f)
    # Prepare the messages for the OpenAI API
    messages = [
        {
            "role": "system",
            "content": (
                "You are a master storyteller and world-builder. Your task is to create a compelling "
                "story about a small settlement. The story should include an overview of the settlement, "
                "a family or individual for each house with a short background story (2-3 sentences max each), "
                "and adhere to a total word limit of 1000 words. The output must be in JSON format."
                "The story should be inspired by the provided map image and settlement details."
                "Adapt the story to match the available plot types, water map and plots placed." 
                "Also consider the location of the plots from the provided images."
                "The image scales are 1:1, so one unit is equal to 1 block within the Minecraft world."
                "The JSON output should have the following example structure: "
                f'{example}'
                # '{"settlement_story": "...", "houses_and_families": [{"house_number": 1, "family_name": "...", "background": "..."}, ...]}'
            ),
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": (
                    f"Generate a detailed story for this Minecraft settlement. "
                    f"It has the following plots: {environment} "
                    f"It is situated in the following biome: {biome} "
                    "Consider the layout of the settlement from the first image. "
                    "Consider the water map from the second image. "
                    "For each house, create a unique family or individual with a short, distinct background story." 
                    "Consider the available professions (from the provided information) and do not add too many details which were not provided."
                    "Ensure the total output, including all background stories, does not exceed 1000 words."
                    "Absolutely make sure you recognize and identify the plots from the images correctly."
                    "Return the response in JSON format."
                )},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image_blueprint}"
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image_water_map}"
                    },
                },
            ],
        },
    ]

    try:
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="o4-mini",
            messages=messages,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except openai.APIError as e:
        print(f"OpenAI API Error: {e}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}. Raw response: {response.choices[0].message.content}")
        return {"error": "Could not decode JSON response from API.", "raw_response": response.choices[0].message.content}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {"error": str(e)}