import ConstResource as Resimport FunctionCommon as Fundef parser():    conf = Fun.get_conf_parser(Res.monkey_conf_file)    Fun.assert_options_presents(conf, ['mail', 'ftp', 'apk', 'monkey_params'])    sender = conf.get('mail', 'sender')    mail_pwd = conf.get('mail', 'pwd')    subject = conf.get('mail', 'subject')    receivers = conf.get('mail', 'receivers').split(',')    anr_receivers = conf.get('mail', 'anr_receivers').split(',')    pkg_name = conf.get('apk', 'package_name')    subject = conf.get('apk', 'name') + subject    keyword = conf.get('apk', 'keyword')    events = conf.get('monkey_params', 'events')    throttle = conf.get('monkey_params', 'throttle')parser()