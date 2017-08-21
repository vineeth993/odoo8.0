# -*- coding: utf-8 -*-

from openerp import models, fields, api, _, exceptions
import openerp.addons.decimal_precision as dp

class SaleReasonCategory(models.Model):
    _name = 'sale.reason.category'

    name = fields.Char("Category")


class SaleReason(models.Model):
    _name = 'sale.reason'

    name = fields.Char(string='Reason For Sale', required=True)
    desc = fields.Text(string='Description')
    group_categ = fields.Many2one('sale.reason.category', string='Group Category')
    profiling_seasons1 = fields.Many2many('product.template', 'product_template_sale_reason_rel',
                                          'sale_reason_id', 'product_template_id',
                                          string='Profiling Season', invisible=True)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    reason = fields.Many2many('sale.reason', string="Purpose", related='product_id.profiling_seasons')
    product_uom_qty = fields.Float('Quantity', digits_compute= dp.get_precision('Product UoS'), default=0.0,
        required=True, readonly=True, states={'draft': [('readonly', False)]})

    def open_form_view(self, cr, uid, ids, context=None):
        if not ids: return []
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sale_customization', 'view_order_line_form')

        line = self.browse(cr, uid, ids[0], context=context)
        return {
            'name':_("Order Line"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'sale.order.line',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'res_id': line.id
        }

    def button_save(self, cr, uid, ids, context=None):
        return True

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    type = fields.Selection([
            ('raw', 'Raw Materials'),
            ('manufacture', 'Manufacturing'),
            ('semi-finished', 'Semi Finished'),
            ('finished', 'Finished'),
            ])

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def _get_warehouse(self):
        warehouse_ids = self.env['stock.warehouse'].search([('type', '=', 'finished')])
        if not warehouse_ids:
            return False
        return warehouse_ids[0]
    
    transaction_type = fields.Selection([('local', 'Local'), ('inter_state', 'Interstate')], 'Transaction Type')
    transport_document_ids = fields.One2many('transport.document', 'sale_id', 'Documents')
    state = fields.Selection([
            ('draft', 'Draft Quotation'),
            ('confirm', 'Quotation Confirmed'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ], 'Status', readonly=True, copy=False, select=True)
    order_line = fields.One2many('sale.order.line', 'order_id', 'Order Lines', 
        readonly=True, states={'draft': [('readonly', False)], 'confirm': [('readonly', False)], 'sent': [('readonly', False)]}, copy=True)
    quot_line_ids = fields.One2many('sale.quotation.line', 'sale_id', 'Quotation Lines')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True, default=_get_warehouse, domain=[('type', '=', 'finished')])

    @api.multi
    def action_quotation_confirm(self):
        self.state = 'confirm'
        for line in self.order_line:
            if line.product_uom_qty <= 0:
                raise exceptions.Warning('Quantity cannot be less than zero')
            self.env['sale.quotation.line'].create({
                'product_id': line.product_id.id,
                'name': line.name,
                'qunatity': line.product_uom_qty,
                'price_unit': line.price_unit,
                'sale_id': self.id
                })
    
    @api.multi
    def action_button_confirm(self):
        for line in self.order_line:
            if line.product_uom_qty <= 0:
                raise exceptions.Warning('Quantity cannot be less than zero')
        return super(SaleOrder, self).action_button_confirm()
    
class TransportDocument(models.Model):
    _name = 'transport.document'
    _description = 'Transport Document'
    
    sale_id = fields.Many2one('sale.order', 'Sale Order')
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    vehicle_no = fields.Char('Vehicle Number')
    driver_name = fields.Char('Driver')
    contact_no = fields.Char('Contact No')
    
class QuotationLine(models.Model):
    _name = 'sale.quotation.line'
    _description = 'Sale Quotation Line'
    _order = 'id'
    
    @api.one
    def _subtotal(self):
        self.price_subtotal = self.price_unit * self.qunatity

    sale_id = fields.Many2one('sale.order', 'Sale Order')
    product_id = fields.Many2one('product.product', 'Product')
    price_unit = fields.Float('Unit Price')
    price_subtotal = fields.Float('Subtotal', compute=_subtotal)
    qunatity = fields.Float('Quantity')
    name = fields.Char('Description')

