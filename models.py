from app import db

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)

class TemplateSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='fk_template', ondelete='CASCADE'), nullable=False)
    template = db.relationship('Template', backref='TemplateSection')
    #sections = db.relationship('TemplateSection', backref='Template')

class TemplateQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('template_section.id', name='fk_section', ondelete='CASCADE'), nullable=False)
    response_type = db.Column(db.String(), nullable=False)
    required = db.Column(db.Boolean, nullable=False)

#template_question = db.relationship('TemplateQuestion', backref='template_section')

class TemplateList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)

class TemplateListItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(), nullable=False)
    label = db.Column(db.String(), nullable=False)
    template_list_id = db.Column(db.Integer, db.ForeignKey('template_list.id', name='fk_list', ondelete='CASCADE'), nullable=False)

class TemplateRisk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='fk_template', ondelete='CASCADE'), nullable=False)
    template_question_id = db.Column(db.Integer, db.ForeignKey('template_question.id', name='fk_question', ondelete='CASCADE'), nullable=False)
    template_response_type = db.Column(db.String(), nullable=True)
    template_response_value = db.Column(db.String(), nullable=False)
    risk_impact = db.Column(db.Integer, nullable=False)
    risk_likelihood = db.Column(db.Integer, nullable=False)
    risk_level = db.Column(db.String(), nullable=False)
    risk_description = db.Column(db.String(), nullable=False)

#template_risk = db.relationship('TemplateRisk', backref='template')


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id', name='fk_manufacturer', ondelete='CASCADE'), nullable=False)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id', name='fk_solution', ondelete='CASCADE'), nullable=False)