from odoo import models,fields


class ProductCategories(models.Model):
	_inherit = 'product.category'
	_description = 'Magento ProductCategories'

	is_magento = fields.Boolean("Is Magento ? ")
	magento_id = fields.Char("Magento ID ")



		

