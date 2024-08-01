import mysql.connector as mysql

def create_database_and_table():
    try:
        # Connect to MySQL without specifying a database
        db = mysql.connect(
            host="localhost",
            user="root",
            passwd=""
        )

        cursor = db.cursor()

        # Create database if it does not exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS IOT")
        print("Database checked/created successfully.")

        # Connect to the IOT database
        db.database = "iot"

        # Check if the users table exists
        cursor.execute("SHOW TABLES LIKE 'users'")
        result_users = cursor.fetchone()

        if result_users:
            print("Users table already exists.")
        else:
            cursor.execute("""
                CREATE TABLE users(
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    username VARCHAR(255) NOT NULL UNIQUE, 
                    password VARCHAR(255) NOT NULL 
                )
            """)
            print("Users table created successfully.")

        # Check if the sensor table exists 
        cursor.execute("SHOW TABLES LIKE 'sensor'")
        result_sensor = cursor.fetchone()

        if result_sensor: 
            print("Sensor table already exists.")
        else: 
            cursor.execute("""
                           CREATE TABLE `sensor` (
                                `datetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
                                `sensor` text NOT NULL,
                                `value` text NOT NULL
                                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                           """)

        # Check if the faceregister table exists
        cursor.execute("SHOW TABLES LIKE 'faceregister'")
        result_faceregister = cursor.fetchone()

        if result_faceregister:
            print("faceregister table already exists.")
        else:
            cursor.execute("""
                CREATE TABLE faceregister(
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11),
                    status VARCHAR(255) NOT NULL
                )
            """)
            print("faceregister table created successfully.")


        # Check if the sleeptrack table exists
        cursor.execute("SHOW TABLES LIKE 'sleeptrack'")
        result_sleeptrack = cursor.fetchone()

        if result_sleeptrack: 
            print("sleeptrack table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE sleeptrack ( 
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11), 
                    start_time VARCHAR(255) NOT NULL, 
                    end_time VARCHAR(255) NOT NULL, 
                    sleep_minute INT(11) NOT NULL,
                    facedetected_minute INT(11) NOT NULL, 
                    date DATE NOT NULL,
                )
            """)
            print("sleeptrack table created successfully.")


        # Check if the userinfo table exists
        cursor.execute("SHOW TABLES LIKE 'userinfo'")
        result_userinfo = cursor.fetchone()

        if result_userinfo: 
            print("userinfo table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE userinfo ( 
                    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    user_id INT(11) NOT NULL, 
                    gender VARCHAR(255), 
                    age INT(11), 
                    birthdate VARCHAR(255), 
                    height INT(11),
                    weight DECIMAL(10, 2),
                    goal VARCHAR(255),
                    sleep_goal_hour INT(11)
                )
            """)
            print("userinfo table created successfully.")

        # Check if the usermeals table exists
        cursor.execute("SHOW TABLES LIKE 'usermeals'")
        result_usermeals = cursor.fetchone()

        if result_usermeals: 
            print("usermeals table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE usermeals ( 
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
                    calories INT NOT NULL,
                    date DATE NOT NULL,
                    user_id INT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES userinfo(id)
                )
            """)
            print("usermeals table created successfully.")

        
        # Check if 'exercises' table exists
        cursor.execute("SHOW TABLES LIKE 'exercises'")
        result_exercises = cursor.fetchone()

        if result_exercises:
            print("exercises table already exists.")

            # Check if there is any data in the table
            cursor.execute("SELECT COUNT(*) FROM exercises")
            count = cursor.fetchone()[0]

            if count == 0:
                # If the table is empty, insert data
                exercises_data = [
                    ('Seated Leg Lifts', 'While seated, extend one leg out straight and hold for a few seconds. Lower it slowly and repeat with the other leg. This helps strengthen the hip flexors and quadriceps.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722437699/Seated_Leg_Lifts_jepa1z.png'),
                    ('Seated Torso Twists', 'Sit up straight, place your hands behind your head, and gently twist your torso to one side, then to the other. This improves spinal mobility and stretches the back muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Torso_Twists_bys5hn.webp'),
                    ('Neck Stretches', 'Gently tilt your head towards one shoulder, hold for 15-30 seconds, and switch sides. This helps relieve tension in the neck and shoulders.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Neck_Stretches_ia8g9q.jpg'),
                    ('Shoulder Shrugs', 'Lift your shoulders towards your ears and then roll them back down. This exercise helps alleviate shoulder stiffness and improve posture.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Shoulder_Shrugs_ogpgdu.webp'),
                    ('Seated Cat-Cow Stretch', 'While seated, place your hands on your knees. Arch your back and lift your chest (Cow Pose), then round your back and tuck your chin (Cat Pose). This improves flexibility in the spine.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Cat-Cow_Stretch_hkjvl5.jpg'),
                    ('Desk Push-Ups', 'Place your hands on the edge of a desk, step back, and perform a push-up by bending your elbows and lowering your chest towards the desk. This strengthens the chest and arms.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Desk_Push-Ups_kpvprc.jpg'),
                    ('Standing Calf Raises', 'Stand up and lift your heels off the ground, then lower them slowly. This helps improve circulation and strengthen the calf muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Standing_Calf_Raises_qcwzjh.jpg'),
                    ('Standing Side Leg Raises', 'Stand with one hand on a chair or desk for balance, lift one leg out to the side, and then lower it back down. Repeat on the other side. This strengthens the hip abductors and improves stability.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Standing_Side_Leg_Raises_tjkly1.jpg'),
                    ('Hamstring Stretch', 'While seated, extend one leg straight out and reach towards your toes. Hold for 15-30 seconds and switch legs. This helps stretch the hamstrings and reduce tightness.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Hamstring_Stretch_lgndhe.jpg'),
                    ('Wrist and Finger Stretches', 'Extend one arm in front, use the other hand to gently pull back the fingers of the extended arm. Hold for 15-30 seconds and switch hands. This helps reduce stiffness from typing.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Wrist_and_Finger_Stretches_gaj4ov.jpg'),
                    ('Glute Squeezes', 'While seated, squeeze your glutes tightly, hold for a few seconds, and then release. This helps activate and strengthen the glute muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Glute_Squeezes_litkbp.png'),
                    ('Hip Flexor Stretch', 'Stand up, step one foot back into a lunge position, and gently push your hips forward. Hold for 15-30 seconds and switch legs. This stretches the hip flexors and reduces tightness.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Hip_Flexor_Stretch_kantwl.png'),
                    ('Seated Side Bends', 'Sit up straight, place one hand on the opposite side of your chair, and lean to the side, stretching the side of your body. Hold for 15-30 seconds and switch sides.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Side_Bends_gfahmz.jpg'),
                    ('Seated Marching', 'While seated, lift one knee towards your chest and then lower it back down. Alternate legs in a marching motion. This helps stimulate circulation and engage the hip flexors.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Marching_kjaa8y.png'),
                    ('T-Spine Rotation', 'Sit up straight, place your hands behind your head, and rotate your upper body to one side, then to the other. This improves thoracic spine mobility.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/T-Spine_Rotation_ev56wl.jpg'),
                    ('Shoulder Blade Squeezes', 'Sit or stand with good posture, squeeze your shoulder blades together, hold for a few seconds, and release. This helps improve posture and strengthen the upper back.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Shoulder_Blade_Squeezes_qy2vzi.jpg'),
                    ('Seated Hip Abduction', 'While seated, place a small resistance band around your thighs. Push your knees outward against the band and then return to the starting position. This strengthens the hip abductors.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Hip_Abduction_pgg52i.jpg'),
                    ('Chair Yoga', 'Incorporate simple yoga poses like seated forward bends or gentle twists while seated to enhance flexibility and relaxation.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722437595/Chair_Yoga_h8pkmq.jpg'),
                    ('Standing Forward Bend', 'Stand up, bend at the waist, and reach towards the floor. This stretches the hamstrings and lower back.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Standing_Forward_Bend_vbtlfb.jpg'),
                    ('Chest Opener Stretch', 'Stand with feet shoulder-width apart, clasp your hands behind your back, and gently lift your arms while opening your chest. This helps stretch the chest and shoulders.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Chest_Opener_Stretch_bzosqs.jpg')
                ]
                cursor.executemany("INSERT INTO exercises (exercise_name, exercise_description, photo_url) VALUES (%s, %s, %s)", exercises_data)
                db.commit()  # Commit the transaction
                print("Data inserted into exercises table successfully.")
            else:
                print("exercises table already has data.")
        else:
            # If the table does not exist, create it
            cursor.execute("""
                CREATE TABLE exercises (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    exercise_name VARCHAR(255) NOT NULL,
                    exercise_description TEXT,
                    photo_url VARCHAR(255)
                )
            """)
            print("exercises table created successfully.")
            
            # Insert data into exercises table
            exercises_data = [
                ('Seated Leg Lifts', 'While seated, extend one leg out straight and hold for a few seconds. Lower it slowly and repeat with the other leg. This helps strengthen the hip flexors and quadriceps.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722437699/Seated_Leg_Lifts_jepa1z.png'),
                ('Seated Torso Twists', 'Sit up straight, place your hands behind your head, and gently twist your torso to one side, then to the other. This improves spinal mobility and stretches the back muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Torso_Twists_bys5hn.webp'),
                ('Neck Stretches', 'Gently tilt your head towards one shoulder, hold for 15-30 seconds, and switch sides. This helps relieve tension in the neck and shoulders.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Neck_Stretches_ia8g9q.jpg'),
                ('Shoulder Shrugs', 'Lift your shoulders towards your ears and then roll them back down. This exercise helps alleviate shoulder stiffness and improve posture.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Shoulder_Shrugs_ogpgdu.webp'),
                ('Seated Cat-Cow Stretch', 'While seated, place your hands on your knees. Arch your back and lift your chest (Cow Pose), then round your back and tuck your chin (Cat Pose). This improves flexibility in the spine.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Cat-Cow_Stretch_hkjvl5.jpg'),
                ('Desk Push-Ups', 'Place your hands on the edge of a desk, step back, and perform a push-up by bending your elbows and lowering your chest towards the desk. This strengthens the chest and arms.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Desk_Push-Ups_kpvprc.jpg'),
                ('Standing Calf Raises', 'Stand up and lift your heels off the ground, then lower them slowly. This helps improve circulation and strengthen the calf muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Standing_Calf_Raises_qcwzjh.jpg'),
                ('Standing Side Leg Raises', 'Stand with one hand on a chair or desk for balance, lift one leg out to the side, and then lower it back down. Repeat on the other side. This strengthens the hip abductors and improves stability.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Standing_Side_Leg_Raises_tjkly1.jpg'),
                ('Hamstring Stretch', 'While seated, extend one leg straight out and reach towards your toes. Hold for 15-30 seconds and switch legs. This helps stretch the hamstrings and reduce tightness.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Hamstring_Stretch_lgndhe.jpg'),
                ('Wrist and Finger Stretches', 'Extend one arm in front, use the other hand to gently pull back the fingers of the extended arm. Hold for 15-30 seconds and switch hands. This helps reduce stiffness from typing.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Wrist_and_Finger_Stretches_gaj4ov.jpg'),
                ('Glute Squeezes', 'While seated, squeeze your glutes tightly, hold for a few seconds, and then release. This helps activate and strengthen the glute muscles.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Glute_Squeezes_litkbp.png'),
                ('Hip Flexor Stretch', 'Stand up, step one foot back into a lunge position, and gently push your hips forward. Hold for 15-30 seconds and switch legs. This stretches the hip flexors and reduces tightness.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Hip_Flexor_Stretch_kantwl.png'),
                ('Seated Side Bends', 'Sit up straight, place one hand on the opposite side of your chair, and lean to the side, stretching the side of your body. Hold for 15-30 seconds and switch sides.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Side_Bends_gfahmz.jpg'),
                ('Seated Marching', 'While seated, lift one knee towards your chest and then lower it back down. Alternate legs in a marching motion. This helps stimulate circulation and engage the hip flexors.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Marching_kjaa8y.png'),
                ('T-Spine Rotation', 'Sit up straight, place your hands behind your head, and rotate your upper body to one side, then to the other. This improves thoracic spine mobility.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/T-Spine_Rotation_ev56wl.jpg'),
                ('Shoulder Blade Squeezes', 'Sit or stand with good posture, squeeze your shoulder blades together, hold for a few seconds, and release. This helps improve posture and strengthen the upper back.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Shoulder_Blade_Squeezes_qy2vzi.jpg'),
                ('Seated Hip Abduction', 'While seated, place a small resistance band around your thighs. Push your knees outward against the band and then return to the starting position. This strengthens the hip abductors.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438746/Seated_Hip_Abduction_pgg52i.jpg'),
                ('Chair Yoga', 'Incorporate simple yoga poses like seated forward bends or gentle twists while seated to enhance flexibility and relaxation.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722437595/Chair_Yoga_h8pkmq.jpg'),
                ('Standing Forward Bend', 'Stand up, bend at the waist, and reach towards the floor. This stretches the hamstrings and lower back.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438747/Standing_Forward_Bend_vbtlfb.jpg'),
                ('Chest Opener Stretch', 'Stand with feet shoulder-width apart, clasp your hands behind your back, and gently lift your arms while opening your chest. This helps stretch the chest and shoulders.', 'https://res.cloudinary.com/sp-esde-p2235105/image/upload/v1722438745/Chest_Opener_Stretch_bzosqs.jpg')
            ]
            cursor.executemany("INSERT INTO exercises (exercise_name, exercise_description, photo_url) VALUES (%s, %s, %s)", exercises_data)
            db.commit()  # Commit the transaction
            print("Data inserted into exercises table successfully.")

        # Check if 'meals' table exists
        cursor.execute("SHOW TABLES LIKE 'meals'")
        result_meals = cursor.fetchone()

        if result_meals:
            print("meals table already exists.")

            # Check if there is any data in the table
            cursor.execute("SELECT COUNT(*) FROM meals")
            count = cursor.fetchone()[0]

            if count == 0:
                # If the table is empty, insert data
                meals_data = [
                    ('Oatmeal with Berries', 'breakfast', 300, 'oats, mixed berries, almond milk, honey', 'Cook oats with almond milk and top with berries and honey.'),
                    ('Avocado Toast', 'breakfast', 350, 'whole grain bread, avocado, cherry tomatoes, olive oil', 'Mash avocado on toasted bread and top with sliced tomatoes and olive oil.'),
                    ('Greek Yogurt with Nuts', 'breakfast', 300, 'Greek yogurt, mixed nuts, honey', 'Top Greek yogurt with nuts and a drizzle of honey.'),
                    ('Quinoa Salad', 'lunch', 400, 'quinoa, cucumbers, cherry tomatoes, feta cheese, olives, lemon vinaigrette', 'Mix all ingredients and dress with lemon vinaigrette.'),
                    ('Grilled Chicken Wrap', 'lunch', 450, 'grilled chicken, whole wheat wrap, lettuce, tomatoes, avocado', 'Fill wrap with grilled chicken and veggies, then roll up.'),
                    ('Lentil Soup', 'lunch', 350, 'lentils, carrots, celery, onions, garlic, vegetable broth', 'Cook all ingredients in a pot until lentils are tender.'),
                    ('Baked Salmon', 'dinner', 500, 'salmon fillets, lemon, garlic, herbs', 'Season salmon with garlic and herbs, bake until cooked through.'),
                    ('Stuffed Bell Peppers', 'dinner', 450, 'bell peppers, ground turkey, quinoa, black beans, corn', 'Stuff peppers with turkey mixture and bake until peppers are tender.'),
                    ('Zucchini Noodles with Pesto', 'dinner', 400, 'zucchini, pesto sauce, cherry tomatoes, pine nuts', 'Toss zucchini noodles with pesto and top with tomatoes and pine nuts.'),
                    ('Chia Seed Pudding', 'snack', 225, 'chia seeds, almond milk, vanilla extract, fruit', 'Mix chia seeds with almond milk and vanilla, let sit overnight, then top with fruit.'),
                    ('Apple Slices with Peanut Butter', 'snack', 250, 'apple, peanut butter', 'Slice apple and serve with peanut butter for dipping.'),
                    ('Hummus and Veggies', 'snack', 230, 'hummus, carrots, cucumber, bell peppers', 'Dip veggies in hummus.'),
                    ('Sweet Potato Fries', 'snack', 250, 'sweet potatoes, olive oil, paprika', 'Cut sweet potatoes into fries, toss with oil and paprika, and bake.'),
                    ('Cottage Cheese with Pineapple', 'snack', 225, 'cottage cheese, pineapple', 'Top cottage cheese with pineapple chunks.'),
                    ('Smoothie Bowl', 'breakfast', 350, 'banana, spinach, almond milk, granola, berries', 'Blend banana and spinach with almond milk, top with granola and berries.'),
                    ('Egg White Omelette', 'breakfast', 300, 'egg whites, spinach, mushrooms, tomatoes', 'Cook egg whites with veggies in a non-stick pan.'),
                    ('Chickpea Salad', 'lunch', 400, 'chickpeas, cucumber, tomatoes, red onion, lemon dressing', 'Mix chickpeas and veggies, dress with lemon dressing.'),
                    ('Turkey and Veggie Stir-Fry', 'lunch', 450, 'ground turkey, bell peppers, broccoli, soy sauce', 'Stir-fry turkey and veggies with soy sauce.'),
                    ('Grilled Tofu with Vegetables', 'dinner', 400, 'tofu, bell peppers, broccoli, soy sauce', 'Grill tofu and vegetables with soy sauce.'),
                    ('Cauliflower Rice Bowl', 'dinner', 350, 'cauliflower rice, edamame, carrots, soy sauce', 'Stir-fry cauliflower rice with edamame and carrots, add soy sauce.'),
                    ('Baked Chicken Breast', 'dinner', 400, 'chicken breast, garlic, lemon, rosemary', 'Season chicken and bake until cooked through.'),
                    ('Spaghetti Squash with Marinara', 'dinner', 350, 'spaghetti squash, marinara sauce', 'Roast squash and top with marinara sauce.'),
                    ('Berry Smoothie', 'snack', 250, 'mixed berries, Greek yogurt, almond milk', 'Blend berries with Greek yogurt and almond milk.'),
                    ('Oven-Roasted Chickpeas', 'snack', 230, 'chickpeas, olive oil, spices', 'Toss chickpeas with oil and spices, roast in the oven.'),
                    ('Peach and Almond Salad', 'lunch', 400, 'peach, mixed greens, almonds, balsamic vinaigrette', 'Mix peach slices with greens and almonds, dress with vinaigrette.'),
                    ('Salmon and Asparagus', 'dinner', 450, 'salmon, asparagus, olive oil, lemon', 'Bake salmon and asparagus with olive oil and lemon.'),
                    ('Grilled Portobello Mushrooms', 'dinner', 300, 'portobello mushrooms, balsamic vinegar, garlic', 'Grill mushrooms with balsamic vinegar and garlic.'),
                    ('Black Bean Soup', 'lunch', 350, 'black beans, tomatoes, onions, spices', 'Cook all ingredients until flavors meld.'),
                    ('Egg Salad Lettuce Wraps', 'lunch', 400, 'eggs, Greek yogurt, mustard, lettuce leaves', 'Mix egg salad with Greek yogurt and mustard, serve in lettuce wraps.'),
                    ('Fruit Salad', 'snack', 225, 'mixed fruit', 'Combine various fruits in a bowl.'),
                    ('Spicy Roasted Sweet Potatoes', 'snack', 250, 'sweet potatoes, chili powder, olive oil', 'Roast sweet potato cubes with chili powder and olive oil.'),
                    ('Tuna Salad', 'lunch', 350, 'tuna, Greek yogurt, celery, onions', 'Mix tuna with Greek yogurt and chopped vegetables.'),
                    ('Zucchini Fritters', 'snack', 250, 'zucchini, egg, flour, herbs', 'Mix grated zucchini with egg and flour, pan-fry until golden.'),
                    ('Turkey Lettuce Wraps', 'lunch', 400, 'ground turkey, lettuce leaves, hoisin sauce', 'Cook turkey with hoisin sauce, serve in lettuce leaves.'),
                    ('Roasted Brussels Sprouts', 'dinner', 300, 'Brussels sprouts, olive oil, garlic', 'Roast Brussels sprouts with olive oil and garlic.'),
                    ('Edamame and Corn Salad', 'lunch', 350, 'edamame, corn, red bell pepper, lime dressing', 'Mix edamame and corn with bell pepper and lime dressing.'),
                    ('Cucumber and Avocado Sushi', 'dinner', 350, 'cucumber, avocado, sushi rice, nori', 'Prepare sushi rice, roll with cucumber and avocado in nori.'),
                    ('Turkey Meatballs', 'dinner', 400, 'ground turkey, breadcrumbs, egg, spices', 'Mix ingredients, form meatballs, and bake.'),
                    ('Roasted Butternut Squash', 'dinner', 300, 'butternut squash, olive oil, cinnamon', 'Roast squash with olive oil and cinnamon.'),
                    ('Quinoa and Black Bean Stuffed Peppers', 'dinner', 400, 'quinoa, black beans, bell peppers, tomatoes, spices', 'Stuff peppers with quinoa mixture and bake.')
                ]
                cursor.executemany("INSERT INTO meals (name, meal_type, calories, ingredients, recipes) VALUES (%s, %s, %s, %s, %s)", meals_data)
                db.commit()  # Commit the transaction
                print("Data inserted into meals table successfully.")
            else:
                print("meals table already has data.")
        else:
            # If the table does not exist, create it
            cursor.execute("""
                CREATE TABLE meals (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
                    calories INT NOT NULL,
                    ingredients TEXT,
                    recipes TEXT
                )
            """)
            print("meals table created successfully.")
            
            # Insert data into meals table
            meals_data = [
                    ('Oatmeal with Berries', 'breakfast', 300, 'oats, mixed berries, almond milk, honey', 'Cook oats with almond milk and top with berries and honey.'),
                    ('Avocado Toast', 'breakfast', 350, 'whole grain bread, avocado, cherry tomatoes, olive oil', 'Mash avocado on toasted bread and top with sliced tomatoes and olive oil.'),
                    ('Greek Yogurt with Nuts', 'breakfast', 300, 'Greek yogurt, mixed nuts, honey', 'Top Greek yogurt with nuts and a drizzle of honey.'),
                    ('Quinoa Salad', 'lunch', 400, 'quinoa, cucumbers, cherry tomatoes, feta cheese, olives, lemon vinaigrette', 'Mix all ingredients and dress with lemon vinaigrette.'),
                    ('Grilled Chicken Wrap', 'lunch', 450, 'grilled chicken, whole wheat wrap, lettuce, tomatoes, avocado', 'Fill wrap with grilled chicken and veggies, then roll up.'),
                    ('Lentil Soup', 'lunch', 350, 'lentils, carrots, celery, onions, garlic, vegetable broth', 'Cook all ingredients in a pot until lentils are tender.'),
                    ('Baked Salmon', 'dinner', 500, 'salmon fillets, lemon, garlic, herbs', 'Season salmon with garlic and herbs, bake until cooked through.'),
                    ('Stuffed Bell Peppers', 'dinner', 450, 'bell peppers, ground turkey, quinoa, black beans, corn', 'Stuff peppers with turkey mixture and bake until peppers are tender.'),
                    ('Zucchini Noodles with Pesto', 'dinner', 400, 'zucchini, pesto sauce, cherry tomatoes, pine nuts', 'Toss zucchini noodles with pesto and top with tomatoes and pine nuts.'),
                    ('Chia Seed Pudding', 'snack', 225, 'chia seeds, almond milk, vanilla extract, fruit', 'Mix chia seeds with almond milk and vanilla, let sit overnight, then top with fruit.'),
                    ('Apple Slices with Peanut Butter', 'snack', 250, 'apple, peanut butter', 'Slice apple and serve with peanut butter for dipping.'),
                    ('Hummus and Veggies', 'snack', 230, 'hummus, carrots, cucumber, bell peppers', 'Dip veggies in hummus.'),
                    ('Sweet Potato Fries', 'snack', 250, 'sweet potatoes, olive oil, paprika', 'Cut sweet potatoes into fries, toss with oil and paprika, and bake.'),
                    ('Cottage Cheese with Pineapple', 'snack', 225, 'cottage cheese, pineapple', 'Top cottage cheese with pineapple chunks.'),
                    ('Smoothie Bowl', 'breakfast', 350, 'banana, spinach, almond milk, granola, berries', 'Blend banana and spinach with almond milk, top with granola and berries.'),
                    ('Egg White Omelette', 'breakfast', 300, 'egg whites, spinach, mushrooms, tomatoes', 'Cook egg whites with veggies in a non-stick pan.'),
                    ('Chickpea Salad', 'lunch', 400, 'chickpeas, cucumber, tomatoes, red onion, lemon dressing', 'Mix chickpeas and veggies, dress with lemon dressing.'),
                    ('Turkey and Veggie Stir-Fry', 'lunch', 450, 'ground turkey, bell peppers, broccoli, soy sauce', 'Stir-fry turkey and veggies with soy sauce.'),
                    ('Grilled Tofu with Vegetables', 'dinner', 400, 'tofu, bell peppers, broccoli, soy sauce', 'Grill tofu and vegetables with soy sauce.'),
                    ('Cauliflower Rice Bowl', 'dinner', 350, 'cauliflower rice, edamame, carrots, soy sauce', 'Stir-fry cauliflower rice with edamame and carrots, add soy sauce.'),
                    ('Baked Chicken Breast', 'dinner', 400, 'chicken breast, garlic, lemon, rosemary', 'Season chicken and bake until cooked through.'),
                    ('Spaghetti Squash with Marinara', 'dinner', 350, 'spaghetti squash, marinara sauce', 'Roast squash and top with marinara sauce.'),
                    ('Berry Smoothie', 'snack', 250, 'mixed berries, Greek yogurt, almond milk', 'Blend berries with Greek yogurt and almond milk.'),
                    ('Oven-Roasted Chickpeas', 'snack', 230, 'chickpeas, olive oil, spices', 'Toss chickpeas with oil and spices, roast in the oven.'),
                    ('Peach and Almond Salad', 'lunch', 400, 'peach, mixed greens, almonds, balsamic vinaigrette', 'Mix peach slices with greens and almonds, dress with vinaigrette.'),
                    ('Salmon and Asparagus', 'dinner', 450, 'salmon, asparagus, olive oil, lemon', 'Bake salmon and asparagus with olive oil and lemon.'),
                    ('Grilled Portobello Mushrooms', 'dinner', 300, 'portobello mushrooms, balsamic vinegar, garlic', 'Grill mushrooms with balsamic vinegar and garlic.'),
                    ('Black Bean Soup', 'lunch', 350, 'black beans, tomatoes, onions, spices', 'Cook all ingredients until flavors meld.'),
                    ('Egg Salad Lettuce Wraps', 'lunch', 400, 'eggs, Greek yogurt, mustard, lettuce leaves', 'Mix egg salad with Greek yogurt and mustard, serve in lettuce wraps.'),
                    ('Fruit Salad', 'snack', 225, 'mixed fruit', 'Combine various fruits in a bowl.'),
                    ('Spicy Roasted Sweet Potatoes', 'snack', 250, 'sweet potatoes, chili powder, olive oil', 'Roast sweet potato cubes with chili powder and olive oil.'),
                    ('Tuna Salad', 'lunch', 350, 'tuna, Greek yogurt, celery, onions', 'Mix tuna with Greek yogurt and chopped vegetables.'),
                    ('Zucchini Fritters', 'snack', 250, 'zucchini, egg, flour, herbs', 'Mix grated zucchini with egg and flour, pan-fry until golden.'),
                    ('Turkey Lettuce Wraps', 'lunch', 400, 'ground turkey, lettuce leaves, hoisin sauce', 'Cook turkey with hoisin sauce, serve in lettuce leaves.'),
                    ('Roasted Brussels Sprouts', 'dinner', 300, 'Brussels sprouts, olive oil, garlic', 'Roast Brussels sprouts with olive oil and garlic.'),
                    ('Edamame and Corn Salad', 'lunch', 350, 'edamame, corn, red bell pepper, lime dressing', 'Mix edamame and corn with bell pepper and lime dressing.'),
                    ('Cucumber and Avocado Sushi', 'dinner', 350, 'cucumber, avocado, sushi rice, nori', 'Prepare sushi rice, roll with cucumber and avocado in nori.'),
                    ('Turkey Meatballs', 'dinner', 400, 'ground turkey, breadcrumbs, egg, spices', 'Mix ingredients, form meatballs, and bake.'),
                    ('Roasted Butternut Squash', 'dinner', 300, 'butternut squash, olive oil, cinnamon', 'Roast squash with olive oil and cinnamon.'),
                    ('Quinoa and Black Bean Stuffed Peppers', 'dinner', 400, 'quinoa, black beans, bell peppers, tomatoes, spices', 'Stuff peppers with quinoa mixture and bake.')
                ]
            cursor.executemany("INSERT INTO meals (name, meal_type, calories, ingredients, recipes) VALUES (%s, %s, %s, %s, %s)", meals_data)
            db.commit()  # Commit the transaction
            print("Data inserted into meals table successfully.")


        # Check if the meal_plan table exists
        cursor.execute("SHOW TABLES LIKE 'meal_plan'")
        result_meal_plan = cursor.fetchone()

        if result_meal_plan: 
            print("meal_plan table already exists.")
        else: 
            cursor.execute(""" 
                CREATE TABLE meal_plan ( 
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    meal_name VARCHAR(255) NOT NULL,
                    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack') NOT NULL,
                    date DATE NOT NULL,
                    calories INT,
                    ingredients TEXT,
                    recipes TEXT
                )
            """)
            print("meal_plan table created successfully.")


    except mysql.Error as err:
        print(f"Error: {err}")

    finally:
        if db.is_connected():
            cursor.close()
            db.close()

if __name__ == "__main__":
    create_database_and_table()
