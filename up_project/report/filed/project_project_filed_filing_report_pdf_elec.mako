<html>
<head>
    <style type="text/css">
            ${css}
        td.center-head {
            text-align: center;
        }

        div.pdf-table > table > tbody > tr > td.table-content {
            padding: 20px 0 10px 5px !important;
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
                归档表3/3 ---项目纸质文件
            </td>
        </tr>
            <td>路径</td>
            <td>文件名</td>
            <td>归档批次</td>
            <td>创建时间</td>
        <% directory_name ='' %>
        %for (dir_name, attachments) in elec_attachments.items():
            <% head =  dir_name%>
            %for attachment in attachments:
                <tr>
                    %if head:
                        <td class="table-content" rowspan="${len(attachments)}">/${head}</td>
                        <% head = ''%>
                    %endif
                    <td class="table-content">${attachment.attachment_id.name}</td>
                    <td class="table-content">${attachment.version}</td>
                    <td class="table-content">${attachment.create_date}</td>
                </tr>
            %endfor
        %endfor
        </tbody>
    </table>
</div>
</body>
</html>