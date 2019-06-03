from odoo import models,fields


class SaleOrder(models.Model):
	_inherit = 'sale.order'
	_description = 'Magento Sale Orders'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")
	shipping_charge = fields.Float("Shipping (Excluded)",readonly=True)



		

