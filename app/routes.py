from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.template_risk import calculate_risk_level

# from app.validator import ComponentForm
from app import db
from app.models import (
    Customer,
    Manufacturer,
    Solution,
    Component,
    Template,
    TemplateSection,
    TemplateQuestion,
    TemplateRisk,
    Questionnaire,
    Section,
    Question,
    DraftStartQuestionnaire,
    DraftQuestionnaireComponent,
)

main_blueprint = Blueprint("main", __name__)


@main_blueprint.route("/")
def home():
    customers_count = Customer.query.count()
    manufacturers_count = Manufacturer.query.count()
    solutions_count = Solution.query.count()
    components_count = Component.query.count()
    return render_template(
        "dashboard.html",
        customers_count=customers_count,
        manufacturers_count=manufacturers_count,
        solutions_count=solutions_count,
        components_count=components_count,
    )


@main_blueprint.route("/customers", methods=["GET", "POST"])
def customers():
    if request.method == "POST":
        # Process the form data and add the customer to the database
        if "name" in request.form:
            customer = Customer(name=request.form["name"])
            db.session.add(customer)
            db.session.commit()
        return redirect(url_for("main.customers"))
    customers = Customer.query.all()
    return render_template("customers.html", customers=customers)


@main_blueprint.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    if request.method == "DELETE":
        # Process the form data and delete the customer from the database
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()
        response = jsonify(message="Cliente excluído")
        response.headers["HX-Redirect"] = url_for("main.customers")
        return response


@main_blueprint.route("/manufacturers", methods=["GET", "POST"])
def manufacturers():
    if request.method == "POST":
        # Process the form data and add the manufacturer to the database
        if "name" in request.form:
            manufacturer = Manufacturer(name=request.form["name"])
            db.session.add(manufacturer)
            db.session.commit()
        return redirect(url_for("main.manufacturers"))
    manufacturers = Manufacturer.query.all()
    return render_template("manufacturers.html", manufacturers=manufacturers)


@main_blueprint.route("/manufacturers/<int:manufacturer_id>", methods=["DELETE"])
def delete_manufacturer(manufacturer_id):
    if request.method == "DELETE":
        # Process the form data and delete the customer from the database
        manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
        db.session.delete(manufacturer)
        db.session.commit()
        response = jsonify(message="Fabricante excluído")
        response.headers["HX-Redirect"] = url_for("main.manufacturers")
        return response


@main_blueprint.route("/solutions", methods=["GET", "POST"])
def solutions():
    if request.method == "POST":
        # Process the form data and add the solution to the database
        if "name" in request.form:
            solution = Solution(
                name=request.form["name"],
                manufacturer_id=request.form["manufacturer_id"],
            )
            db.session.add(solution)
            db.session.commit()
        return redirect(url_for("main.solutions"))
    solutions = Solution.query.all()
    manufacturers = Manufacturer.query.all()
    return render_template(
        "solutions.html", solutions=solutions, manufacturers=manufacturers
    )


@main_blueprint.route("/solutions/<int:solution_id>", methods=["DELETE"])
def delete_solution(solution_id):
    if request.method == "DELETE":
        # Process the form data and delete the customer from the database
        solution = Solution.query.get_or_404(solution_id)
        db.session.delete(solution)
        db.session.commit()
        response = jsonify(message="Solução excluída")
        response.headers["HX-Redirect"] = url_for("main.solutions")
        return response


@main_blueprint.route("/components", methods=["GET", "POST"])
def components():
    if request.method == "POST":
        if "name" and "solution_id" in request.form:
            name = request.form["name"]
            solution_id = request.form["solution_id"]
            component = Component(name=name, solution_id=solution_id)
            db.session.add(component)
            db.session.commit()
            return redirect(url_for("main.components"))
    args = request.args
    if args:
        search = args.get("search", default="", type=str)
        components = (
            Component.query.filter(Component.name.ilike(f"%{search}%"))
            .order_by(Component.name)
            .all()
        )
        return render_template(
            "components/section_component.html", components=components
        )
    components = Component.query.all()
    return render_template(
        "components.html", components=components, solutions=Solution.query.all()
    )


@main_blueprint.route("/components/<int:component_id>", methods=["DELETE"])
def delete_component(component_id):
    if request.method == "DELETE":
        # Process the form data and delete the customer from the database
        component = Component.query.get_or_404(component_id)
        db.session.delete(component)
        db.session.commit()
        response = jsonify(message="Componente excluído")
        response.headers["HX-Redirect"] = url_for("main.components")
        return response


