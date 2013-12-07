from flask import Blueprint, request, jsonify

mod = Blueprint('attr', __name__, url_prefix='/attr')
