from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from sorted_months_weekdays import Weekday_Sorted_Week
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup, Club, ClubDay, ClubYearGroup, ContactToBook, StaffClub, StaffMember, ExternalCompany
from schoolclubinfomanager.clubs.forms import CreateClub, Publish, DeleteClub, EditStaffDetails, EditCompanyDetails, ChooseDay
from schoolclubinfomanager.clubs.picture_handler import add_photo
from schoolclubinfomanager.clubs.helpers import addCheckboxes, updateCheckboxes, contactToBook, setupClubRunner, format_yeargroups, staff_or_company, popup_card
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
    #contact to book details
    teachers = [contact.teacher_name for contact in ContactToBook.query.all()]
    emails = [contact.email for contact in ContactToBook.query.all()]
    phone_numbers = [contact.call for contact in ContactToBook.query.all()]
    #club runners
    staff_list = StaffMember.query.all()
    company_list = ExternalCompany.query.all()

    if form.validate_on_submit():
        #CREATE CLUB
        at_school = form.location.data == 'at_school'
        location = form.at_school_premises.data if at_school else form.off_school_premises.data
        is_free = (form.is_free.data == "free")
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
                    drop_in = drop_in)
        db.session.add(club)
        db.session.commit()

        # SAVE PHOTO
        if form.photo.data: #if they actually uploaded a photo
            club_name = form.name.data
            club_name = club_name.replace(' ', '') + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')[-6:]
            pic = add_photo(form.photo.data, club_name)
        else:
            pic = None

        # NOT COMPULSORY CLUB INFO
        club.experience = form.experience.data
        club.outfit = form.outfit.data
        club.equipment = form.equipment.data
        club.description = form.description.data
        club.photo = pic
        club.cost = None if is_free else form.cost.data
        db.session.commit()

        #DAYS
        addCheckboxes(ClubDay, form.days.data, club)
        #YEAR GROUPS
        addCheckboxes(ClubYearGroup, form.year_groups.data, club)
        # CONTACT TO BOOK
        contactToBook(drop_in, form, club)
        # CLUB RUNNING COMPANY OR STAFF
        setupClubRunner(form, club)

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

    # club runners
    staff_list = StaffMember.query.all()
    company_list = ExternalCompany.query.all()

    # variables needed in some cases
    sm = None
    comp = None
    start_d = club.start_date.date()
    end_d = club.end_date.date()
    start_t = club.start_time
    end_t = club.end_time

    if form.validate_on_submit():
        # SAVE PHOTO
        if form.photo.data: #if they actually uploaded a photo
            club_name = form.name.data
            club_name = club_name.replace(' ', '') + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')[-6:]
            club.photo = add_photo(form.photo.data, club_name) # old picture is still in the system - decide if you want to delete it?

        at_school = form.location.data == 'at_school'
        location = form.at_school_premises.data if at_school else form.off_school_premises.data
        is_free = form.is_free.data == "free"
        cost =  None if is_free else form.cost.data
        drop_in = form.book.data == 'drop_in'

        club.name = form.name.data
        club.start_date = form.start_date.data
        club.end_date = form.end_date.data
        club.start_time = form.start_time.data
        club.end_time = form.end_time.data
        club.location = location
        club.at_school = at_school
        club.is_free = is_free
        club.num_of_places = form.num_places.data
        club.drop_in = drop_in
        club.cost = cost
        club.experience = form.experience.data
        club.outfit = form.outfit.data
        club.equipment = form.equipment.data
        club.description = form.description.data
        db.session.commit()

        # DAYS
        updateCheckboxes(ClubDay, existing_days, set(form.days.data), club)
        # YEAR GROUPS
        updateCheckboxes(ClubYearGroup, existing_ygs, set(form.year_groups.data), club)
        # CONTACT TO BOOK
        contactToBook(drop_in, form, club)
        # CLUB RUNNER
        setupClubRunner(form, club)

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
        # user has pressed "Delete club,
        # so delete it and return to list overview"
        for yg in ygs:
            db.session.delete(yg)
        for day in days:
            db.session.delete(day)
        if sc:
            db.session.delete(sc)
        db.session.delete(club)
        db.session.commit()
        return redirect(url_for('clubs.list_clubs', _anchor="close-delete-club"))
    return render_template('admin/club.html', school=school, club=club, days=days, ygs=ygs, book=book, staff_member=staff_member, ext_c=ext_c, form=form)

# LIST CLUBS
@clubs.route('/list_clubs/', methods=['GET', 'POST'])
@login_required
def list_clubs():
    school= School.query.first()
    clubs = Club.query.all()
    form = Publish()
    test = None

    if form.validate_on_submit():
        club_id = request.form['publish']
        club = Club.query.filter_by(id=club_id).first()
        #Flip the boolean to opposite state depending on prior state.
        club.published = False if club.published else True
        db.session.commit()

        return redirect(url_for('clubs.list_clubs'))
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
    popup_club = Club.query.filter_by(id=club_id).first() if club_id else None

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
    popup_club = Club.query.filter_by(id=club_id).first() if club_id else None

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

