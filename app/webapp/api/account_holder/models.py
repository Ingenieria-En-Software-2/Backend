from ...import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship


class AccountHolder(db.Model):
    __tablename__ = "account_holder"

    user = relationship("User", cascade="delete")

    # Personal Data
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="cascade"))
    id_number = db.Column(db.String())
    gender = db.Column(db.String())
    civil_status = db.Column(db.String())
    birthdate = db.Column(db.Date())
    phone = db.Column(db.String())
    nacionality = db.Column(db.String())

    # Residence address
    street = db.Column(db.String())
    sector = db.Column(db.String())
    city = db.Column(db.String())
    country = db.Column(db.String())
    province = db.Column(db.String())
    township = db.Column(db.String())
    address = db.Column(db.Text())

    # Employer data
    employer_name = db.Column(db.String())
    employer_rif = db.Column(db.String())
    employer_phone = db.Column(db.String())
    employer_city = db.Column(db.String())
    employer_country = db.Column(db.String())
    employer_province = db.Column(db.String())
    employer_township = db.Column(db.String())
    employer_address = db.Column(db.Text())

    def __init__(
        self,
        user_id,
        id_number,
        gender,
        civil_status,
        birthdate,
        phone,
        nacionality,
        street,
        sector,
        city,
        country,
        province,
        township,
        address,
        employer_name,
        employer_rif,
        employer_phone,
        employer_city,
        employer_country,
        employer_province,
        employer_township,
        employer_address,
    ):
        # Personal Data
        self.user_id = user_id
        self.id_number = id_number
        self.gender = gender
        self.civil_status = civil_status
        self.birthdate = birthdate
        self.phone = phone
        self.nacionality = nacionality

        # Residence address
        self.street = street
        self.sector = sector
        self.city = city
        self.country = country
        self.province = province
        self.township = township
        self.address = address

        # Employer Data
        self.employer_name = employer_name
        self.employer_rif = employer_rif
        self.employer_phone = employer_phone
        self.employer_city = employer_city
        self.employer_country = employer_country
        self.employer_province = employer_province
        self.employer_township = employer_township
        self.employer_address = employer_address

    def __repr__(self):
        return "<AccountHolder id {}>".format(self.id)
