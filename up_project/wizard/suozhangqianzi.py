# -*- coding: utf-8 -*-
from osv import osv, fields


class updis_project(osv.Model):
    _inherit = 'project.project'
    _columns = {
        'director_approve': fields.many2one('res.users', string="Director Approve"),

    }

    def director_approve_submit(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids,
                   {'director_approve': uid,
                    'project_logs': [(0, 0,
                                      {'project_id': ids[0],
                                       'log_user': uid,
                                       'log_info': u'所长签字通过'})]})
        self._workflow_signal(cr, uid, ids, 'fuzeren_submit')
        return True


    def zongshishi_reject(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids,
                   {'project_logs': [(0, 0,
                                      {'project_id': ids[0],
                                       'log_user': uid,
                                       'log_info': u'所长未通过,打回总师室'})]})
        self._workflow_signal(cr, uid, ids, 'zongshishi_reject')
        return True

