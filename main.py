import webapp2
import re

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

#.match() will return None --> FALSE or a match object --> TRUE
#This is for checking for regular expression and length for the username
valid_username = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def username_checker(usernameCheck):
    return usernameCheck and valid_username.match(usernameCheck)

#This is for checking for regular expression and length for the password
valid_password = re.compile(r"^.{3,20}$")
def password_checker(passwordCheck):
    return passwordCheck and valid_password.match(passwordCheck)

#This is for checking for regular expression and length for the email, which is optional
valid_email = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def email_checker(emailCheck):
    return not emailCheck or valid_email.match(emailCheck)

# The idea is to allow the user to enter information
class Index(webapp2.RequestHandler):
    def get(self):
        edit_header = "<h1>Signup</h1>"
        text_form = """
        <form action="/errorcheck" method="post">
        <br>
        <label>Username</label>
        <input type="text" name="username"></input>
        <br>
        <label>Password</label>
        <input type="password" name="password"></input>
        <br>
        <label>Verify Password</label>
        <input type="password" name="verify"></input>
        <br>
        <label>Email (optional)</label>
        <input type="text" name="email"></input>
        <br>
        <input type="submit" value="Submit">
        </form>
        """

        body_content = edit_header + text_form
        response = page_header + body_content + page_footer
        self.response.write(response)

class ErrorCheck(webapp2.RequestHandler):
    def post(self):
        edit_header = "<h1>Signup</h1>"
        #get username, password, verify, and email for validation
        errorpresent = False
        usernameCheck = self.request.get("username")
        passwordCheck = self.request.get("password")
        verifyCheck = self.request.get("verify")
        emailCheck = self.request.get("email")

        errorlist = {"username_error":" ", "password_error":" ", "verify_error":" ", "email_error":" "}
        #errorlist = dict[usernameCheck = usernameCheck, emailCheck = emailCheck]

        if not username_checker(usernameCheck):
            errorpresent = True
            errorlist["username_error"] = "<span class='error'>" + " That's not a valid username" + "</span>"

        if not password_checker(passwordCheck):
            errorpresent = True
            errorlist["password_error"] = "<span class='error'>" + "That wasn't a valid password" + "</span>"

        if passwordCheck != verifyCheck:
            errorpresent = True
            errorlist["verify_error"] = "<span class='error'>" + "Your passwords didn't match." + "</span>"

        if not email_checker(emailCheck):
            errorpresent = True
            errorlist["email_error"] = "<span class='error'>" + "That's not a valid email" + "</span>"

        if not errorpresent:
            self.redirect('/welcome?username=' + usernameCheck)

        text_form1 = """
        <form method="post">
        <label>Username</label>
        <input type="text" name="username" value={0}>{1}</input>
        </form>
        """.format(usernameCheck,errorlist["username_error"])


        text_form2="""
        <form method="post">
        <label>Password</label>
        <input type="password" name="password">{0}</input>
        <br>
        </form>
        """.format(errorlist["password_error"])

        text_form3 = """
        <form method="post">
        <label>Verify Password</label>
        <input type="password" name="verify">{0}</input>
        <br>
        </form>
        """.format(errorlist["verify_error"])

        text_form4 = """
        <form method="post">
        <label>Email (optional)</label>
        <input type="text" name="email" value={0}>{1}</input>
        <br>
        </form>
        """.format(emailCheck,errorlist["email_error"])

        text_form = text_form1 + text_form2 + text_form3 + text_form4
        body_content = edit_header + text_form
        response = page_header + body_content + page_footer
        self.response.write(response)

class Welcome(webapp2.RequestHandler):
    def get(self):
        welcome_user = self.request.get("username")
        edit_header = "<h1>Welcome, %s</h1>"%welcome_user

        response = page_header + edit_header + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/errorcheck',ErrorCheck),
    ('/welcome',Welcome)
], debug=True)
