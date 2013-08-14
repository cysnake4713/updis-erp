# -*- encoding:utf-8 -*-
import datetime
from openerp.osv import fields
from openerp.osv import osv

__author__ = 'cysnake4713'


class project_active_tasking_engineer(osv.osv_memory):
    _name = "project.project.active.tasking.engineer"
    _description = "Project Active Tasking"

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        res = super(project_active_tasking_engineer, self).default_get(cr, uid, fields, context=context)
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        if not record_id:
            return res
        tasking_pool = self.pool.get('project.project.active.tasking')
        tasking = tasking_pool.browse(cr, uid, record_id, context=context)

        if 'categories_id' in fields:
            res['categories_id'] = tasking.categories_id.id if tasking.categories_id else None
            # if 'category_name' in fields:
        #     res['category_name'] = tasking.category_name
        if 'guanlijibie' in fields:
            res['guanlijibie'] = tasking.guanlijibie
        if 'categories_else' in fields:
            res['categories_else'] = tasking.categories_else
        if 'tender_category' in fields:
            res['tender_category'] = tasking.tender_category
        if 'zhuguanzongshi_id' in fields:
            res['zhuguanzongshi_id'] = [z.id for z in tasking.zhuguanzongshi_id]
        if 'shifoutoubiao' in fields:
            res['shifoutoubiao'] = tasking.shifoutoubiao
        if 'user_id' in fields:
            user_ids = tasking_pool.read(cr, uid, record_id, ['user_id'], context=context)
            if user_ids['user_id']:
                res['user_id'] = [u.id for u in
                                  self.pool.get('res.users').browse(cr, 1, user_ids['user_id'], context=context)]
            else:
                res['user_id'] = None
        if 'project_type' in fields:
            res['project_type'] = tasking.project_type.id if tasking.project_type else None

        return res


    _columns = {
        "shifoutoubiao": fields.boolean(string="is Tender?"),
        "project_type": fields.many2one("project.type", string="Project Type", ),
        "categories_id": fields.many2one("project.upcategory", u"项目类别"),
        "category_name": fields.related('categories_id', 'name', type='char', string="Project Category Name"),
        "guanlijibie": fields.selection([('LH200307240001', u'院级'), ('LH200307240002', u'所级')], u'项目管理级别'),
        "categories_else": fields.char(size=128, string='Else Category'),
        "tender_category": fields.selection([('business', u'商务标'), ('technology', u'技术标'), ('complex', u'综合标')],
                                            u"投标类别"),
        'user_id': fields.many2many('res.users', 'wizard_tasking_user_id', 'project_user_id', 'res_user_id',
                                    string='Project Manager'),
        "zhuguanzongshi_id": fields.many2many("res.users", "tasking_zongshi_res_user", "tasking_id", "res_user_id",
                                              u"主管总师"),
    }

    def engineer_review_accept(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        tasking = self.pool.get("project.project.active.tasking").browse(cr, uid, record_id, context)
        self_record = self.browse(cr, uid, ids[0], context)
        tasking.write({
            'categories_id': self_record.categories_id.id if self_record.categories_id else None,
            # 'category_name': self_record.category_name,
            'guanlijibie': self_record.guanlijibie,
            'user_id': [(6, 0, [u.id for u in self_record.user_id])],
            'categories_else': self_record.categories_else,
            'tender_category': self_record.tender_category,
            'zhuguanzongshi_id': [(6, 0, [z.id for z in self_record.zhuguanzongshi_id])],
            'project_type': self_record.project_type.id if self_record.project_type else None,

        })
        return tasking.engineer_review_accept()

    def onchange_category_id(self, cr, uid, ids, category_id, context=None):
        ret = {'value': {}}
        if category_id:
            category = self.pool.get('project.upcategory').browse(cr, uid, category_id)
            sms_vals = {
                'category_name': category.name,
            }
            ret['value'].update(sms_vals)
        return ret

    def onchange_type_id(self, cr, uid, ids, type_id, context=None):
        ret = {'value': {}}
        sms_vals = {
            'category_name': "",
            'categories_id': None,
        }
        ret['value'].update(sms_vals)
        return ret


class project_active_tasking_operator(osv.osv_memory):
    _name = "project.project.active.tasking.operator"

    def default_get(self, cr, uid, fields, context=None):
        """
        This function gets default values
        """
        res = super(project_active_tasking_operator, self).default_get(cr, uid, fields, context=context)
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        if not record_id:
            return res
        tasking_pool = self.pool.get('project.project.active.tasking')
        tasking = tasking_pool.browse(cr, uid, record_id, context=context)

        if 'xiangmubianhao' in fields:
            res['xiangmubianhao'] = tasking.xiangmubianhao
        if 'pingshenfangshi' in fields:
            res['pingshenfangshi'] = tasking.pingshenfangshi
        if 'yinfacuoshi' in fields:
            res['yinfacuoshi'] = tasking.yinfacuoshi
        if 'renwuyaoqiu' in fields:
            res['renwuyaoqiu'] = tasking.renwuyaoqiu
        if 'chenjiebumen_id' in fields:
            res['chenjiebumen_id'] = tasking.chenjiebumen_id.id if tasking.chenjiebumen_id else None

        return res


    _columns = {
        ##Operator Room
        "xiangmubianhao": fields.char(u"项目编号", select=True, size=128, ),
        "pingshenfangshi": fields.selection([(u'会议', u'会议'), (u'会签', u'会签'), (u'审批', u'审批')], u"评审方式"),
        "yinfacuoshi": fields.selection([(u'可以接受', u'可以接受'), (u'不接受', u'不接受'), (u'加班', u'加班'),
                                         (u'院内调配', u'院内调配'), (u'外协', u'外协'), (u'其它', u'其它')], u"引发措施记录"),
        "renwuyaoqiu": fields.selection([(u'见委托书', u'见委托书'), (u'见合同草案', u'见合同草案'), (u'见洽谈记录', u'见洽谈记录'),
                                         (u'见电话记录', u'见电话记录'), (u'招标文件', u'招标文件')], u"任务要求"),
        "chenjiebumen_id": fields.many2one("hr.department", u"承接部门"),
    }

    def operator_review_accept(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        record_id = context and context.get('active_id', False) or False
        tasking = self.pool.get("project.project.active.tasking").browse(cr, uid, record_id, context)
        self_record = self.browse(cr, uid, ids[0], context)
        tasking.write({
            'xiangmubianhao': self_record.xiangmubianhao,
            'pingshenfangshi': self_record.pingshenfangshi,
            'yinfacuoshi': self_record.yinfacuoshi,
            'renwuyaoqiu': self_record.renwuyaoqiu,
            'chenjiebumen_id': self_record.chenjiebumen_id.id if self_record.chenjiebumen_id else None,

        })
        return tasking.operator_review_accept()


class project_active_tasking(osv.osv):
    _log_access = True
    _name = "project.project.active.tasking"
    _inherits = {'project.project': "project_id"}
    _form_name = u'产品要求评审及任务下达记录'

    _rec_name = 'form_name'

    def workflow_signal(self, cr, uid, ids, signal):
        return self._workflow_signal(cr, uid, ids, signal)

    def _is_display_button(self, cr, uid, ids, field_name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            review_id = obj.director_reviewer_id
            if review_id and review_id.id == uid:
                result[obj.id] = True
            else:
                result[obj.id] = False
        return result

    def _is_wait_user_process(self, cr, uid, ids, field_name, args, context=None):
        result = dict.fromkeys(ids, False)
        if context is None:
            context = {}
        current_uid = context and context.get('uid', False) or False
        for obj in self.browse(cr, uid, ids, context=context):
            result_flag = False
            if obj.state == 'open':
                if obj.create_uid and current_uid == obj.create_uid.id:
                    result_flag = True
            if obj.state == 'suozhangshenpi':
                if obj.director_reviewer_id and current_uid == obj.director_reviewer_id.id:
                    result_flag = True
            if obj.state == 'zhidingbumen':
                if self.user_has_groups(cr, uid, 'up_project.group_up_project_jingyingshi', context=context):
                    result_flag = True
            if obj.state == 'zhidingfuzeren':
                if self.user_has_groups(cr, uid, 'up_project.group_up_project_zongshishi', context=context):
                    result_flag = True
            if obj.state == 'suozhangqianzi':
                project = self.pool.get('project.project.active.tasking')
                user_ids = project.read(cr, uid, obj.id, ['user_id'], context=context)
                if current_uid in user_ids['user_id']:
                    result_flag = True

            result[obj.id] = result_flag
        return result

    _columns = {
        'is_display_button': fields.function(_is_display_button, type="boolean",
                                             string="Is Display Button"),
        'form_name': fields.char(size=128, string="Form Name"),
        "project_id": fields.many2one('project.project', string='Related Project', ondelete="cascade",
                                      required=True),
        "state": fields.selection([
                                      # ("draft",u"New project"),
                                      ("open", u"提出申请"),
                                      ("suozhangshenpi", u"所长审批"),
                                      ("zhidingbumen", u"经营室审批"),
                                      ("zhidingfuzeren", u"总师室审批"),
                                      ("suozhangqianzi", u"负责人签字"),
                                      ("end", u'表单归档'),
                                  ], "State", help='When project is created, the state is \'open\''),

        "partner_address": fields.related('partner_id', "street", type="char", string='Custom Address'),


        #Director apply
        "yaoqiuxingchengwenjian": fields.selection([
                                                       (u"已形成", u"已形成"),
                                                       (u"未形成，但已确认", u"未形成，但已确认")],
                                                   u"顾客要求形成文件否"),
        "express_requirement": fields.selection([(u"有招标书", u"有招标书"), (u"有委托书", u"有委托书"),
                                                 (u"有协议/合同草案", u"有协议/合同草案"), (u"有口头要求记录", u"有口头要求记录")],
                                                string="Express Requirement"),

        "yinhanyaoqiu": fields.selection([(u"有", u"有（需在评审记录一栏中标明记录）"), (u"无", u"无")], u"隐含要求"),
        "difangfagui": fields.selection([(u"有", u"有（需在评审记录一栏中标明记录）"), (u"无", u"无")], u"地方规范或特殊法律法规", ),
        "fujiayaoqiu": fields.selection([(u"有", u"有（需在评审记录一栏中标明记录）"), (u"无", u"无")], u"附加要求", ),
        "hetongyizhi": fields.selection([(u"合同/协议要求表述不一致已解决", u"合同/协议要求表述不一致已解决"),
                                         (u"没有出现不一致", u"没有出现不一致")], u"不一致是否解决", ),
        "ziyuan": fields.selection([(u'人力资源满足', u'人力资源满足'), (u'人力资源不足', u'人力资源不足')], u'人力资源', ),
        "shebei": fields.selection([(u'设备满足', '设备满足'), (u'设备不满足', u'设备不满足')], u"设备", ), #本院是否有能力满足规定要求
        "gongqi": fields.selection([(u'工期可接受', '工期可接受'), (u'工期太紧', u'工期太紧')], u"工期", ), #本院是否有能力满足规定要求
        "shejifei": fields.selection([(u'设计费合理', '设计费合理'), (u'设计费太低', u'设计费太低')], u'设计费', ), #本院是否有能力满足规定要求


        "duofanghetong": fields.boolean(u"多方合同"),
        "jianyishejibumen_id": fields.many2one("hr.department", u"建议设计部门"),
        "jianyixiangmufuzeren_id": fields.many2many("res.users", "tasking_jianyi_manager_user_id", "tasking_user_id",
                                                    "res_user_id", u"建议项目负责人"),


        'director_reviewer_apply_id': fields.many2one('res.users', string=u'Review Apply By'),
        'director_reviewer_apply_image': fields.related('director_reviewer_apply_id', "sign_image", type="binary",
                                                        string=u'Review Image'),
        'director_reviewer_apply_time': fields.datetime(string="Director Reviewer Approve Time"),

        'director_approve': fields.many2one('res.users', string="Director Approve"),
        'director_approve_image': fields.related('director_approve', "sign_image", type="binary",
                                                 string=u'Review Image'),
        'director_approve_time': fields.datetime(string="Director Approve Time"),

        ##Operator Room

        "pingshenfangshi": fields.selection([(u'会议', u'会议'), (u'会签', u'会签'), (u'审批', u'审批')], u"评审方式"),
        "yinfacuoshi": fields.selection([(u'可以接受', u'可以接受'), (u'不接受', u'不接受'), (u'加班', u'加班'),
                                         (u'院内调配', u'院内调配'), (u'外协', u'外协'), (u'其它', u'其它')], u"引发措施记录"),
        "renwuyaoqiu": fields.selection([(u'见委托书', u'见委托书'), (u'见合同草案', u'见合同草案'), (u'见洽谈记录', u'见洽谈记录'),
                                         (u'见电话记录', u'见电话记录'), (u'招标文件', u'招标文件')], u"任务要求"),


        "jinyinshi_submitter_id": fields.many2one('res.users', string=u"Operator Room Submitter"),
        "jinyinshi_submitter_id_image": fields.related('jinyinshi_submitter_id', "sign_image", type="binary",
                                                       string=u'Review Image'),
        "jinyinshi_submitter_datetime": fields.datetime(string=u"Operator Room Submit Date"),

        #Engineer Room
        # 'is_tender_project': fields.related('project_id', 'shifoutoubiao', type='boolean', string=u'is Tender Project'),

        "category_name": fields.related("categories_id", 'name', type="char", string="Category Name"),

        "categories_else": fields.char(size=128, string='Else Category'),
        "tender_category": fields.selection([('business', u'商务标'), ('technology', u'技术标'), ('complex', u'综合标')],
                                            u"投标类别"),
        "zongshishi_submitter_id": fields.many2one("res.users", string=u"Zongshishi Submitter"),
        "zongshishi_submitter_id_image": fields.related('zongshishi_submitter_id', "sign_image", type="binary",
                                                        string=u'Review Image'),
        "zongshishi_submit_datetime": fields.datetime(string=u"Zongshishi Submit Date"),

        'is_wait_user_process': fields.function(_is_wait_user_process, type="boolean",
                                                string="Is User is The Project Manager"),

    }

    _defaults = {
        'form_name': _form_name,
        'state': 'open',

    }


    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        ret = {'value': {}}
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
            state_name = partner.state_id and partner.state_id.name or ""
            country_name = partner.country_id and partner.country_id.name or ""
            city = partner.city and partner.city or ""
            street = partner.street and partner.street or ""
            street2 = partner.street2 and partner.street2 or ""
            if country_name == "China":
                country_name = u"中国"

            sms_vals = {
                'partner_address': "%s" % (street)
            }
            ret['value'].update(sms_vals)
        else:
            sms_vals = {
                'partner_address': ""
            }
            ret['value'].update(sms_vals)
        return ret

    def onchange_category_id(self, cr, uid, ids, category_id, context=None):
        ret = {'value': {}}
        if category_id:
            category = self.pool.get('project.upcategory').browse(cr, uid, category_id)
            sms_vals = {
                'category_name': category.name,
            }
            ret['value'].update(sms_vals)
        return ret

    def _sign_form(self, cr, uid, ids, submitter_id_field_name, submit_date_field_name, is_clean=False, context=None):
        if not is_clean:
            self.write(cr, uid, ids, {submitter_id_field_name: uid, submit_date_field_name: datetime.datetime.now()},
                       context=context)
        else:
            self.write(cr, uid, ids, {submitter_id_field_name: None, submit_date_field_name: None},
                       context=context)

    def _send_workflow_signal(self, cr, uid, ids, log_info, signal, context=None):
        project = self.pool.get('project.project')
        suozhangshenpi = self.browse(cr, uid, ids, context=None)
        if suozhangshenpi and suozhangshenpi[0].project_id:
            project.write(cr, uid, suozhangshenpi[0].project_id.id,
                          {'project_logs': [(0, 0, {'project_id': suozhangshenpi[0].project_id.id,
                                                    'log_user': uid,
                                                    'log_info': log_info})]})
            self._workflow_signal(cr, uid, ids, signal)
            return True
        else:
            return False


    def director_review_submit(self, cr, uid, ids, context=None):
        suozhangshenpi = self.browse(cr, uid, ids, context=None)
        log_info = u'提交所长审批请求到--> %s' % suozhangshenpi[0].director_reviewer_id.name
        return self._send_workflow_signal(cr, uid, ids, log_info, 'draft_submit')

    def director_review_accept(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'director_reviewer_apply_id', 'director_reviewer_apply_time', context=context)
        log_info = u'所长审批通过,提交请求到经营室'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'suozhangshenpi_submit')

    def draft_reject(self, cr, uid, ids, context=None):
        # self._sign_form(cr, uid, ids, 'director_reviewer_apply_id', 'director_reviewer_apply_time', is_clean=True,
        #                 context=context)
        log_info = u'所长打回申请单'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'draft_reject')


    def operator_review_accept(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'jinyinshi_submitter_id', 'jinyinshi_submitter_datetime', context=context)
        log_info = u'经营室审批通过,提交申请到总师室'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'jingyinshi_submit')

    def operator_reject(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'director_reviewer_apply_id', 'director_reviewer_apply_time', is_clean=True,
                        context=context)
        log_info = u'经营室打回申请单'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'suozhangshenpi_reject')


    def engineer_review_accept(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'zongshishi_submitter_id', 'zongshishi_submit_datetime', context=context)
        log_info = u'总师室审批通过,提交请求到负责人'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'zongshishi_submit')

    def engineer_reject(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'jinyinshi_submitter_id', 'jinyinshi_submitter_datetime', is_clean=True,
                        context=context)
        log_info = u'总师室打回申请单'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'jingyinshi_reject')


    def manager_review_accept(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'director_approve', 'director_approve_time', context=context)
        log_info = u'负责人确认,启动项目'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'fuzeren_submit')

    def manager_reject(self, cr, uid, ids, context=None):
        self._sign_form(cr, uid, ids, 'zongshishi_submitter_id', 'zongshishi_submit_datetime', is_clean=True,
                        context=context)
        log_info = u'负责人打回申请单'
        return self._send_workflow_signal(cr, uid, ids, log_info, 'zongshishi_reject')


    def workflow_director_submit(self, cr, uid, ids, context=None):
        tasking = self.browse(cr, 1, ids[0], context=context)
        self.write(cr, 1, ids,
                   {'state': 'suozhangshenpi', 'status_code': 10102,
                    'related_user_id': tasking.director_reviewer_id.id},
                   context=context)
        return True


    def workflow_operator_room(self, cr, uid, ids, context=None):
        tasking = self.browse(cr, 1, ids[0], context=context)
        self.write(cr, 1, ids,
                   {'chenjiebumen_id': tasking.jianyishejibumen_id.id, 'state': 'zhidingbumen', 'status_code': 10103, },
                   context=context)
        return True

    def workflow_engineer_room(self, cr, uid, ids, context=None):
        tasking = self.browse(cr, 1, ids[0], context=context)
        self.write(cr, 1, ids, {'tender_category': tasking.toubiaoleibie,
                                'user_id': [(6, 0, [j.id for j in tasking.jianyixiangmufuzeren_id])],
                                'state': 'zhidingfuzeren',
                                'status_code': 10104},
                   context=context)
        return True

    def workflow_manager_room(self, cr, uid, ids, context=None):
        tasking = self.browse(cr, 1, ids[0], context=context)
        if not tasking.is_import:
            self.write(cr, 1, ids, {'state': 'end', 'status_code': 10106, 'begin_date': datetime.date.today()},
                       context=context)
        else:
            self.write(cr, 1, ids, {'state': 'end', 'status_code': 10106, },
                       context=context)

        return True


class project_project_inherit(osv.osv):
    _inherit = 'project.project'
    _name = 'project.project'

    _columns = {
        'active_tasking': fields.many2one("project.project.active.tasking", string='Active Tasking Form',
                                          ondelete="cascade"),
        'active_tasking_is_wait_user_process': fields.related('active_tasking', 'is_wait_user_process', type='boolean',
                                                              string="Active Tasking Is Waiting User"),
        'active_tasking_state': fields.related('active_tasking', 'state', type='selection', selection=[
            # ("draft",u"New project"),
            ("open", u"提出申请"),
            ("suozhangshenpi", u"所长审批"),
            ("zhidingbumen", u"经营室审批"),
            ("zhidingfuzeren", u"总师室审批"),
            ("suozhangqianzi", u"负责人签字"),
            ("end", u'归档'),
        ], string='Tasking State'),
    }

    def act_active_tasking(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state': 'project_active', 'state_active': 'project_active_tasking'})
        return self.init_form(cr, uid, ids, "project.project.active.tasking", 'active_tasking', context=context)


