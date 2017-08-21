# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    gst_no = fields.Char('GST No', size=64)
    letter_head_ok = fields.Boolean('Print in Letter Head', default=False)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: