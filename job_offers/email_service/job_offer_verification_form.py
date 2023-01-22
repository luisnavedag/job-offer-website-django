from general_utils.email_service.email_base_form import base_email_form


@base_email_form
def job_offer_verification_email_form(data: dict[str, any]) -> str:
    """
    The function returns a html code that will be sent to the admin to verify the added job offer
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
                    <h2>Verification of the job offer</h2>
                </div>
                <div class="content">
                    <h3>Please verify that the offer below does not contain any prohibited elements</h3>
                </div>
                <div class="content">
                    <p>{data['title']}</p>
                    <p>{data['job_description']}</p>
                    <p>{data['address']}</p>
                    <p>{data['information_clause']}</p>
                    <p>{data['contact_name']}</p>
                    <p>{data['contact_email']}</p>
                    <p>{data['contact_phone']}</p>
                </div>
                <div class="content">
                    <h3>If the above job offer is correct, please click on the link below:</h3>
                    <div class="btn-con">
                        <div>
                            <a target="_blank" class="btn" href="{data['url']}"><p class="color-button">Verify</p></a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <footer>
        </footer>
        </body>
        """
