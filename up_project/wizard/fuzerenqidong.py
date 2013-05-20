# -*- coding: utf-8 -*-
from osv import osv,fields
from tools.translate import _
from . import common

class fuzerenqidong_form(osv.Model):
	"""项目负责人启动项目"""
	_name="project.review.fuzerenqidong.form"
	_description=u"经营室审批"
	_inherit=['project.review.abstract']
	_columns={
		'shizhengxietiaoren_id':fields.many2one("res.users",u"市政协调人"),
		'gongzuodagang':fields.boolean(u'有工作大纲（保存归档）'),
		'chuangyouxiangmu':fields.boolean(u'创优项目'),
		'zhuantihuozixiang':fields.boolean(u'专题或子项（详见工作大纲）'),
		'youfenbaofang':fields.boolean(u'有分包方（详见分包协议）'),
		'project_assignment_ids':fields.many2many("project.assignment",'fuzerenqidong_assignment_rel',"fuzerenqidong_form_id","assignment_id",string="Assignments"),
		#'assignment_ids':fields.related('project_id','assignment_ids',relation="project.assignment", type="one2many",string="Assignment"),
		'state':fields.selection([
			('draft',u'项目负责人创建'),
			(u'设计部门负责人签字',u'设计部门负责人签字'),
			(u'配合部门负责人签字',u'配合部门负责人签字')],'State',readonly=True)
	}
	_defaults={
		'state':'draft',
	}
	def update_project_fuzerenqidong_form(self,cr,uid,ids,*args):		
		return self._update_project_form(cr,uid,ids,'fuzerenqidong_form_id')
class updis_project(osv.Model):
	_inherit='project.project'	
	_columns={		
		'shizhengxietiaoren_id':fields.many2one("res.users",u"市政协调人"),
		'fuzerenqidong_form_id':fields.many2one('project.review.fuzerenqidong.form',u'项目负责人启动项目'),
	}
	def action_fuzerenqidong(self, cr, uid, ids, context=None):
		return self._get_action(cr,uid,ids,'project.review.fuzerenqidong.form',u'项目负责人启动项目')
	def test_fuzerenqidong_accepted(self, cr, uid, ids, *args):
		return self._test_accepted(cr,uid,ids,'fuzerenqidong_form_id',*args)
	def fuzerenqidong_get(self, cr, uid, ids, *args):
		return self._get_form(cr,uid,ids,'fuzerenqidong_form_id',*args)