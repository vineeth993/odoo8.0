# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    gst_no = fields.Char('GST No', size=64)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: