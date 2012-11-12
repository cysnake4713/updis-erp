from osv import osv,fields
import tools

class document_page(osv.osv):
	_inherit="document.page"
	def _get_image(self, cr, uid, ids, name, args, context=None):
		result = dict.fromkeys(ids, False)
		for obj in self.browse(cr, uid, ids, context=context):
			result[obj.id] = tools.image_get_resized_images(obj.image)
		return result
	
	def _set_image(self, cr, uid, id, name, value, args, context=None):
		return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)

	def _default_department(self,cr,uid,context=None):
		user_ids = self.pool.get('hr.employee').search(cr,uid,[('user_id','=',uid)])
		if user_ids:
			return self.pool.get('hr.employee').browse(cr,uid,user_ids[0]).department_id.id

	_columns = {
		# 'content': fields.html("Content"),
		'photo_news':fields.boolean("Photo News?"),
		'image':fields.binary("Photo",
			help="This field holds the image used as photo for the news."),
		'image_medium': fields.function(_get_image, fnct_inv=_set_image,
			string="Medium-sized photo", type="binary", multi="_get_image",
			store = {
				'document.page': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Medium-sized photo of the page. It is automatically "\
				 "resized as a 128x128px image, with aspect ratio preserved. "\
				 "Use this field in form views or some kanban views."),
		'image_small': fields.function(_get_image, fnct_inv=_set_image,
			string="Smal-sized photo", type="binary", multi="_get_image",
			store = {
				'document.page': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
			},
			help="Small-sized photo of the page. It is automatically "\
				 "resized as a 64x64px image, with aspect ratio preserved. "\
				 "Use this field anywhere a small image is required."),
		'display_name':fields.boolean("Display Name?",help="Check this if you don't want to display your name"),
		'description':fields.text("Description",help="Description of the category",size=128),
		'read_times': fields.integer("Read Times"),
		'department_id':fields.many2one("hr.department","Department"),
		'display_position':fields.selection(
			[("shortcut","Shortcuts"),("content_left","Content Left"),("content_right","Content Right")]
			,"Display Position"),
		'display_in_departments':fields.many2many("hr.department",string="Display in Departments"),
		'sequence':fields.integer("Display Sequence"),
	}
	_defaults={
		'sequence':10,	
		'department_id':_default_department
	}
	_order='sequence,id'

	def onchange_photo_news(self,cr,uid,ids,photo_news):
		res = {}		
		return res
	def onchange_image(self,cr,uid,ids,image_medium):
		res = {}
		if image_medium:
			res['value']={'photo_news':True}
		return res

	