@main_blueprint.route("/components/<int:component_id>", methods=["GET", "POST"])
def component_details(component_id):
    if request.method == "POST":
        # Process the form data and update the component in the database
        if "name" in request.form:
            component = Component.query.get_or_404(component_id)
            component.name = request.form["name"]
            db.session.commit()
        return redirect(url_for("main.component_details", component_id=component_id))
    component = Component.query.get_or_404(component_id)
    return render_template("component_details.html", component=component)


@main_blueprint.route("/templates", methods=["GET", "POST"])
def templates():
    if request.method == "POST":
        # Process the form data and add the template to the database
        if "name" and "description" in request.form:
            template = Template(
                name=request.form["name"], description=request.form["description"]
            )
            db.session.add(template)
            db.session.commit()
        return redirect(url_for("main.templates"))
    templates = Template.query.all()
    return render_template("templates.html", templates=templates)


@main_blueprint.route("/templates/<int:template_id>", methods=["GET", "POST"])
def template_details(template_id):
    if request.method == "POST":
        # Process the form data and update the template in the database
        if "name" and "description" in request.form:
            template = Template.query.get_or_404(template_id)
            template.name = request.form["name"]
            template.description = request.form["description"]
            db.session.commit()
        return redirect(url_for("main.template_details", template_id=template_id))
    template = Template.query.get_or_404(template_id)
    return render_template(
        "template_details.html",
        template=template,
        template_sections=TemplateSection.query.filter_by(
            template_id=template_id
        ).all(),
        components=Component.query.all(),
    )


@main_blueprint.route("/templates/<int:template_id>/sections", methods=["GET", "POST"])
def template_sections(template_id):
    if request.method == "POST":
        # Process the form data and add the section to the database
        if "name" in request.form:
            last_section_number = (
                TemplateSection.query.filter_by(template_id=template_id)
                .order_by(TemplateSection.number.desc())
                .first()
            )
            if last_section_number:
                section_number = last_section_number.number + 1
            else:
                section_number = 1
            section = TemplateSection(
                name=request.form["name"],
                number=section_number,
                template_id=template_id,
            )
            db.session.add(section)
            db.session.commit()
        return redirect(url_for("main.template_details", template_id=template_id))
    template_sections = TemplateSection.query.filter_by(template_id=template_id).all()
    # Variável para armazenar a seção selecionada
    selected_section_id = request.args.get("selected_section_id", None, type=int)
    return render_template(
        "partials/template_sections.html",
        template_sections=template_sections,
        selected_section_id=selected_section_id,
    )
    # sections = TemplateSection.query.filter_by(template_id=template_id).all()
    # return render_template('template_details.html', template=Template.query.get_or_404(template_id), template_sections=TemplateSection.query.filter_by(template_id=template_id).all(), sections=sections)


@main_blueprint.route(
    "/templates/<int:template_id>/sections/<int:section_id>", methods=["DELETE"]
)
def delete_section(template_id, section_id):
    section = TemplateSection.query.get_or_404(section_id)
    db.session.delete(section)
    db.session.commit()
    # Retorna o cabeçalho HX-Redirect para redirecionar para 'template_details'
    response = jsonify(message="Seção excluída")
    response.headers["HX-Redirect"] = url_for(
        "main.template_details", template_id=template_id
    )
    return response
    # return redirect(url_for('template_details', template_id=template_id), code=303)


