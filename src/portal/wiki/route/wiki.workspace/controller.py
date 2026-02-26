from PIL import Image

import math 
import season
import time
import datetime
import os
import urllib

segment = wiz.request.match("/api/wiki/attachment/<action>/<book_id>/<path:path>")
action = segment.action
book_id = segment.book_id

# FN-0011: 세션 캐시 제거, 매 요청 시 인증 검증
book = wiz.model("portal/wiki/book").get(book_id)
if book is None:
    wiz.response.status(404)
book.access.accessLevel(["admin", "user", "guest", "visitor"])

fs = wiz.model("portal/wiki/fs").use(f"book/{book_id}/attachment")
cachefs = wiz.model("portal/wiki/fs").use(f"book/{book_id}/cache")

if action == 'upload':
    orm = wiz.model("portal/season/orm")
    book = wiz.model("portal/wiki/book").get(book_id)
    file = wiz.request.file("upload")
    if file is None: 
        wiz.response.status(404)

    filename = file.filename
    filepath = book.content.update(dict(type="attachment", root_id="", title=filename))
    fs.makedirs(".")
    fs.write.file(filepath, file)
    urlfilename = urllib.parse.quote(file.filename)

    wiz.response.json(dict(
        code=200,
        filename=filename,
        book_id=book_id,
        id=filepath,
        url=f'/api/wiki/attachment/download/{book_id}/{filepath}/{urlfilename}'
    ))

elif action == 'download':
    segment = wiz.request.match("/api/wiki/attachment/<action>/<project_id>/<filepath>/<filename>")

    filepath = segment.filepath
    filename = segment.filename
    filename = urllib.parse.unquote(filename)

    if fs.isfile(filepath) == False:
        wiz.response.abort(404)
        
    filepath = fs.abspath(filepath)
    wiz.response.download(filepath, as_attachment=False, filename=filename)

elif action == 'thumbnail':
    segment = wiz.request.match("/api/wiki/attachment/<action>/<project_id>/<filepath>/<filename>")

    filepath = segment.filepath
    filename = segment.filename
    filename = urllib.parse.unquote(filename)

    if fs.isfile(filepath) == False:
        wiz.response.abort(404)
    
    resfilepath = fs.abspath(filepath)

    try:
        ext = os.path.splitext(filename)[-1]
        if ext.lower() in ['.png', '.jpg', '.jpeg']:
            cachefs.makedirs()
            cachefilepath = f"{filepath}{ext}"
            
            if cachefs.isfile(cachefilepath) == False:
                cachefs.copy(fs.abspath(filepath), cachefilepath)
                with Image.open(cachefs.abspath(cachefilepath)) as im:
                    ratio = 512 / im.size[0]
                    size = (int(im.size[0] * ratio), int(im.size[1] * ratio))
                    im.thumbnail(size)
                    im.save(cachefs.abspath(cachefilepath))
            
            resfilepath = cachefs.abspath(cachefilepath)
    except Exception as e:
        pass

    wiz.response.download(resfilepath, as_attachment=False, filename=filename)
