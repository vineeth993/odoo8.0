# -*- coding: utf-8 -*-

import time
from openerp import api, models

class ReportInvoice(models.AbstractModel):
    _name = 'report.nice_gst.report_invoice_gst'

    @api.model
    def render_html(self, docids, data=None):
        docs = self.env['account.invoice'].browse(data.get('id', []))
        invoice_id = data['id']
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse(invoice_id)
        templates = {}
        lines = []
        count = 0
        sgst_values = {'2.5': 0.0, '6.0': 0.0, '9.0': 0.0, '14.0': 0.0}
        cgst_values = {'2.5': 0.0, '6.0': 0.0, '9.0': 0.0, '14.0': 0.0}
        igst_values = {'5.0': 0.0, '12.0': 0.0, '18.0': 0.0, '28.0': 0.0}
        taxable_values = {'5.0': 0.0, '12.0': 0.0, '18.0': 0.0, '28.0': 0.0}
        total_nodiscount, total_discount, total_qty = 0.0, 0.0, 0.0
        for line in invoice.invoice_line:
            count += 1
            total_qty += line.quantity
            discount_perc = line.discount
            subtotal = line.quantity*line.price_unit
            total_nodiscount += subtotal
            discount = subtotal * discount_perc / 100
            total_discount += discount
            taxable_value = line.price_subtotal
            gst_perc, gst, cgst_perc, sgst_perc, igst_perc = 0.0, 0.0, 0.0, 0.0, 0.0
            sgst_amt, cgst_amt, igst_amt = 0.0, 0.0, 0.0
            for tax in line.invoice_line_tax_id:
                gst_perc += tax.amount*100
                if tax.gst_type == 'sgst':
                    sgst_perc = tax.amount*100
                    sgst_amt  = round(sgst_perc * taxable_value / 100, 2)
                elif tax.gst_type == 'cgst':
                    cgst_perc = tax.amount*100
                    cgst_amt  = round(cgst_perc * taxable_value / 100, 2)
                elif tax.gst_type == 'igst':
                    igst_perc = tax.amount*100
                    igst_amt  = round(igst_perc * taxable_value / 100, 2)
            gst = gst_perc * taxable_value / 100
            gst_perc_str = str(gst_perc)
            sgst_perc_str = str(sgst_perc)
            cgst_perc_str = str(cgst_perc)
            igst_perc_str = str(igst_perc)
            if gst_perc_str in taxable_values:
                taxable_values.update({gst_perc_str: taxable_values[gst_perc_str]+taxable_value})
            if sgst_perc_str in sgst_values:
                sgst_values.update({sgst_perc_str: sgst_values[sgst_perc_str]+sgst_amt})
            if cgst_perc_str in cgst_values:
                cgst_values.update({cgst_perc_str: cgst_values[cgst_perc_str]+cgst_amt})
            if igst_perc_str in igst_values:
                igst_values.update({igst_perc_str: igst_values[igst_perc_str]+igst_amt})
            lines.append({
                's_no': count,
                'hsn': line.product_id.hs_code_id and line.product_id.hs_code_id.code or '', 
                'code': line.product_id.default_code,
                'name': line.product_id.name,
                'qty': line.quantity,
                'price_unit': line.price_unit,
                'disc_perc': discount_perc,
                'discount': '%.2f' % discount,
                'subtotal': '%.2f' % subtotal,
                'gst_perc': gst_perc,
                'gst': '%.2f' % gst,
                'taxable_value': '%.2f' % taxable_value
                })

        sgst_values.update({'sgst_total': sum(sgst_values.values())})
        cgst_values.update({'cgst_total': sum(cgst_values.values())})
        igst_values.update({'igst_total': sum(igst_values.values())})
        total_values = {
            'total_5': (sgst_values['2.5']+cgst_values['2.5']+igst_values['5.0']+taxable_values['5.0']),
            'total_12':(sgst_values['6.0']+cgst_values['6.0']+igst_values['12.0']+taxable_values['12.0']),
            'total_18':(sgst_values['9.0']+cgst_values['9.0']+igst_values['18.0']+taxable_values['18.0']),
            'total_28':(sgst_values['14.0']+cgst_values['14.0']+igst_values['28.0']+taxable_values['28.0']),
            'total_nodiscount': '%.2f' % total_nodiscount,
            'total_discount': '%.2f' % total_discount,
            'total_qty': total_qty
            }
        blank_lines = []
        min_count = 11
        if count < min_count:
            for line_count in range(count+1, min_count):
                blank_lines.append({'no': line_count})
        gst_vals = [sgst_values, cgst_values]
        gst_slabs = ['2.5', '6.0', '9.0', '14.0']
        for gst_val in gst_vals:
            for gst_slab in gst_slabs:
                print gst_val, gst_slab, gst_val[gst_slab]
                gst_val.update({gst_slab: '%.2f' % gst_val[gst_slab]})
        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'data': data,
            'docs': docs,
            'time': time,
            'lines': lines,
            'sgst_values': sgst_values,
            'cgst_values': cgst_values,
            'igst_values': igst_values,
            'taxable_values': taxable_values,
            'total_values': total_values,
            'blank_lines': blank_lines
        }
        return self.env['report'].render('nice_gst.report_invoice_gst', docargs)