from flask import Flask,request,abort

app=Flask("")

def makeCode(headerCode="", bodyCode="<p>Test</p>", title="Kai's Blog"):
    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>{title}</title>
            {headerCode}
        </head>
        <body>
            <h1>{title}</h1>
            {bodyCode}
        </body>
    </html>
    """

@app.get("/")
def main():
    return makeCode()

@app.route("/createPost", methods=["GET","POST"])
def createPost():
    if request.method=="GET":
        print("Page loaded")
        return makeCode(title="Create Post", bodyCode="""
    <form action="/createPost" target="_blank" method="post">
        <label for="username">Display name:</label><br>
        <input type="text" id="username" name="username"><br><br>
        <label for="title">Post title:</label><br>
        <input type="text" id="title" name="title"><br><br>
        <label for="code">Code:</label><br>
        <input type="text" id="code" name="code"><br><br>
        <input type="submit" value="Create" onclick="submit();"></input>
    </form>
    <p id="conf"></p>
    """, headerCode="""<script>
    function submit() {
        document.getElementById("conf").innerText="Success!";
            setTimeout(function() {
            document.getElementById("conf").innerText="";
        }, 1000);
    }
            </script>""")
    elif request.method=="POST":
        username=request.form["username"]
        title=request.form["title"]
        code=request.form["code"]
        print("Recived.")
        print(username,title,code)
        try:open(f"posts/{username}_{title}.html","x", encoding="utf-8")
        except FileExistsError:return "<p>Blog exists.</p>"
        with open(f"posts/{username}_{title}.html", "w", encoding="utf-8") as post:post.write(makeCode(bodyCode=code,title=title))
        return "<p>You may close this tab now.</p>"
    else:
        abort(405) # Code 405, Request method invalid for URL