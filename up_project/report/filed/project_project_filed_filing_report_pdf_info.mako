<html>
<head>
    <style type="text/css">
            ${css}
        .table-text {
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <% setLang('zh_CN') %>
<div class="pdf-title">
    <h1>项目文件归档表</h1>
</div>
<div class="pdf-small-title">
    <div class="pdf-small-title-left">
        QRT4.2.3-3
    </div>
    <div class="pdf-small-title-center">
        版别/修改码:E/1112
    </div>
    <div class="pdf-small-title-right">
        项目编号: ${object.project_serial_number or ''|entity}
    </div>
</div>
<div class="pdf-table">
    <table>
        <tbody>
        <tr>
            <td colspan="4">
                归档表1/3 ---项目简介
            </td>
        </tr>
        <tr>
            <td style="width: 20%">项目名称</td>
            <td colspan="3" class="table-content">${object.project_id.name or ''|entity}</td>
        </tr>
        <tr>
            <td>项目类别</td>
            <td class="table-content">一级分类：${object.project_category_id.name or ''|entity}
                <br/>二级分类：${','.join([u.name for u in object.project_second_category]) or ''|entity}
            </td>
            <td>项目负责人</td>
            <td class="table-content">${','.join([u.name for u in object.project_user]) or ''|entity}</td>
        </tr>
        <tr>
            <td>所在地区</td>
            <td class="table-content">
                %if object.project_country_id.name == 'China':
                    中国
                %else:
                    ${object.project_country_id.name or '' | entity}
                %endif
                ${object.project_state_id.name or ''|entity} ${object.project_id.city or ''|entity}
            </td>
            <td>中止项目填写归档阶段</td>
            <td class="table-content">
                %if object.end_stage:
                    ${dict(object._columns['end_stage'].selection)[object.end_stage]}
                %endif
            </td>
        </tr>
        <tr>
            <td>项目规模</td>
            <td colspan="3" class="table-content">${object.project_scale or ''|entity}</td>
        </tr>
        <tr>
            <td>项目起止日期</td>
            <td colspan="3" class="table-content">${object.project_begin_date and formatLang(object.project_begin_date,date=True) or ''}
                ~ ${object.project_end_date and formatLang(object.project_end_date,date=True) or ''}</td>
        </tr>
        <tr>
            <td>项目关键字</td>
            <td colspan="3" class="table-content">
                %if tags:
                    % for tag in tags.items():
                        <div>${tag[0]}: ${','.join(tag[1])}</div>
                    % endfor
                %endif
            </td>
        </tr>
        <tr>
            <td>项目概况</td>
            <td colspan="3" class="table-content table-text">${object.description or ''|n}</td>
        </tr>
        <tr>
            <td>借鉴的主要案例</td>
            <td colspan="3" class="table-content table-text">${object.note or ''|n}</td>
        </tr>
        <tr>
            <td>推荐主要表达图纸名称</td>
            <td colspan="3">
                %for index in range(min(3,len(object.show_images))):
                        ${helper.embed_image('jpg',setHtmlImage(object.show_images[index].id),150)}
                %endfor
            </td>
        </tr>
        <tr>
            <td>项目负责人签字</td>
            <td>
                %if object.manager_approver_id and object.manager_approver_id.sign_image:
                    ${helper.embed_image('jpg',object.manager_approver_id.sign_image,150)}
                %elif object.manager_approver_id and not object.manager_approver_id.sign_image:
                    ${object.manager_approver_id.name}
                %endif
            </td>
            <td>签字时间</td>
            <td>${object.manager_approver_date and formatLang(object.manager_approver_date,date_time=True) or ''|entity}</td>
        </tr>
        </tbody>
    </table>
</div>
</body>
</html>