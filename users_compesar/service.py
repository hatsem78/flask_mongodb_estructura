from bson import ObjectId
from flask_jwt_extended import get_jwt_identity

from models import Usuarios, Cluster, Usos
from utils.db_utils import Base
from utils.helper import custom_marshal, update_timestamp
from common.constants import COLLECTIONS
import copy

base_obj = Base()


class UsersCompensarService(object):
    """
    Tasks Service
    """

    def get_user_compensar(self, id, id_type):
        """
            Get Usuarios active or inactive
            :param id:
            :return:
        """
        #records = Usuarios.objects(id_usuario__exact=id)
        #rows = Usuarios.objects(id_usuario='1000000765')
        try:
            elemento_usos = []

            record = records = Usuarios.objects(
                id_usuario__exact=id, tipo_id_usurio__exact=id_type.upper())
            if record.count() == 0:
                return {'msg': 'User Not Activated', 'code': 0}

            records = Usuarios.objects(id_usuario__exact=id, tipo_id_usurio__exact=id_type.upper()).aggregate(*[
                {
                    '$lookup': {
                        'from': Usos._get_collection_name(),
                        'localField': 'id_trabajador',
                        'foreignField': 'id_trabajador',
                        'as': 'Usos'
                    },
                },
                {
                    '$lookup': {
                        'from': Cluster._get_collection_name(),
                        'localField': 'cluster_id',
                        'foreignField': 'cluster_id',
                        'as': 'Cluster'
                    }
                },

            ])

            for element in records:
                elemento_usos = element
                elemento_usos = copy.deepcopy(elemento_usos)
                if len(element['Usos']) == 0:
                    elemento_usos['Usos'] = {'red': 0,  'aliados': 0}
                else:
                    elemento_usos['Usos'] = []
                    elemento_usos['Usos'] = {
                        "red": element['Usos'][0]['usos_red'],
                        "aliados": element['Usos'][0]['usos_aliados'],
                    }

            return elemento_usos
        except Exception as err:
            print(err)
            return err

    def create_user_compensar(self, id, payload):
        """
        Create a task in task room
        :param payload:
        :return:
        """
        #payload = custom_marshal(payload, task_db_input, 'create')
        #payload['_id'] = ObjectId()
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(id)},
                                 {"$push": {'tasks': payload}})

    def update_user_compensar(self, taskroom_id, task_id, payload):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        #email = get_jwt_identity()
        #payload = custom_marshal(payload, task_request, 'update', prefix="tasks.$")
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email},
                                 {"$set": payload})
        print(payload, result)

    def archive_user_compensar(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        email = get_jwt_identity()
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = True, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email},
                                 {"$set": payload})
        print(payload, result)

    def delete_user_compensar(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        email = get_jwt_identity()
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, True
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email},
                                 {"$set": payload})
        print(payload, result)

    def undo_user_compensar(self, taskroom_id, task_id):
        """
        Update the task id with payload
        :param taskroom_id:
        :param task_id:
        :param payload:
        :return:
        """
        email = get_jwt_identity()
        payload = update_timestamp(prefix="tasks.$")
        payload["tasks.$.meta.is_archived"], payload["tasks.$.meta.is_deleted"] = False, False
        result = base_obj.update(COLLECTIONS['ROOMS'], {'_id': ObjectId(taskroom_id), "tasks._id": ObjectId(task_id), "users": email},
                                 {"$set": payload})
        print(payload, result)
