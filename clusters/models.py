from flask_restplus import fields
from run import api
from common.models import meta

cluster_base = api.model('cluster', {
    'cluster_name': fields.String(description="Cluster Name"),
    'cluster_id': fields.String(description="Cluster Id"),
})
