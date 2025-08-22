# -*- coding: utf-8 -*-
"""
"""


import xmlrpc.client

import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Odoo ERP connection setup
ODOO_URL = 'http://localhost:8069/'
DB_NAME = 'odoo_demo'

USERNAME = os.getenv('OODO_USER')
PASSWORD = os.getenv('PASSWORD')




def get_open_pos():
    # Setup connection
    common = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/common')
    models = xmlrpc.client.ServerProxy(f'{ODOO_URL}/xmlrpc/2/object')
    uid = common.authenticate(DB_NAME, USERNAME, PASSWORD, {})

    # Fetch open Purchase Orders
    po_data = models.execute_kw(
        DB_NAME,
        uid,
        PASSWORD,
        'purchase.order',
        'search_read',
        [[['state', '=', 'purchase']]],  # Only open POs
        {
            'fields': [
                'name',
                'date_order',
                'partner_id',
                'amount_total',
                'picking_type_id',
            ]
        }
    )

    # Enrich PO data with addresses
    for po in po_data:
        # Get supplier shipping address (delivery type child of partner)
        supplier_children = models.execute_kw(
            DB_NAME, uid, PASSWORD,
            'res.partner', 'search_read',
            [[['parent_id', '=', po['partner_id'][0]], ['type', '=', 'delivery']]],
            {'fields': ['name', 'street', 'city', 'state_id', 'zip', 'country_id']}
        )
        po['supplier_ship_from'] = supplier_children[0] if supplier_children else {}

        # Get deliver-to address (from warehouse via picking type)
        picking_type_id = po.get('picking_type_id')
        if picking_type_id:
            picking_type = models.execute_kw(
                DB_NAME, uid, PASSWORD,
                'stock.picking.type', 'read',
                [picking_type_id[0]],
                {'fields': ['warehouse_id']}
            )
            warehouse_id = picking_type[0].get('warehouse_id', [None])[0] if picking_type else None

            if warehouse_id:
                warehouse = models.execute_kw(
                    DB_NAME, uid, PASSWORD,
                    'stock.warehouse', 'read',
                    [warehouse_id],
                    {'fields': ['partner_id']}
                )
                warehouse_partner_id = warehouse[0].get('partner_id', [None])[0] if warehouse else None

                if warehouse_partner_id:
                    deliver_to = models.execute_kw(
                        DB_NAME, uid, PASSWORD,
                        'res.partner', 'read',
                        [warehouse_partner_id],
                        {'fields': ['name', 'street', 'city', 'state_id', 'zip', 'country_id']}
                    )
                    po['po_deliver_to'] = deliver_to[0] if deliver_to else {}
                else:
                    po['po_deliver_to'] = {}
            else:
                po['po_deliver_to'] = {}
        else:
            po['po_deliver_to'] = {}

    return po_data

print(get_open_pos())