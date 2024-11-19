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