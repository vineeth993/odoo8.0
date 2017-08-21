# -*- encoding: utf-8 -*-
##############################################################################
#    
#    Odoo, Open Source Management Solution
#
#    Author: Andrius Laukavičius. Copyright: JSC NOD Baltic
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


{
    'name': 'Stage Deadline Calculation',
    'version': '1.1',
    'category': 'CRM Resources management',
    'summary': 'Stages Deadline Calculation Extension',
    'description': """
	Extends stage deadline calculation to take in considarion users working time.
	""",
    'author': 'OERP',
    'website': 'www.oerp.eu',
    'depends': [
        'crm_stages_extend',
        'product',
        'resource',
        'sales_team_resource',      
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sales_team_view.xml',
        #'data/,        

    ],
    'demo': [
    ],
    'test': [

    ],
    'installable': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
