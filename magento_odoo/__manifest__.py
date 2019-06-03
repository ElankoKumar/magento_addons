
{
    "name": """Odoo + Magento""",
    "summary": """Used to connect Odoo with Magento""",
    "category": "Connector",
    # "live_test_url": "http://www.dreameffectsmedia.com",
    "images": [],
    "version": "1.0.0",
    "application": True,

    "author": "DFX",
    "support": "info@dreameffectsmedia.com",
    "website": "http://www.dreameffectsmedia.com",
    "license": "LGPL-3",
    # "price": 9.00,
    # "currency": "EUR",

    "depends": [
        'base',
        'product',
		'sale',
		'account'
    ],
    "data": [
     'security/ir.model.access.csv',
	   'data/generate_token.xml',
     'views/template.xml',
     'views/customer_view.xml',
     'views/products_template_view.xml',
	   'views/product_categories_view.xml',
	   'views/product_variants_view.xml',
	   'views/sale_order_view.xml',
	   'views/invoice_view.xml',
	   'views/shipments_view.xml',
	   'views/tax_view.xml',
	   'views/currency_view.xml',
	   'views/email_template_view.xml',
	   'views/coupon_view.xml',
     'views/dashboard_view.xml',
     'data/dashboard_data.xml',
     'views/menus.xml'

    ],

}