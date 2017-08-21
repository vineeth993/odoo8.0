# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2013 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp
from openerp import api

class account_invoice_line(osv.Model):
    _inherit = 'account.invoice.line'

    _columns = {
        'packaging_cost': fields.float('Packing Cost'),
    }

    # @api.one
    # @api.depends('price_unit', 'discount', 'packaging_cost', 'invoice_line_tax_id', 'quantity',
    #              'product_id', 'invoice_id', 'invoice_id.partner_id', 'invoice_id.currency_id',
    #              )
    # def _compute_price(self):
    #     price = self.price_unit * (1 - (self.discount or 0.0) / 100.0) + self.packaging_cost / self.quantity
    #     taxes = self.invoice_line_tax_id.compute_all(price, self.quantity, product=self.product_id,
    #                                                  partner=self.invoice_id.partner_id)
    #     self.price_subtotal = taxes['total']
    #     if self.invoice_id:
    #         self.price_subtotal = self.invoice_id.currency_id.round(self.price_subtotal)

    @api.multi
    def product_id_change(self, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, company_id=None):
        res = super(account_invoice_line, self).product_id_change(product=product, uom_id=uom_id, qty=qty, name=name, type=type, partner_id=partner_id, fposition_id=fposition_id, price_unit=price_unit, currency_id=currency_id, company_id=company_id)
        product_pool = self.pool.get('product.product')
        res['value']['packaging_cost'] = 0.0
        if product:
            package = product_pool.browse(self._cr, self._uid, product)
            if package.container_id:
                res['value']['packaging_cost'] = package.container_id.list_price

        return res


class account_invoice(osv.osv):
    _inherit = 'account.invoice'

    def _amount_all(self, cr, uid, ids, name, args, context=None):
        res = {}
        val1 = val2 = 0
        for invoice in self.browse(cr, uid, ids, context=context):
            res[invoice.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
                'amount_packing': 0.0,
            }
            for line in invoice.invoice_line:
                val1 += line.price_subtotal
                val2 += line.packaging_cost
            res[invoice.id]['amount_untaxed'] = val1
            res[invoice.id]['amount_packing'] = val2
            for line in invoice.tax_line:
                res[invoice.id]['amount_tax'] += line.amount
            res[invoice.id]['amount_total'] = res[invoice.id]['amount_tax'] + res[invoice.id]['amount_untaxed'] + res[invoice.id]['amount_packing'] + invoice.round_off
        return res

    def _get_invoice_line(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()

    _columns = {
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Subtotal', track_visibility='always',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit', 'invoice_line_tax_id', 'quantity', 'discount', 'invoice_id', 'packaging_cost'], 20),
            },
            multi='all'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Tax',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit', 'invoice_line_tax_id', 'quantity', 'discount', 'invoice_id', 'packaging_cost'], 20),
            },
            multi='all'),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line', 'round_off'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit', 'invoice_line_tax_id', 'quantity', 'discount', 'invoice_id', 'packaging_cost'], 20),
            },
            multi='all'),
        'amount_packing': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Packing Cost',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line'], 20),
                'account.invoice.tax': (_get_invoice_tax, None, 20),
                'account.invoice.line': (_get_invoice_line, ['price_unit', 'invoice_line_tax_id', 'quantity', 'discount', 'invoice_id', 'packaging_cost'], 20),
            },
            multi='all'),
        'round_off': fields.float('Round Off', help="Round Off Amount"),
    }


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
