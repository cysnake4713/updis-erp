import time
import datetime
from report import report_sxw


class renwuxiada(report_sxw.rml_parse):
    """docstring for renwuxiada"""

    def __init__(self, cr, uid, name, context):
        super(renwuxiada, self).__init__(cr, 1, name, context)
        self.localcontext.update({
            'time': time,
            'date_format': self.date_format,
            # 'project_active_tasking': self._get_project_active_tasking_form,
        })

    def date_format(self, current_date):
        if current_date:
            create_date_display = datetime.datetime.strptime(current_date.split('.')[0],
                                                             '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8)
            return create_date_display.strftime('%Y/%m/%d %p %I:%M:%S')
        else:
            return current_date

    def _get_category_names(self, pid):
        # import pdb;pdb.set_trace()
        project = self.pool.get('project.project')
        return [cat.name for cat in project.browse(self.cr, self.uid, pid).categories_id]

    def _get_project_active_tasking_form(self, pid):
        form = self.pool.get('project.project.active.tasking')
        form_ids = form.search(self.cr, self.uid, [('project_id', '=', pid)])
        if form_ids:
            return form.browse(self.cr, self.uid, form_ids[0])


report_sxw.report_sxw('report.project.active.tasking.report.pdf', 'project.project.active.tasking',
                      'up_project/report/active/project_project_active_tasking_report_pdf.rml', parser=renwuxiada,
                      header=True)