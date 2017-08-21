# -*- encoding: utf-8 -*-

import xlwt
from datetime import datetime as dt
from openerp.report import report_sxw
from openerp.addons.report_xls.report_xls import report_xls
from openerp.tools.translate import _
import time
from gdata.contentforshopping.data import Price
import datetime

def get_ratio(no1, no2):
    if no2 != 0:
        return no1 / no2
    return 0

class sale_status_report_parser(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context):
        super(sale_status_report_parser, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'datetime': dt,
            })
        self.context = context
    
class sale_status_report(report_xls):
    
    def generate_xls_report(self, parser, xls_styles, data, objects, wb):
        cr, uid = self.cr, self.uid
        report_name = 'Sale Summary Report' + '-' + time.strftime('%d-%m-%Y')
        ws = wb.add_sheet(report_name)
        ws.panes_frozen = True
        ws.remove_splits = True
        ws.portrait = 0  # Landscape
        ws.fit_width_to_pages = 1
        row_pos = 0
        cols = range(10)
        for col in cols:
            ws.col(col).width = 4000
        title2          = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on; align: horiz centre;')
        normal          = xlwt.easyxf('font: height 200, name Arial, colour_index black; align: horiz centre;')
        number          = xlwt.easyxf(num_format_str='#,##0;(#,##0)')
        number2d        = xlwt.easyxf(num_format_str='#,##0.00;(#,##0.00)')
        number2d_bold   = xlwt.easyxf('font: height 200, name Arial, colour_index black, bold on;',num_format_str='#,##0.00;(#,##0.00)')

        headers = {
            0: 'SO DATE', 1: 'SO NUMBER', 2: 'SO QTY', 3: 'SO VALUE', 4: 'ISSUED QTY', 5: 'INVOICED QTY',
            6: 'INVOICED VALUE', 7: 'SO STATUS'
            }
        for header in headers:
            ws.write(1, header, headers[header], title2)
        sale_obj = self.pool.get('sale.order')
        picking_obj = self.pool.get('stock.picking')
        if 'object' in data:
            sale_ids = data['object']
        else:
            sale_ids = sale_obj.search(cr, uid, [('state', 'not in', ('draft', 'cancel')),
                ('date_order', '>=', data['form']['date_from']), ('date_order', '<=', data['form']['date_to'])
                ])
        count = 2
        for sale in sale_obj.browse(cr, uid, sale_ids):
            qty = 0
            for line in sale.order_line:
                qty += line.product_uom_qty
            issue_qty, pick_list = 0, []
            pick_list += [picking for picking in sale.picking_ids]
            for picking in pick_list:
                for move in picking.move_lines:
                    issue_qty += move.product_qty
            inv_qty, inv_amount, inv_list = 0, 0, []
            inv_list += [invoice for invoice in sale.invoice_ids]
            for invoice in inv_list:
                for line in invoice.invoice_line:
                    inv_qty += line.quantity
                inv_amount += invoice.amount_total
            date = datetime.datetime.strptime(sale.date_order, '%Y-%m-%d %H:%M:%S').date().strftime('%d-%m-%Y'),
            ws.write(count, 0, date, normal)
            ws.write(count, 1, sale.name, normal)
            ws.write(count, 2, qty, number2d)
            ws.write(count, 3, sale.amount_total, number2d)
            ws.write(count, 4, issue_qty, number2d)
            ws.write(count, 5, inv_qty, number2d)
            ws.write(count, 6, inv_amount, number2d)
            ws.write(count, 7, '', normal)
            count += 1

sale_status_report('report.sale.status.report', 'sale.status.report', parser=sale_status_report_parser)