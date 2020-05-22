# Stem-IAA Portal

The Stem-IAA Portal was created to provide a way for students, instructors, and mentors to interact in various ways over the duration of a course. It is meant to supplement an Education Management System, rather than replace it. Importantly, however, mentors of the course do not have access to the EMS, and thus features are provided in the portal to counteract this.

The following topics are discussed in this documentation:

- [Portal setup](#portal-setup)
- [Portal usage guide](#portal-usage)
- [Flask/static hosting information](#hosting-information)
- [Virtual machine information](#virtual-machines)
- [Supplementary scripts](#supplementary-scripts)


## Portal Setup

Before running, create a new file `config.json` in the root directory for the project. In this file, provide the following information:

- "secret": A complex random value sent to the flask app for cryptography.
- "SQLALCHEMY_DATABASE_URI": The URI pointing to the database to use for the portal. Example: `sqlite:///worm.db`
- "azure": A new dictionary with the following values found in the azure account:
    - "client_id"
    - "secret"
    - "tenant"
    - "subscription_id"

Then, launch the portal via:
```
export FLASK_APP=app.py
flask run --host=0.0.0.0
```

## Portal Usage

Pre-login, the portal serves a single static page describing the content of the course. In future courses, this page and simply be swapped for a page describing a different course. The same login button should be kept, however, which allows students/mentors/instructors to login to their accounts. The initial administrator account can be initialized via the [create admin script](util/create_admin.py). Subsequent accounts can be created on the /register page. This is intended to be performed ahead of time by an administrator; there is no way to create an account without an administrator account, and as such students can not create their own accounts.

After logging in, the user is taken to their `Profile` page. The profile is visible to all other users in their cohort. Visible elements on a profile can be changed by clicking the `Edit` button at the top right, changing the content, and then clicking `Save`. In edit mode, the profile picture can be changed by clicking on it. The `Content` section is intended to be used by students to demonstrate the projects they are creating from the course. However, the content page exists on mentor and instructor accounts as well, in case there are other reasons to use it. To view other profiles, use the search feature in the navbar.

Information set during account creation can also be changed via the username dropdown -> Account option. The settings available to set will change depending on the type of account (student/mentor/instructor). For example, students don't have permission to change their username after it's been assigned. If a locked setting needs to be changed, an administrator can navigate to the student/mentor's profile and click the `Settings` button for the profile at the top right.
 
 The `Course Information` page can be accessed at the top right of the profile page, or in the username dropdown menu. This page is intended for students to view information about the course, such as the login for the EMS, login and hosting information for the applications and static content, and contact information for their instructors/TAs/mentors. Additionally, the page allows students to launch and connect to their virtual machines used for course work. Software downloads are also listed for students working on their own machines locally. These first three pages are the only ones that concern students.
 
 The `Solutions` page allows for instructors to post solutions to coursework and mentors to view the solutions. The posted solutions are protected by account role, and are not viewable by students. If logged into a mentor or instructor account, the solutions page can be viewed via the username dropdown -> Solutions. Solutions are categorized by the cohort they belong to. Solutions are read only for mentors, and read/write for instructors. If logged into an instructor account, a new solution can be added at the top by typing the name of the solution and clicking `Create`. Within a solution, the description for the assignment can be provided and any corresponding source code files can be attached. When viewing the solution, the file can be clicked and a syntax-highlighted preview will display. The file can also be downloaded. Solutions can be removed by instructors by clicking `Delete` in the solutions page for a cohort.
 
 The `Administration` page (username dropdown -> Administration) provides two features: registering new users and managing cohorts.
 
 New users are added in the user registration page. An instructor account must navigate to this page and fill out the information, choose the role, and click `Register User`. There currently is a bug where the role must be pressed each time after adding a user, even if the role appears to be selected. A list of mentors/mentees can be provided at the time of registration, though this can also be added after all of the accounts are set up in each of the user's settings pages.
 
 There is currently no way to delete a user via the interface. This can be done via SQLAlchemy relatively easily, however. For example (relative to the project root directory):
 
 ```python
from model.User import db, User
to_remove = User.query.filter_by(username="sam").first()
db.session.delete(to_remove)
db.session.commit()
```
 
 Cohorts can be added/deleted/managed via the `Manage cohorts` button on the `Administration` page. Existing cohorts are displayed on this page, and can be renamed or deleted. Additionally, an `Is Active` toggle allows a cohort to be removed from view so as to not clutter pages that would otherwise show every enrolled cohort. It is still possible for users to view old cohort information with this toggle checked. A new cohort can be added by typing in a name and clicking `Create` at the top. After clicking on a cohort after it has been created, a page is shown which allows the specific cohort to be managed. On this screen, new users can be added and removed from a cohort. To add a user, start typing their name/username and click it from the autocompleted list. To remove a user, click the x at the top right of their profile picture.
 
 Lastly, the user can logout of their account via the username dropdown -> Logout feature.
 
 
 ## Hosting Information
 
 Several technologies were used to setup the hosting service for students. The goal was to provide each student with a custom domain name associated with their username, such as `sam.w3.stem-iaa.org` for static content, and `sam.flask.stem-iaa.org` for flask specific content, which was the web application framework taught in the course. 
 
 To accomplish this, [openresty](https://openresty.org/en/) (from [nginx](https://www.nginx.com/)) and [uwsgi](https://uwsgi-docs.readthedocs.io/en/latest/) were used. Both of these libraries should be installed on the server machine.
 
 Openresty was chosen over a standard version of nginx due to the added ability to write lua in routing network traffic. This is how the custom URLs were created from the student usernames. The nginx scripts to accomplish this can be found in the [nginx_sites folder of the worm Github repo](https://github.com/stem-iaa/worm/tree/master/nginx_sites). Additionally, custom landing pages were created from each of the routes. The landing pages can be found [here](https://github.com/stem-iaa/worm/tree/master/worm_html).
 
 The nginx setup assumes a uwsgi ini file is created for each user. This has been automated by creating .ini files when a new user is added to the hosting server. The `/usr/local/sbin/adduser.local` was updated to execute the [create_w3.py](https://github.com/stem-iaa/worm/blob/master/create_w3.py) script, which generates ini files for each user in the `w3` group. This script can also be run manually after adding all the users.
 
 For reference, an example of a auto-generated .ini script for a hosted user looks like the following:
 
 ```
[uwsgi]
socket = /tmp/flask_socks/sam.sock
pythonpath = python3
callable = app
vhost = true
py-autoreload = 3
plugins = python3
manage-script-name = true
chdir = /home/sam/www/flask
mount = /=app.py
touch-reload = /home/sam/www/flask_reload
module = app
```
 
The `touch-reload` parameter is enabled so that students can have multiple different flask applications in their www directory in their home folder, and switch the `flask` symlink to the one they want to host at any given time. After doing this, they can execute `touch flask_reload` to have the change be updated on the hosting server. `py-autoreload` is enabled so that they do not have to touch reload when making changes to their existing flask app.
 
 If hosting the portal with nginx/uwsgi, a very similar script as the previous can be created depending on the system-dependent locations. The .ini used for our hosting is provided [here](https://github.com/stem-iaa/worm/blob/master/portal.ini).
 
 ## Virtual Machines
 
 
 ## Supplementary Scripts
 