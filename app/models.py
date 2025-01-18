import datetime
from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class Manufacturer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class Solution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id', name='fk_manufacturer', ondelete='CASCADE'), nullable=False)
    manufacturer = db.relationship('Manufacturer')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey('solution.id', name='fk_solution', ondelete='CASCADE'), nullable=False)
    solution = db.relationship('Solution')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class TemplateSection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='fk_template', ondelete='CASCADE'), nullable=False)
    template = db.relationship('Template', backref='TemplateSection')
    component_id = db.Column(db.Integer, db.ForeignKey('component.id', name='fk_component', ondelete='CASCADE'), nullable=True)
    component = db.relationship('Component')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class TemplateQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('template_section.id', name='fk_section', ondelete='CASCADE'), nullable=False)
    response_type = db.Column(db.String(), nullable=False)
    required = db.Column(db.Boolean, nullable=False)
    template_section = db.relationship('TemplateSection')
    risk_level = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

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
    template_question = db.relationship('TemplateQuestion')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='fk_template', ondelete='CASCADE'), nullable=False)
    template = db.relationship('Template')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', name='fk_customer', ondelete='CASCADE'), nullable=False)
    customer = db.relationship('Customer')
    component_id = db.Column(db.Integer, db.ForeignKey('component.id', name='fk_component', ondelete='CASCADE'), nullable=False)
    component = db.relationship('Component')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    sections = db.relationship('Section', backref='Questionnaire', lazy=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id', name='fk_questionnaire', ondelete='CASCADE'), nullable=False)
    component_id = db.Column(db.Integer, db.ForeignKey('component.id', name='fk_component', ondelete='CASCADE'), nullable=True)
    component = db.relationship('Component')
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    response_type = db.Column(db.String(), nullable=False)
    response = db.Column(db.String(), nullable=True)
    required = db.Column(db.Boolean, nullable=False)
    risk_impact = db.Column(db.Integer, nullable=True)
    risk_likelihood = db.Column(db.Integer, nullable=True)
    risk_level = db.Column(db.String(), nullable=True)
    risk_description = db.Column(db.String(), nullable=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id', name='fk_section', ondelete='CASCADE'), nullable=False)
    section = db.relationship('Section')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class DraftStartQuestionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id', name='fk_template', ondelete='CASCADE'), nullable=True)
    template = db.relationship('Template')
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id', name='fk_customer', ondelete='CASCADE'), nullable=True)
    customer = db.relationship('Customer')
    updated_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)

class DraftQuestionnaireComponent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.Integer, db.ForeignKey('component.id', name='fk_component', ondelete='CASCADE'), nullable=False)
    component = db.relationship('Component')
    component_amount = db.Column(db.Integer, nullable=True)
    draft_start_questionnaire_id = db.Column(db.Integer, db.ForeignKey('draft_start_questionnaire.id', name='fk_draft_start_questionnaire', ondelete='CASCADE'), nullable=False)
    draft_start_questionnaire = db.relationship('DraftStartQuestionnaire')
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)