from odoo import models,fields


class ProductVariants(models.Model):
	_inherit = 'product.product'
	_description = 'Magento Product Variants'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")



		

