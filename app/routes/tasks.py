from app import app, db, auto, ENTITY_MAPPING
from app.models import tasks
from flask import abort, jsonify, request, Response
from flask.ext.login import login_required, current_user
from dateutil import parser
import json
from sqlalchemy import or_

from app.models.bookmarks import Bookmarks
from app.models.users import KBUser
from app.routes.bookmarks import is_bookmarked, delete_bookmarks


@app.route('/ThreatKB/tasks', methods=['GET'])
@auto.doc()
@login_required
def get_all_tasks():
    """Return all active tasks

    Pagination variables:
    page_number: page number to start on, default 0
    page_size: the size of each page, default None (don't paginate)
    sort_by: column to sort by, must exist on the Task model, default None
    sort_direction: the direction to sort by if sorting, default ASC
    searches: dictionary of column filters as {column1:filter1, column2:filter2}, columns must exist on Task model, default {}

    Return: list of task dictionaries"""
    searches = request.args.get('searches', '{}')
    page_number = request.args.get('page_number', False)
    page_size = request.args.get('page_size', False)
    sort_by = request.args.get('sort_by', False)
    sort_direction = request.args.get('sort_dir', 'ASC')

    entities = tasks.Tasks.query.filter_by(active=True)

    if not current_user.admin:
        entities = entities.filter(or_(tasks.Tasks.owner_user_id == current_user.id, tasks.Tasks.owner_user_id == None))

    searches = json.loads(searches)
    for column, value in searches.items():
        if not value:
            continue

        if column == "owner_user.email":
            entities = entities.join(KBUser, tasks.Tasks.owner_user_id == KBUser.id) \
                .filter(KBUser.email.like("%" + str(value) + "%"))
            continue

        try:
            column = getattr(tasks.Tasks, column)
            entities = entities.filter(column.like("%" + str(value) + "%"))
        except:
            continue

    filtered_entities = entities
    total_count = entities.count()

    if sort_by:
        filtered_entities = filtered_entities.order_by("%s %s" % (sort_by, sort_direction))
    else:
        filtered_entities = filtered_entities.order_by("date_created DESC")

    if page_size:
        filtered_entities = filtered_entities.limit(int(page_size))

    if page_number:
        filtered_entities = filtered_entities.offset(int(page_number) * int(page_size))

    filtered_entities = filtered_entities.all()

    response_dict = dict()
    response_dict['data'] = [entity.to_dict() for entity in filtered_entities]
    response_dict['total_count'] = total_count

    return Response(json.dumps(response_dict), mimetype='application/json')


@app.route('/ThreatKB/tasks/<int:id>', methods=['GET'])
@login_required
@auto.doc()
def get_tasks(id):
    """Return task associated with given id
    Return: task dictionary"""
    entity = tasks.Tasks.query.get(id)
    if not entity:
        abort(404)

    if not current_user.admin and not entity.owner_user_id == current_user.id and not entity.owner_user_id == None:
        return jsonify({})

    return_dict = entity.to_dict()
    return_dict["bookmarked"] = True if is_bookmarked(ENTITY_MAPPING["TASK"], id, current_user.id) else False

    return jsonify(return_dict)


@app.route('/ThreatKB/tasks', methods=['POST'])
@auto.doc()
@login_required
def create_tasks():
    """Create new task
    From Data: title (str), description (str), final_artifact(str), state (str)
    Return: task dictionary"""
    entity = tasks.Tasks(
        title=request.json['title'],
        description=request.json['description'],
        final_artifact=request.json['final_artifact'],
        state=request.json['state']['state'] if 'state' in request.json['state'] else None,
        created_user_id=current_user.id,
        modified_user_id=current_user.id,
        owner_user_id=current_user.id
    )
    db.session.add(entity)
    db.session.commit()

    return jsonify(entity.to_dict()), 201


@app.route('/ThreatKB/tasks/<int:id>', methods=['PUT'])
@auto.doc()
@login_required
def update_tasks(id):
    """Update task associated with given id
    From Data: title (str), description (str), final_artifact(str), state (str)
    Return: task dictionary"""
    entity = tasks.Tasks.query.get(id)
    if not entity:
        abort(404)

    entity.title = request.json['title']
    entity.description = request.json['description']
    entity.final_artifact = request.json['final_artifact']
    entity.state = request.json['state']['state'] if request.json['state'] and 'state' in request.json['state'] else \
        request.json['state']
    entity.created_user_id = current_user.id
    entity.modified_user_id = current_user.id
    entity.owner_user_id = request.json['owner_user']['id'] if request.json.get("owner_user", None) and request.json[
        "owner_user"].get("id", None) else None,

    db.session.commit()

    entity = tasks.Tasks.query.filter(tasks.Tasks.id == entity.id).first()
    return jsonify(entity.to_dict()), 200


@app.route('/ThreatKB/tasks/<int:id>', methods=['DELETE'])
@auto.doc()
@login_required
def delete_tasks(id):
    """Delete task associated with the given id
    Return: None"""
    entity = tasks.Tasks.query.get(id)

    if not entity:
        abort(404)

    # db.session.delete(entity)
    entity.active = False
    db.session.add(entity)
    db.session.commit()

    delete_bookmarks(ENTITY_MAPPING["TASK"], id, current_user.id)

    return jsonify(''), 204
