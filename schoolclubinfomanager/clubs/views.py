from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from sorted_months_weekdays import Weekday_Sorted_Week
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup, Club, ClubDay, ClubYearGroup, ContactToBook, StaffClub, StaffMember, ExternalCompany
from schoolclubinfomanager.clubs.forms import CreateClub, Publish, DeleteClub, EditStaffDetails, EditCompanyDetails
from schoolclubinfomanager.clubs.picture_handler import add_photo
import datetime
import sys

clubs = Blueprint('clubs', __name__)

# CREATE NEW CLUB
@clubs.route('/create_club', methods=['GET', 'POST'])
@login_required
def create_club():
    form = CreateClub()
    school = School.query.first()
    # for validating datepickers:
    today = datetime.date.today()
    one_year = str(today)
    one_year = one_year[:3] + str(int(one_year[3]) + 1) + one_year[4:]
    #one_year = ''.join(one_year)
    #one_year = str(datetime.datetime.now())[:10]
    #one_year = one_year[:3] + str(int(one_year[3]) + 1) + one_year[4:10]
    teachers = [contact.teacher_name for contact in ContactToBook.query.all()]
    emails = [contact.email for contact in ContactToBook.query.all()]
    phone_numbers = [contact.call for contact in ContactToBook.query.all()]

    staff_list = StaffMember.query.all()
    company_list = ExternalCompany.query.all()

    if form.validate_on_submit():


        '''name = form.name.data
        start_date = form.start_date.data
        end_date = form.end_date.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        location = form.location.data
        at_school = form.at_school_premises.data
        off_school = form.off_school_premises.data
        days = form.days.data
        ygs = form.year_groups.data
        exp = form.experience.data
        outfit = form.outfit.data
        equipment = form.equipment.data
        num_places = form.num_places.data
        book = form.book.data
        teacher = form.teacher.data
        email = form.email.data
        call = form.call.data
        is_free = form.is_free.data
        cost = form.cost.data
        photo = form.photo.data
        description = form.description.data
        new_entry = form.new_entry.data
        type = form.type_of_staff.data
        staff_name = form.staff_name.data
        staff_email = form.staff_email.data
        staff_description = form.staff_description.data
        comp_name = form.company_name.data
        comp_email = form.company_email.data
        comp_des = form.company_description.data
        comp_web = form.company_website.data
        in_system = form.existing_clubrunner.data
        staff = form.staff.data
        companies = form.companies.data

        #, name=name,photo=photo, pic=pic,
        #

        #
        return render_template('admin/test.html', school=school, name=name, start_date=start_date, end_date=end_date,
                                                  start_time=start_time, end_time=end_time, at_school=at_school,
                                                  location=location, off_school=off_school, days=days, exp=exp,
                                                  outfit=outfit, equipment=equipment, ygs=ygs, num_places=num_places,
                                                  book=book, teacher=teacher, call=call, email=email, is_free=is_free,
                                                  cost=cost, photo=photo, description=description, type=type,
                                                  new_entry=new_entry, staff_description=staff_description,
                                                  staff_name=staff_name, staff_email=staff_email, comp_web=comp_web,
                                                  comp_des=comp_des, comp_email=comp_email, comp_name=comp_name,
                                                  staff=staff, companies=companies, in_system=in_system)
    return (render_template('admin/club_form.html', form=form, title="Create", school=school, teachers=teachers,
                                                    emails=emails, phone_numbers=phone_numbers))'''#, today=today, one_year=one_year

        # SAVE PHOTO
        if form.photo.data: #if they actually uploaded a photo
            club_name = form.name.data
            club_name = club_name.replace(' ', '') + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')[-6:]

            pic = add_photo(form.photo.data, club_name)

        else:
            pic = None



        location = form.location.data
        if location == 'at_school':
            at_school = True
            location = form.at_school_premises.data
        else:
            at_school = False
            location = form.off_school_premises.data

        is_free = (form.is_free.data == "free")
        cost = form.cost.data

        '''if free_boolean == 'free':
            is_free = True
            cost = free_boolean#None
        else:
            is_free = False
            cost = form.cost.data'''


        drop_in = form.book.data == 'drop_in'


        num_places = form.num_places.data

        club = Club(name = form.name.data,
                    start_date = form.start_date.data,
                    end_date = form.end_date.data,
                    start_time = form.start_time.data,
                    end_time = form.end_time.data,
                    location = location,
                    at_school = at_school,
                    is_free = is_free,
                    num_of_places = num_places,
                    drop_in = drop_in
                    )

        db.session.add(club)
        db.session.commit()

        #update database with days
        days = form.days.data
        for d in days:
            day = ClubDay(d, club.id)
            db.session.add(day)
        db.session.commit()

        #update database with year groups
        year_groups = form.year_groups.data
        for group in year_groups:
            yg = ClubYearGroup(group, club.id)
            db.session.add(yg)
        db.session.commit()

        booking_details_exist = False

        # CONTACT TO BOOK
        if not drop_in: # checks radio button for choosing how to book
            if form.book.data == 'teacher':
                teacher_name = form.teacher.data
                if bool(ContactToBook.query.filter_by(teacher_name=teacher_name).first()):
                    #name already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(teacher_name=teacher_name).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                teacher_name = None

            if form.book.data == 'email':
                email = form.email.data
                if bool(ContactToBook.query.filter_by(email=email).first()):
                    #email already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(email=email).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                email = None

            if form.book.data =='call':
                call = form.call.data
                if bool(ContactToBook.query.filter_by(call=call).first()):
                    #number already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(call=call).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                call = None

            if not booking_details_exist:
                #new entry, create new object/row
                contact = ContactToBook(teacher_name = teacher_name,
                                        email = email,
                                        call = call)

                db.session.add(contact)
                db.session.commit()
                club.contact_to_book_id = contact.id
                db.session.commit()

        # Add data about StaffMember or ExternalCompany
        if form.new_entry.data == 'new':
            # New entry to system, add to database
            if form.type_of_staff.data == 'person':
                staff_member = StaffMember(name = form.staff_name.data,
                                           email = form.staff_email.data,
                                           description = form.staff_description.data)
                db.session.add(staff_member)
                db.session.commit()

                staff_club = StaffClub(club_id = club.id,
                                       staffmember_id = staff_member.id)

                db.session.add(staff_club)
                db.session.commit()

            else:
                #company
                company = ExternalCompany(name = form.company_name.data,
                                          website = form.company_website.data,
                                          email = form.company_email.data,
                                          description = form.company_description.data)

                db.session.add(company)
                db.session.commit()

                club.ext_company_id = company.id
                db.session.commit()

        else:
            # Staff or company exists in system, link to clubs
            if form.existing_clubrunner.data == 'existing_staff':
                #staff
                staff_member = form.staff.data
                staff_member = StaffMember.query.filter_by(name=staff_member).first()
                staff_club = StaffClub(club_id = club.id,
                                     staffmember_id = staff_member.id)

                db.session.add(staff_club)
                db.session.commit()
            else:
                #company
                company = form.companies.data
                company = ExternalCompany.query.filter_by(name=company).first()
                club.ext_company_id = company.id
                db.session.commit()


        # ALL CLUB INFO NOT COMPULSORY
        club.experience = form.experience.data
        club.outfit = form.outfit.data
        club.equipment = form.equipment.data
        club.description = form.description.data
        club.photo = pic
        club.cost = cost

        db.session.commit()
        return redirect(url_for('clubs.club', club_id=club.id))
    return (render_template('admin/club_form.html', form=form, title="Create", school=school, today=today, one_year=one_year, teachers=teachers, emails=emails, phone_numbers=phone_numbers, staff_list=staff_list, company_list=company_list))

