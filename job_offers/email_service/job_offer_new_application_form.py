from general_utils.email_service.email_base_form import base_email_form


@base_email_form
def job_offer_new_application_email_form(data: dict[str, any]) -> str:
    """
    The function returns the html code that will be sent to
    the employer for whom the application has been submitted
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
                    <h2>Application for the position - {data["job_offer_title"]}</h2>
                </div>
                <div class="content">
                    <h3>Hi {data['first_name']} {data['last_name']}</h3>
                    <h3>Someone just applied for one of your job offers!</h3>
                </div>
                <div class="content">
                    <h3>To go to the profile of the candidate for the position you are applying for, 
                        click on the link below:
                    </h3>
                <div class="btn-con">
                    <div>
                        <a target="_blank" class="btn" href="{data['employee_url']}"><p class="color-button">Click</p></a>
                    </div>
                </div>
                <div class="content">
                    <h3>To go to the offer you applied for, click the button below:
                    </h3>
                <div class="btn-con">
                    <div>
                        <a target="_blank" class="btn" href="{data['job_offer_url']}"><p class="color-button">Click</p></a>
                    </div>
                </div>
                </div>
            </div>
        </div>
        <footer>
        </footer>
        </body>
        """
