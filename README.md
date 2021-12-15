# School Club Information Manager (SCIM)

The School Club Information Manager is an application that aims to address the problem that many parents find it difficult to find timely and sufficient information about school clubs, and that it is potentially time consuming or difficult for schools to share this information. It provides easy to use interfaces to add and update clubs to the system, which are then displayed in two formats on a "parent/public" page: Timetable view and Detailed Cards view. 

The application is built using Python with a Flask framework, and uses Flask Assets to integrate Sass(Scss) to facilitate development. 
Jinja2 templates are used to create dynamic webpages, and a few front end issues are solved using JavaScript. It uses SQLAlchemy to manage the database, and WTForms to facilitate the creation of web forms.

## Core functionality
The admin side currently allows users to 
- manage admin users 
  - register
  - login
  - logout
  -  edit details 
  -  delete users 
  -  (further restrictions and facilities to be implemented)
- setup (and edit) manager for school specific details, including:
  - school name 
  - logo
  - colour of public banner
  - available year groups
  - future implementation should allow filter categories
- create club form
- edit club form
- list clubs
- view single clubs
- delete club form
- manage info on club staff

*Note - This is **only** an information sharing system, not a system to handle bookings. Its aim is to help schools more effectively share information about the clubs, and for parents (and school kids) to more easily access information about available clubs.*

## Admin side interfaces 
To give an idea of what to expect, here is a selection of Admin side interfaces.

User registration and login interfaces are included. *Further improvements are required, such as adding user roles and implementing the "forget password" functionality.*
![image](https://user-images.githubusercontent.com/20923607/146198460-91aacc59-d239-45f6-9bf8-abfc24723aba.png)

School setup pages allow a school to customise the look of the parent side with school name, font, logo and colour of banner and font. Future improvements should include a third step - set up filter categories (for instance, type of club, free or paid, days, etc).

*School setup page - step 1*
![image](https://user-images.githubusercontent.com/20923607/146198958-0f6257ed-6a05-4b9a-bfee-9345ee549b04.png)

*School setup page - step 2*
![image](https://user-images.githubusercontent.com/20923607/146199109-d9f4124b-0dad-466a-9c23-d3785e84c2d2.png)

An overview page gives admin users a snapshot of their club setting and offers, showing what the banner will look like in parent side, stating the number of clubs on offer and provides a link to the parent side.
![image](https://user-images.githubusercontent.com/20923607/146199421-7044407c-5a22-4d09-bad8-3c7c9f1399cc.png)

"List users" gives admin an overview of all users, and links to delete individual users (pop up warnings requireing a confirmation of the action help users avoid accidentally deleting users). 
![image](https://user-images.githubusercontent.com/20923607/146200168-46760fbd-4315-4763-a117-89a5c5e03901.png)

A form to create new clubs with descriptive fields aiming to guide an admin user through the process of adding new club information. The fields have been chosen based on surveys of parents on what they and their children would like to know about school clubs. Existing clubs can be edited using the same form (then has "Edit club details" as heading), which is then pre-filled with all existing information to make updates easier.
![image](https://user-images.githubusercontent.com/20923607/146200846-2180e729-d6e8-4433-8020-8825fa057e1d.png)

Clubs are not automatically published when created. Under "List clubs" each club can be accessed by clicking on its name, and there is a button to publish or unpublish a club to the parent page (unpblished clubs are still in the system, they are just not visible to the public). There are also three inactive "status" buttons for each club, ready for implementing a feature to set the current status of the club (running, cancelled, holiday).
![image](https://user-images.githubusercontent.com/20923607/146201222-231b789e-6cb2-459d-a3d6-abdba79e1917.png)

As the club forms also includes information about the people and companies running the clubs, these specific bits of information can also be updated outside of the club info, as a single person or company may run more than one club.
![image](https://user-images.githubusercontent.com/20923607/146201800-05791e17-c900-4247-8c70-96c3cfc22d7c.png)

These interfaces are responsive and can be viewed on most screen sizes (though based on interviews and research into the domain, the admin side is assumed to be used primarily on desktop/laptop computers).

A few examples of the admin side mobile view interfaces:
<img width="697" alt="Screenshot 2021-12-15 at 14 16 14" src="https://user-images.githubusercontent.com/20923607/146202675-3d69240d-9125-48c4-aea5-d9ac44dd8a6c.png">

<img width="697" alt="Screenshot 2021-12-15 at 14 16 38" src="https://user-images.githubusercontent.com/20923607/146202728-bbf8acdf-2426-41e9-994b-9adf3a60eebc.png">

# Parent side interfaces
The "Details" page shows detailed cards (taking inspiration from "Top Trumps" cards well known to children) with all the information about each clubs presented in an easy-to-read format. Future filter and sorting facilities will make the parent pages better for schools with a large number of clubs.
![image](https://user-images.githubusercontent.com/20923607/146203118-f8c69015-ca2f-4191-a3e0-d9d877f22567.png)

*Clicking on any card makes it pop up and stand out, and makes all fonts etc larger and easier to see*
![image](https://user-images.githubusercontent.com/20923607/146203319-b8bf61b7-4f28-4170-916a-f4c3e7ce3fed.png)

The timetable view shows when all the clubs are on, and provides only a minimum of information about each club. Clicking on a club card in the timetable view should bring up a large detailed popup card as on the Details tab/page.
![image](https://user-images.githubusercontent.com/20923607/146203606-4ff522f1-d213-4800-ab1b-da95b1642167.png)

*Extract of timetable to show the cards and their information more clearly*
![image](https://user-images.githubusercontent.com/20923607/146203724-1ef92a3c-6725-4f40-814e-1eadac439d5c.png)







