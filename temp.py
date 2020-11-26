from controllers import config_file as config_file

import re
def pre_process_mail_text(subject,mail_body):
    punctuation_rmvd = r"""!#$%&'*+<=>?\^_`{|}~"""
    filter_li=['De:','Enviada em:','Para:','Assunto:','Desde:','Enviado el:','From:','Sent on:','To:','Cc:','CC:']
    text_sent_each_mail = [k for k in mail_body.split('\n') if not 'True' in list(map(lambda x:k.startswith(x),filter_li))]
    senetences = text_sent_each_mail
    text_sent_each_mail = '\n'.join(text_sent_each_mail)
    cmbined_val = subject + " " + mail_body
    cmbined_val = cmbined_val.replace(config_file.config_path.find('removal_String').text, '').replace(
        config_file.config_path.find('removal_String_last').text, '').strip()
    cmbined_val = cmbined_val.strip('\n')
    cmbined_val = cmbined_val.strip('\t')
    cmbined_val = cmbined_val.strip('\r')
    cmbined_val1 = cmbined_val.replace("\r\n\r\n", '')
    cmbined_val2 = cmbined_val1.replace('\n', '')
    cmbined_val3 = cmbined_val2.replace("\t", '').strip()
    removed_link = re.sub(r'http\S+', '', cmbined_val3)
    remove_email = re.sub(r'[^@\s]+@[^@\s]+\.[^@\s]+', '', removed_link)
    final_data = remove_email.replace("..", '.')
    translation_table = dict.fromkeys(map(ord, punctuation_rmvd), ' ')
    _removed_punct = final_data.translate(translation_table)
    return senetences,_removed_punct
import extract_msg
import os 
from controllers import config_file as config_file
from pre_process import pre_process_mail_text 

text_sent_level =[]
subject_body =[]
def Email_Parse_Msg(mail_extract_path, process, year, month, day, logger):
    try:
        # punctuation_rmvd = r"""!#$%&'*+<=>?\^_`{|}~"""
        for top, dirs, files in os.walk(mail_extract_path):
            count_msg_files = len(files)
            number_of_msg_processed = 0
            for filename in files:
                if filename.endswith('.msg'):
                    number_of_msg_processed = number_of_msg_processed + 1
                    abspath = os.path.join(top, filename)
                    msg = extract_msg.Message(abspath)
                    logger.info("processing email name "+str(abspath))
                    subject = str(msg.subject)
                    sender_from = str(msg.sender)[str(msg.sender).find("<")+1:str(msg.sender).find(">")]
                    #to read the subject and sender email id
                    subject_sender_path = config_file.config_path.find('subject_sender').text
                    subject_sender = pd.ExcelFile(subject_sender_path).parse("Sheet1")
                    subject_name = list(subject_sender.iloc[:, 0])
                    subject_name = [x.lower() for x in subject_name]
                    sender_email_id = list(subject_sender.iloc[:, 1])
                    sender_email_id = [x.lower() for x in sender_email_id]

                    if ((subject.strip().lower() in subject_name) and (sender_from.strip().lower() in sender_email_id)):
                        print("subject+++++++++++:",subject)

                    else:
                        body = str(msg.body)
                        # print('---body',body)
                        sentences,_removed_punct=pre_process_mail_text(subject,body)
                        text_sent_level.append(sentences)
                        subject_body.append(_removed_punct)
                        # with open(r'C:\Users\akash148363\PycharmProjects\LM\Phrase_extraction_project\nmt_shared_drive\mails\portugal\2020\August\25\msg.txt','w',encoding='utf-8') as f:
                        #     f.write(body)
                        # print('message_id',msg.message_id)
                        stripped_id = msg.message_id.replace("<", '').replace('>', '').strip()
                        stripped_id = ''
                        # print('subject_body',subject_body)
                        #save_attch_path=top.replace("mails","attachments")
                        save_attch_path = os.path.join(config_file.config_path.find('mail_attachment_path').text, process, year, month, day ,filename[:-4])
                        att = msg.attachments
                        for i in att:
                            longFilename_modified = rename_obj(i.longFilename)
                            # print('i.longFilename',i.longFilename)
                            # print('longFilename_modified',longFilename_modified)
                            if i.type == 'msg':
                                pass
                            else:
                                if not os.path.exists(save_attch_path):
                                    os.makedirs(save_attch_path)

                                    #i.save(customFilename=stripped_id + "_" + str(i.longFilename),customPath=save_attch_path)
                                    i.save(customFilename= str(longFilename_modified),customPath=save_attch_path)
                                    logger.info("saving attachment to"+save_attch_path+" "+ stripped_id + "_" + str(i.longFilename))
                                else:
                                    i.save(customFilename=str(longFilename_modified),
                                           customPath=save_attch_path)

                                    logger.info("saving attachment to"+save_attch_path+" " + str(longFilename_modified))
            
            logger.info("{} messages processed out of {}".format(number_of_msg_processed,count_msg_files))
        return subject_body, save_attch_path, text_sent_level
    except Exception as e:
        logger.error("unable to fetch the body and attachment"+str(e))
        return subject_body.append("error in parsing the emails")
