from app import db

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)

class TemplateSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)    

class TemplateQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('template_section.id'), nullable=False)
    response_type = db.Column(db.String(), nullable=False)
    required = db.Column(db.Boolean, nullable=False)

class TemplateList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)

class TemplateListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False)
    label = db.Column(db.String(), nullable=False)
    template_list_id = db.Column(db.Integer, db.ForeignKey('template_list.id'), nullable=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    #email = db.Column(db.String(), nullable=False)

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id'), nullable=False)