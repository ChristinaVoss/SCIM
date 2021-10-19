from sorted_months_weekdays import Weekday_Sorted_Week
from schoolclubinfomanager import db
from schoolclubinfomanager.models import Club, ClubDay, ClubYearGroup, ContactToBook, StaffClub, StaffMember, ExternalCompany

#ADMIN HELPER FUNCTIONS
def addCheckboxes(obj, values, club):
    for item in values:
        temp = obj(item, club.id)
        db.session.add(temp)
    db.session.commit()

def updateCheckboxes(obj, existing, new, club):
    for item in new:
        if item not in existing:
            temp = obj(item, club.id)
            db.session.add(temp)
    to_delete = existing - new
    if to_delete:
        for item in to_delete:
            temp = obj.query.filter_by(name=item, club_id=club.id).first()
            db.session.delete(temp)
    db.session.commit()


def check_if_exists(value, club):
    teacher = ContactToBook.query.filter_by(teacher_name=value).first()
    email = ContactToBook.query.filter_by(email=value).first()
    call = ContactToBook.query.filter_by(call=value).first()

    if not teacher and not email and not call:
        return False

    if teacher:
        contact = teacher
    elif email:
        contact = email
    else:
        contact = call
    club.contact_to_book_id = contact.id
    db.session.commit()
    return True

def bookingDetails(form, club):
    booking_details_exist = False
    teacher_name = None
    email = None
    call = None
    if form.book.data == 'teacher':
        teacher_name = form.teacher.data
        booking_details_exist = check_if_exists(teacher_name, club)

    elif form.book.data == 'email':
        email = form.email.data
        booking_details_exist = check_if_exists(email, club)

    elif form.book.data =='call':
        call = form.call.data
        booking_details_exist = check_if_exists(call, club)

    if not booking_details_exist:
        #new entry, create new object/row
        contact = ContactToBook(teacher_name = teacher_name,
                                email = email,
                                call = call)
        db.session.add(contact)
        db.session.commit()
        club.contact_to_book_id = contact.id
        db.session.commit()

def contactToBook(drop_in, form, club):
    if drop_in:
        club.contact_to_book_id = None
        db.session.commit()
    else:
        bookingDetails(form, club)



def createAndAddStaffMember(form, club):
    staff_member = StaffMember(name = form.staff_name.data,
                               email = form.staff_email.data if form.staff_email.data else None,
                               description = form.staff_description.data)
    db.session.add(staff_member)
    db.session.commit()

    staff_club = StaffClub(club_id = club.id,
                           staffmember_id = staff_member.id)

    db.session.add(staff_club)
    db.session.commit()

def createAndAddCompany(form, club):
    company = ExternalCompany(name = form.company_name.data,
                              website = form.company_website.data if form.company_website.data else None,
                              email = form.company_email.data if form.company_email.data else None,
                              description = form.company_description.data)

    db.session.add(company)
    db.session.commit()

    club.ext_company_id = company.id
    db.session.commit()

def removeClubRunner(club):
    sc = StaffClub.query.filter_by(club_id=club.id).first()
    if sc:
        db.session.delete(sc)
        db.session.commit()
    if club.ext_company_id:
        club.ext_company_id = None

def linkExistingCompanyToClub(club, form, existing_sc):
    if existing_sc:
        #make sure club is only linked to staff or a company, not both
        db.session.delete(existing_sc)
    company = form.companies.data
    company = ExternalCompany.query.filter_by(name=company).first()
    club.ext_company_id = company.id
    db.session.commit()

def linkExistingStaffToClub(club, form, existing_sc):
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

def setupClubRunner(form, club):
    if form.new_entry.data == 'new':
        # New entry to system, add to database,
        # remove old staff from club then add new staff/company
        removeClubRunner(club)
        if form.type_of_staff.data == 'person':
            createAndAddStaffMember(form, club)
        else:
            createAndAddCompany(form, club)

    else:
        # Staff or company exists in system, link to clubs
        # check if club has existing staff member to change
        existing_sc = StaffClub.query.filter_by(club_id=club.id).first()
        if form.existing_clubrunner.data == 'existing_staff':
            linkExistingStaffToClub(club, form, existing_sc)
        else:
            linkExistingCompanyToClub(club, form, existing_sc)


# PARENT HELPER FUNCTIONS
def format_yeargroups(ygs):
    year_groups = []
    for yg in ygs:
        year_groups.append(int(yg.name))
    # if there is more than one year group connected to the club:
    if len(year_groups) > 1:
        # check if the year groups are consequtive:
        if (sorted(year_groups) == list(range(min(year_groups), max(year_groups)+1))): #https://www.geeksforgeeks.org/python-check-if-list-contains-consecutive-numbers/
            return str(year_groups[0]) + '-' + str(year_groups[-1])
        else:
            #not consequtive, just sort and store as string
            temp = sorted(year_groups)
            temp2 = [str(x) for x in temp]
            return ", ".join(temp2)
    else:
        #single year group, just store name
        return ygs[0].name

def staff_or_company(sc, club):
    if sc:
        # club is run by individual staff and not a company. (should I check for all instead of first?)
        staff_member = StaffMember.query.filter_by(id=sc.staffmember_id).first()
    else:
        staff_member = None
    if club.ext_company_id:
        ext_company = ExternalCompany.query.filter_by(id=club.ext_company_id).first()
    else:
        ext_company = None
    return (staff_member, ext_company)

def popup_card(club_id):
    if club_id:
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
        popup_ext_c = None
    return [popup_club, popup_days, popup_ygs, popup_sc, popup_book, popup_staff_member, popup_ext_c]