# EDIT CLUB
@clubs.route('/edit_club/<club_id>', methods=['GET', 'POST'])
@login_required
def edit_club(club_id):
    form = CreateClub()
    school = School.query.first()
    club = Club.query.filter_by(id=club_id).first()
    contact_to_book = ContactToBook.query.filter_by(id=club.contact_to_book_id).first()
    sc = StaffClub.query.filter_by(club_id=club.id).first()

    # for updating the days and year groups (so previously checked days that have been unchecked now are removed)
    existing_days = ClubDay.query.filter_by(club_id=club.id).all()
    existing_days = {day.name for day in existing_days}

    existing_ygs = ClubYearGroup.query.filter_by(club_id=club.id).all()
    existing_ygs = {yg.name for yg in existing_ygs}

    # for validating datepickers:
    start_date = club.start_date
    one_year = str(start_date)
    one_year = one_year[:3] + str(int(one_year[3]) + 1) + one_year[4:10]

    # existing contacts
    teachers = [contact.teacher_name for contact in ContactToBook.query.all()]
    emails = [contact.email for contact in ContactToBook.query.all()]
    phone_numbers = [contact.call for contact in ContactToBook.query.all()]

    staff_list = StaffMember.query.all()
    company_list = ExternalCompany.query.all()

    # variables needed in some cases
    sm = None
    comp = None
    start_d = None
    end_d = None
    start_t = None
    end_t = None


    #school = School.query.first()
    if form.validate_on_submit():

        # SAVE PHOTO
        if form.photo.data: #if they actually uploaded a photo
            club_name = form.name.data
            club_name = club_name.replace(' ', '') + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')[-6:]

            club.photo = add_photo(form.photo.data, club_name) # old picture is still in the system - decide if you want to delete it?


        location = form.location.data
        if location == 'at_school':
            at_school = True
            location = form.at_school_premises.data
        else:
            at_school = False
            location = form.off_school_premises.data

        free_boolean = form.is_free.data
        if free_boolean == 'free':
            is_free = True
            cost = None
        else:
            is_free = False
            cost = form.cost.data

        drop_in = form.book.data == 'drop_in'


        num_places = form.num_places.data

        club.name = form.name.data
        club.start_date = form.start_date.data
        club.end_date = form.end_date.data
        club.start_time = form.start_time.data
        club.end_time = form.end_time.data
        club.location = location
        club.at_school = at_school
        club.is_free = is_free
        club.num_of_places = num_places
        club.drop_in = drop_in

        db.session.commit()

        #update database with days
        new_days = set(form.days.data)
        for d in new_days:
            if d not in existing_days:
                day = ClubDay(d, club.id)
                db.session.add(day)

        to_delete = existing_days - new_days
        if to_delete:
            for d in to_delete:
                temp = ClubDay.query.filter_by(name=d, club_id=club.id).first()
                db.session.delete(temp)
        db.session.commit()

        #update database with year groups
        '''to_delete = ClubYearGroup.query.filter_by(club_id=club.id).all()
        for yg in to_delete:
            db.session.delete(yg)'''

        new_year_groups = set(form.year_groups.data)
        for group in new_year_groups:
            if group not in existing_ygs:
                yg = ClubYearGroup(group, club.id)
                db.session.add(yg)

        to_delete = existing_ygs - new_year_groups
        if to_delete:
            for yg in to_delete:
                temp = ClubYearGroup.query.filter_by(name=yg, club_id=club.id).first()
                db.session.delete(temp)

        db.session.commit()

        booking_details_exist = False

        # CONTACT TO BOOK
        if not drop_in: # checks radio button for choosing how to book
            if form.book.data == 'teacher':
                teacher_name = form.teacher.data
                if bool(ContactToBook.query.filter_by(teacher_name=teacher_name).first()):
                    #name already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(teacher_name=teacher_name).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                teacher_name = None

            if form.book.data == 'email':
                email = form.email.data
                if bool(ContactToBook.query.filter_by(email=email).first()):
                    #email already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(email=email).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                email = None

            if form.book.data =='call':
                call = form.call.data
                if bool(ContactToBook.query.filter_by(call=call).first()):
                    #number already exists in the system, just link to club
                    booking_details_exist = True
                    contact = ContactToBook.query.filter_by(call=call).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                call = None

            if not booking_details_exist:
                #new entry, create new object/row
                contact = ContactToBook(teacher_name = teacher_name,
                                        email = email,
                                        call = call)

                db.session.add(contact)
                db.session.commit()
                club.contact_to_book_id = contact.id
                db.session.commit()

        # Add data about StaffMember or ExternalCompany
        if form.new_entry.data == 'new':
            # New entry to system, add to database
            if form.type_of_staff.data == 'person':
                staff_member = StaffMember(name = form.staff_name.data,
                                           email = form.staff_email.data,
                                           description = form.staff_description.data)
                db.session.add(staff_member)
                db.session.commit()

                staff_club = StaffClub(club_id = club.id,
                                       staffmember_id = staff_member.id)

                db.session.add(staff_club)
                db.session.commit()

            else:
                #company
                company = ExternalCompany(name = form.company_name.data,
                                          website = form.company_website.data,
                                          email = form.company_email.data,
                                          description = form.company_description.data)

                db.session.add(company)
                db.session.commit()

                club.ext_company_id = company.id
                db.session.commit()

        else:
            # Staff or company exists in system, link to clubs

            # check if club has existing staff member to change
            existing_sc = StaffClub.query.filter_by(club_id=club.id).first()
            if form.existing_clubrunner.data == 'existing_staff':
                #staff
                staff_member = form.staff.data

                staff_member = StaffMember.query.filter_by(name=staff_member).first()
                club.ext_company_id = None #make sure club is only linked to staff or a company, not both

                if existing_sc:
                    existing_sc.staffmember_id = staff_member.id
                else:
                    if staff_member:#FIX THIS -- SOME VALIDATION TO ENSURE REMOVED STAFF ARE NOT STILL LINKED TO CLUBS!
                        staff_club = StaffClub(club_id = club.id,
                                           staffmember_id = staff_member.id)

                        db.session.add(staff_club)
                db.session.commit()
            else:
                #company
                if existing_sc:
                    #make sure club is only linked to staff or a company, not both
                    db.session.delete(existing_sc)
                company = form.companies.data
                company = ExternalCompany.query.filter_by(name=company).first()
                club.ext_company_id = company.id
                db.session.commit()


        # ALL CLUB INFO NOT COMPULSORY
        club.experience = form.experience.data
        club.outfit = form.outfit.data
        club.equipment = form.equipment.data
        club.description = form.description.data

        db.session.commit()
        return redirect(url_for('clubs.club', club_id=club.id))
    elif request.method == "GET":
        # they are not yet submitting, they want to see the form, so we grab the current details and populate the form
        form.name.data = club.name
        start_d = club.start_date.date()
        end_d = club.end_date.date()
        start_t = club.start_time #consider adding these to html tag as value? Will be today and one_year for create club
        end_t = club.end_time #consider adding these to html tag as value? Will be today and one_year for create club
        if club.at_school:
            form.at_school_premises.data = club.location
        else:
            form.off_school_premises.data = club.location
        form.days.data = existing_days
        form.year_groups.data = existing_ygs
        form.experience.data = club.experience
        form.equipment.data = club.equipment
        form.outfit.data = club.outfit
        form.num_places.data = club.num_of_places
        if contact_to_book:
            if contact_to_book.teacher_name:
                form.teacher.data = contact_to_book.teacher_name
            elif contact_to_book.email:
                form.email.data = contact_to_book.email
            elif contact_to_book.call:
                form.call.data = contact_to_book.call
        form.cost.data = club.cost
        form.description.data = club.description
        '''if sc:
            staffmember = StaffMember.query.filter_by(id=sc.staffmember_id).first()
            form.staff.data = staffmember.name
        if club.ext_company_id:
            company = ExternalCompany.query.filter_by(id = club.ext_company_id).first()
            form.companies.data = company.name'''

        if sc:
            staffmember = StaffMember.query.filter_by(id=sc.staffmember_id).first()
            sm = staffmember.name

        if club.ext_company_id:
            company = ExternalCompany.query.filter_by(id = club.ext_company_id).first()
            comp = company.name





    return (render_template('admin/club_form.html', form=form, title="Edit",
                                school=school, today=start_date, one_year=one_year,
                                teachers=teachers, emails=emails, phone_numbers=phone_numbers,
                                club=club, contact_to_book=contact_to_book,
                                staff_list=staff_list, company_list=company_list,
                                sm=sm, comp=comp, start_d=start_d, end_d=end_d, start_t=start_t,
                                end_t=end_t))



