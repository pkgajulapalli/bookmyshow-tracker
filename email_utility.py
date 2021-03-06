import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


import os
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('SENDINBLUE_API_KEY')


def get_email_data(to, subject, body):
    sender = {'name': 'Sendinblue', 'email': 'contact@sendinblue.com'}
    reply_to = {'name': 'Sendinblue', 'email': 'contact@sendinblue.com'}
    to = [{'email': to}]
    return sib_api_v3_sdk.SendSmtpEmail(to=to, reply_to=reply_to, html_content=body,
                                        sender=sender, subject=subject)


def send_email(to, subject, body):
    try:
        email_api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        api_response = email_api_instance.send_transac_email(get_email_data(to, subject, body))
        print(api_response)
    except ApiException as e:
        print('Exception when calling SMTPApi -> send_transac_email: %s\n' % e)


def send_sms():
    sms_api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))
    send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender='string', recipient='string', content='string',
                                                     type='string', web_url='https://example.com/notifyUrl')
    try:
        api_response = sms_api_instance.send_transac_sms(send_transac_sms)
        print(api_response)
    except ApiException as e:
        print('Exception when calling TransactionalSMSApi->send_transac_sms: %s\n' % e)