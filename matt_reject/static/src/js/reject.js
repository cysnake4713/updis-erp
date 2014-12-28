/**
 * Created by cysnake4713 on 14-11-13.
 */
openerp.matt_reject = function (instance) {
    var _t = instance.web._t,
        QWeb = instance.web.qweb;

    function getParameterByName(name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp(name + "=([^&#]*)"),
            results = regex.exec(location.hash);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }

    instance.web.form.WidgetButton.include({
        execute_action: function () {
            var self = this;
            var parent_dataset = self.view.dataset;

            var exec_action = function () {
                if (self.node.attrs.log == "1") {
                    var def = $.Deferred();
                    var confirm = "";
                    if (self.node.attrs.confirm) {
                        confirm = self.node.attrs.confirm
                    }
                    var prompt = "审批意见";
                    if (self.node.attrs.prompt) {
                        prompt = self.node.attrs.prompt;
                    }
                    var dialog = instance.web.dialog($(QWeb.render("WorkflowDialog", {'confirm': confirm, 'prompt': prompt})), {
                        title: prompt,
                        modal: true,
                        dialogClass: 'oe_act_window',
                        width: 500,
                        buttons: [
                            {
                                text: _t("Cancel"), click: function () {
                                $(this).dialog("close");
                            }
                            },
                            {
                                text: _t("Ok"), click: function () {
                                var self2 = this;

                                $.when(self.on_confirmed()).then(function (result) {
                                    var body = $(self2).find('textarea').val();
                                    if (body != '') {
                                        var values = {
                                            'body': prompt + ':' + body,
                                            'context': _.extend({}, {
                                                'mail_post_autofollow': false,
                                            }),
                                            'content_subtype': 'plaintext',
                                        };
                                        var active_id = 0;
                                        if (parent_dataset.ids.length > 1) {
                                            active_id = [parseInt(getParameterByName('id'))];
                                        } else {
                                            active_id = parent_dataset.ids;
                                        }
                                        new instance.web.Model(parent_dataset.model).call('message_post', active_id, values).done(function (message_id) {
                                            $(self2).dialog("close");
                                        });
                                    } else {
                                        $(self2).dialog("close");
                                    }
                                });
                            }
                            }
                        ],
                        beforeClose: function () {
                            def.resolve();
                        },
                    });
                    return def.promise();
                }
                if (self.node.attrs.confirm) {
                    var def = $.Deferred();
                    var dialog = instance.web.dialog($('<div/>').text(self.node.attrs.confirm), {
                        title: _t('Confirm'),
                        modal: true,
                        buttons: [
                            {
                                text: _t("Cancel"), click: function () {
                                $(this).dialog("close");
                            }
                            },
                            {
                                text: _t("Ok"), click: function () {
                                var self2 = this;
                                self.on_confirmed().always(function () {
                                    $(self2).dialog("close");
                                });
                            }
                            }
                        ],
                        beforeClose: function () {
                            def.resolve();
                        },
                    });
                    return def.promise();
                } else {
                    return self.on_confirmed();
                }
            };
            if (!this.node.attrs.special) {
                return this.view.recursive_save().then(exec_action);
            } else {
                return exec_action();
            }
        },
    });
};