# SINGLE CLUB OVERVIEW
@clubs.route('/club/<club_id>', methods=['GET', 'POST'])
@login_required
def club(club_id):
    school= School.query.first()
    club = Club.query.filter_by(id=club_id).first()
    days = ClubDay.query.filter_by(club_id=club.id).all()
    ygs = ClubYearGroup.query.filter_by(club_id=club.id).all()
    sc = StaffClub.query.filter_by(club_id=club.id).first()
    book = ContactToBook.query.filter_by(id=club.contact_to_book_id).first()
    form = DeleteClub()
    if sc:
        # club is run by individual staff and not a company. (should I check for all instead of first?)
        staff_member = StaffMember.query.filter_by(id=sc.staffmember_id).first()
    else:
        staff_member = None
    if club.ext_company_id:
        ext_c = ExternalCompany.query.filter_by(id=club.ext_company_id).first()
    else:
        ext_c = None

    if form.validate_on_submit():
        for yg in ygs:
            db.session.delete(yg)

        for day in days:
            db.session.delete(day)

        if sc:
            db.session.delete(sc)

        db.session.delete(club)
        db.session.commit()
        # user has pressed "Delete club,
        # so delete it and return to list overview"


        return redirect(url_for('clubs.list_clubs', _anchor="close-delete-club"))
    return render_template('admin/club.html', school=school, club=club, days=days, ygs=ygs, book=book, staff_member=staff_member, ext_c=ext_c, form=form)