@main_blueprint.route("/templates/<int:template_id>/risks", methods=["GET", "POST"])
def template_risks(template_id):
    if request.method == "POST":
        # Process the form data and add the risk to the database
        if (
            "template_question_id"
            and "template_response_value"
            and "risk_impact"
            and "risk_likelihood"
            and "risk_description" in request.form
        ):
            template_question_id = request.form["template_question_id"]
            template_response_value = request.form["template_response_value"]
            risk_impact = int(request.form["risk_impact"])
            risk_likelihood = int(request.form["risk_likelihood"])
            risk_level = calculate_risk_level(risk_impact, risk_likelihood)
            risk_description = request.form["risk_description"]
            risk = TemplateRisk(
                template_id=template_id,
                template_question_id=template_question_id,
                template_response_value=template_response_value,
                risk_impact=risk_impact,
                risk_likelihood=risk_likelihood,
                risk_level=risk_level,
                risk_description=risk_description,
            )
            db.session.add(risk)
            db.session.commit()
            return redirect(url_for("main.template_risks", template_id=template_id))
    template = Template.query.get_or_404(template_id)
    template_questions = TemplateQuestion.query.join(TemplateSection).filter(
        TemplateSection.template_id == template_id
    )
    template_risks = (
        TemplateRisk.query.join(TemplateQuestion)
        .join(TemplateSection)
        .filter(TemplateRisk.template_id == template_id)
    )
    # print(dir(template_risks[0].template_question))
    risk_impacts = ["Muito Baixo", "Baixo", "Médio", "Alto", "Muito Alto"]
    risk_likelihoods = ["1% - 20%", "21% - 40%", "41% - 60%", "61% - 80%", "81% - 100%"]
    risk_levels = [
        "Muito Baixo",
        "Muito Baixo",
        "Muito Baixo",
        "Muito Baixo",
        "Muito Baixo",
        "Baixo",
        "Baixo",
        "Baixo",
        "Baixo",
        "Baixo",
        "Médio",
        "Médio",
        "Médio",
        "Médio",
        "Médio",
        "Alto",
        "Alto",
        "Alto",
        "Alto",
        "Alto",
        "Muito Alto",
        "Muito Alto",
        "Muito Alto",
        "Muito Alto",
        "Muito Alto",
    ]
    return render_template(
        "template_risks.html",
        template=template,
        template_questions=template_questions,
        template_risks=template_risks,
        risk_levels=risk_levels,
        risk_likelihoods=risk_likelihoods,
        risk_impacts=risk_impacts,
    )
    # query = text("SELECT * FROM template t JOIN template_section ts ON t.id = ts.template_id JOIN template_question tq ON ts.id = tq.section_id LEFT JOIN template_risk tr ON tq.id = tr.template_question_id WHERE t.id = :id;")
    # results = db.session.execute(query, {"id": template_id}).all()


@main_blueprint.route("/filter-components", methods=["GET"])
def filter_components():
    search_term = request.args.get("search", "").lower()

    # Filtra os componentes pelo nome
    filtered_components = Component.query.filter(
        Component.name.ilike(f"%{search_term}%")
    ).all()

    # Renderiza o partial com os componentes filtrados
    return render_template(
        "partials/_component_options.html", components=filtered_components
    )


def section_questions(section_id):
    questions = TemplateQuestion.query.filter_by(section_id=section_id).all()
    return render_template(
        "section_questions.html", section_id=section_id, template_questions=questions
    )


@main_blueprint.route(
    "/templates/sections/<int:section_id>/questions", methods=["GET", "POST"]
)
def questions(section_id):
    if request.method == "POST":
        # Process the form data and add the question to the database
        if "title" in request.form and "risk_level" in request.form:
            risk_level = request.form["risk_level"]
        if "title" in request.form and "response_type" in request.form:
            last_question_number = (
                TemplateQuestion.query.filter_by(section_id=section_id)
                .order_by(TemplateQuestion.number.desc())
                .first()
            )
            if last_question_number:
                question_number = last_question_number.number + 1
            else:
                question_number = 1

            # Verifica a presença de 'required' e ajusta
            required = False
            if "required" in request.form and request.form["required"] == "on":
                required = True

            question = TemplateQuestion(
                title=request.form["title"],
                risk_level=risk_level,
                number=question_number,
                section_id=section_id,
                response_type=request.form["response_type"],
                required=required,
            )
            db.session.add(question)
            db.session.commit()

    return render_template(
        "section_questions.html",
        template_section=TemplateSection.query.get_or_404(section_id),
        template_questions=TemplateQuestion.query.filter_by(
            section_id=section_id
        ).all(),
        components=Component.query.all(),
    )


@main_blueprint.route(
    "/templates/sections/<int:section_id>/components", methods=["POST"]
)
def section_components(section_id):
    if request.method == "POST":
        # Process the form data and add the component to the database
        if "component_id" in request.form:
            component_id = request.form["component_id"]
            section = TemplateSection.query.get_or_404(section_id)
            section.component_id = component_id
            db.session.commit()
        return redirect(
            url_for("main.template_details", template_id=section.template_id)
        )


@main_blueprint.route(
    "/templates/sections/questions/<int:question_id>", methods=["DELETE"]
)
def delete_question(question_id):
    question = TemplateQuestion.query.get_or_404(question_id)
    section_id = question.section_id
    db.session.delete(question)
    db.session.commit()
    return render_template(
        "section_questions.html",
        template_section=TemplateSection.query.get_or_404(section_id),
        template_questions=TemplateQuestion.query.filter_by(
            section_id=section_id
        ).all(),
        components=Component.query.all(),
    )


