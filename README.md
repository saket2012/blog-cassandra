# Blog-Scaling

1) Install the dependencies by using following command<br />
pip3 install -r requirements.txt<br />

2) To install foreman type following command<br />
On MacOS:<br />
npm install foreman<br />
On Ubuntu:<br />
sudo apt install --yes ruby-foreman<br />

3) Start the application by typing following commands<br />
For some reasons, database is not getting created using foreman
So, please run the command python3 users.py
Terminate the process.
and the run following command
foreman start user=3,article=3,tag=3,comment=3,feed=1<br />

4)Use the curl commands given in curl_commands.txt<br />

5)To run the tests, type following commands<br />
For users and articles:<br />
py.test test_user.tavern.yaml -v<br />
For tags:<br />
py.test test_tag.tavern.yaml -v<br />
For comments:<br />
py.test test_comments.tavern.yaml -v
