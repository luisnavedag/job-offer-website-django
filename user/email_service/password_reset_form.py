from api.email_service.email_base_form import base_email_form


@base_email_form
def reset_password_email_form(data: dict[str, any]) -> str:
    """
    The function returns the html code that will be sent to the user who wants to reset his password
    """
    return f"""
        <body>
        <div class="main">
            <div class="logo-con">
                <div class="logo">
                    <img alt="" class="img-job" src='cid:{data['image_name']}'/>
                </div>
            </div>
            <div class="text-con">
                <div class="title">
                    <h2>Hello {data['username']}</h2>
                </div>
                <div class="content">
                    <h3>We’ve received a request to reset the password for the Job-Website account associated
                   with {data['email']}. No changes have been made to your account yet.
                </h3>
                </div>
                <div class="content">
                    <h3>Click below button to reset your password:</h3>
                    <div class="btn-con">
                        <div>
                            <a target="_blank" class="btn" href="{data['url']}"><p class="color-button">Reset</p></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <footer>
        </footer>
        </body>
        """
