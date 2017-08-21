# -*- coding: utf-8 -*-

import math

from openerp import api, models, fields
from openerp.tools import amount_to_text_en

class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def print_invoice_gst(self):
        datas = {'id': self.id}
        return self.env['report'].get_action(self, 'nice_gst.report_invoice_gst', data=datas)
    
    @api.one
    def _amount_in_words(self):
        amount_in_words = amount_to_text_en.amount_to_text(math.floor(self.amount_total), lang='en', currency='')
        amount_in_words = amount_in_words.replace(' and Zero Cent', '') + ' Rupees'
        decimals = self.amount_total % 1
        if decimals >= 10**-2:
            amount_in_words += ' and '+ amount_to_text_en.amount_to_text(math.floor(decimals*100), lang='en', currency='')
            amount_in_words = amount_in_words.replace(' and Zero Cent', '') + ' Paise'
        amount_in_words += ' Only'    
        self.amount_in_words = amount_in_words
        
    amount_in_words = fields.Char('Amount in Words', compute='_amount_in_words')
    