@main_blueprint.route("/questionnaires", methods=["GET"])
def questionnaires():
    questionnaires = Questionnaire.query.all()
    return render_template("questionnaires.html", questionnaires=questionnaires)


@main_blueprint.route("/questionnaires/<int:questionnaire_id>", methods=["GET"])
def questionnaire_details(questionnaire_id):
    questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
    return render_template("questionnaires_details.html", questionnaire=questionnaire)


@main_blueprint.route("/questionnaires/<int:questionnaire_id>", methods=["DELETE"])
def delete_questionnaire(questionnaire_id):
    if request.method == "DELETE":
        questionnaire = Questionnaire.query.get_or_404(questionnaire_id)
        db.session.delete(questionnaire)
        db.session.commit()
        response = jsonify(message="Questionário excluído")
        response.headers["HX-Redirect"] = url_for("main.questionnaires")
        return response


@main_blueprint.route(
    "/questionnaires/<int:questionnaire_id>/sections", methods=["GET"]
)
def sections(questionnaire_id):
    sections = Section.query.filter_by(questionnaire_id=questionnaire_id).all()
    # Variável para armazenar a seção selecionada
    selected_section_id = request.args.get("selected_section_id", None, type=int)
    return render_template(
        "partials/sections.html",
        sections=sections,
        selected_section_id=selected_section_id,
    )


@main_blueprint.route(
    "/questionnaires/sections/<int:section_id>/questions", methods=["GET"]
)
def list_questions(section_id):
    questions = Question.query.filter_by(section_id=section_id).all()
    return render_template("questions.html", questions=questions)


@main_blueprint.route("/questions/<int:question_id>/answer", methods=["POST"])
def answer_question(question_id):
    if request.method == "POST":
        answer = request.form["response"]
        question = Question.query.get_or_404(question_id)
        question.response = answer
        db.session.commit()
        return render_template(
            "components/success_message.html", message="Resposta salva com sucesso!✍️"
        )


