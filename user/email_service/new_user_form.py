from general_utils.email_service.email_base_form import base_email_form


@base_email_form
def new_user_email_form(data: dict[str, any]) -> str:
    """
    The function returns the html code which will be sent to the newly registered user
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
                    <h2>Hello {data['first_name']}</h2>
                </div>
                <div class="content">
                    <h3>Thanks you for being with us!</h3>
                </div>
                <div class="content">
                    <h3>Click below button to activate your account:</h3>
                    <div class="btn-con">
                        <div>
                            <a target="_blank" class="btn" href="{data['url']}"><p class="color-button">Activate</p></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <footer>
        </footer>
        </body>
        """
