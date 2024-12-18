from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from werkzeug.wrappers.response import Response
from app.template_risk import calculate_risk_level
from app.validator import ComponentForm
from app import db
from app.models import Customer,\
Manufacturer,\
Solution,\
Component,\
Template,\
TemplateSection,\
TemplateQuestion,\
TemplateRisk,\
Questionnaire,\
Section,\
DraftStartQuestionnaire

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def home():
    customers_count = Customer.query.count()
    manufacturers_count = Manufacturer.query.count()
    solutions_count = Solution.query.count()
    components_count = Component.query.count()
    return render_template('dashboard.html', customers_count=customers_count, manufacturers_count=manufacturers_count, solutions_count=solutions_count, components_count=components_count)

@main_blueprint.route('/customers', methods=['GET', 'POST'])
def customers():
    if request.method == 'POST':
        # Process the form data and add the customer to the database
        if 'name' in request.form:
            customer = Customer(name=request.form['name'])
            db.session.add(customer)
            db.session.commit()
        return redirect(url_for('customers'))
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@main_blueprint.route('/manufacturers', methods=['GET', 'POST'])
def manufacturers():
    if request.method == 'POST':
        # Process the form data and add the manufacturer to the database
        if 'name' in request.form:
            manufacturer = Manufacturer(name=request.form['name'])
            db.session.add(manufacturer)
            db.session.commit()
        return redirect(url_for('manufacturers'))
    manufacturers = Manufacturer.query.all()
    return render_template('manufacturers.html', manufacturers=manufacturers)

@main_blueprint.route('/solutions', methods=['GET', 'POST'])
def solutions():
    if request.method == 'POST':
        # Process the form data and add the solution to the database
        if 'name' in request.form:
            solution = Solution(name=request.form['name'], manufacturer_id=request.form['manufacturer_id'])
            db.session.add(solution)
            db.session.commit()
        return redirect(url_for('solutions'))
    solutions = Solution.query.all()
    return render_template('solutions.html', solutions=solutions, manufacturers=Manufacturer.query.all())

@main_blueprint.route('/components', methods=['GET', 'POST'])
def components():
    if request.method == 'POST':
        form = ComponentForm()
        if form.validate_on_submit():
            name = form.name.data
            solution_id = form.solution_id.data
            component = Component(name=name, solution_id=solution_id)
            db.session.add(component)
            db.session.commit()
            return redirect(url_for('components'))
    components = Component.query.all()
    return render_template('components.html', components=components, solutions=Solution.query.all())

@main_blueprint.route('/components/<int:component_id>', methods=['GET', 'POST'])
def component_details(component_id):
    if request.method == 'POST':
        # Process the form data and update the component in the database
        if 'name' in request.form:
            component = Component.query.get_or_404(component_id)
            component.name = request.form['name']
            db.session.commit()
        return redirect(url_for('component_details', component_id=component_id))
    component = Component.query.get_or_404(component_id)
    return render_template('component_details.html', component=component)

@main_blueprint.route('/templates', methods=['GET', 'POST'])
def templates():
    if request.method == 'POST':
        # Process the form data and add the template to the database
        if 'name' and 'description' in request.form:
            template = Template(name=request.form['name'], description=request.form['description'])
            db.session.add(template)
            db.session.commit()
        return redirect(url_for('main.templates'))
    templates = Template.query.all()
    return render_template('templates.html', templates=templates)

@main_blueprint.route('/templates/<int:template_id>', methods=['GET', 'POST'])
def template_details(template_id):
    if request.method == 'POST':
        # Process the form data and update the template in the database
        if 'name' and 'description' in request.form:
            template = Template.query.get_or_404(template_id)
            template.name = request.form['name']
            template.description = request.form['description']
            db.session.commit()
        return redirect(url_for('template_details', template_id=template_id))
    template = Template.query.get_or_404(template_id)
    return render_template('template_details.html', template=template, template_sections=TemplateSection.query.filter_by(template_id=template_id).all())


