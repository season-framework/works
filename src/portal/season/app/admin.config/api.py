import os
import datetime

def config_load():
    sys_config = wiz.model("portal/season/system_config")
    category = wiz.request.query("category", "")

    if category:
        rows = sys_config.list(category=category)
    else:
        rows = sys_config.list()

    # 카테고리별 그룹핑
    result = {}
    for row in rows:
        cat = row['category']
        if cat not in result:
            result[cat] = []
        result[cat].append({
            'key': row['key_name'],
            'value': row['value'],
            'type': row['value_type'],
            'description': row.get('description', '')
        })

    wiz.response.status(200, result)

def config_update():
    sys_config = wiz.model("portal/season/system_config")
    data = wiz.request.query("data", True)

    if isinstance(data, str):
        import json
        data = json.loads(data)

    for item in data:
        category = item.get('category', '')
        key = item.get('key', '')
        value = item.get('value', '')
        value_type = item.get('type', 'string')
        description = item.get('description', '')

        if not category or not key:
            continue

        # password 타입: '********' 전송 시 기존 값 유지 (변경 안함)
        if value_type == 'password' and value == '********':
            continue

        sys_config.set(category, key, value, value_type=value_type, description=description)

    wiz.response.status(200, True)

def smtp_test():
    to = wiz.request.query("to", True)

    # config.py가 DB → season.py fallback을 자동 처리
    config = wiz.model("portal/season/config")

    smtp_host = config.smtp_host
    smtp_port = config.smtp_port
    smtp_sender = config.smtp_sender
    smtp_password = config.smtp_password

    if not smtp_host or not smtp_sender:
        wiz.response.status(400, "SMTP 설정이 완료되지 않았습니다")

    import smtplib
    from email.mime.text import MIMEText

    html = """<div style="padding: 24px;">
    <h2>SMTP 테스트 이메일</h2>
    <p>이 이메일은 관리자 페이지에서 발송한 SMTP 테스트 메일입니다.</p>
    <p>발송 시간: {time}</p>
</div>""".format(time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    msg = MIMEText(html, 'html', _charset='utf8')
    msg['Subject'] = '[시즌웍스] SMTP 테스트 이메일'
    msg['From'] = smtp_sender
    msg['To'] = to

    try:
        mailserver = smtplib.SMTP(smtp_host, int(smtp_port))
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.login(smtp_sender, smtp_password)
        mailserver.sendmail(smtp_sender, to, msg.as_string())
        mailserver.quit()
    except Exception as e:
        wiz.response.status(500, f"SMTP 테스트 실패: {str(e)}")

    wiz.response.status(200, "테스트 이메일이 발송되었습니다")

def template_list():
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    files = fs.list()
    templates = []
    for f in files:
        if f.endswith('.html'):
            name = f.replace('.html', '')
            templates.append({'name': name, 'filename': f})
    wiz.response.status(200, templates)

def template_read():
    name = wiz.request.query("name", True)
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    filename = f"{name}.html"
    if not fs.exists(filename):
        wiz.response.status(404, "템플릿을 찾을 수 없습니다")
    content = fs.read(filename)
    wiz.response.status(200, {'name': name, 'content': content})

def template_update():
    name = wiz.request.query("name", True)
    content = wiz.request.query("content", True)
    fs = wiz.project.fs(os.path.join("config", "smtp"))
    filename = f"{name}.html"
    fs.write(filename, content)
    wiz.response.status(200, True)
