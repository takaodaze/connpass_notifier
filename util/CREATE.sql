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


SELECT event_name,event_date,insert_date
        FROM events
        WHERE insert_date BETWEEN '2020-02-01' AND '2020-02-05'
        AND event_date >= '2020-02-05'
        ORDER BY event_date ASC
        LIMIT 50