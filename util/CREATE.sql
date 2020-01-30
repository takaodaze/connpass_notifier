CREATE TABLE events(
	event_name varchar(100),
	event_date date,
	event_url varchar(300),
	img_url varchar(300),
	prefectures varchar(20),
	domain varchar(20)
);

CREATE TABLE users(
	user_id VARCHAR(255),
	display_name VARCHAR(30)
);