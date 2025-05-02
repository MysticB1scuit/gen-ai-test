from flask import Flask, render_template, request, jsonify
from models.load_stable_diffusion import load_sd_model
from datetime import datetime
import os
import torch
import gc

app = Flask(__name__)
pipe = load_sd_model()

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

@app.route('/')
def index():
    	return render_template('index.html')
	
@app.route('/generate-image', methods=['POST'])
def generate_image():
	data = request.get_json()
	prompt = data.get('text', 'a photo of a cat')
	print(f"[INFO] Generating Image for Prompt: {prompt}")

	image = pipe(prompt).images[0]

	timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"generated_{timestamp}.png"
	output_path = os.path.join('static', 'generated', filename)
	image.save(output_path)

	return jsonify({'image_url': f'/static/generated/{filename}'})

@app.route('/generate-video', methods=['POST'])
def generate_video():
	try:
		data = request.get_json()
		prompt = data.get('text', '')
		print(f"[INFO] Generating Video for Prompt: {prompt}")

		best_match = None
		max_priority = -1

		for keyword, video_filename in keyword_to_video.items():
			if keyword in prompt.lower():
				if len(keyword) > max_priority:
					best_match = video_filename
					max_priority = len(keyword)
		
		if best_match:
			selected_video = os.path.join('static', 'tdiuc_videos', best_match)
		else:
			print("[WARNING] No good match found")
			selected_video = os.path.join('static', 'tdiuc_videos', 'fallback.mp4')

		filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
		output_path = os.path.join('static', 'generated', filename)

		with open(selected_video, "rb") as src, open(output_path, "wb") as dst:
			dst.write(src.read())

		print(f"[DEBUG] Attempting to load video from: {selected_video}")
		print(f"[SUCCESS] Matched and Saved Video to: {output_path}")
		return jsonify({'video_url': f'/static/generated/{filename}'})
	
	except Exception as e:
		import traceback
		print("[ERROR] Failed to Generate Video:")
		traceback.print_exc()
		return jsonify({'error': str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate():
	data = request.get_json()
	prompt = data.get('prompt', '')
	print(f"[INFO] Unified Generate Endpoint. Prompt: {prompt}")

	best_match = None
	max_priority = -1

	for keyword, video_filename in keyword_to_video.items():
		if keyword in prompt.lower():
			if len(keyword) > max_priority:
				best_match = video_filename
				max_priority = len(keyword)

	if best_match:
		selected_video = os.path.join('static', 'tdiuc_videos', best_match)
		filename = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
		output_path = os.path.join('static', 'generated', filename)
		with open(selected_video, "rb") as src, open(output_path, "wb") as dst:
			dst.write(src.read())
		print(f"[INFO] Sending Matched Video: {output_path}")
		base_url = request.host_url.rstrip('/')
		return jsonify({'video_url': f'{base_url}/static/generated/{filename}'})
	
	else:
		image = pipe(prompt).images[0]
		filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
		output_path = os.path.join('static', 'generated', filename)
		image.save(output_path)
		print(f"[INFO] Sending Generated Image: {output_path}")
		base_url = request.host_url.rstrip('/')
		return jsonify({'image_url': f'{base_url}/static/generated/{filename}'})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=False)