@main_blueprint.route("/question/<int:question_id>/risk_level", methods=["GET"])
def question_risk_level(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template("components/risk_level.html", question=question)


@main_blueprint.route("/questionnaires/start", methods=["GET", "POST"])
def start_questionnaire():
    draft_start_questionnaire = DraftStartQuestionnaire.query.first()
    if request.method == "POST":
        questionnaire = Questionnaire(
            title=draft_start_questionnaire.title,
            template_id=draft_start_questionnaire.template_id,
            customer_id=draft_start_questionnaire.customer_id,
        )
        db.session.add(questionnaire)
        db.session.commit()
        sections = TemplateSection.query.filter_by(
            template_id=questionnaire.template_id
        ).all()
        for section in sections:
            questionnaire_section = Section(
                name=section.name,
                number=section.number,
                questionnaire_id=questionnaire.id,
            )
            db.session.add(questionnaire_section)
            questions = TemplateQuestion.query.filter_by(section_id=section.id).all()
            for question in questions:
                questionnaire_question = Question(
                    title=question.title,
                    number=question.number,
                    response_type=question.response_type,
                    required=question.required,
                    risk_level=question.risk_level,
                    section_id=questionnaire_section.id,
                )
                db.session.add(questionnaire_question)
                db.session.commit()
        db.session.delete(draft_start_questionnaire)
        db.session.commit()
        response = jsonify(message="Questionário iniciado!👌")
        response.headers["HX-Redirect"] = url_for("main.questionnaires")
        return response
    if draft_start_questionnaire is None:
        return redirect(url_for("main.handle_step", step=1))
    if (
        draft_start_questionnaire.title is not None
        and draft_start_questionnaire.template_id is not None
        and draft_start_questionnaire.customer_id is not None
    ):
        return redirect(url_for("main.handle_step", step=2))
    if (
        draft_start_questionnaire.template_id is not None
        and draft_start_questionnaire.title is not None
    ):
        return render_template("start_questionnaire.html", step=2)
    return render_template("start_questionnaire.html", step=1)


@main_blueprint.route("/questionnaires/start/<int:step>", methods=["GET", "POST"])
def handle_step(step):
    if request.method == "POST":
        if step == 1:
            if "questionnaire_template" and "questionnaire_customer" in request.form:
                template_id = request.form["questionnaire_template"]
                template = Template.query.filter_by(id=template_id).first()
                customer_id = request.form["questionnaire_customer"]
                customer = Customer.query.filter_by(id=customer_id).first()
                title = template.name + " - " + customer.name
                draft_start_questionnaire = DraftStartQuestionnaire.query.first()
                if draft_start_questionnaire:
                    draft_start_questionnaire.title = title
                    draft_start_questionnaire.template_id = template_id
                    draft_start_questionnaire.customer_id = customer_id
                    db.session.commit()
                    return redirect(url_for("main.handle_step", step=2))
                draft_start_questionnaire = DraftStartQuestionnaire(
                    title=title, template_id=template_id, customer_id=customer_id
                )
                db.session.add(draft_start_questionnaire)
                db.session.commit()
                return redirect(url_for("main.handle_step", step=2))
        elif step == 2:
            if "questionnaire_title" in request.form:
                title = request.form["questionnaire_title"]
                draft_start_questionnaire = DraftStartQuestionnaire.query.first()
                draft_start_questionnaire.title = title
                db.session.commit()
            draft_questionnaire_components = DraftQuestionnaireComponent.query.all()
            for dqc in draft_questionnaire_components:
                if (
                    request.form["component_id_{}".format(dqc.id)]
                    and request.form["component_amount_{}".format(dqc.id)]
                ):
                    component_id = request.form["component_id_{}".format(dqc.id)]
                    component_amount = request.form[
                        "component_amount_{}".format(dqc.id)
                    ]
                    dqc.component_id = component_id
                    dqc.component_amount = component_amount
                    db.session.commit()
            return redirect(url_for("main.handle_step", step=3))
        elif step == 3:
            return redirect(url_for("main.questionnaires"))
    draft_start_questionnaire = DraftStartQuestionnaire.query.first()
    if step == 1:
        templates = Template.query.all()
        customers = Customer.query.all()
        return render_template(
            "first_step_start_questionnaire.html",
            draft_start_questionnaire=draft_start_questionnaire,
            templates=templates,
            customers=customers,
            step=step,
        )
    elif step == 2:
        template = Template.query.filter_by(
            id=draft_start_questionnaire.template_id
        ).first()
        sections = TemplateSection.query.filter_by(template_id=template.id).all()
        for section in sections:
            if section.component_id:
                draft_questionnaire_component = (
                    DraftQuestionnaireComponent.query.filter_by(
                        component_id=section.component_id
                    ).first()
                )
                if not draft_questionnaire_component:
                    draft_questionnaire_component = DraftQuestionnaireComponent(
                        component_id=section.component_id,
                        component_amount=1,
                        draft_start_questionnaire_id=draft_start_questionnaire.id,
                    )
                    db.session.add(draft_questionnaire_component)
                    db.session.commit()
        draft_questionnaire_components = DraftQuestionnaireComponent.query.filter_by(
            draft_start_questionnaire_id=draft_start_questionnaire.id
        ).all()
        components = Component.query.all()
        return render_template(
            "second_step_start_questionnaire.html",
            draft_start_questionnaire=draft_start_questionnaire,
            draft_questionnaire_components=draft_questionnaire_components,
            components=components,
            step=step,
        )
    elif step == 3:
        draft_questionnaire_components = DraftQuestionnaireComponent.query.filter_by(
            draft_start_questionnaire_id=draft_start_questionnaire.id
        ).all()
        return render_template(
            "third_step_start_questionnaire.html",
            draft_start_questionnaire=draft_start_questionnaire,
            draft_questionnaire_components=draft_questionnaire_components,
            step=step,
        )
    else:
        return render_template("partials/fourth_step_start_questionnaire.html")


@main_blueprint.route("/questionnaires/start/template", methods=["GET"])
def render_template_title():
    template_id = request.args.get("questionnaire_template")
    template = Template.query.filter_by(id=template_id).first()
    if template:
        template_name = template.name
        return render_template(
            "components/template_title.html", template_name=template_name
        )
    else:
        return render_template("components/template_title.html")
    # return Response("Erro", status=404)


@main_blueprint.route("/questionnaires/draft/component/<int:id>", methods=["PATCH"])
def update_draft_questionnaire_component(id):
    draft_questionnaire_component = DraftQuestionnaireComponent.query.get_or_404(id)
    if "component_amount" in request.args:
        component_amount = request.args.get("component_amount")
        draft_questionnaire_component.component_amount = component_amount
        db.session.commit()
        return jsonify(message="Componente atualizado")
    else:
        return jsonify(message="Erro")
