import pandas as pd
import os
df = pd.read_csv("tdiuc_questions_preprocessed.csv")

keyword_to_video = {
    "animal": "animal_type.mp4",
    "baseball": "baseball_position.mp4",
    "bed": "bed_posts.mp4",
    "bench": "bench_man.mp4",
    "bowl": "bowl_food.mp4",
    "boy": "boy_animal.mp4",
    "cat": "cat_activity.mp4",
    "visible": "cat_visible.mp4",
    "chair": "chair_material.mp4",
    "group": "group_people.mp4",
    "horse": "horse_riding.mp4",
    "happy": "man_happy.mp4",
    "hat": "man_hat_colour.mp4",
    "tie": "man_white_shirt_tie.mp4",
    "game": "men_playing_game.mp4",
    "plane": "multiple_planes.mp4",
    "tv": "multiple_tvs.mp4",
    "background": "person_behind_view.mp4",
    "behind": "person_behind_view.mp4",
    "activity": "person_activity.mp4",
    "plant": "potted_plants.mp4",
    "sink": "sink_scene.mp4",
    "car": "street_car_colour.mp4",
    "marking": "street_marking_colour.mp4",
    "sign": "street_sign_colour.mp4",
    "train": "train_front_colour.mp4",
    "tree": "tree_scene.mp4",
    "woman": "woman_colour_shirt.mp4"
}

def assign_video_path(question):
    for keyword, video_filename in keyword_to_video.items():
        if keyword in question.lower():
            return os.path.join("static", "tdiuc_videos", video_filename)
    return ""

df["video_path"] = df["question"].apply(assign_video_path)

df.to_csv("tdiuc_questions_with_videos.csv", index=False)

print("CSV file updated and saved as 'tdiuc_questions_with_videos.csv'")
