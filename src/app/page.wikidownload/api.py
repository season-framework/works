def load():
    docid = wiz.request.query("id")
    bookModel = wiz.model("portal/wiki/book")
    book = bookModel.get(docid)

    tree = []

    def getChild(docid="", level=1):
        rows = book.content.tree(docid)
        for child in rows['children']:
            child['level'] = level
            child['content'] = book.content.load(child['id'])
            tree.append(child)

            getChild(child['id'], level+1)

    getChild()

    contents = ""

    for item in tree:
        title = ""
        for lv in range(item['level']):
            title = title + "#"
        title = title + " " + item['title']
        try:
            content = item['content']['content']
        except Exception as e:
            content = ""

        contents = contents + title + "\n\n" + content + "\n\n"
        if item['level'] == 1:
            contents = contents + "---\n\n"

    wiz.response.status(200, contents)