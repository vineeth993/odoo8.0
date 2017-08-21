# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Business Applications
#    Copyright (C) 2004-2012 OpenERP S.A. (<http://openerp.com>).
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

import logging

from openerp.osv import fields, osv

_logger = logging.getLogger(__name__)

class indian_base_configuration(osv.osv_memory):
    _name = 'indian.base.config.settings'
    _inherit = 'res.config.settings'

    _columns = {
        'module_product_coding': fields.boolean('Define automatic codings on products',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'group_major_sub_group_config':fields.boolean('Allows to configure Major and Sub Groups', implied_group='l10n_in_base.group_major_sub_group_config', help = """TODO"""),
        'module_product_container': fields.boolean('Define container or packaging and repairable products',
            help = """Allows gate keeper to pass the outgoing materials, products, etc. and keeps track of returning items.
            It installs the stock_gatepass module."""),
        
        'default_coding_method':fields.selection([('category','Based on the Category'), ('group','Based on Major / Sub Groups')], required=True, default_model='product.product'),
        
        'module_stock_indent': fields.boolean('Manage internal requests for material, service through Indents.',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_stock_gatepass': fields.boolean('Track outgoing material through Gatepass',
            help = """Allows gate keeper to pass the outgoing materials, products, etc. and keeps track of returning items.
            It installs the stock_gatepass module."""),
        
        'module_stock_serial_tracking': fields.boolean('Track products by location on serial numbers',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_product_container_tracking': fields.boolean('Track container and its movement in warehouse',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_stock_indent_gatepass': fields.boolean('Track your machine or material sent outside company for repairing, with approvals',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_stock_sale_gatepass': fields.boolean('Track your returnable containers you deliver with products',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_excise_receipt': fields.boolean('Manage excise on Incoming Shipments and prepare Invoice based on Excise Receipt',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_quotation_template': fields.boolean('Prepare bundle offers with templates quotation',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_sale_after_service': fields.boolean('Manage after sale service using service contracts for products',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_account_tax': fields.boolean('Manage categories on Tax to differentiate taxes as per Indian Taxonomy',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_l10n_in_invoice_adjust': fields.boolean('Adjust payable and receivables with each other using vouchers',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_attachment_size_limit': fields.boolean('Restrict on size of attachments and users for attachments',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_web_group_expand': fields.boolean('Enable expand and collapse features on group by list view',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        'module_l10n_in_sales_packing': fields.boolean('Add packaging cost on sales order line, to compute the packaging cost for product',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_dealers_discount': fields.boolean('Add dealer discount on sales order line, to compute the commission for dealer',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_packing_stock_invoice': fields.boolean('Transfer Packaging cost on customer invoice when invoice prepared based on Delivery Order',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        'module_l10n_in_dealer_discount_stock_invoice': fields.boolean('Transfer Dealers discount on customer invoice when invoice prepared based on Delivery Order',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_tax_retail_invoice': fields.boolean('Print Tax / Retail Invoice in 4 copies',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        'module_l10n_in_excise_invoice': fields.boolean('Print Excise Invoice in 4 copies',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        
        'module_l10n_in_dealer_discount_invoice': fields.boolean('Compute Dealer Discount on Invoice',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
        'module_l10n_in_packing_invoice': fields.boolean('Compute Packaging Cost on Invoice',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        
        'module_purchase_crm': fields.boolean('Get the Supplier price before proposing to Customer on Opportunity',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        'group_cst_config':fields.boolean('Enable Central Sales Tax on Partners', implied_group='l10n_in_base.group_cst_config', help = """TODO"""),
        'group_excise_config':fields.boolean('Enable Excise Control Code on Partners', implied_group='l10n_in_base.group_excise_config', help = """TODO"""),
        'group_tin_config':fields.boolean('Enable Tax Identification Number on Partners', implied_group='l10n_in_base.group_tin_config', help = """TODO"""),
        'group_service_config':fields.boolean('Enable Service Tax Number on Partner', implied_group='l10n_in_base.group_service_config', help = """TODO"""),
        
        'module_l10n_in_purchase': fields.boolean('Additional feature and computation on purchase orders',
            help = """Allows you to keeps track of internal material request.
            It installs the stock_indent module."""),
                
        'group_packing_config':fields.boolean('Allow Packaging and Forwarding charges on Purchase', implied_group='l10n_in_base.group_packing_config', help = """TODO"""),
        'group_freight_config':fields.boolean('Allow Fright charges on Purchase', implied_group='l10n_in_base.group_freight_config', help = """TODO"""),
        'group_insurance_config':fields.boolean('Allow Insurance charges on Purchase', implied_group='l10n_in_base.group_insurance_config', help = """TODO"""),
        
        'group_discount_purchase_config':fields.boolean('Allow Discount on Purchase Order lines', implied_group='l10n_in_base.group_discount_purchase_config', help = """TODO"""),
        
        'group_round_off_purchase_config':fields.boolean('Round-off feature on Purchase Order', implied_group='l10n_in_base.group_round_off_purchase_config', help = """TODO"""),
        'group_round_off_sale_config':fields.boolean('Round-off feature on Sales Order', implied_group='l10n_in_base.group_round_off_sale_config', help = """TODO"""),
        
        'group_dealer_price_on_sale_config':fields.boolean('Display dealer price on sales order line', implied_group='l10n_in_base.group_dealer_price_on_sale_config', help = """TODO"""),
        'group_inter_state_tax_config':fields.boolean('Maintain Register of Forms to be issue and to be receive for Inter-State, Intet-Warehouse or Export Sales', implied_group='l10n_in_base.group_inter_state_tax_config', help = """i.e. C-Form, H-Form, E1-Form, etc"""),
        
        'group_invoice_types_config':fields.boolean('Allow to have different types on Invoices and printing based on Types', implied_group='l10n_in_base.group_invoice_types_config', help = """TODO"""),
    }        
    
    _defaults = {
        'default_coding_method':'category'
    }

indian_base_configuration()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
