# -*- encoding:UTF-8 -*-
import wx
import libs.Function as Function
import libs.Variable as Variable

class TestSuite(wx.Panel):
    def __init__(self, parent):
        self.dict_test_suite = dict()
        # OSC-COVERAGE_CBA=ts_decorSupport,ts_hsstaf_EpsNam_in_EPC_domain...
        # {'OSC-COVERAGE_CBA' : ['ts_decorSupport','ts_hsstaf_EpsNam_in_EPC_domain','...'] , others: [...]
        self.dict_group = dict()
        # [ALL] ALL_CBA= ... ALL_TSP-FE=...
        # {'ALL': ['ALL_CBA', 'ALL_TSP-FE', '...'], others: [...]
        self.test_suite_list =list()
        wx.Panel.__init__(self, parent=parent)

        all_sizer = self.__init_all_module()
        team_sizer = self.__init_group_module()
        middle_sizer = self.__init_middle_module()
        parse_sizer = self.__init_parse_module()
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(all_sizer, 1, wx.EXPAND)
        sizer.Add(middle_sizer, 0, wx.ALIGN_CENTER_VERTICAL)
        sizer.Add(team_sizer, 1, wx.EXPAND)
        sizer.Add(parse_sizer, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def __init_all_module(self):
        all_sizer = wx.BoxSizer(wx.VERTICAL)
        wx_text = wx.StaticText(self, -1, label='ALL', style=wx.ALIGN_RIGHT)
        self.all_member_choice = wx.Choice(self, -1, choices=[])
        self.Bind(wx.EVT_CHOICE, self.__choose_all_member, self.all_member_choice)
        self.all_test_suite_list = wx.ListBox(self, -1, choices=[])
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.__double_click_on_all_test_suite_list, self.all_test_suite_list)
        all_sizer.Add(wx_text, 0, wx.LEFT, 3)

        all_sizer.Add(self.all_member_choice, 0, wx.EXPAND|wx.ALL, 1)
        all_sizer.Add(self.all_test_suite_list, 1, wx.EXPAND|wx.ALL, 1)
        return all_sizer

    def __init_group_module(self):
        team_sizer = wx.BoxSizer(wx.VERTICAL)
        team_top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        team_top_class_sizer = wx.BoxSizer(wx.VERTICAL)
        team_top_member_sizer = wx.BoxSizer(wx.VERTICAL)
        wx_class_text = wx.StaticText(self, -1, label='Group', style=wx.ALIGN_RIGHT)
        wx_member_text = wx.StaticText(self, -1, label='TestSuite', style=wx.ALIGN_RIGHT)
        self.group_choice = wx.Choice(self, -1, choices=[])
        self.Bind(wx.EVT_CHOICE, self.__choose_group, self.group_choice)
        self.group_test_suite_choice = wx.Choice(self, -1, choices=[])
        self.Bind(wx.EVT_CHOICE, self.__choose_group_test_suite, self.group_test_suite_choice)
        team_top_class_sizer.Add(wx_class_text)
        team_top_class_sizer.Add(self.group_choice)
        team_top_member_sizer.Add(wx_member_text)
        team_top_member_sizer.Add(self.group_test_suite_choice)
        team_top_sizer.Add(team_top_class_sizer)
        team_top_sizer.Add(team_top_member_sizer)

        self.group_test_suite_list = wx.ListBox(self, -1, choices=[],style=wx.LB_EXTENDED)
        save_button = wx.Button(self, -1, label='SAVE')
        self.Bind(wx.EVT_BUTTON, self.__on_save, save_button)
        team_sizer.Add(team_top_sizer)
        team_sizer.Add(self.group_test_suite_list, 1, wx.EXPAND | wx.ALL, 1)
        team_sizer.Add(save_button, 0, wx.EXPAND | wx.ALL, 1)
        return team_sizer

    def __init_middle_module(self):
        middle_sizer = wx.BoxSizer(wx.VERTICAL)
        left_to_right_button = wx.Button(self, -1, label='>>', size=(30,30))
        right_to_left_button =  wx.Button(self, -1, label='<<', size=(30,30))
        middle_sizer.Add(left_to_right_button, 1, wx.ALIGN_CENTER_VERTICAL)
        middle_sizer.Add(right_to_left_button, 1, wx.ALIGN_CENTER_VERTICAL)
        return middle_sizer

    def __init_parse_module(self):
        def import_export_module():
            sizer = wx.BoxSizer(wx.HORIZONTAL)
            import_button = wx.Button(self, id=-1, label='Import')
            export_button = wx.Button(self, id=-1, label='Export')
            self.Bind(wx.EVT_BUTTON, self.__on_export, export_button)
            self.Bind(wx.EVT_BUTTON, self.__on_import, import_button)
            sizer.Add(import_button)
            sizer.Add(export_button)
            return sizer

        parse_sizer = wx.BoxSizer(wx.VERTICAL)
        wx_text = wx.StaticText(self, -1, label='INPUT', style=wx.ALIGN_RIGHT)
        self.text_ctrl = wx.TextCtrl(self, -1, '', style=(wx.TE_MULTILINE))
        self.text_ctrl.SetInsertionPoint(0)
        parse_button = wx.Button(self, -1, label='PARSE')
        self.Bind(wx.EVT_BUTTON, self.__on_parse, parse_button)
        self.merge_check = wx.CheckBox(self, label='Merge')
        parse_sizer.Add(wx_text)
        parse_sizer.Add(self.text_ctrl, 1, wx.EXPAND|wx.ALL, 1)
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        options_sizer.Add(parse_button, 0, wx.EXPAND|wx.ALL, 1)
        options_sizer.Add(self.merge_check, 0, wx.EXPAND|wx.ALL, 1)
        parse_sizer.Add(options_sizer)
        parse_sizer.Add(import_export_module())
        return parse_sizer

    def __on_import(self, event):
        dlg = wx.FileDialog(self,
                            message="Select Test Suites Configuration",
                            wildcard="Test Suites Configuration (*.cfg)|*.cfg|All files (*.*)|*.*",
                            defaultDir=Variable.ts_default_dir,
                            style=wx.FD_OPEN
                            )
        if dlg.ShowModal() == wx.ID_OK:
            config_path = dlg.GetPaths()[0]
            dict_config = Function.parse_configuration(config_path)
            self.__convert_dict_config(dict_config=dict_config)
            self.__set_choice()
        dlg.Destroy()

    def __convert_dict_config(self, dict_config):
        group_keys = dict_config.keys()
        for group_key in group_keys:
            test_suite_keys = dict_config.get(group_key).keys()
            self.dict_group[group_key] = test_suite_keys
            for test_suite_key in test_suite_keys:
                self.dict_test_suite[test_suite_key] = dict_config.get(group_key).get(test_suite_key)
        tmp = list()
        for value in dict_config.get(Variable.string_all).values():
            tmp.extend(value)
        self.test_suite_list = list(set(tmp))
        self.test_suite_list.sort(key=lambda x: len(x), reverse=True)
        print self.dict_group
        print self.dict_test_suite

    def __on_export(self, event):
        dlg = wx.FileDialog(self,
                            message="Save As Test Suites Configuration",
                            wildcard="Test Suites Configuration (*.cfg)|*.cfg|All files (*.*)|*.*",
                            defaultDir=Variable.ts_default_dir,
                            style=wx.FD_SAVE
                            )
        if dlg.ShowModal() == wx.ID_OK:
            profile_path = dlg.GetPaths()[0]
            Function.write_configuration(config_path=profile_path, dict_group=self.dict_group, dict_test_suite=self.dict_test_suite)
            # profile = self.__output_options_value()
            # Utility.save_profile(profile_path=profile_path, profile=profile)
        dlg.Destroy()

    def __set_choice(self):
        self.__set_all_member_choice(self.dict_group.get(Variable.string_all))
        self.__set_group_choice(self.dict_group.keys())



    def __set_all_member_choice(self, member_list):
        member_list = member_list[:]
        member_list.insert(0, '')
        self.all_member_choice.Set(member_list)
        self.all_member_choice.SetStringSelection('')

    def __set_group_choice(self, member_list):
        member_list = member_list[:]
        member_list.insert(0, '')
        member_list.remove(Variable.string_all)
        self.group_choice.Set(member_list)
        self.group_choice.SetStringSelection('')

    def __set_group_test_suite_choice(self, member_list):
        member_list = member_list[:]
        member_list.insert(0, '')
        self.group_test_suite_choice.Set(member_list)
        self.group_test_suite_choice.SetStringSelection('')

    def __set_all_test_suite_list(self, ts_list):
        self.all_test_suite_list.Set(ts_list)

    def __set_group_test_suite_list(self, ts_list):
        self.group_test_suite_list.Set(ts_list)

    def __choose_all_member(self, event):
        select = self.all_member_choice.GetStringSelection()
        self.__set_all_test_suite_list(self.dict_test_suite.get(select, []))

    def __choose_group(self, event):
        select = self.group_choice.GetStringSelection()
        self.__set_group_test_suite_choice(self.dict_group.get(select, []))

    def __choose_group_test_suite(self, event):
        select = self.group_test_suite_choice.GetStringSelection()
        self.__set_group_test_suite_list(self.dict_test_suite.get(select, []))

    def __on_parse(self, event):
        if not self.__check_status_is_correct():
            return
        tmp = list()
        value = self.text_ctrl.GetValue()
        for test_suite in self.test_suite_list:
            if test_suite in value:
                tmp.append(test_suite)
                value = value.replace(test_suite, '')
        self.text_ctrl.SetValue(value)
        self.__set_group_test_suite_list(tmp)

    def __double_click_on_all_test_suite_list(self, event):
        if not self.__check_status_is_correct():
            return
        select = self.all_test_suite_list.GetStringSelection()
        already_add_list = self.group_test_suite_list.Items
        if select not in already_add_list:
            self.group_test_suite_list.Append(select)

    def __check_status_is_correct(self):
        test_suite = self.group_test_suite_choice.GetStringSelection()
        flag = True
        if test_suite:
            pass
        else:
            msg = wx.MessageDialog(self, message='Please select some test suite first',
                                   caption="Error", style=wx.OK, pos=wx.DefaultPosition)
            msg.ShowModal()
            msg.Destroy()
            flag = False

        return flag


    def __on_save(self, event):
        select = self.group_test_suite_choice.GetStringSelection()
        if select:
            items = self.group_test_suite_list.Items
            if '' in items:
                items.remove('')
            self.dict_test_suite[select] = items
