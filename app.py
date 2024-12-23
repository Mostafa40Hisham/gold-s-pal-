from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from datetime import timedelta
from database import *
import os
import secrets
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = secrets.token_hex(16)

@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        if account_login(email, password):
            user = check_email(email)  # الحصول على معلومات المستخدم بعد نجاح تسجيل الدخول
            if request.form.get('stay_logged_in'):
                session.permanent = True  # Set the session to permanent
                app.permanent_session_lifetime = timedelta(weeks=1)  # Set session lifetime to 1 week
            else:
                 session.permanent = False  # Session will expire when the browser closes

            session['user_id'] = user['id']
            session['email'] = email
            session['user_name'] = f"{user['firstname']} {user['lastname']}"
            flash('Logged in successfully!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', category='error')
            return render_template('login.html')

    return render_template('login.html')

    
@app.route('/signup', methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')
        if check_email(email):
            return "Email already exists", 400

        if not all([first_name, last_name, email, password, dob]):
            flash("All fields are required!")
            return render_template('sign-up.html')
        
        insert_account({'firstname': first_name,
                         'lastname': last_name, 
                         'email': email, 
                         'date_of_birth': dob,
                         'password': password })
        flash("Account created successfully! Please log in.")
        return render_template('login.html')
    elif request.method == "GET":
        return render_template('sign-up.html')
    
@app.route('/home')
def home():
    if "user_id" in session:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/recipe')
def recipe():
    if "user_id" in session:
        return render_template('recipe.html')
    else:
        return redirect(url_for('login'))

@app.route('/inbody')
def inbody():
    if "user_id" in session:
        return render_template('inbody.html')
    else:
        return redirect(url_for('login'))

@app.route('/about')
def about():
    if "user_id" in session:
        return render_template('about.html')
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/show')
def show():
    if "user_id" in session:
        data = get_recipes_data()
        return render_template('show.html', data = data)
    else:
        return redirect(url_for('login'))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if "user_id" in session:
        if request.method == 'GET':
            return render_template('upload.html')
        
        if request.method == 'POST':
            recipe_name = request.form.get('name')  
            description = request.form.get('description')  
            calories = request.form.get('calories')  
            photo = request.files.get('photo')  
            file_name = photo.filename

            if not all([recipe_name, description, calories, photo]):
                flash("Please fill out all fields.", category="warning")
                return render_template('upload.html')
            
            
            if not photo.filename:
                flash("Please upload a valid photo.", category="warning")
                return render_template('upload.html')
            
            filename = photo.filename
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            insert_recipes({'name': recipe_name,
                            'calories': calories, 
                            'description': description,
                            'file_name':  file_name })
            flash('Recipe uploaded successfully!', category='success')
            return render_template('upload.html')
    else:
        return redirect(url_for('login'))
    



@app.route('/profile', methods=["POST", "GET"])
def profile():
    if request.method == "POST":
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        date_of_birth = request.form.get('date_of_birth')

        user = check_email(email)  

        if user and firstname and lastname and date_of_birth:
            update_user_data(email,firstname,lastname,date_of_birth)
        else:
            flash('missing Data please try again', category='error')
            return render_template('profile.html')
    if "user_id" in session:
        data = check_email(session['email'])
        return render_template('profile.html',email=data['email'],firstname=data['firstname'],lastname=data['lastname'],date_of_birth=data['date_of_birth'])
    else:
        return redirect(url_for('login'))

@app.route('/contact')
def contact():
    if "user_id" in session:
        return render_template('contact.html')
    else:
        return redirect(url_for('login'))

muscles = [
      {
        "id": 1,
        "muscle_name": "arm",
        "muscle_image": "https://bod-blog-assets.prod.cd.beachbodyondemand.com/bod-blog/wp-content/uploads/2022/06/14153553/arm-muscles-960-715x358.png",
        "sections": {
            "Biceps": {
                "Concentration curl": " https://www.garagegymreviews.com/wp-content/uploads/concentration-curl.gif",
                "Preacher curl": "https://www.garagegymreviews.com/wp-content/uploads/EZ-bar-preacher-curl.gif",
                "Chin-up": "https://www.garagegymreviews.com/wp-content/uploads/banded-chin-up.gif",
                "Reverse curls": "https://builtwithscience.com/wp-content/uploads/2019/04/2-2.jpg",
                "Hammer curls": "https://builtwithscience.com/wp-content/uploads/2019/04/3-2.jpg",
                "Reverse grip - EZ bar curls": "https://builtwithscience.com/wp-content/uploads/2019/04/4-2.jpg"
            },
            "Triceps": {
                "Triangle Pushups": "https://cdn.shopify.com/s/files/1/1633/7705/files/best_long_head_triceps_exercises_480x480.png?v=1635395188",
                "Dips": "https://cdn.shopify.com/s/files/1/1633/7705/files/exercises_to_target_long_head_of_triceps_480x480.jpg?v=1635395240",
                "Close Grip Bench Press": "https://cdn.shopify.com/s/files/1/1633/7705/files/triceps_muscle_long_head_exercises_480x480.jpg?v=1635395285",
                "Close-Grip Dumbbell Bench Press": "https://hips.hearstapps.com/hmg-prod/images/close-grip-bench-1626695039.jpg?resize=980:*",
                "Laying Tricep Extension": "https://hips.hearstapps.com/hmg-prod/images/lying-tricep-extension-657c460f80892.jpg?resize=980:*",
                "Laying Single Dumbbell Crush Extension": "https://hips.hearstapps.com/hmg-prod/images/dumbbell-skull-crusher-475x546-1-6626420456003.jpg?resize=640:*"
            }
        }
    },
    {
        "id": 2,
        "muscle_name": "back",
        "muscle_image": "https://images.contentstack.io/v3/assets/blt45c082eaf9747747/blt6c7d5e3aece27291/66ba7ddf316653eea049c7c8/back-muscles-header.jpg?format=pjpg&auto=webp&quality=76&width=1232",
        "sections": {
            "upper": {
                "Horizontal Pulling": "https://cdn-0.weighttraining.guide/wp-content/uploads/2020/11/Horizontal-pulling-exercises-upper-arms-close-to-torso.png",
                "Vertical Pulling Movements": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTKiHlSgDV3ekSLeof9UlOhzhgiBMhZbmg0NA&s",
                "Shoulder Extension and Rear Deltoid Movements": "https://hips.hearstapps.com/menshealth-uk/main/thumbs/33038/lying-rear-delt-fly.jpg?resize=980:*",
                "Rotational Movements and Stability": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT_yYwxTKgzGIHcJdES7Q5nK71FUuMZClKcQg&s",
                "Isometric Holds": "https://hips.hearstapps.com/hmg-prod/images/female-athlete-practicing-side-plank-at-home-royalty-free-image-1632260664.jpg?crop=0.668xw:1.00xh;0.102xw,0&resize=640:*",
                "Stretching and Mobility Exercises": "https://www.uofmhealthsparrow.org/sites/default/files/2024-02/yoga-stretch-mobility-poses-q1-email-newsletter.png",
                "Combined Movements for Upper Back": "https://images.squarespace-cdn.com/content/v1/5e18bc2a7fcc9522d36a7373/1579724590021-NC3934N23BGRZKITJE6D/upper+back+exercises.jpg"
            },
            "lower": {
                "Bodyweight Exercises": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ-ttHVF2CSAiuWuQdQ8wwPhw62P-UxrRVibw&s",
                "Resistance Training": "https://cdn.shopify.com/s/files/1/0405/9358/8374/files/Strengthen_Your_Lower_Back_480x480.jpg?v=1693952194",
                "Core Stabilization Exercises": "https://static.wixstatic.com/media/36c99a_b4e0ca58031848aabc75a6834373f9c8~mv2.jpg/v1/fill/w_568,h_448,al_c,q_80,usm_0.66_1.00_0.01,enc_auto/36c99a_b4e0ca58031848aabc75a6834373f9c8~mv2.jpg",
                "Yoga and Pilates": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTJb3JVoOivZ2FuWS8cud91Ug5lCPgxyJohiA&s",
                "Rehabilitation and Prehab Exercises": "https://www.csp.org.uk/sites/default/files/styles/section_index_teaser/public/images/2020-07/back-pain-video-exercise.jpg?itok=4dc1L1IU",
                "Flexibility and Mobility Work": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMvq7NB94LrG6zSLXdVC-2JYtN_Ag_pWT9JA&s"
            },
            "lats": {
                "Deadlifts": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQg5VpOJVOaQgd1VQ1hVJHs9bFALcvg0kwMFg&s",
                "Machine and Cable Movements": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzVeLMPHl9iNiWZPxE-kTJZW4C7c4s-gjl-Q&s",
                "Pulling with Rotation": "https://images.squarespace-cdn.com/content/v1/5bb4d0259b7d154602dbcdaa/768de9d6-f386-4e47-ae0f-47a8514dcff5/paloff+rotation.jpg",
                "Isometric Holds": "https://b1494239.smushcdn.com/1494239/wp-content/uploads/2014/08/isometrics-600x600.jpg?lossy=0&strip=1&webp=1",
                "Stretching and Mobility Exercises for Lats": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVfQDfJpWdcf7ntBfc1e1WS44SESXUB6wQDg&s"
            }
        }
    },
    {
        "id": 3,
        "muscle_name": "shoulder",
        "muscle_image": "https://i0.wp.com/www.strengthlog.com/wp-content/uploads/2022/09/back-and-shoulder-workout-scaled.jpg?fit=2560%2C1426&ssl=1",
        "sections": {
            "front delts": {
                "Barbell Front Raise": "https://cdn.jefit.com/assets/img/exercises/gifs/6.gif",
                "Dumbbell Front Raise": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZ4U5DV0CTS4KrEnHuzb4iPcbyZk-GzqDJ6A&s",
                "Cable Front Raise": "https://i.pinimg.com/originals/83/e2/92/83e2920256d8968d916463fcd691c394.jpg",
                "Plate Front Raise": "https://julielohre.com/wp-content/uploads/2017/12/Plate-Front-Delt-Raise-1024x986.jpg",
                "Landmine Press": "https://www.dmoose.com/cdn/shop/articles/1_29c9d6a3-c2ad-4ad0-af9d-eadc397b0ac0.jpg?v=1653734257",
                "Arnold Press": "https://hips.hearstapps.com/hmg-prod/images/db-seated-shoulder-pressat1-25x-64d387fe154b1.jpg?resize=980:*"
            },
            "lateral delts": {
                "Dumbbell Lateral Raise": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeP9RykiOPP-aUYF33OmwuHOarVg9JWIILkw&s",
                "Cable Lateral Raise": "https://cdn.shopify.com/s/files/1/1214/7132/files/mt-cable-lateral-raise-900x675_05489ca8-5457-451c-a109-c173f4409a85.jpg?v=1707499502",
                "Seated Dumbbell Lateral Raise": "https://www.dmoose.com/cdn/shop/articles/Seated-Dumbbell-Lateral-Raise-Guide-Image-1.jpg",
                "Incline Lateral Raise": "https://www.mybodycreator.com/content/files/2023/05/26/86_M.png",
                "Machine Lateral Raise": "https://cdn.prod.website-files.com/5c34b1d990599d5d94b3e8d8/5fd18f49d94da00988c9e921_05841201-Lever-Lateral-Raise-shoulder.jpeg",
                "Kettlebell Lateral Raise": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSc6tP5og87cPcWiZIvFWkym9ToNIRYJ48dEA&s"
            }
        }
    },
    {
        "id": 4,
        "muscle_name": "chest",
        "muscle_image": "https://barbend.com/wp-content/uploads/2023/07/chest-muscles-anatomy-barbend.com_.jpg",
        "sections": {
            "inner": {
                "Incline Bench Press": "https://www.barbellmedicine.com/wp-content/uploads/2023/10/Incline-Bench-Press.jpg",
                "Flat Dumbbell Bench Press": "https://www.barbellmedicine.com/wp-content/uploads/2024/01/Flat-Dumbbell-Bench-Press.jpg",
                "Dumbbell Flyes": "https://www.barbellmedicine.com/wp-content/uploads/2023/10/Dumbbell-Flyes.jpg",
                "High-to-Low Cable Flyes": "https://www.barbellmedicine.com/wp-content/uploads/2024/01/High-to-Low-Cable-Flyes.jpg",
                "Dumbbell Hex Press": "https://www.barbellmedicine.com/wp-content/uploads/2024/01/Dumbbell-Hex-Press.jpg"
            },
            "lower": {
                "Cable Crossover": "https://www.barbellmedicine.com/wp-content/uploads/2023/10/Cable-Crossover.jpg",
                "Push-up": "https://www.barbellmedicine.com/wp-content/uploads/2023/10/Push-Up.jpg",
                "Incline Push-up": "https://www.barbellmedicine.com/wp-content/uploads/2023/11/Incline-Push-ups.jpg",
                "Decline Push-up": "https://www.barbellmedicine.com/wp-content/uploads/2023/11/Decline-Push-ups.jpg",
                "Medicine Ball Push-up": "https://www.barbellmedicine.com/wp-content/uploads/2023/12/Medicine-Ball-Push-up.jpg",
                "Seated Machine Flyes": "https://www.barbellmedicine.com/wp-content/uploads/2023/12/Seated-Machine-Flyes.jpg"
            },
            "upper": {
                "Incline Hex Press": "https://barbend.com/wp-content/uploads/2023/04/incline-hex-press-barbend-movement-gif-masters.gif",
                "Close-Grip Bench Press": "https://barbend.com/wp-content/uploads/2022/05/barbell-close-grip-bench-press-barbend-movement-gif-masters.gif",
                "Incline Bench Press": "https://barbend.com/wp-content/uploads/2024/01/incline-barbell-bench-press-barbend-movement-gif-masters-2.gif",
                "Incline Dumbbell Bench Press": "https://barbend.com/wp-content/uploads/2024/01/incline-dumbbell-bench-press-barbend-movement-gif-masters.gif",
                "Guillotine Press": "https://barbend.com/wp-content/uploads/2023/04/guillotine-press-barbend-movement-gif-masters.gif",
                "Low Cable Crossover": "https://barbend.com/wp-content/uploads/2023/04/low-cable-flye-barbend-movement-gif-masters.gif"
            }
        }
    },
     {
        "id": 5,
        "muscle_name": "leg",
        "muscle_image": "https://steelsupplements.com/cdn/shop/articles/shutterstock_185279813_1000x.jpg?v=1632331479",
        "sections": {
            "calves": {
                "standing calf raises": "https://training.fit/wp-content/uploads/2020/03/wadenheben-langhantel-stehend-2.png",
                "sitting calf raises": "https://weighttraining.guide/wp-content/uploads/2016/10/Lever-Seated-Calf-Raise-plate-loaded-resized.png",
                "Box Calf Raises": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRrV08OjnNtLraOakArMb8k0AX3wuFI6jGaog&s",
                "Jump Rope": "https://cdn.shopify.com/s/files/1/1142/3440/articles/kR4o8Nh.png?v=1712211815",
                "Weighted Calf Raises": "https://hips.hearstapps.com/hmg-prod/images/bent-knee-calf-raise-653a68dbdc9c1.png?resize=980:*"
            },
            "hamstrings": {
                "Romanian Deadlifts": "https://hips.hearstapps.com/hmg-prod/images/romanian-dl-1582015033.jpg?crop=1.00xw:0.888xh;0,0.112xh&resize=980:*",
                "Leg Curl": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUxAgC3DeIkig6P8sudq-ZvNP581bNN6jGBA&s",
                "Deadlifts": "https://www.evolvefitstudios.com/uploads/1/0/2/9/102951852/deadlifts_orig.jpeg",
                "Swiss Ball Leg Curls": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRCWrGbGPutCF3l-zaoy1G8tlijYEKVq5cBSw&s",
                "Reverse Lunges": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRr9OdiVsaxLxR6vRTB1RjOq30WkaEPhQuAsQ&s",
                "Kettlebell Swing": "https://i.ytimg.com/vi/mKDIuUbH94Q/maxresdefault.jpg"
            },
            "quadriceps": {
                "Squats": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMofx0xA2qL9FeiJHraHd5HV0xoCtsGyq87A&s",
                "Lunges": "https://media.post.rvohealth.io/wp-content/uploads/2021/11/cardio-class-woman-lunges-thumbnail-732x549.jpg",
                "Leg Extension": "https://cdn.shopify.com/s/files/1/0252/3155/6686/files/Leg_Extension_Machine_1.jpg?v=1710959433",
                "Bulgarian Split Squats": "https://www.tonal.com/wp-content/uploads/2024/01/Bulgarian-Split-Squat-Hero.jpg",
                "Leg Press": "https://powertec.com/cdn/shop/files/P-LP23_3SQUARE_1800x1800.jpg?v=1723123620"
            },
            "glutes": {
                "Deadlifts": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ75opp3mFCoE4WpvaEnUX41TgxCt5hNSH-5g&s",
                "Hip Thrusts": "https://bretcontreras.com/wp-content/uploads/KAZ-Glute-Bridge-Alt-2.jpeg",
                "Squats": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMofx0xA2qL9FeiJHraHd5HV0xoCtsGyq87A&s",
                "Bulgarian Split Squats": "https://www.tonal.com/wp-content/uploads/2024/01/Bulgarian-Split-Squat-Hero.jpg",
                "Jumping Lunges": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEo7tsnV-ycCvKwL1NqjsRUcY3Q8SFrdclRg&s",
                "Glute Kickbacks": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRWubw502d0raTSuTUG_wtetvX6SzHCPL_arw&s"
            },
            "adductors": {
                "Leg Adduction Machine": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQg8zHnJzuIQ_NgncKtXhHq-C7EA56-iOGUYg&s",
                "Sumo Squats": "https://www.kettlebellkings.com/cdn/shop/articles/Kettlebell_Sumo_Squat_1200x1200_crop_center.jpg?v=1732016655",
                "Standing Adduction with Resistance Band": "https://www.sparkpeople.com/assets/exercises/Standing-Hip-Adduction-with-Band.gif",
                "Plank with Leg Lift": "https://media.post.rvohealth.io/wp-content/uploads/sites/2/2020/06/1.1.PlankLegRaises.gif",
                "Wide Leg Deadlifts": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQuh3s5Vyy9WfAwR0nOqgvUK5Vn1Ct6-WOZJw&s",
                "Lying Adduction": "https://www.sparkpeople.com/assets/exercises/Lying-Adduction.gif"
            }
        }
    },
    {
        "id": 6,
        "muscle_name": "six packs",
        "muscle_image": "https://cosmetic-dermatology-center.com/wp-content/uploads/2019/02/Six-packs-men-912x608.jpg",
        "sections": {
            "exercises": {
                "Overhead Squats": "https://hips.hearstapps.com/menshealth-uk/main/assets/overhead-squat.gif?crop=1xw:1xh;center,top&resize=980:*",
                "Prone Knee to Opposite Elbow": "https://hips.hearstapps.com/hmg-prod/images/mountain-climber-1583755965.jpg?resize=980:*",
                "Press-ups": "https://hips.hearstapps.com/hmg-prod/images/press-up-1619177576.jpg?resize=980:*",
                "Uphill Treadmill – Walking": "https://hips.hearstapps.com/hmg-prod/images/cropped-view-of-man-workout-on-treadmill-in-living-royalty-free-image-1613481771.?resize=980:*"
            }
        }
    }
]


@app.route('/excercise')
def excercise():
    if "user_id" in session:
       return render_template('excercise.html', muscles=muscles)
    else:
        return redirect(url_for('login'))
    

@app.route('/muscles')
def muscle_page():
    return render_template('muscles.html')

@app.route('/muscleTraning')
def muscleTraning_page():
    return render_template('muscleTraning.html')


# Route to get all muscle data
@app.route('/api/muscles', methods=['GET'])
def get_muscles():
    return jsonify(muscles)


@app.route("/api/muscles/<int:muscle_id>", methods=["GET"])
def get_muscle_by_id(muscle_id):
    muscle = next((m for m in muscles if m["id"] == muscle_id), None)
    if muscle is None:
        return jsonify({"error": "Muscle not found"}), 404
    return jsonify(muscle)


# http://127.0.0.1:5000/muscles/${muscleId}/sections/${sectionName}
@app.route('/muscles/<int:muscle_id>/sections/<section_name>/', methods=['GET'])
def get_muscle_section_by_id(muscle_id, section_name):
    # Find the muscle by ID
    muscle = next((m for m in muscles if m["id"] == muscle_id), None)
    if muscle:
        # Retrieve the requested section
        section_data = muscle.get("sections", {}).get(section_name, None)
        if section_data:
            return jsonify(section_data)
        return jsonify({"error": f"Section '{section_name}' not found for muscle ID '{muscle_id}'"}), 404
    return jsonify({"error": f"Muscle with ID '{muscle_id}' not found"}), 404

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)


