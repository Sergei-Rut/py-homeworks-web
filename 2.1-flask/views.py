from flask import request, jsonify
from flask.views import MethodView
from app import app
from models import Advertisement
from app import db


class AdvertisementView(MethodView):

    def get(self, adv_id):
        adv = Advertisement.query.get(adv_id)
        if not adv:
            response = jsonify(
                {
                    'error': 'Adv not found'
                }
            )
            response.status_code = 404
            return response
        else:
            response = jsonify(adv.to_dict())
            return response

    def post(self):
        adv = Advertisement(**request.json)
        adv.add()
        return jsonify(adv.to_dict())

    def patch(self, adv_id):
        data = request.json
        adv = Advertisement.query.filter_by(id=adv_id).update(data)
        if adv:
            db.session.commit()
            return jsonify(
                {
                    'status': 'patched',
                    'adv_id': adv_id
                }
            )
        else:
            return jsonify({'error': 'Adv does not exist or not get permission'})

    def delete(self, adv_id):
        adv = Advertisement.query.filter_by(id=adv_id).first()
        if adv:
            Advertisement.query.filter_by(id=adv_id).delete()
            db.session.commit()
            return jsonify(
                {
                    'status': 'removed',
                    'adv_id': adv_id
                }
            )
        else:
            return jsonify({'error': 'Adv does not exist or not get permission'})


@app.route('/health/', methods=['GET', ])
def health():
    if request.method == 'GET':
        return jsonify({'status': 'OK'})

    return {'status': 'OK'}


app.add_url_rule('/advertisement/<int:adv_id>', view_func=AdvertisementView.as_view('adv_get'), methods=['GET', ])
app.add_url_rule('/advertisement/', view_func=AdvertisementView.as_view('adv_create'), methods=['POST', ])
app.add_url_rule('/advertisement/<int:adv_id>', view_func=AdvertisementView.as_view('adv_patch'), methods=['PATCH', ])
app.add_url_rule('/advertisement/<int:adv_id>', view_func=AdvertisementView.as_view('adv_delete'), methods=['DELETE', ])