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

class stock_move(osv.Model):
    _inherit = 'stock.move'

    _columns = {
        'price_dealer': fields.float('Dealer Price'),
        'dealer_discount': fields.float('Dealer Discount'),
        'dealer_discount_per': fields.float('Dealer Discount (%)'),
    }

stock_move()

class stock_picking(osv.Model):
    _inherit = "stock.picking"
    _table = "stock_picking"

    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=None):
        res = super(stock_picking, self)._prepare_invoice_line(cr, uid, group=group, picking=picking, move_line=move_line, invoice_id=invoice_id, invoice_vals=invoice_vals, context=context)
        res = dict(res, price_dealer = move_line.price_dealer * move_line.product_qty, dealer_discount=move_line.dealer_discount * move_line.product_qty, dealer_discount_per=move_line.dealer_discount_per)
        return res

stock_picking()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
