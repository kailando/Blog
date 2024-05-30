from flask import Flask,request,abort
from glob import glob

app=Flask("")

def makeCode(headerCode="", bodyCode="<p>Test</p>", title="Kai's Blog"):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>{title}</title>
<style>body {'{'}background-color: #888888;{'}'}</style>
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
    return makeCode(bodyCode="""<h2>Hello.</h2><br>
<a href="/createPost">Create a post</a><br>
<a href="/viewPosts">Look at existing posts</a>
""")

@app.route("/createPost", methods=["GET","POST"])
def createPost():
    if request.method=="GET":
        return makeCode(title="Create Post", bodyCode="""
<p><b>Note:</b>Underscores ( _ ) in usernames are not allowed.</p><br>
<form action="/createPost" target="_blank" method="post">
<label for="username">Display name:</label><br>
<input type="text" id="username" name="username"><br><br>
<label for="title">Post title:</label><br>
<input type="text" id="title" name="title"><br><br>
<label for="code">Code:</label><br>
<input type="text" id="code" name="code"><br><br>
<input type="submit" value="Create" onclick="submit();"></input>
</form><br>
<a href="/"><- Home</a>
<p id="conf"></p>
""")
    elif request.method=="POST":
        username=request.form["username"]
        title=request.form["title"]
        code=request.form["code"]
        if "_" in username:
            return "<p>Invalid username. Has underscore ( _ )</p>"
        try:open(f"posts/{username}_{title}.html","x", encoding="utf-8")
        except FileExistsError:return "<p>Blog exists.</p>"
        with open(f"posts/{username}_{title}.html", "w", encoding="utf-8") as post:post.write(makeCode(bodyCode=code,title=title))
        return f"<a href='/posts/{username}_{title}.html>View your post</a>"
    else:
        abort(405) # Code 405, Request method invalid for URL

@app.get("/viewPosts")
def viewPosts():
    posts=[file[6::] for file in glob("posts/*_*.html")]
    fileList=""
    for file in posts:
        formatFile=file.removesuffix(".html")
        formatFileSplit=formatFile.split("_")
        secOne=formatFileSplit[0]
        secTwo=formatFileSplit[1]
        fileList+="<a href='posts/{}'>{}</a><br>\n".format(file,f"{secOne} - {secTwo}")
    return makeCode(bodyCode=fileList+"\n<a href='/'><- Home</a>",title="Post listing")

@app.route("/posts/<filename>")
def openPost(filename):
    return f"{open(f'posts/{filename}', 'r', encoding='utf-8').read()}\n<a href='/viewPosts'><- Posts</a>"
