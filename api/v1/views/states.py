#!/usr/bin/python3
"""City objects that handles all default API"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/states', strict_slashes=False,
                 methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET'])
def retrieve_state(state_id=None):
    """retrieve state obj"""
    dict_obj = storage.all(State)

    if state_id is None:
        all_obj = [obj.to_dict() for obj in dict_obj.values()]
        return jsonify(all_obj)

    obj = storage.get(State, state_id)

    if obj:
        obj_todict = obj.to_dict()
        return jsonify(obj_todict)
    else:
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """Delete a state"""

    obj = storage.get(State, state_id)

    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/', strict_slashes=False,
                 methods=['POST'])
def add_state():
    """Add a new state"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')
    if not data.get('name'):
        abort(400, 'Missing Name')

    new_state = State(**data)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id=None):
    """Update info about state"""
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, 'Not a JSON')

    obj = storage.get(State, state_id)

    if obj:
        for key, value in data.items():
            if key not in ("id", "created_at", "updated_at"):
                setattr(obj, key, value)
        storage.save()
    else:
        abort(404)

    return jsonify(obj.to_dict()), 200