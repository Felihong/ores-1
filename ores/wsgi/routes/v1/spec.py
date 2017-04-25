import json
from urllib.parse import urlparse

from flask import render_template, request

from ... import preprocessors, util


def configure(config, bp, score_processor):

    # /spec/
    @bp.route("/v1/spec/", methods=["GET"])
    @preprocessors.nocache
    @preprocessors.minifiable
    def v1_spec():
        return generate_spec()

    return bp


def generate_spec():
    return util.jsonify(json.loads(render_template(
        "v1_swagger.json",
        host=urlparse(request.url_root).netloc,
        scheme=urlparse(request.url_root).scheme)))
