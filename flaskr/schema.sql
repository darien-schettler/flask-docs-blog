-- If the user or post table exists than delete it
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
 
-- Command to create the user table
	-- id (PRIMARY KEY) 	--> 	autoincremented integer
	-- username 			--> 	unique string required
	-- password 			--> 	string required
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

-- Command to create the post table
	-- id (PRIMARY KEY) 		--> 	autoincremented integer
	-- author_id (FOREIGN KEY) 	--> 	integer required
	-- created		 			--> 	timestamp (has default value) required
	-- title					--> 	string required
	-- body						--> 	string required
CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);