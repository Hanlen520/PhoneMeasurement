# coding=utf-8import osimport syssys.path.append('..')import FunctionCommon as Funimport PhoneCommon as Phoimport STFDevicesControl as Stfdef trigger_phone_task(keyboard, date_published, target_file_path, task_id,                       flag_file=Pho.default_flag_file):    flag_file_full_path = '/sdcard/%s' % flag_file    ip_id = get_available_device(flag_file_full_path)    if ip_id is None:        Fun.sleep(Pho.delay_to_recheck_available_device)        trigger_phone_task(keyboard, date_published, target_file_path, task_id, flag_file)    else:        Fun.p_open(Pho.adb_connect_remote % ip_id)        file_name = target_file_path[target_file_path.rfind('/') + 1:]        Fun.p_open(            Fun.adb_s_tag_prefix(ip_id) + ' push %s %s' % (target_file_path,                                                           ('/sdcard/%s' % file_name)))        Fun.force_stop_app(ip_id, Pho.process_name)        Fun.clear_date_force_stop(ip_id, Pho.auto_hook_process_name)        Fun.clear_date_force_stop(ip_id, Pho.entrance_process_name)        if keyboard not in Pho.keyword_dict:            raise Exception('keyword not support')        Fun.clear_app_data(ip_id, Pho.keyword_dict[keyboard])        Fun.sleep(5, 'wait ime clear process finish')        Fun.p_open(Fun.asb_shell_start_activity(ip_id, Pho.entrance_activity_name)                   + fill_es(Pho.Key.keyboard, keyboard)                   + fill_es(Pho.Key.target, file_name)                   + fill_es(Pho.Key.task_id, task_id)                   + fill_es(Pho.Key.non_root_device, Pho.non_root_device)                   + fill_es(Pho.Key.flag_file, flag_file)                   + fill_es(Pho.Key.date_published, date_published))        Fun.exe_py_in_background_if_not_running(Pho.connection_keeper_py_name)    return [1]def fill_es(key, val):    return ' --es \"%s\" \"%s\" ' % (key, val)def get_available_device(flag_file):    device_status = parse_devices_status(flag_file)    Fun.log(device_status.keys())    # for ip_id, status in device_status.iteritems():    #     if status == Pho.Status.idle:    #         return ip_id    return Nonedef parse_devices_status(finish_flag_file):    device_status = dict()    sc = Stf.STFDevicesControl()    devices = sc.get_remote_connect_url(Pho.remote_devices)    for serial, ip_id in devices.iteritems():        if not connect_device_ok(ip_id):            device_status[ip_id] = Pho.Status.unreachable            continue        res = Fun.p_open_with_line_1_result(Fun.find_file(ip_id, finish_flag_file))        print 'res:' + str(res) if res is not None else 'res NONE'        if Fun.tell_process_running(ip_id, Pho.entrance_process_name):            device_status[ip_id] = Pho.Status.busy        elif res is None:            device_status[ip_id] = Pho.Status.unreachable        elif Pho.file_not_found_keyword not in res:            device_status[ip_id] = Pho.Status.idle        else:            running = Fun.tell_process_running(ip_id, Pho.process_name)            device_status[ip_id] = Pho.Status.busy if running else Pho.Status.idle    print device_status    return device_statusdef connect_device_ok(d):    # 如果直接要链接多台 需要 每一个链接命令执行两次    for _ in range(2):        res = Fun.p_open_with_line_1_result(Pho.adb_connect_remote % d)        if res is None or Pho.connect_refuse_keyword in res or Pho.connected_keyword not in res:            return False    return Trueif __name__ == '__main__':    trigger_phone_task('gboard', Pho.default_date_published, Pho.target_file, '007')