# LIST CLUBS
@clubs.route('/list_clubs/', methods=['GET', 'POST'])
@login_required
def list_clubs():
    school= School.query.first()
    clubs = Club.query.all()
    form = Publish()
    #form = UnPublish()
    test = None

    if form.validate_on_submit():
        club_id = request.form['publish']

        club = Club.query.filter_by(id=club_id).first()
        if club.published:
            club.published = False
        else:
            club.published = True
        db.session.commit()
        #club = Club.query.filter_by(id=publish_form['publish']).first()
        #club.published = True
        #db.session.commit()

        return redirect(url_for('clubs.list_clubs'))#render_template('admin/list_clubs.html',test=club_id, school=school, clubs=clubs, form=form)#render_template('admin/list_clubs.html',test=test, school=school, clubs=clubs, publish_form=publish_form, unpublish_form=unpublish_form)

    '''if unpublish_form.validate_on_submit():
        club = Club.query.filter_by(id=unpublish_form['unpublish']).first()
        club.published = False
        db.session.commit()'''

    return render_template('admin/list_clubs.html',test=test, school=school, clubs=clubs, form=form)



# MANAGE STAFF AND Companies
@clubs.route('/list_staff_and_companies/', methods=['GET', 'POST'])
@login_required
def list_staff_and_companies():
    school= School.query.first()
    staffmembers = StaffMember.query.all()
    scs = StaffClub.query.all()
    companies = ExternalCompany.query.all()
    clubs = Club.query.all()
    return render_template('admin/list_staff_and_companies.html',school=school, staffmembers=staffmembers, scs=scs, clubs=clubs, companies=companies)

