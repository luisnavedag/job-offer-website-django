from general_utils.email_service.email_base_form import base_email_form


@base_email_form
def job_offer_matchmaking_email_form(data: dict[str, any]) -> str:
    """
    The function returns a html code that will be sent to a user who has required skills
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
                    <h2>Hi {data['first_name']} {data['last_name']}</h2>
                </div>
                <div class="content">
                    <h3>A new job offer has just been added that may interest you!</h3>
                    <h3>{data["job_offer_title"]}</h3>
                <div class="content">
                    <h3>Click on the link below to go to the offer:</h3>
                    <div class="btn-con">
                        <div>
                            <a target="_blank" class="btn" href="{data['url']}"><p class="color-button">Click</p></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <footer>
        </footer>
        </body>
        """