@main_blueprint.route('/templates/<int:template_id>/sections', methods=['POST'])
def template_sections(template_id):

        # Process the form data and add the section to the database
        if 'name' in request.form:
            last_section_number = TemplateSection.query.filter_by(template_id=template_id).order_by(TemplateSection.number.desc()).first()
            if last_section_number:
                section_number = last_section_number.number + 1
            else:
                section_number = 1
            section = TemplateSection(name=request.form['name'], number=section_number, template_id=template_id)
            db.session.add(section)
            db.session.commit()
        return redirect(url_for('template_details', template_id=template_id))
    #sections = TemplateSection.query.filter_by(template_id=template_id).all()
    #return render_template('template_details.html', template=Template.query.get_or_404(template_id), template_sections=TemplateSection.query.filter_by(template_id=template_id).all(), sections=sections)

@main_blueprint.route('/templates/<int:template_id>/sections/<int:section_id>', methods=['DELETE'])
def delete_section(template_id, section_id):
    section = TemplateSection.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    # Retorna o cabeçalho HX-Redirect para redirecionar para 'template_details'
    response = jsonify(message="Seção excluída")
    response.headers['HX-Redirect'] = url_for('template_details', template_id=template_id)
    return response
    #return redirect(url_for('template_details', template_id=template_id), code=303)

@main_blueprint.route('/templates/<int:template_id>/risks', methods=['GET', 'POST'])
def template_risks(template_id):
    if request.method == 'POST':
        # Process the form data and add the risk to the database
        if 'template_question_id' and 'template_response_value' and 'risk_impact' and 'risk_likelihood' and 'risk_description' in request.form:
            template_question_id = request.form['template_question_id']
            template_response_value = request.form['template_response_value']
            risk_impact = int(request.form['risk_impact'])
            risk_likelihood = int(request.form['risk_likelihood'])
            risk_level = calculate_risk_level(risk_impact, risk_likelihood)
            risk_description = request.form['risk_description']
            risk = TemplateRisk(template_id=template_id, template_question_id=template_question_id, template_response_value=template_response_value, risk_impact=risk_impact, risk_likelihood=risk_likelihood, risk_level=risk_level, risk_description=risk_description)
            db.session.add(risk)
            db.session.commit()
            return redirect(url_for('template_risks', template_id=template_id))
    template = Template.query.get_or_404(template_id)
    template_questions = TemplateQuestion.query.join(TemplateSection).filter(TemplateSection.template_id==template_id)
    template_risks = TemplateRisk.query.join(TemplateQuestion).join(TemplateSection).filter(TemplateRisk.template_id==template_id)
    print(dir(template_risks[0].template_question))
    risk_impacts = ['Muito Baixo', 'Baixo', 'Médio', 'Alto', 'Muito Alto']
    risk_likelihoods = ['1% - 20%', '21% - 40%', '41% - 60%', '61% - 80%', '81% - 100%']
    risk_levels = [
        'Muito Baixo',
        'Muito Baixo',
        'Muito Baixo',
        'Muito Baixo',
        'Muito Baixo',
        'Baixo',
        'Baixo',
        'Baixo',
        'Baixo',
        'Baixo',
        'Médio',
        'Médio',
        'Médio',
        'Médio',
        'Médio',
        'Alto',
        'Alto',
        'Alto',
        'Alto',
        'Alto',
        'Muito Alto',
        'Muito Alto',
        'Muito Alto',
        'Muito Alto',
        'Muito Alto'
    ]
    return render_template('template_risks.html', template=template, template_questions=template_questions, template_risks=template_risks, risk_levels=risk_levels, risk_likelihoods=risk_likelihoods, risk_impacts=risk_impacts)
    #query = text("SELECT * FROM template t JOIN template_section ts ON t.id = ts.template_id JOIN template_question tq ON ts.id = tq.section_id LEFT JOIN template_risk tr ON tq.id = tr.template_question_id WHERE t.id = :id;")
    #results = db.session.execute(query, {"id": template_id}).all()

