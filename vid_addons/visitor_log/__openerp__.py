# -*- encoding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2014 Jarsa Sistemas,S.A.de C.V.(<http://www.jarsa.com.mx>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    "name": "Visitor Log",
    "version": "1.0",
    "author": "JARSA Sistemas, S.A. de C.V.",
    "website": "http://www.jarsa.com.mx",
    "category": "security",
    "depends": ['hr'],
    "data": ['views/menu_view.xml',
             'security/security.xml',
             'security/ir.model.access.csv',
             'views/visitor_log_view.xml',
             'security/security_menu.xml'],
    "demo_xml": [],
    "update_xml": [],
    "active": False,
    "installable": True,
    "certificate": "",
}
