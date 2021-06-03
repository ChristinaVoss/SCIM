from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from schoolclubinfomanager import db
from schoolclubinfomanager.models import School, YearGroup, Club, ClubDay, ClubYearGroup, ContactToBook, StaffClub, StaffMember, ExternalCompany
from schoolclubinfomanager.clubs.forms import CreateClub, Publish, DeleteClub
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
    one_year = str(datetime.datetime.now())[:10]
    one_year = one_year[:3] + str(int(one_year[3]) + 1) + one_year[4:10]
    teachers = [contact.teacher_name for contact in ContactToBook.query.all()]
    emails = [contact.email for contact in ContactToBook.query.all()]
    phone_numbers = [contact.call for contact in ContactToBook.query.all()]

    #school = School.query.first()
    if form.validate_on_submit():
        '''

        name = form.name.data
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


        photo = form.photo.data
        #staff=staff, companies=companies, in_system=in_system, comp_web=comp_web, comp_des=comp_des, comp_email=comp_email, comp_name=comp_name, staff_description=staff_description, staff_name=staff_name, staff_email=staff_email, type=type, new_entry=new_entry, photo=photo, description=description, is_free=is_free, cost=cost, book=book, teacher=teacher, email=email, call=call, exp=exp, outfit=outfit, equipment=equipment, ygs=ygs, days=days, name=name, start_date=start_date, end_date=end_date, start_time=start_time, end_time=end_time, at_school=at_school, location=location, off_school=off_school
        return render_template('admin/test.html', school=school, photo=photo, pic=pic)
    return (render_template('admin/club_form.html', form=form, title="Create", school=school, today=today, one_year=one_year))
'''
        # SAVE PHOTO
        if form.photo.data: #if they actually uploaded a photo
            club_name = form.name.data
            club_name = club_name.replace(' ', '') + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '-')[-6:]

            pic = add_photo(form.photo.data, club_name)

        else:
            pic = None



        location = form.location.data
        print('Hello world!', file=sys.stderr)
        print(location, file=sys.stdout)
        if location == 'at_school':
            at_school = True
            location = form.at_school_premises.data
        else:
            at_school = False
            location = form.off_school_premises.data

        cost = form.is_free.data
        if cost == 'free':
            is_free = True
            cost = None
        else:
            is_free = False
            cost = form.cost.data

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
                    contact = ContactToBook.query.filter_by(teacher_name=teacher_name).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                teacher_name = None

            if form.book.data == 'email':
                email = form.email.data
                if bool(ContactToBook.query.filter_by(email=email).first()):
                    #email already exists in the system, just link to club
                    contact = ContactToBook.query.filter_by(email=email).first()
                    club.contact_to_book_id = contact.id
                    db.session.commit()
            else:
                email = None

            if form.book.data =='call':
                call = form.call.data
                if bool(ContactToBook.query.filter_by(call=call).first()):
                    #number already exists in the system, just link to club
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

        db.session.commit()
        return redirect(url_for('clubs.club', club_id=club.id))
    return (render_template('admin/club_form.html', form=form, title="Create", school=school, today=today, one_year=one_year, teachers=teachers, emails=emails, phone_numbers=phone_numbers))



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