# SINGLE STAFF MEMBER
@clubs.route('/staffmember/<sm_id>', methods=['GET', 'POST'])
@clubs.route('/staffmember/<sm_id>/<club_id>', methods=['GET', 'POST'])
@login_required
def staffmember(sm_id, club_id=None):
    form = EditStaffDetails()
    school= School.query.first()
    sm = StaffMember.query.filter_by(id=sm_id).first()
    scs = StaffClub.query.filter_by(staffmember_id=sm.id).all()
    clubs = [Club.query.filter_by(id=sc.club_id).first() for sc in scs]
    if club_id:
        popup_club = Club.query.filter_by(id=club_id).first()
    else:
        popup_club = None
    if form.validate_on_submit():
        if form.removeStaff.data:#if request.form['removeStaff']:
            for sc in scs:
                db.session.delete(sc)
            db.session.commit()

            db.session.delete(sm)
            db.session.commit()

            return redirect(url_for('clubs.list_staff_and_companies'))
        sc = StaffClub.query.filter_by(club_id=club_id).first()
        if sc:
            db.session.delete(sc)
            db.session.commit()
            # user has pressed "Remove <name> from <club> - They no longer run this club" button,
            # so delete link to club and return to their overview"
            return redirect(url_for('clubs.staffmember', _anchor="close-remove-from-club", sm_id=sm.id))
        if form.name.data:
            sm.name = form.name.data
        if form.email.data:
            sm.email = form.email.data
        if form.description.data:
            sm.description = form.description.data

        db.session.commit()
        return redirect(url_for('clubs.staffmember', sm_id=sm.id))

    return render_template('admin/staffmember.html',school=school, sm=sm, clubs=clubs, form=form, popup_club=popup_club)