@main_blueprint.route('/templates/sections/<int:section_id>/questions', methods=['GET'])
def section_questions(section_id):
    questions = TemplateQuestion.query.filter_by(section_id=section_id).all()
    return render_template('section_questions.html', section_id=section_id, template_questions=questions)

@main_blueprint.route('/templates/sections/<int:section_id>/questions', methods=['POST'])
def questions(section_id):
        # Process the form data and add the question to the database
        if 'title' and 'response_type' and 'required' in request.form:
            last_question_number = TemplateQuestion.query.filter_by(section_id=section_id).order_by(TemplateQuestion.number.desc()).first()
            if last_question_number:
                question_number = last_question_number.number + 1
            else:
                question_number = 1
            if request.form['required'] == 'on':
                required = True
            else:
                required = False
            question = TemplateQuestion(title=request.form['title'], number=question_number, section_id=section_id, response_type=request.form['response_type'], required=required)
            db.session.add(question)
            db.session.commit()
        return render_template('section_questions.html', section_id=section_id, template_questions=TemplateQuestion.query.filter_by(section_id=section_id).all())

@main_blueprint.route('/templates/sections/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = TemplateQuestion.query.get_or_404(question_id)
    db.session.delete(question)
    db.session.commit()
    return '', 204

@main_blueprint.route('/questionnaires', methods=['GET'])
def questionnaires():
    return render_template('questionnaires.html')

@main_blueprint.route('/questionnaires/start', methods=['GET', 'POST'])
def start_questionnaire():
    if request.method == 'POST':
        print(request.form);
        return 'hello'
    draft_start_questionnaire = DraftStartQuestionnaire.query.first()
    if draft_start_questionnaire == None:
        return render_template('start_questionnaire.html', step=1)
    elif draft_start_questionnaire.template_id != None and draft_start_questionnaire.title != None:
        return render_template('start_questionnaire.html', step=2)
    elif draft_start_questionnaire.customer_id != None and draft_start_questionnaire.component_id != None:
        return render_template('start_questionnaire.html', step=3)
    return render_template('start_questionnaire.html', step=1)

@main_blueprint.route('/questionnaires/start/<int:step>', methods=['GET', 'POST'])
def handle_step(step):
    if request.method == 'POST':
        if step == 1:
            template_id = request.form['questionnaire_template']
            title = request.form['questionnaire_title']
            draft_start_questionnaire = DraftStartQuestionnaire(template_id=template_id, title=title)
            db.session.add(draft_start_questionnaire)
            db.session.commit()
            return redirect(url_for('main.handle_step', step=2))
        elif step == 2:
            customer_id = request.form['customer_id']
            component_id = request.form['component_id']
            draft_start_questionnaire = DraftStartQuestionnaire.query.first()
            draft_start_questionnaire.customer_id = customer_id
            draft_start_questionnaire.component_id = component_id
            db.session.commit()
            return redirect(url_for('main.handle_step', step=3))
        elif step == 3:
            return redirect(url_for('questionnaires'))
    draft_start_questionnaire = DraftStartQuestionnaire.query.first()
    if step == 1:
        templates = Template.query.all()
        return render_template('partials/first_step_start_questionnaire.html', draft_start_questionnaire=draft_start_questionnaire, templates=templates)
    elif step == 2:
        customers = Customer.query.all()
        components = Component.query.all()
        return render_template('partials/second_step_start_questionnaire.html', draft_start_questionnaire=draft_start_questionnaire, customers=customers, components=components)
    elif step == 3:
        return render_template('partials/third_step_start_questionnaire.html')
    else:
        return render_template('partials/fourth_step_start_questionnaire.html')

@main_blueprint.route('/questionnaires/start/template', methods=['GET'])
def render_template_title():
    template_id = request.args.get('questionnaire_template')
    template = Template.query.filter_by(id=template_id).first()
    if template:
        template_name = template.name
        return render_template('components/template_title.html', template_name=template_name)
    else:
        return render_template('components/template_title.html')
    #return Response("Erro", status=404)