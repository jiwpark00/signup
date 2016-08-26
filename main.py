import webapp2

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
"""

page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def post(self):
        edit_header = "<h1>Signup</h1>"
        text_form = """
        <form action="/" method="post">
        <br>
        <label>Username</label>
        <input type="text" name="username"></input>
        <br>
        <label>Password</label>
        <input type="text" name="password"></input>
        <br>
        <label>Verify Password</label>
        <input type="text" name="verify"></input>
        <br>
        <label>Email (optional)</label>
        <input type="text" name="email"></input>
        <br>
        <input type="submit" value="Submit">
        </form>
        """

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        body_content = edit_header + text_form + error_element
        response = page_header + body_content + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