# SINGLE COMPANY
@clubs.route('/company/<c_id>', methods=['GET', 'POST'])
@clubs.route('/company/<c_id>/<club_id>', methods=['GET', 'POST'])
@login_required
def company(c_id, club_id=None):
    form = EditCompanyDetails()
    school= School.query.first()
    c = ExternalCompany.query.filter_by(id=c_id).first()
    clubs = Club.query.filter_by(ext_company_id=c.id).all()
    if club_id:
        popup_club = Club.query.filter_by(id=club_id).first()
    else:
        popup_club = None
    if form.validate_on_submit():
        if form.removeCompany.data:
            for club in clubs:
                club.ext_company_id = None
                club.published = False #if a company can no longer run the club, the club should be unpublished until a new company or staff is added.

            db.session.delete(c)
            db.session.commit()

            return redirect(url_for('clubs.list_staff_and_companies'))
        if form.removeCompanyFromClub.data:
            if popup_club:
                popup_club.ext_company_id = None
            db.session.commit()
            # user has pressed "Remove <company> from <club> - They no longer run this club" button,
            # so delete link to club and return to their overview"
            return redirect(url_for('clubs.company', _anchor="close-remove-from-club", c_id=c.id))
        if form.name.data:
            c.name = form.name.data
        if form.email.data:
            c.email = form.email.data
        if form.website.data:
            c.website = form.website.data
        if form.description.data:
            c.description = form.description.data

        db.session.commit()
        return redirect(url_for('clubs.company', c_id=c.id))

    return render_template('admin/company.html',school=school, c=c, clubs=clubs, form=form, popup_club=popup_club)

######################################################
################### PARENT SIDE ######################
######################################################


# View all clubs (parent side)
@clubs.route('/clubs', methods=['GET', 'POST'])
def school_clubs():
    school = School.query.first()
    clubs = Club.query.all()
    club_info_grouped = []
    for club in clubs:
        if club.published:
            days = ClubDay.query.filter_by(club_id=club.id).all()
            ygs = ClubYearGroup.query.filter_by(club_id=club.id).all()
            sc = StaffClub.query.filter_by(club_id=club.id).first()
            book = ContactToBook.query.filter_by(id=club.contact_to_book_id).first()

            if sc:
                # club is run by individual staff and not a company. (should I check for all instead of first?)
                staff_member = StaffMember.query.filter_by(id=sc.staffmember_id).first()
            else:
                staff_member = None
            if club.ext_company_id:
                ext_c = ExternalCompany.query.filter_by(id=club.ext_company_id).first()
            else:
                ext_c = None

            year_groups = []
            for yg in ygs:
                year_groups.append(int(yg.name))
            # if there is more than one year group connected to the club:
            if len(year_groups) > 1:
                # check if the year groups are consequtive:
                if (sorted(year_groups) == list(range(min(year_groups), max(year_groups)+1))): #https://www.geeksforgeeks.org/python-check-if-list-contains-consecutive-numbers/
                    ygs = str(year_groups[0]) + '-' + str(year_groups[-1])
                else:
                    #not consequtive, just sort and store as string
                    temp = sorted(year_groups)
                    temp2 = [str(x) for x in temp]
                    ygs = ", ".join(temp2)
            else:
                #single year group, just store name
                ygs = ygs[0].name

            # Sort weekday names
            temp = [day.name for day in days]
            days = Weekday_Sorted_Week(temp)

            club_info_grouped.append((club, days, ygs, staff_member, book, ext_c))
    '''
    club = Club.query.filter_by(id=club_id).first()
    days = ClubDay.query.filter_by(club_id=club.id).all()
    ygs = ClubYearGroup.query.filter_by(club_id=club.id).all()
    sc = StaffClub.query.filter_by(club_id=club.id).first()
    book = ContactToBook.query.filter_by(id=club.contact_to_book_id).first()
    '''

    return render_template('parent/cards.html', school=school, clubs=club_info_grouped)