# View all clubs (parent cards)
@clubs.route('/clubs', methods=['GET', 'POST'])
@clubs.route('/clubs/<club_id>', methods=['GET', 'POST'])
def school_clubs(club_id=None):
    school = School.query.first()
    clubs = Club.query.all()
    club_info_grouped = []

    # POPUP CLUB CARD
    popup = popup_card(club_id)
    '''if club_id:
        popup_club = Club.query.filter_by(id=club_id).first()
        popup_days = ClubDay.query.filter_by(club_id=popup_club.id).all()
        popup_ygs = format_yeargroups(ClubYearGroup.query.filter_by(club_id=popup_club.id).all())
        popup_sc = StaffClub.query.filter_by(club_id=popup_club.id).first()
        popup_book = ContactToBook.query.filter_by(id=popup_club.contact_to_book_id).first()
        popup_staff_member, popup_ext_c = staff_or_company(popup_sc, popup_club)

        # Sort weekday names
        temp = [day.name for day in popup_days]
        popup_days = Weekday_Sorted_Week(temp)

    else:
        popup_club = None
        popup_days = None
        popup_ygs = None
        popup_sc = None
        popup_book = None
        popup_staff_member = None
        popup_ext_c = None'''

    # NOT POPUP - LIST ALL PUBLISHED CLUBS
    for club in clubs:
        if club.published:
            days = ClubDay.query.filter_by(club_id=club.id).all()
            ygs = ClubYearGroup.query.filter_by(club_id=club.id).all()
            sc = StaffClub.query.filter_by(club_id=club.id).first()
            book = ContactToBook.query.filter_by(id=club.contact_to_book_id).first()
            staff_member, ext_c = staff_or_company(sc, club)

            ygs = format_yeargroups(ygs)

            # Sort weekday names
            temp = [day.name for day in days]
            days = Weekday_Sorted_Week(temp)

            club_info_grouped.append((club, days, ygs, staff_member, book, ext_c))

    return render_template('parent/cards.html', school=school, clubs=club_info_grouped, popup=popup)#school=school, clubs=club_info_grouped, popup_club=popup_club, popup_days=popup_days, popup_ygs=popup_ygs, popup_staff_member=popup_staff_member, popup_book=popup_book, popup_ext_c=popup_ext_c


# View all clubs (parent timetable)
@clubs.route('/timetable', methods=['GET', 'POST'])
@clubs.route('/timetable/<x>', methods=['GET', 'POST'])# x as mixed variable for either weekday or club_id, as Flask gets confused by different routes with same number arguments
def timetable(x=None):
    school = School.query.first()
    clubs = Club.query.all()
    form = ChooseDay()
    today = datetime.datetime.now()

    # CHECK ARGUMENT (weekday, club id or nothing)
    if x and x.isnumeric():
        club_id = x
        weekday = None
    elif x and not x.isnumeric():
        club_id = None
        weekday = x
    else:
        club_id = None
        weekday = None

    # POPUP CLUB CARD
    popup = popup_card(club_id)
    '''if club_id and club_id.isnumeric():
        popup_club = Club.query.filter_by(id=club_id).first()
        popup_days = ClubDay.query.filter_by(club_id=popup_club.id).all()
        popup_ygs = ClubYearGroup.query.filter_by(club_id=popup_club.id).all()
        popup_sc = StaffClub.query.filter_by(club_id=popup_club.id).first()
        popup_book = ContactToBook.query.filter_by(id=popup_club.contact_to_book_id).first()
        popup_staff_member, popup_ext_c = staff_or_company(popup_sc, popup_club)
        popup_ygs = format_yeargroups(popup_ygs)

        # Sort weekday names
        temp = [day.name for day in popup_days]
        popup_days = Weekday_Sorted_Week(temp)

    else:
        popup_club = None
        popup_days = None
        popup_ygs = None
        popup_sc = None
        popup_book = None
        popup_staff_member = None
        popup_ext_c = None'''

    # TIMETABLE variables
    # first find out wether the timetable should include weekend days (are there clubs in weekend?)
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    saturday = ClubDay.query.filter_by(name="Saturday").all()
    sunday = ClubDay.query.filter_by(name="Sunday").all()
    if saturday or sunday:
        weekdays.append("Saturday")
        weekdays.append("Sunday")

    # create dictionary to hold clubs, separated by days for the timetable columns
    timetable_clubs = {}
    timeofday = {}

    for d in weekdays:
        timetable_clubs[d] = ClubDay.query.filter_by(name=d).all()
        day_clubs = []
        for day_club in timetable_clubs[d]:
            temp = Club.query.filter_by(id=day_club.club_id).first()
            temp_ygs = ClubYearGroup.query.filter_by(club_id=temp.id).all()
            f_ygs = format_yeargroups(temp_ygs)
            day_clubs.append((temp, f_ygs))

        day_clubs.sort(key=lambda c: c[0].start_time)
        timetable_clubs[d] = day_clubs
        # create set of clubs starting hours, and check if there are clubs for each time of day
        hours = {c[0].start_time.hour for c in day_clubs}
        morning = not hours.isdisjoint(range(6,9))
        lunch = not hours.isdisjoint(range(9,15))
        after_school = not hours.isdisjoint(range(15,24))
        timeofday[d] = (morning, lunch, after_school)

    return render_template('parent/timetable.html', school=school, form=form, popup=popup, timetable_clubs=timetable_clubs, weekdays=weekdays, weekday=weekday, timeofday=timeofday, today=today)#school=school, form=form, popup_club=popup_club, popup_days=popup_days, popup_ygs=popup_ygs, popup_staff_member=popup_staff_member, popup_book=popup_book, popup_ext_c=popup_ext_c, timetable_clubs=timetable_clubs, weekdays=weekdays, weekday=weekday, timeofday=timeofday, today=today
