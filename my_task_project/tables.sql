CREATE TABLE user_info (
	user_id SERIAL PRIMARY KEY,
	user_name VARCHAR(255) NOT NULL,
	user_surname VARCHAR(255) NOT NULL,
	user_email VARCHAR(255) NOT NULL,
	user_password_hash VARCHAR(255) NOT NULL,
	user_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE task_info (
	task_id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    task_description VARCHAR(255),
    id_owner INT NOT NULL,
    task_importance VARCHAR(255),
    task_urgency VARCHAR(255),
    task_status VARCHAR(255) NOT NULL,
    task_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    task_deadline TIMESTAMP,
    task_avatar_url VARCHAR(255)
);

ALTER TABLE task_info ADD FOREIGN KEY (id_owner) REFERENCES user_info(user_id);

CREATE TABLE comment_info (
	id SERIAL PRIMARY KEY,
	comment_text TEXT NOT NULL,
	owner_id INT NOT NULL,
	task_id INT NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

ALTER TABLE comment_info ADD FOREIGN KEY (owner_id) REFERENCES user_info(user_id);
ALTER TABLE comment_info ADD FOREIGN KEY (task_id) REFERENCES task_info(task_id);