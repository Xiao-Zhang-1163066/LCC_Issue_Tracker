INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`)
VALUES 
    -- 20 Visitors
    ('alice_j', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'alice@example.com', 'Alice', 'Johnson', 'Greenwoods Camp', NULL, 'visitor', 'active'),
    ('bob_smith', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'bob@example.com', 'Bob', 'Smith', 'Lakeside Park', NULL, 'visitor', 'active'),
    ('charlie_b', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'charlie@example.com', 'Charlie', 'Brown', 'Highlands Retreat', NULL, 'visitor', 'active'),
    ('diana_m', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'diana@example.com', 'Diana', 'Miller', 'Sunset Valley', NULL, 'visitor', 'active'),
    ('edward_k', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'edward@example.com', 'Edward', 'King', 'Riverbend', NULL, 'visitor', 'active'),
    ('frank_h', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'frank@example.com', 'Frank', 'Harrison', 'Forest Camp', NULL, 'visitor', 'active'),
    ('george_t', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'george@example.com', 'George', 'Taylor', 'Beachview Camp', NULL, 'visitor', 'active'),
    ('hannah_p', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'hannah@example.com', 'Hannah', 'Parker', 'Sunset Camp', NULL, 'visitor', 'inactive'),
    ('ian_d', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'ian@example.com', 'Ian', 'Dawson', 'Mountain Camp', NULL, 'visitor', 'active'),
    ('julia_r', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'julia@example.com', 'Julia', 'Roberts', 'Lakeside Camp', NULL, 'visitor', 'active'),
    ('kevin_l', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'kevin@example.com', 'Kevin', 'Lopez', 'Greenwoods', NULL, 'visitor', 'active'),
    ('lucas_m', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'lucas@example.com', 'Lucas', 'Martinez', 'Sunset Valley', NULL, 'visitor', 'active'),
    ('maria_c', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'maria@example.com', 'Maria', 'Clark', 'Forest Camp', NULL, 'visitor', 'active'),
    ('nathan_s', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'nathan@example.com', 'Nathan', 'Scott', 'Riverbend', NULL, 'visitor', 'active'),
    ('olivia_j', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'olivia@example.com', 'Olivia', 'James', 'Highlands', NULL, 'visitor', 'inactive'),
    ('paul_b', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'paul@example.com', 'Paul', 'Baker', 'Mountain Camp', NULL, 'visitor', 'active'),
    ('quinn_f', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'quinn@example.com', 'Quinn', 'Foster', 'Lakeside', NULL, 'visitor', 'active'),
    ('rachel_g', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'rachel@example.com', 'Rachel', 'Gibson', 'Greenwoods', NULL, 'visitor', 'active'),
    ('steven_h', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'steven@example.com', 'Steven', 'Hall', 'Sunset Camp', NULL, 'visitor', 'active'),
    ('teresa_v', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'teresa@example.com', 'Teresa', 'Vega', 'Beachview', NULL, 'visitor', 'active'),
    
    -- 5 Helpers
    ('helper_1', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'helper1@example.com', 'Ryan', 'Nelson', 'Greenwoods Camp', NULL, 'helper', 'inactive'),
    ('helper_2', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'helper2@example.com', 'Samantha', 'Brooks', 'Lakeside Park', NULL, 'helper', 'active'),
    ('helper_3', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'helper3@example.com', 'Thomas', 'Evans', 'Highlands', NULL, 'helper', 'active'),
    ('helper_4', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'helper4@example.com', 'Emily', 'Carter', 'Sunset Camp', NULL, 'helper', 'active'),
    ('helper_5', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'helper5@example.com', 'Daniel', 'Morris', 'Mountain Camp', NULL, 'helper', 'active'),

    -- 2 Admins
    ('admin_1', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'admin1@example.com', 'Michael', 'Stewart', 'Greenwoods Camp', NULL, 'admin', 'active'),
    ('admin_2', '$2b$12$E5Fj9FX/A8vwK1Q5PYbQKeTygUegWYC4TtU0W8KG2aEPkN4Jt0ofW', 'admin2@example.com', 'Sarah', 'Wright', 'Lakeside Park', NULL, 'admin', 'active');

    
INSERT INTO `issues` (`user_id`, `summary`, `description`, `issue_status`, `created_at`)
VALUES 
    (1, 'Broken Picnic Table', 'The table near the entrance is missing a leg.', 'new', '2025-01-05 10:30:00'),
    (2, 'Blocked Toilet', 'Toilet near campsite #5 is overflowing.', 'new', '2025-01-07 14:45:00'),
    (3, 'Wi-Fi Not Working', 'No Wi-Fi at the visitor center.', 'open', '2025-01-10 09:15:00'),
    (4, 'No Hot Water in Showers', 'Only cold water is available.', 'stalled', '2025-01-12 16:20:00'),
    (5, 'Full Trash Bins', 'Bins near the playground are overflowing.', 'open', '2025-01-15 11:00:00'),
    (6, 'Tent Rental Issue', 'The tent I rented has holes.', 'resolved', '2025-01-18 13:10:00'),
    (7, 'BBQ Grill Not Working', 'The grill near the lake is broken.', 'new', '2025-01-20 17:30:00'),
    (8, 'Low Water Pressure', 'Water taps near site #10 barely work.', 'open', '2025-01-22 08:45:00'),
    (9, 'Wild Animals Spotted', 'A raccoon is getting into campers’ food.', 'new', '2025-01-25 19:00:00'),
    (10, 'Streetlight Flickering', 'Light near the BBQ area is flickering.', 'new', '2025-01-28 20:15:00'),
    (11, 'Dirty Bathrooms', 'Bathrooms haven’t been cleaned today.', 'open', '2025-02-01 12:25:00'),
    (12, 'Loud Music at Night', 'People playing loud music past quiet hours.', 'resolved', '2025-02-03 22:30:00'),
    (13, 'Campfire Restrictions', 'Unclear if campfires are allowed.', 'new', '2025-02-05 07:50:00'),
    (14, 'Leaking Water Faucet', 'Dripping water at site #15.', 'new', '2025-02-08 18:40:00'),
    (15, 'Power Outage', 'No electricity at RV section.', 'stalled', '2025-02-10 21:55:00'),
    (16, 'Broken Swing Set', 'A swing at the playground is damaged.', 'resolved', '2025-02-12 10:05:00'),
    (17, 'Campsite Overbooked', 'I booked site #3, but someone is already there.', 'open', '2025-02-15 15:20:00'),
    (18, 'No Maps Available', 'The main office ran out of park maps.', 'new', '2025-02-18 09:35:00'),
    (19, 'Mudslide Blocking Trail', 'The main hiking trail is blocked by mud.', 'stalled', '2025-02-20 14:50:00'),
    (20, 'Lack of Firewood', 'No firewood left in the camp store.', 'resolved', '2025-02-25 16:00:00');

INSERT INTO `comments` (`issue_id`, `user_id`, `content`, `created_at`)
VALUES 
    (2, 3, 'I checked the toilet, definitely needs fixing.', '2025-01-07 15:00:00'),
    (2, 4, 'Maintenance will fix it tomorrow.', '2025-01-07 16:30:00'),
    (3, 5, 'Wi-Fi issue affects the entire campground.', '2025-01-10 10:00:00'),
    (3, 6, 'Router restarted, should be working now.', '2025-01-10 11:15:00'),
    (4, 7, 'Plumber scheduled for tonight.', '2025-01-12 17:00:00'),
    (5, 8, 'Trash pickup is tomorrow morning.', '2025-01-15 12:00:00'),
    (7, 9, 'Park staff notified about BBQ issue.', '2025-01-20 18:00:00'),
    (10, 10, 'Electrician coming tomorrow.', '2025-01-28 21:00:00'),
    (11, 11, 'Bathrooms were cleaned at noon.', '2025-02-01 13:00:00'),
    (12, 12, 'Park rangers warned the noisy campers.', '2025-02-03 23:00:00'),
    (13, 13, 'Campfires are allowed in designated areas.', '2025-02-05 08:30:00'),
    (15, 14, 'Power issue reported to electric company.', '2025-02-10 22:30:00'),
    (16, 15, 'Swing set repair is scheduled.', '2025-02-12 11:00:00'),
    (17, 16, 'Please contact the front desk for booking issues.', '2025-02-15 16:00:00'),
    (18, 17, 'More maps will arrive tomorrow.', '2025-02-18 10:00:00'),
    (19, 18, 'Trail maintenance crew notified.', '2025-02-20 15:30:00'),
    (20, 19, 'Firewood will be restocked by evening.', '2025-02-25 17:30:00');